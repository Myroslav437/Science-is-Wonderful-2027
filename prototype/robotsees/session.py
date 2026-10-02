"""Run one "visitor" (a real recorded clip) through the full pipeline.

camera frames (2 fps) ---> VisionPerception --\
                                               >-- EvidenceMemory --> fusion + XAI snapshots
audio windows (~6 s) ---> AudioPerception  ---/      (for every sensor configuration, every second)

The camera and microphone are processed once; each sensor configuration is
then just a different set of evidence the fusion is allowed to use -- the same
thing that happens when a visitor flips a switch at the booth.

Output: a JSON timeline for the exhibition UI plus privacy-filtered
"robot's-eye" frames (pixelated, with the boxes the robot used).
"""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict

import numpy as np

from .config import CAMERA, MICROPHONE, MODALITIES, SLOTS
from .fusion import EvidenceMemory, all_configs
from .xai import snapshot


def load_audio(path: str, start: float = 0.0, end: float | None = None, sr: int = 16000) -> np.ndarray:
    import imageio_ffmpeg
    cmd = [imageio_ffmpeg.get_ffmpeg_exe(), "-v", "quiet", "-ss", str(start)]
    if end is not None:
        cmd += ["-t", str(end - start)]
    cmd += ["-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def robot_eye_view(frame: np.ndarray, fr, block: int = 12, width: int = 480) -> np.ndarray:
    """What the public screen shows: a pixelated frame + the regions the robot used."""
    import cv2
    h, w = frame.shape[:2]
    scale = width / w
    small = cv2.resize(frame, (width, int(h * scale)), interpolation=cv2.INTER_AREA)
    sh, sw = small.shape[:2]
    pix = cv2.resize(cv2.resize(small, (max(1, sw // block), max(1, sh // block)),
                                interpolation=cv2.INTER_AREA), (sw, sh), interpolation=cv2.INTER_NEAREST)
    out = pix.copy()
    if fr is not None:
        if fr.head_box:
            x0, y0, x1, y1 = (int(v * scale) for v in fr.head_box)
            cv2.rectangle(out, (x0, y0), (x1, y1), (47, 125, 225), 2)
        if fr.torso_box:
            x0, y0, x1, y1 = (int(v * scale) for v in fr.torso_box)
            cv2.rectangle(out, (x0, y0), (x1, y1), (255, 255, 255), 2)
            if fr.swatch:
                cv2.rectangle(out, (x0, max(0, y0 - 22)), (x0 + 22, y0), tuple(int(c) for c in fr.swatch), -1)
    return out


def perceive_camera(video: str, start: float, end: float, vision, fps: float = 2.0,
                    camera_degrade: float = 0.0, frames_dir: str | None = None,
                    rotate: int | None = None, pixel_aspect: float = 1.0):
    """Camera stream -> (observations, frame log). Pictures are analysed in RAM;
    only the pixelated robot's-eye view is written (for the screen / video)."""
    import cv2
    from .perception.vision import degrade
    obs, frames = [], []
    duration = end - start
    vision.reset()
    cap = cv2.VideoCapture(video)
    cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
    next_t, idx = 0.0, 0
    while True:
        ok, bgr = cap.read()
        if not ok:
            break
        t = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000 - start
        if t > duration:
            break
        if t + 1e-6 < next_t:
            continue
        next_t += 1 / fps
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        if rotate is not None:
            rgb = cv2.rotate(rgb, rotate)
        if pixel_aspect != 1.0:
            rgb = cv2.resize(rgb, (int(rgb.shape[1] * pixel_aspect), rgb.shape[0]), interpolation=cv2.INTER_AREA)
        if max(rgb.shape[:2]) > 960:
            k = 960 / max(rgb.shape[:2])
            rgb = cv2.resize(rgb, (int(rgb.shape[1] * k), int(rgb.shape[0] * k)), interpolation=cv2.INTER_AREA)
        rgb = degrade(rgb, camera_degrade, seed=idx)
        fr = vision.analyse_frame(rgb, round(t, 2))
        obs.extend(fr.observations)
        rec = {"t": round(t, 2), "person": fr.person, "quality": round(fr.quality, 3),
               "scores": fr.scores, "swatch": fr.swatch}
        if frames_dir:
            os.makedirs(frames_dir, exist_ok=True)
            name = f"f{idx:04d}.jpg"
            cv2.imwrite(os.path.join(frames_dir, name),
                        cv2.cvtColor(robot_eye_view(rgb, fr, width=360), cv2.COLOR_RGB2BGR),
                        [cv2.IMWRITE_JPEG_QUALITY, 78])
            rec["img"] = name
        frames.append(rec)
        idx += 1
    return obs, frames


def perceive_audio(audio_path: str, start: float, end: float, audio, audio_window: float = 6.0,
                   audio_snr: float | None = None, noise: np.ndarray | None = None):
    """Microphone stream -> (observations, event log). Only closed-vocabulary
    keywords leave this function, never the transcript."""
    from .perception.audio import add_noise
    obs, events = [], []
    duration = end - start
    y = load_audio(audio_path, start, end)
    if audio_snr is not None:
        y = add_noise(y, audio_snr, seed=1, noise=noise)
    n = int(audio_window * 16000)
    for k in range(0, len(y), n):
        chunk = y[k:k + n]
        if len(chunk) < 16000 * 0.5:
            continue
        r = audio.analyse(chunk, 16000, t0=k / 16000)
        # The robot only knows about loudness once it has heard the window.
        t_end = round(min(duration, (k + len(chunk)) / 16000), 2)
        for o in r.observations:
            if o.slot in ("voice", "energy"):
                o.t = t_end
        obs.extend(r.observations)
        events.append({
            "t0": round(k / 16000, 2), "t1": t_end,
            "keywords": [{"slot": o.slot, "value": o.detail.get("word"), "canon": next(iter(o.likelihood)),
                          "t": round(float(o.t), 2), "p": o.detail.get("asr_prob")}
                         for o in r.observations if o.slot in ("animal", "colour")],
            "loudness_db": r.loudness_db, "words_per_second": r.words_per_second,
            "snr_db": r.snr_db, "speech_s": round(r.speech_seconds, 2), "quality": round(r.quality, 3),
            "language": r.language})
    return obs, events


def assemble(cam_obs: list, frames: list, aud_obs: list, events: list, duration: float,
             step: float = 1.0, meta: dict | None = None) -> dict:
    memory = EvidenceMemory()
    memory.add(list(cam_obs))
    memory.add(list(aud_obs))
    configs = all_configs()
    times = sorted(set(list(np.arange(0, duration + 1e-6, step).round(2)) + [round(duration, 2)]))
    timeline = []
    for t in times:
        snaps = {}
        for cfg in configs:
            snap = snapshot(memory, cfg, float(t))
            for s in snap["slots"].values():
                s.pop("counterfactuals", None)  # other configs are stored side by side
            snaps["+".join(cfg) or "none"] = snap
        timeline.append({"t": float(t), "configs": snaps})
    final = {("+".join(cfg) or "none"): snapshot(memory, cfg) for cfg in configs}
    return {
        "meta": {"duration": round(duration, 2), "camera_degrade": 0.0, "audio_snr": None, **(meta or {})},
        "slots": {k: {"question": v.question, "values": list(v.values),
                      "sensors": list(v.sensors), "how": v.how} for k, v in SLOTS.items()},
        "frames": frames, "audio": events,
        "observations": [{**{k: v for k, v in asdict(o).items() if k != "detail"},
                          "detail": {k: v for k, v in o.detail.items() if k != "box"}}
                         for o in memory.observations],
        "timeline": timeline, "final": final,
    }


def run_session(video: str | None, audio_path: str | None, start: float, end: float,
                vision=None, audio=None, fps: float = 2.0, audio_window: float = 6.0,
                camera_degrade: float = 0.0, audio_snr: float | None = None,
                frames_dir: str | None = None, step: float = 1.0, meta: dict | None = None,
                rotate: int | None = None, pixel_aspect: float = 1.0) -> dict:
    cam_obs, frames, aud_obs, events = [], [], [], []
    if video and vision is not None:
        cam_obs, frames = perceive_camera(video, start, end, vision, fps, camera_degrade,
                                          frames_dir, rotate, pixel_aspect)
    if audio_path and audio is not None:
        aud_obs, events = perceive_audio(audio_path, start, end, audio, audio_window, audio_snr)
    return assemble(cam_obs, frames, aud_obs, events, end - start, step,
                    {**(meta or {}), "start": start, "end": end, "fps": fps,
                     "camera_degrade": camera_degrade, "audio_snr": audio_snr})


def save(session: dict, path: str) -> None:
    def conv(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(session, f, default=conv, separators=(",", ":"))
