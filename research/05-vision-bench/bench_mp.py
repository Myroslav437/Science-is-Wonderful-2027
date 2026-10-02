"""MediaPipe Tasks (Python, CPU delegate) latency on the dev laptop."""
import os, time, statistics, json
import cv2
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "models")
print("mediapipe", mp.__version__)
frame = cv2.imread(os.path.join(M, "zidane.jpg"))
frame = cv2.resize(frame, (640, 360))
img = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
results = {}

def bench(name, fn, n=40, warm=5):
    out = None
    for _ in range(warm):
        out = fn()
    ts = []
    for _ in range(n):
        t = time.perf_counter(); out = fn(); ts.append((time.perf_counter() - t) * 1000)
    med = statistics.median(ts); p90 = sorted(ts)[int(0.9 * len(ts)) - 1]
    results[name] = {"median_ms": round(med, 1), "p90_ms": round(p90, 1)}
    print(f"{name:60s} median {med:7.1f} ms  p90 {p90:7.1f} ms", flush=True)
    return out

def base(f):
    return mpt.BaseOptions(model_asset_path=os.path.join(M, f))

IM = vision.RunningMode.IMAGE
try:
    for f in ["pose_landmarker_lite.task", "pose_landmarker_full.task"]:
        for n in [1, 3]:
            lm = vision.PoseLandmarker.create_from_options(vision.PoseLandmarkerOptions(base_options=base(f), running_mode=IM, num_poses=n))
            r = bench(f"PoseLandmarker {f} num_poses={n} 640x360", lambda: lm.detect(img))
            print("   poses found:", len(r.pose_landmarks))
except Exception as e:
    print("pose fail", repr(e)[:300])
try:
    fd = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(base_options=base("blaze_face_short_range.tflite"), running_mode=IM))
    r = bench("FaceDetector BlazeFace short-range 640x360", lambda: fd.detect(img)); print("   faces:", len(r.detections))
except Exception as e:
    print("fd fail", repr(e)[:300])
try:
    fl = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(base_options=base("face_landmarker.task"), running_mode=IM, num_faces=2, output_face_blendshapes=True, output_facial_transformation_matrixes=True))
    r = bench("FaceLandmarker (478 lm + blendshapes + matrix) num_faces=2", lambda: fl.detect(img)); print("   faces:", len(r.face_landmarks))
except Exception as e:
    print("fl fail", repr(e)[:300])
try:
    gr = vision.GestureRecognizer.create_from_options(vision.GestureRecognizerOptions(base_options=base("gesture_recognizer.task"), running_mode=IM, num_hands=2))
    r = bench("GestureRecognizer num_hands=2", lambda: gr.recognize(img)); print("   hands:", len(r.hand_landmarks))
except Exception as e:
    print("gr fail", repr(e)[:300])
try:
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(base_options=base("selfie_multiclass_256x256.tflite"), running_mode=IM, output_category_mask=True, output_confidence_masks=True))
    r = bench("ImageSegmenter selfie_multiclass_256x256 (6 classes)", lambda: seg.segment(img))
    print("   labels:", seg.labels)
except Exception as e:
    print("seg fail", repr(e)[:300])
try:
    od = vision.ObjectDetector.create_from_options(vision.ObjectDetectorOptions(base_options=base("efficientdet_lite0.tflite"), running_mode=IM, score_threshold=0.4, category_allowlist=["person"]))
    r = bench("ObjectDetector EfficientDet-Lite0 int8 (person)", lambda: od.detect(img)); print("   persons:", len(r.detections))
except Exception as e:
    print("od fail", repr(e)[:300])
json.dump(results, open(os.path.join(HERE, "results_mp.json"), "w"), indent=1)
