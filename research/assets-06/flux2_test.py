"""FLUX.2-klein-4B int4 (OpenVINO IR, rupeshs/flux2-klein-4b-int4-ov) on the dev laptop: t2i and hybrid i2i at 512."""
import sys, os, time, json, statistics
import numpy as np
import openvino as ov
import openvino_genai as g
from PIL import Image, ImageDraw
here = os.path.dirname(os.path.abspath(__file__))
model_dir, dev, mode, steps = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
strength = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
N = int(os.environ.get("NRUNS", "2")); W = H = 512


def layer_a(shirt=(40, 90, 220), hat=(250, 210, 30)):
    im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    d.ellipse((156, 200, 356, 440), fill=shirt, outline="black", width=6)
    for y in range(230, 430, 40):
        d.rectangle((170, y, 342, y + 14), fill=(255, 255, 255))
    d.ellipse((186, 110, 326, 240), fill=(200, 200, 200), outline="black", width=6)
    d.ellipse((220, 160, 240, 180), fill="black"); d.ellipse((272, 160, 292, 180), fill="black")
    d.polygon([(176, 125), (336, 125), (256, 40)], fill=hat, outline="black")
    d.line((160, 290, 90, 200), fill="black", width=10)
    d.ellipse((380, 360, 470, 440), fill=(255, 140, 0), outline="black", width=4)
    d.polygon([(390, 370), (405, 330), (420, 368)], fill=(255, 140, 0), outline="black")
    d.polygon([(430, 368), (445, 330), (460, 372)], fill=(255, 140, 0), outline="black")
    return im


T2I = ("children's crayon drawing of a cute friendly robot mascot with a blue striped body, "
       "a yellow hat and a small orange cat, simple shapes, white paper")
STYLE = ("children's crayon drawing of a cute friendly robot mascot and a small cat, "
         "simple shapes, bold colours, white paper")
res = dict(model=os.path.basename(model_dir), dev=dev, mode=mode, steps=steps, strength=strength, res=f"{W}x{H}")
try:
    t0 = time.perf_counter()
    pipe = g.Text2ImagePipeline(model_dir) if mode == "t2i" else g.Image2ImagePipeline(model_dir)
    cfg = pipe.get_generation_config(); res["default_gs"] = cfg.guidance_scale
    pipe.reshape(1, H, W, cfg.guidance_scale)
    pipe.compile(dev, dev, dev, config={"CACHE_DIR": os.path.join(here, "ov_cache")})
    res["load_compile_s"] = round(time.perf_counter() - t0, 2)
    init = ov.Tensor(np.array(layer_a())[None])
    n = []

    def run():
        n.clear()
        kw = dict(num_inference_steps=steps, rng_seed=7, width=W, height=H, callback=lambda s, t, l: n.append(t) or False)
        if mode == "t2i":
            return pipe.generate(T2I, **kw)
        return pipe.generate(STYLE, init, strength=strength, **kw)

    t = time.perf_counter(); out = run(); res["first_run_s"] = round(time.perf_counter() - t, 2); res["steps_executed"] = len(n)
    ts = []
    for _ in range(N):
        t = time.perf_counter(); out = run(); ts.append(time.perf_counter() - t)
    res["mean_s"] = round(statistics.mean(ts), 2); res["min_s"] = round(min(ts), 2)
    Image.fromarray(out.data[0]).save(os.path.join(here, f"r2_flux2klein_{mode}_{dev}_{steps}x{strength}.png"))
except Exception as e:
    res["error"] = repr(e)[:500]
res["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
print("RESULT " + json.dumps(res), flush=True)
with open(os.path.join(here, "results2.jsonl"), "a") as fh:
    fh.write(json.dumps(res) + "\n")
os._exit(0)
