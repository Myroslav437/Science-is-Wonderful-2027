"""Build all prototype sessions: every visitor x {clean, noisy-ears, foggy-eyes}.

Each camera and audio stream is perceived once per condition and re-used:
  clean      = clean camera + clean audio
  noisy-ears = clean camera + audio mixed with crowd babble at 0 dB SNR
  foggy-eyes = degraded camera (blur + dark + sensor noise, level 0.7) + clean audio
Outputs
  demo/sessions/<id>-<variant>.json      compact UI files (pixelated frames embedded)
  experiments/results/sessions/<id>-<variant>.json   full sessions for analysis
  demo/sessions/index.json
Usage: python experiments/build_sessions.py [--only v01,v02] [--no-imagination]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import random
import shutil
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from robotsees.perception.audio import AudioPerception  # noqa: E402
from robotsees.perception.vision import VisionPerception  # noqa: E402
from robotsees.session import assemble, perceive_audio, perceive_camera, save  # noqa: E402
from robotsees.ui_export import export  # noqa: E402

ROOT = os.path.join(HERE, "..", "..")
DEMO = os.path.join(HERE, "..", "demo", "sessions")
RES = os.path.join(HERE, "results", "sessions")
TMP = os.path.join(ROOT, "scratch", "frames")
SEAM = os.path.join(ROOT, "data", "seamless")
SOURCE = "Seamless Interaction (Meta, 2025), CC BY-NC 4.0 - naturalistic/dev"


def babble(seconds: float, seed: int = 0) -> np.ndarray:
    """Crowded-hall noise: 6 overlapping streams of other talkers (Lombard GRID, CC BY 4.0)."""
    import soundfile as sf
    rng = random.Random(seed)
    files = sorted(glob.glob(os.path.join(ROOT, "data", "grid", "audio", "*_p_*.wav")))
    n = int(seconds * 16000)
    mix = np.zeros(n, np.float32)
    for _ in range(6):
        stream = []
        while sum(len(x) for x in stream) < n:
            y, sr = sf.read(rng.choice(files), dtype="float32")
            stream.append(y / (np.sqrt(np.mean(y ** 2)) + 1e-9))
        mix += np.concatenate(stream)[:n]
    return mix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--no-imagination", action="store_true")
    args = ap.parse_args()
    import cv2
    cfg = json.load(open(os.path.join(HERE, "visitors.json")))
    visitors = [v for v in cfg["visitors"] if not args.only or v["id"] in args.only.split(",")]
    os.makedirs(DEMO, exist_ok=True)
    os.makedirs(RES, exist_ok=True)
    vision = VisionPerception()
    audio = AudioPerception("small", language=None)
    imag = None
    timings = {}
    for v in visitors:
        t0 = time.time()
        video = os.path.join(SEAM, "video", v["file"] + ".mp4")
        wav = os.path.join(SEAM, "audio", v["file"] + ".wav")
        rot = {"ccw": cv2.ROTATE_90_COUNTERCLOCKWISE, "cw": cv2.ROTATE_90_CLOCKWISE}.get(v["rotate"])
        audio.calibration_db = v["calibration_db"]
        dur = v["end"] - v["start"]
        streams = {}
        for name, deg in [("cam_clean", 0.0), ("cam_fog", 0.7)]:
            fdir = os.path.join(TMP, v["id"], name)
            shutil.rmtree(fdir, ignore_errors=True)
            streams[name] = (*perceive_camera(video, v["start"], v["end"], vision, 2.0, deg, fdir,
                                              rot, v["pixel_aspect"]), fdir)
        streams["aud_clean"] = perceive_audio(wav, v["start"], v["end"], audio)
        streams["aud_noisy"] = perceive_audio(wav, v["start"], v["end"], audio, audio_snr=0.0,
                                              noise=babble(dur + 1, seed=int(v["id"][1:])))
        variants = {"clean": ("cam_clean", "aud_clean", 0.0, None),
                    "noisy-ears": ("cam_clean", "aud_noisy", 0.0, 0.0),
                    "foggy-eyes": ("cam_fog", "aud_clean", 0.7, None)}
        files = {}
        for var, (cam, aud, deg, snr) in variants.items():
            cam_obs, frames, fdir = streams[cam]
            aud_obs, events = streams[aud]
            s = assemble(cam_obs, frames, aud_obs, events, dur,
                         meta={"visitor": v["id"], "variant": var, "start": v["start"], "end": v["end"],
                               "camera_degrade": deg, "audio_snr": snr, "fps": 2.0,
                               "calibration_db": v["calibration_db"]})
            imagination = None
            if var == "clean" and not args.no_imagination:
                if imag is None:
                    from robotsees.render.imagination import Imagination, save_marked
                    imag = Imagination()
                imagination = {}
                for c in ("camera+microphone", "camera", "microphone"):
                    d = imag.draw_for(s["final"][c], seed=7)
                    save_marked(d["pil"], os.path.join(RES, f"{v['id']}-imagination-{c}.jpg"), d["prompt"], 88)
                    imagination[c] = {k: d[k] for k in ("img", "prompt", "words")}
                s["imagination_prompts"] = {c: {"prompt": d["prompt"], "words": d["words"]}
                                            for c, d in imagination.items()}
            save({k: val for k, val in s.items() if k != "frames"} | {"truth": v["truth"]},
                 os.path.join(RES, f"{v['id']}-{var}.json"))
            name = f"{v['id']}-{var}.json"
            export(s, fdir, os.path.join(DEMO, name), sid=v["id"], variant=var, label=v["label"],
                   source={"dataset": SOURCE, "file": v["file"], "segment": [v["start"], v["end"]]},
                   imagination=imagination)
            files[var] = name
        v["_files"] = files
        timings[v["id"]] = round(time.time() - t0, 1)
        print(v["id"], "done in", timings[v["id"]], "s", flush=True)

    # index.json (merge with visitors already built)
    idx_path = os.path.join(DEMO, "index.json")
    idx = {"visitors": []}
    if os.path.exists(idx_path):
        idx = json.load(open(idx_path))
        idx["visitors"] = [x for x in idx["visitors"] if x["id"].startswith("v") and not x["id"].startswith("sample")
                           and os.path.exists(os.path.join(DEMO, next(iter(x["variants"].values()))))]
    known = {x["id"]: x for x in idx["visitors"]}
    for v in visitors:
        prev_audio = known.get(v["id"], {}).get("audio")      # keep voices from build_visitor_audio.py
        known[v["id"]] = {"id": v["id"], "label": v["label"], "story": v["story"], "variants": v["_files"],
                          **({"audio": prev_audio} if prev_audio else {})}
    idx = {"note": ("Each visitor is a real person from a public dataset, processed by the real pipeline "
                    "(MediaPipe + CLIP ViT-B/32 + Silero VAD + Whisper small + evidence fusion). "
                    "Variants re-use the same recording with a simulated sensor problem."),
           "source": SOURCE,
           "visitors": [known[k] for k in sorted(known)]}
    json.dump(idx, open(idx_path, "w"), indent=1)
    json.dump(timings, open(os.path.join(HERE, "results", "build_timings.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
