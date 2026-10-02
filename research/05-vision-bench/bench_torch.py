"""CPU latency micro-benchmarks on the dev laptop (Core Ultra 7 255U).
Measures median wall-clock latency of single-image inference after warm-up.
"""
import os, time, statistics, sys, platform, json
import numpy as np
import cv2
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "models")
IMG = cv2.imread(os.path.join(M, "zidane.jpg"))  # 1280x720, 2 people
BUS = cv2.imread(os.path.join(M, "bus.jpg"))      # 810x1080, 4 people
results = {}

def bench(name, fn, n=30, warm=5):
    for _ in range(warm):
        fn()
    ts = []
    for _ in range(n):
        t = time.perf_counter(); fn(); ts.append((time.perf_counter() - t) * 1000)
    med = statistics.median(ts); p90 = sorted(ts)[int(0.9 * len(ts)) - 1]
    results[name] = {"median_ms": round(med, 1), "p90_ms": round(p90, 1)}
    print(f"{name:55s} median {med:7.1f} ms  p90 {p90:7.1f} ms", flush=True)

print("python", sys.version.split()[0], "torch", torch.__version__, "threads", torch.get_num_threads(), platform.processor())

which = sys.argv[1:] or ["clip", "yolo", "yunet"]

if "yunet" in which:
    det = cv2.FaceDetectorYN.create(os.path.join(M, "face_detection_yunet_2023mar.onnx"), "", (640, 360), 0.6, 0.3, 5000)
    small = cv2.resize(IMG, (640, 360))
    bench("YuNet 2023mar (OpenCV DNN) 640x360", lambda: det.detect(small))

if "clip" in which:
    import open_clip
    from PIL import Image
    pil = Image.fromarray(cv2.cvtColor(IMG, cv2.COLOR_BGR2RGB))
    for arch, tag in [("ViT-B-32", "laion2b_s34b_b79k"), ("ViT-B-16-SigLIP2", "webli")]:
        try:
            model, _, pre = open_clip.create_model_and_transforms(arch, pretrained=tag)
            model.eval()
            x = pre(pil).unsqueeze(0)
            with torch.inference_mode():
                bench(f"open_clip {arch} image encoder {tuple(x.shape[-2:])} fp32", lambda: model.encode_image(x))
                tok = open_clip.get_tokenizer(arch)
                t = tok(["a photo of a person wearing a hat"] * 20)
                bench(f"open_clip {arch} text encoder 20 prompts (one-off)", lambda: model.encode_text(t), n=5, warm=1)
        except Exception as e:
            print("CLIP fail", arch, repr(e)[:300])

if "yolo" in which:
    from ultralytics import YOLO
    os.chdir(M)
    for w in ["yolo26n.pt", "yolo11n.pt", "yolo26n-pose.pt", "yolo11n-pose.pt"]:
        try:
            m = YOLO(w)
            bench(f"ultralytics {w} torch CPU imgsz=640", lambda: m.predict(IMG, imgsz=640, verbose=False, classes=[0] if 'pose' not in w else None))
            bench(f"ultralytics {w} torch CPU imgsz=320", lambda: m.predict(IMG, imgsz=320, verbose=False))
            continue
            onnx = m.export(format="onnx", imgsz=640, verbose=False)
            mo = YOLO(onnx, task="pose" if "pose" in w else "detect")
            bench(f"ultralytics {w} ONNXRuntime CPU imgsz=640", lambda: mo.predict(IMG, imgsz=640, verbose=False))
        except Exception as e:
            print("YOLO fail", w, repr(e)[:300])

with open(os.path.join(HERE, f"results_{'_'.join(which)}.json"), "w") as f:
    json.dump(results, f, indent=1)
