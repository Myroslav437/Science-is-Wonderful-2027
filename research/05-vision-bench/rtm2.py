import time, statistics, cv2
from rtmlib import Body
IMG = cv2.imread("models/zidane.jpg")
def b(name, fn, n=20):
    for _ in range(3): fn()
    ts=[]
    for _ in range(n):
        t=time.perf_counter(); fn(); ts.append((time.perf_counter()-t)*1000)
    print(f"{name:60s} median {statistics.median(ts):7.1f} ms  min {min(ts):7.1f}", flush=True)
for be, dev in [("onnxruntime","cpu"), ("openvino","cpu"), ("openvino","gpu"), ("openvino","npu")]:
    try:
        body = Body(mode="lightweight", backend=be, device=dev)
        b(f"rtmlib lightweight {be}/{dev}, 2 people", lambda: body(IMG))
    except Exception as e:
        print(be, dev, "FAIL", repr(e)[:200], flush=True)
