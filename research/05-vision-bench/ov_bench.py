import time, statistics, numpy as np, onnxruntime as ort, openvino as ov
x = np.random.rand(1,3,224,224).astype(np.float32)
def b(name, fn, n=30):
    for _ in range(5): fn()
    ts=[]
    for _ in range(n):
        t=time.perf_counter(); fn(); ts.append((time.perf_counter()-t)*1000)
    print(f"{name:55s} median {statistics.median(ts):7.1f} ms  min {min(ts):7.1f}", flush=True)
core = ov.Core()
for f in ["clip_b32_visual.onnx", "siglip2_b16_visual.onnx"]:
    s = ort.InferenceSession(f, providers=["CPUExecutionProvider"])
    b(f"{f} onnxruntime CPU fp32", lambda: s.run(None, {"pixel": x}))
    m = core.read_model(f)
    for dev in ["CPU", "GPU", "NPU"]:
        try:
            t=time.perf_counter(); cm = core.compile_model(m, dev, {"PERFORMANCE_HINT":"LATENCY"}); ct=time.perf_counter()-t
            req = cm.create_infer_request()
            b(f"{f} OpenVINO {dev} (compile {ct:.1f}s)", lambda: req.infer({0: x}))
        except Exception as e:
            print(f, dev, "FAIL", repr(e)[:200])
