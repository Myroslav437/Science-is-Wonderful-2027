import time, statistics, cv2
from ultralytics import YOLO
IMG = cv2.imread("zidane.jpg")
def b(name, fn, n=30):
    for _ in range(5): fn()
    ts=[]
    for _ in range(n):
        t=time.perf_counter(); fn(); ts.append((time.perf_counter()-t)*1000)
    print(f"{name:55s} median {statistics.median(ts):7.1f} ms  min {min(ts):7.1f}", flush=True)
for w in ["yolo26n.pt", "yolo26n-pose.pt"]:
    p = YOLO(w).export(format="openvino", imgsz=640, verbose=False)
    for dev in ["intel:cpu", "intel:gpu", "intel:npu"]:
        try:
            m = YOLO(p, task="pose" if "pose" in w else "detect")
            b(f"{w} OpenVINO {dev} imgsz=640 (end-to-end predict)", lambda: m.predict(IMG, imgsz=640, device=dev, verbose=False))
        except Exception as e:
            print(w, dev, "FAIL", repr(e)[:250])
    p2 = YOLO(w).export(format="onnx", imgsz=640, verbose=False)
    m = YOLO(p2, task="pose" if "pose" in w else "detect")
    b(f"{w} ONNXRuntime CPU imgsz=640 (end-to-end predict)", lambda: m.predict(IMG, imgsz=640, verbose=False))
