"""One benchmark config per process: model_dir mode te_dev unet_dev vae_dev steps [strength]
Prints one JSON line with timings (seconds). Warm-up run excluded; mean/min of N runs."""
import sys, time, json, os, statistics
import numpy as np
import openvino as ov
import openvino_genai as g
from PIL import Image

model_dir, mode, te_dev, unet_dev, vae_dev, steps = sys.argv[1:7]
steps = int(steps)
strength = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
N = int(os.environ.get("NRUNS", "3"))
W = H = 512
here = os.path.dirname(os.path.abspath(__file__))
cache = os.path.join(here, "ov_cache")
prompt = ("children's crayon drawing of a friendly round character with a red striped shirt "
          "and a yellow hat, simple shapes, white background")
res = dict(model=os.path.basename(model_dir.rstrip("/\\")), mode=mode, te=te_dev, unet=unet_dev,
           vae=vae_dev, steps=steps, strength=strength, res=f"{W}x{H}")
try:
    t0 = time.perf_counter()
    if mode == "t2i":
        pipe = g.Text2ImagePipeline(model_dir)
    else:
        pipe = g.Image2ImagePipeline(model_dir)
    gs = pipe.get_generation_config().guidance_scale
    res["guidance_scale_cfg"] = gs
    if "turbo" in model_dir.lower():
        gs = 0.0
        cfg = pipe.get_generation_config(); cfg.guidance_scale = 0.0; pipe.set_generation_config(cfg)
    pipe.reshape(1, H, W, gs)
    pipe.compile(te_dev, unet_dev, vae_dev, config={"CACHE_DIR": cache})
    res["load_compile_s"] = round(time.perf_counter() - t0, 2)
    init = None
    if mode == "i2i":
        src = os.path.join(here, "init.png")
        img = np.array(Image.open(src).convert("RGB").resize((W, H)))[None]
        init = ov.Tensor(img)

    def run(seed):
        kw = dict(num_inference_steps=steps, rng_seed=seed, width=W, height=H)
        if "turbo" in model_dir.lower():
            kw["guidance_scale"] = 0.0
        if mode == "t2i":
            return pipe.generate(prompt, **kw)
        return pipe.generate(prompt.replace("red", "blue"), init, strength=strength, **kw)

    t = time.perf_counter(); out = run(1); res["first_run_s"] = round(time.perf_counter() - t, 2)
    times = []
    for i in range(N):
        t = time.perf_counter(); out = run(42 + i); times.append(time.perf_counter() - t)
    res["mean_s"] = round(statistics.mean(times), 3)
    res["min_s"] = round(min(times), 3)
    Image.fromarray(out.data[0]).save(os.path.join(
        here, f"out_{res['model']}_{mode}_{te_dev}-{unet_dev}-{vae_dev}_{steps}.png"))
    if mode == "t2i" and not os.path.exists(os.path.join(here, "init.png")):
        Image.fromarray(out.data[0]).save(os.path.join(here, "init.png"))
except Exception as e:  # report and continue
    res["error"] = repr(e)[:400]
print("RESULT " + json.dumps(res), flush=True)
with open(os.path.join(here, "results.jsonl"), "a") as fh:
    fh.write(json.dumps(res) + chr(10))
sys.stdout.flush()
os._exit(0)
