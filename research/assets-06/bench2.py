"""Bench round 2 (idle machine): one config per process.
usage: bench2.py model_dir mode(t2i|hyb) device steps strength [tag]
- hyb = img2img from a procedural Layer A render (blue body), style-only prompt.
- counts denoising steps actually executed via the GenAI step callback.
Writes one JSON line to results2.jsonl. Warm-up excluded; mean/min/max of NRUNS runs."""
import sys, os, time, json, statistics
import numpy as np
import openvino as ov
import openvino_genai as g
from PIL import Image, ImageDraw

model_dir, mode, dev, steps, strength = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
tag = sys.argv[6] if len(sys.argv) > 6 else ""
N = int(os.environ.get("NRUNS", "5"))
W = H = 512
here = os.path.dirname(os.path.abspath(__file__))
turbo = "turbo" in model_dir.lower()


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


T2I_PROMPT = ("children's crayon drawing of a cute friendly robot mascot with a blue striped body, "
              "a yellow hat and a small orange cat, simple shapes, white paper")
STYLE_PROMPT = ("children's crayon drawing of a cute friendly robot mascot and a small cat, "
                "simple shapes, bold colours, white paper")
res = dict(model=os.path.basename(model_dir.rstrip("/\\")), mode=mode, dev=dev, steps=steps,
           strength=strength, tag=tag, res=f"{W}x{H}", nruns=N)
try:
    t0 = time.perf_counter()
    pipe = g.Text2ImagePipeline(model_dir) if mode == "t2i" else g.Image2ImagePipeline(model_dir)
    gs = 0.0 if turbo else pipe.get_generation_config().guidance_scale
    if turbo:
        cfg = pipe.get_generation_config(); cfg.guidance_scale = 0.0; pipe.set_generation_config(cfg)
    pipe.reshape(1, H, W, gs)
    pipe.compile(dev, dev, dev, config={"CACHE_DIR": os.path.join(here, "ov_cache")})
    res["load_compile_s"] = round(time.perf_counter() - t0, 2)
    init = ov.Tensor(np.array(layer_a())[None]) if mode == "hyb" else None
    executed = []

    def cb(step, num_steps, latent):
        executed.append((step, num_steps))
        return False

    def run(seed):
        executed.clear()
        kw = dict(num_inference_steps=steps, rng_seed=seed, width=W, height=H, callback=cb)
        if turbo:
            kw["guidance_scale"] = 0.0
        if mode == "t2i":
            return pipe.generate(T2I_PROMPT, **kw)
        return pipe.generate(STYLE_PROMPT, init, strength=strength, **kw)

    t = time.perf_counter(); out = run(7); res["first_run_s"] = round(time.perf_counter() - t, 2)
    res["steps_executed"] = len(executed)
    res["callback_num_steps"] = executed[-1][1] if executed else None
    times = []
    for i in range(N):
        t = time.perf_counter(); out = run(7); times.append(time.perf_counter() - t)
    res["mean_s"] = round(statistics.mean(times), 3)
    res["min_s"] = round(min(times), 3)
    res["max_s"] = round(max(times), 3)
    Image.fromarray(out.data[0]).save(os.path.join(here, f"r2_{res['model']}_{mode}_{dev}_{steps}x{strength}{tag}.png"))
except Exception as e:
    res["error"] = repr(e)[:400]
res["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
print("RESULT " + json.dumps(res), flush=True)
with open(os.path.join(here, "results2.jsonl"), "a") as fh:
    fh.write(json.dumps(res) + "\n")
sys.stdout.flush()
os._exit(0)
