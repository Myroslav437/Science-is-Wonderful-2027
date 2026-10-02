"""Generation loop on a device for DURATION s (after warm-up): hybrid img2img from the Layer A render.
Writes per-run wall-clock (time.time()) start/end so overlap with the perception load can be computed."""
import sys, os, time, json
import numpy as np
import openvino as ov
import openvino_genai as g
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
model_dir, dev, steps, strength, dur, tag = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
W = H = 512
turbo = "turbo" in model_dir.lower()
from PIL import Image, ImageDraw

def layer_a(shirt=(40, 90, 220), hat=(250, 210, 30)):
    im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    d.ellipse((156, 200, 356, 440), fill=shirt, outline="black", width=6)
    for y in range(230, 430, 40):
        d.rectangle((170, y, 342, y + 14), fill=(255, 255, 255))
    d.ellipse((186, 110, 326, 240), fill=(200, 200, 200), outline="black", width=6)
    d.polygon([(176, 125), (336, 125), (256, 40)], fill=hat, outline="black")
    d.line((160, 290, 90, 200), fill="black", width=10)
    d.ellipse((380, 360, 470, 440), fill=(255, 140, 0), outline="black", width=4)
    return im

STYLE = "children's crayon drawing of a cute friendly robot mascot and a small cat, simple shapes, bold colours, white paper"
pipe = g.Image2ImagePipeline(model_dir)
gs = 0.0 if turbo else pipe.get_generation_config().guidance_scale
if turbo:
    c = pipe.get_generation_config(); c.guidance_scale = 0.0; pipe.set_generation_config(c)
pipe.reshape(1, H, W, gs)
pipe.compile(dev, dev, dev, config={"CACHE_DIR": os.path.join(here, "ov_cache")})
init = ov.Tensor(np.array(layer_a())[None])
kw = dict(strength=strength, num_inference_steps=steps, rng_seed=7)
if turbo: kw["guidance_scale"] = 0.0
pipe.generate(STYLE, init, **kw)
print("READY", flush=True)
stop = os.path.join(here, f"stop_{tag}.flag")
runs = []; t_end = time.time() + dur
while time.time() < t_end and not os.path.exists(stop):
    a = time.time(); pipe.generate(STYLE, init, **kw); runs.append((a, time.time()))
res = dict(tag=tag, model=os.path.basename(model_dir), dev=dev, steps=steps, strength=strength, runs=runs)
print("GEN " + json.dumps(res), flush=True)
os._exit(0)
