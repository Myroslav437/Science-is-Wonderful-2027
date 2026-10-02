"""Compact, self-contained session files for the exhibition UI.

One JSON per (visitor, variant): frames are embedded as small pixelated JPEG
data URIs, only the fields the screen needs are kept, numbers are rounded.
Contract (consumed by demo/app.html):

{
  "id", "variant", "label", "source": {...}, "duration",
  "slots":    {slot: {"question", "values", "sensors", "how": {sensor: text}}},
  "frames":   [{"t", "img", "person", "quality", "swatch"}],
  "audio":    [{"t0", "t1", "keywords": [{"slot", "value", "canon", "t", "p"}],
                "loudness_db", "words_per_second", "snr_db", "quality"}],
  "timeline": [{"t", "configs": {"camera+microphone"|"camera"|"microphone"|"none": SNAP}}],
  "imagination": {config: {"img", "prompt", "words"}}   # optional, see render/imagination.py
}
SNAP = {"summary": {"known", "total", "mean_certainty", "sensor_share"},
        "slots": {slot: {"best", "certainty", "certainty_phrase", "certainty_score", "values",
                         "probs", "clues": {sensor: log-odds}, "evidence": [...], "explanation": [...]}}}
"""
from __future__ import annotations

import base64
import json
import os


def _r(x, n=3):
    return round(float(x), n)


def lite_snapshot(snap: dict) -> dict:
    slots = {}
    for k, s in snap["slots"].items():
        slots[k] = {
            "best": s["best"], "certainty": s["certainty"], "certainty_phrase": s["certainty_phrase"],
            "certainty_score": _r(s["certainty_score"]),
            "probs": [_r(p) for p in s["probs"]],
            "clues": {m: _r(v) for m, v in s["clues"].items()},
            "evidence": [{"t": e["t"], "sensor": e["sensor"], "evidence": e["evidence"],
                          "push": _r(e["push"]), "count": e.get("count", 1)} for e in s["evidence"][:3]],
            "explanation": s["explanation"],
        }
    return {"summary": snap["summary"], "slots": slots}


def export(session: dict, frames_dir: str | None, out_path: str, *, sid: str, variant: str,
           label: str, source: dict, imagination: dict | None = None) -> str:
    frames = []
    for f in session["frames"]:
        rec = {"t": f["t"], "person": f["person"], "quality": f["quality"], "swatch": f.get("swatch")}
        if frames_dir and f.get("img"):
            with open(os.path.join(frames_dir, f["img"]), "rb") as fh:
                rec["img"] = "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode()
        frames.append(rec)
    out = {
        "id": sid, "variant": variant, "label": label, "source": source,
        "duration": session["meta"]["duration"],
        "conditions": {"camera_degrade": session["meta"]["camera_degrade"],
                       "audio_snr": session["meta"]["audio_snr"]},
        "slots": session["slots"],
        "frames": frames,
        "audio": [{k: v for k, v in a.items() if k != "language"} for a in session["audio"]],
        "timeline": [{"t": step["t"], "configs": {c: lite_snapshot(s) for c, s in step["configs"].items()}}
                     for step in session["timeline"]],
    }
    if imagination:
        out["imagination"] = imagination
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, separators=(",", ":"), default=float)
    return out_path
