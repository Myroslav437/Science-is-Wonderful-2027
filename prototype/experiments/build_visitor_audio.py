"""Export each visitor's voice for the exhibition screen (demo/audio/*.m4a).

Exactly the audio the pipeline analysed for that visitor's segment, aligned so
that t = 0 is the start of the session:
  clean       the recording itself
  noisy-ears  the same recording mixed with the crowd babble at 0 dB SNR
              (reconstructed with the same seed as build_sessions.py)
The "foggy-eyes" variant only changes the camera, so it reuses the clean audio.
Loudness is matched across visitors (recordings differ by up to 33 dB).

Run after build_sessions.py (from prototype/): python experiments/build_visitor_audio.py
Writes demo/audio/<id>-<variant>.mp3 and adds an "audio" map to demo/sessions/index.json.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "video"))
from render_video import VisitorAudio  # noqa: E402

DEMO = os.path.join(HERE, "..", "demo")
AUDIO_DIR = os.path.join(DEMO, "audio")
SR = 22050


def normalise(y: np.ndarray, target_db: float = -21.0) -> np.ndarray:
    frame = int(0.05 * SR)
    e = np.array([np.sqrt(np.mean(y[i:i + frame] ** 2) + 1e-12) for i in range(0, len(y), frame)])
    speech_rms = np.sqrt(np.mean(np.sort(e)[len(e) // 2:] ** 2)) + 1e-9
    y = y * 10 ** (target_db / 20) / speech_rms
    peak = np.max(np.abs(y))
    if peak > 0.95:
        y *= 0.95 / peak
    fade = int(0.05 * SR)
    y[:fade] *= np.linspace(0, 1, fade)
    y[-fade:] *= np.linspace(1, 0, fade)
    return y.astype(np.float32)


def main():
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    os.makedirs(AUDIO_DIR, exist_ok=True)
    va = VisitorAudio(SR)
    idx_path = os.path.join(DEMO, "sessions", "index.json")
    idx = json.load(open(idx_path, encoding="utf-8"))
    for v in idx["visitors"]:
        amap = {}
        for variant in ("clean", "noisy-ears"):
            if variant not in v["variants"]:
                continue
            y = normalise(va.segment(v["id"], variant).copy())
            tmp = os.path.join(AUDIO_DIR, "_tmp.wav")
            with wave.open(tmp, "wb") as w:
                w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
                w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())
            name = f"{v['id']}-{variant}.mp3"
            subprocess.run([ff, "-y", "-v", "error", "-i", tmp, "-c:a", "libmp3lame", "-b:a", "64k",
                            os.path.join(AUDIO_DIR, name)], check=True)
            os.remove(tmp)
            amap[variant] = "audio/" + name
            print(name, round(len(y) / SR, 1), "s", os.path.getsize(os.path.join(AUDIO_DIR, name)) // 1024, "KB", flush=True)
        if "foggy-eyes" in v["variants"] and "clean" in amap:
            amap["foggy-eyes"] = amap["clean"]       # only the camera is foggy
        v["audio"] = amap
    idx["audio_note"] = ("Visitor voices: the original recordings (loudness-matched); the noisy-room files contain the "
                         "crowd mix the robot heard. Seamless Interaction, Meta 2025, CC BY-NC 4.0.")
    json.dump(idx, open(idx_path, "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
