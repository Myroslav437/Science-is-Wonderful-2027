"""The robot's imagination, v2: restyle the robot's own drawing.

For each visitor and sensor configuration we take the procedural avatar the
exhibition screen draws (renderAvatar in demo/app.html - every element is one
inferred slot), rasterise it, and let a small image generator restyle it
(img2img, strength 0.7) with a prompt built only from closed-vocabulary words.
Because the generator starts from the avatar, the picture keeps the colours,
pose and companion the robot actually inferred; it never sees a camera image.

Generator: LCM-Dreamshaper v7 int8 (OpenVINO, MIT licence) with TAESD, 4 steps,
on the laptop's integrated GPU (~2.6 s per image measured on the Core Ultra 7 255U).
Each image carries machine-readable AI-generated marking (IPTC + EXIF).

Usage (from prototype/): python experiments/build_imagination.py
Updates demo/sessions/<id>-clean.json ("imagination") and results/sessions/*-imagination-*.jpg
"""
from __future__ import annotations

import base64
import contextlib
import http.server
import io
import json
import os
import socketserver
import sys
import threading

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from robotsees.render.imagination import save_marked  # noqa: E402

ROOT = os.path.join(HERE, "..", "..")
DEMO = os.path.join(HERE, "..", "demo")
RES = os.path.join(HERE, "results", "sessions")
MODEL = os.path.join(ROOT, "models", "ov", "lcm_taesd")
CONFIGS = ("camera+microphone", "camera", "microphone")

STYLE = "children's crayon drawing of a cute friendly robot mascot"
TAIL = "simple shapes, bold colours, white paper"
PHRASES = {
    "shirt": lambda v: f"wearing {'an' if v[0] in 'aeiou' else 'a'} {v} t-shirt",
    "glasses": lambda v: "wearing round glasses" if v == "glasses" else None,
    "animal": lambda v: f"with a small friendly pet {v}",
    "colour": lambda v: f"{v} background",
    "energy": lambda v: {"still": "standing calmly", "moving": "waving hello", "very active": "jumping happily"}[v],
    "voice": lambda v: {"quiet": "whispering", "normal": None, "loud": "singing loudly"}[v],
}
ORDER = ("shirt", "glasses", "energy", "voice", "animal", "colour")


def words_for(snap: dict) -> list[str]:
    """Only what the robot believes at least 'guessing' level; uncertain slots stay out."""
    out = []
    for slot in ORDER:
        s = snap["slots"][slot]
        if s["certainty"] != "unknown":
            p = PHRASES[slot](s["best"])
            if p:
                out.append(p)
    return out


@contextlib.contextmanager
def serve(directory: str, port: int = 8793):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=directory, **k)  # noqa: E731
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            yield f"http://127.0.0.1:{port}"
        finally:
            httpd.shutdown()


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    args = ap.parse_args()
    import openvino as ov
    import openvino_genai as g
    from playwright.sync_api import sync_playwright

    pipe = g.Image2ImagePipeline(MODEL)
    pipe.reshape(1, 512, 512, pipe.get_generation_config().guidance_scale)
    pipe.compile("GPU", "GPU", "GPU", config={"CACHE_DIR": os.path.join(ROOT, "models", "ov", "cache")})
    index = json.load(open(os.path.join(DEMO, "sessions", "index.json"), encoding="utf-8"))
    with serve(DEMO) as base, sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.emulate_media(color_scheme="light")
        page.goto(base + "/local.html")
        page.wait_for_function("window.demo && window.demo.ready")
        page.evaluate("window.demo.ready")
        page.evaluate("""() => { const d = document.createElement('div'); d.id = '__avatar_raster';
            d.style.cssText = 'position:fixed;left:0;top:0;width:512px;height:512px;background:#fff;z-index:99999;display:flex;align-items:center;justify-content:center';
            document.body.appendChild(d); }""")
        for v in index["visitors"]:
            if args.only and v["id"] not in args.only.split(","):
                continue
            ui_path = os.path.join(DEMO, "sessions", v["variants"]["clean"])
            full_path = os.path.join(RES, f"{v['id']}-clean.json")
            ui = json.load(open(ui_path, encoding="utf-8"))
            full = json.load(open(full_path, encoding="utf-8"))
            imagination = {}
            for cfg in CONFIGS:
                snap = ui["timeline"][-1]["configs"][cfg]
                page.evaluate("""(snap) => { const d = document.getElementById('__avatar_raster');
                    d.innerHTML = window.demo.renderAvatar(snap, 480); }""", snap)
                png = page.locator("#__avatar_raster").screenshot()
                sketch = Image.open(io.BytesIO(png)).convert("RGB").resize((512, 512))
                words = words_for(snap)
                prompt = ", ".join([STYLE] + words + [TAIL])
                r = pipe.generate(prompt, ov.Tensor(np.array(sketch)[None]), strength=0.7,
                                  num_inference_steps=4, rng_seed=7)
                img = Image.fromarray(r.data[0])
                save_marked(img, os.path.join(RES, f"{v['id']}-imagination-{cfg}.jpg"), prompt, 88)
                sketch.save(os.path.join(RES, f"{v['id']}-avatar-{cfg}.png"))
                buf = io.BytesIO()
                save_marked(img, buf, prompt, 82)
                imagination[cfg] = {"img": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(),
                                    "prompt": prompt, "words": words,
                                    "generator": "LCM-Dreamshaper v7 (OpenVINO int8, MIT), img2img from the robot's own drawing, strength 0.7"}
                print(v["id"], cfg, "|", "; ".join(words) or "(no words)", flush=True)
            ui["imagination"] = imagination
            json.dump(ui, open(ui_path, "w", encoding="utf-8"), separators=(",", ":"))
            full["imagination_prompts"] = {c: {"prompt": d["prompt"], "words": d["words"]} for c, d in imagination.items()}
            json.dump(full, open(full_path, "w", encoding="utf-8"), separators=(",", ":"))
        browser.close()


if __name__ == "__main__":
    main()
