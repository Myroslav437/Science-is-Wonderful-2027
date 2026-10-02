"""Hybrid test: procedural 'Layer A' render -> img2img stylisation. Colours/layout come from pixels,
prompt carries style only. Usage: hybrid_test.py model_dir device"""
import sys, os, time, json
import numpy as np
from PIL import Image, ImageDraw
import openvino as ov
import openvino_genai as g

here = os.path.dirname(os.path.abspath(__file__))
model_dir, dev = sys.argv[1], sys.argv[2]
W = H = 512

def layer_a(shirt=(40, 90, 220), hat=(250, 210, 30), companion=True):
    im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    d.ellipse((156, 200, 356, 440), fill=shirt, outline="black", width=6)          # body
    for y in range(230, 430, 40):                                                   # stripes
        d.rectangle((170, y, 342, y + 14), fill=(255, 255, 255))
    d.ellipse((186, 110, 326, 240), fill=(200, 200, 200), outline="black", width=6)  # robot head (grey, neutral)
    d.ellipse((220, 160, 240, 180), fill="black"); d.ellipse((272, 160, 292, 180), fill="black")
    d.polygon([(176, 125), (336, 125), (256, 40)], fill=hat, outline="black")        # hat
    d.line((160, 290, 90, 200), fill="black", width=10)                              # waving arm
    if companion:                                                                    # small 'cat' companion
        d.ellipse((380, 360, 470, 440), fill=(255, 140, 0), outline="black", width=4)
        d.polygon([(390, 370), (405, 330), (420, 368)], fill=(255, 140, 0), outline="black")
        d.polygon([(430, 368), (445, 330), (460, 372)], fill=(255, 140, 0), outline="black")
    return im

prompt = "children's crayon drawing of a cute friendly robot mascot and a small cat, simple shapes, bold colours, white paper"
pipe = g.Image2ImagePipeline(model_dir)
gs = 0.0 if "turbo" in model_dir.lower() else pipe.get_generation_config().guidance_scale
pipe.reshape(1, H, W, gs)
pipe.compile(dev, dev, dev, config={"CACHE_DIR": os.path.join(here, "ov_cache")})
out = {}
for name, kw in [("blue", {}), ("green", {"shirt": (30, 170, 60)})]:
    a = layer_a(**kw); a.save(os.path.join(here, f"layerA_{name}.png"))
    t = ov.Tensor(np.array(a)[None])
    for s in (0.5, 0.7, 0.85):
        steps = 4 if "lcm" in model_dir.lower() else 2
        kw2 = dict(strength=s, num_inference_steps=steps, rng_seed=7)
        if gs == 0.0: kw2["guidance_scale"] = 0.0
        t0 = time.perf_counter(); r = pipe.generate(prompt, t, **kw2); dt = time.perf_counter() - t0
        Image.fromarray(r.data[0]).save(os.path.join(here, f"hyb_{os.path.basename(model_dir)}_{name}_{s}.png"))
        out[f"{name}_{s}"] = round(dt, 2)
print("HYBRID " + json.dumps(out), flush=True)
os._exit(0)
