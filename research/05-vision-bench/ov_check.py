import numpy as np, onnxruntime as ort, openvino as ov, open_clip, torch
from PIL import Image
m,_,pre = open_clip.create_model_and_transforms("ViT-B-16-SigLIP2", pretrained="webli")
x = pre(Image.open("models/zidane.jpg").convert("RGB")).unsqueeze(0).numpy()
ref = ort.InferenceSession("siglip2_b16_visual.onnx").run(None, {"pixel": x})[0][0]
core = ov.Core(); mdl = core.read_model("siglip2_b16_visual.onnx")
for dev in ["CPU","GPU","NPU"]:
    o = core.compile_model(mdl, dev)({0:x})[0][0]
    print(dev, "cosine vs ORT fp32:", float(np.dot(o,ref)/np.linalg.norm(o)/np.linalg.norm(ref)))
