"""Perception load: the prototype's real VisionPerception (MediaPipe face+pose + open_clip ViT-B/32 on CPU)
run back-to-back on stored frames for DURATION seconds. Prints frames/s and per-frame latency."""
import sys, os, time, json, glob, statistics
import numpy as np
from PIL import Image
proj = r"C:\Users\myros\projects\Science Is Wonderful 2027"
sys.path.insert(0, os.path.join(proj, "prototype"))
from robotsees.perception.vision import VisionPerception

dur = float(sys.argv[1]); tag = sys.argv[2]
frames = sorted(glob.glob(os.path.join(proj, "scratch", "frames", "v01", "cam_clean", "*.jpg")))[:40]
imgs = [np.array(Image.open(f).convert("RGB")) for f in frames]
vp = VisionPerception()
for im in imgs[:3]:
    vp.analyse_frame(im, 0.0)  # warm-up
print("READY", flush=True)
lat = []; t_end = time.perf_counter() + dur; i = 0; t0 = time.perf_counter(); w0 = time.time()
while time.perf_counter() < t_end:
    t = time.perf_counter(); vp.analyse_frame(imgs[i % len(imgs)], i / 4.0); lat.append(time.perf_counter() - t); i += 1
el = time.perf_counter() - t0; w1 = time.time()
res = dict(tag=tag, frames=i, fps=round(i / el, 2), mean_ms=round(1000 * statistics.mean(lat), 1),
           p95_ms=round(1000 * sorted(lat)[int(0.95 * len(lat)) - 1], 1), frame_shape=list(imgs[0].shape),
           w0=w0, w1=w1, ts=time.strftime("%H:%M:%S"))
print("PERC " + json.dumps(res), flush=True)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results2.jsonl"), "a") as fh:
    fh.write(json.dumps(res) + "\n")
os._exit(0)
