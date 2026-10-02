"""Live mode: the same pipeline on a real camera + microphone, fully offline.

Sources (the "robot adapter"):
  --camera 0                         laptop webcam (device index)
  --camera http://<pidog>:9000/mjpg  SunFounder PiDog camera stream (vilib MJPEG)
  --camera some_video.mp4            a recording (for testing)
  --mic default | <device index>     a microphone (e.g. the hand-held close-talk mic)
  --mic some_audio.wav               a recording, streamed in real time (for testing)

The exhibition UI (demo/local.html#live) polls GET /live/session.json and posts
the switches to POST /live/sensors {"camera": bool, "microphone": bool}.
A switched-off sensor is gated AT THE SOURCE: its frames/samples are dropped
before any model sees them. POST /live/forget wipes the robot's memory.
Nothing is written to disk: frames and audio live in RAM for seconds only.

Usage (from prototype/): python live/run_live.py --camera 0 --mic default
then open http://127.0.0.1:8800/local.html#live
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from robotsees.config import SLOTS  # noqa: E402
from robotsees.fusion import EvidenceMemory, all_configs  # noqa: E402
from robotsees.session import robot_eye_view  # noqa: E402
from robotsees.ui_export import lite_snapshot  # noqa: E402
from robotsees.xai import snapshot  # noqa: E402

DEMO = os.path.join(HERE, "..", "demo")


class LiveRobot:
    def __init__(self, vision, audio, fps: float = 2.0, window: float = 5.0):
        self.vision, self.audio = vision, audio
        self.fps, self.window = fps, window
        self.lock = threading.Lock()
        self.enabled = {"camera": False, "microphone": False}   # off by default
        self.reset()

    def reset(self):
        with getattr(self, "lock", threading.Lock()):
            self.memory = EvidenceMemory()
            self.t0 = time.time()
            self.frames, self.audio_events, self.timeline = [], [], []
            self.last_img = None
            if self.vision is not None:
                self.vision.reset()

    def now(self) -> float:
        return round(time.time() - self.t0, 2)

    # -- camera ------------------------------------------------------------
    def camera_loop(self, source):
        import cv2
        cap = cv2.VideoCapture(int(source) if str(source).isdigit() else source)
        is_file = os.path.exists(str(source))
        period = 1.0 / self.fps
        while True:
            ok, bgr = cap.read()
            if not ok:
                if is_file:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                time.sleep(0.5)
                continue
            if not self.enabled["camera"]:          # source-side gating: drop the frame
                time.sleep(period)
                continue
            rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
            k = 960 / max(rgb.shape[:2])
            if k < 1:
                rgb = cv2.resize(rgb, (int(rgb.shape[1] * k), int(rgb.shape[0] * k)), interpolation=cv2.INTER_AREA)
            t = self.now()
            fr = self.vision.analyse_frame(rgb, t)
            view = robot_eye_view(rgb, fr, width=360)
            ok, jpg = cv2.imencode(".jpg", cv2.cvtColor(view, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 75])
            with self.lock:
                self.memory.add(fr.observations)
                self.last_img = "data:image/jpeg;base64," + base64.b64encode(jpg.tobytes()).decode()
                self.frames.append({"t": t, "person": fr.person, "quality": round(fr.quality, 3), "swatch": fr.swatch})
                self.frames = self.frames[-400:]
            del rgb, bgr, view                          # nothing kept
            time.sleep(max(0.0, period - 0.05) if is_file else 0)

    # -- microphone ----------------------------------------------------------
    def mic_loop(self, source):
        sr = 16000
        n = int(self.window * sr)
        if os.path.exists(str(source)):
            from robotsees.session import load_audio
            y = load_audio(source)
            k = 0
            while True:
                chunk = y[k:k + n]
                k = (k + n) % max(1, len(y) - n)
                time.sleep(self.window)                 # real-time pacing
                self._audio_window(chunk, sr)
        import sounddevice as sd
        dev = None if source in (None, "default") else int(source)
        buf = []
        with sd.InputStream(samplerate=sr, channels=1, dtype="float32", device=dev) as stream:
            while True:
                data, _ = stream.read(int(0.25 * sr))
                buf.append(data[:, 0].copy())
                if sum(len(b) for b in buf) >= n:
                    chunk = np.concatenate(buf)[:n]
                    buf = []
                    self._audio_window(chunk, sr)

    def _audio_window(self, chunk, sr):
        if not self.enabled["microphone"]:           # source-side gating: drop the samples
            return
        t_end = self.now()
        r = self.audio.analyse(chunk, sr, t0=max(0.0, t_end - len(chunk) / sr))
        for o in r.observations:
            if o.slot in ("voice", "energy"):
                o.t = t_end
        with self.lock:
            self.memory.add(r.observations)
            self.audio_events.append({
                "t0": round(max(0.0, t_end - len(chunk) / sr), 2), "t1": t_end,
                "keywords": [{"slot": o.slot, "value": o.detail.get("word"), "canon": next(iter(o.likelihood)),
                              "t": round(float(o.t), 2), "p": o.detail.get("asr_prob")}
                             for o in r.observations if o.slot in ("animal", "colour")],
                "loudness_db": r.loudness_db, "snr_db": r.snr_db,
                "speech_s": round(r.speech_seconds, 2), "quality": round(r.quality, 3)})
        del chunk                                       # transcript and samples are discarded

    # -- state for the UI ----------------------------------------------------
    def session(self) -> dict:
        with self.lock:
            t = self.now()
            step = {"t": t, "configs": {("+".join(c) or "none"): lite_snapshot(snapshot(self.memory, c, t))
                                        for c in all_configs()}}
            self.timeline = [s for s in self.timeline if s["t"] < t - 0.5][-300:] + [step]
            frames = [dict(f) for f in self.frames]
            if frames and self.last_img:
                frames[-1]["img"] = self.last_img
            return {"id": "live", "variant": "live", "label": "Live", "live": True,
                    "enabled": dict(self.enabled), "duration": t,
                    "source": {"dataset": "live camera and microphone (nothing recorded)"},
                    "conditions": {"camera_degrade": 0.0, "audio_snr": None},
                    "slots": {k: {"question": v.question, "values": list(v.values), "sensors": list(v.sensors),
                                  "how": v.how} for k, v in SLOTS.items()},
                    "frames": frames, "audio": list(self.audio_events), "timeline": list(self.timeline)}


def make_handler(robot: LiveRobot):
    class H(SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=DEMO, **k)

        def log_message(self, *a):
            pass

        def _json(self, obj, code=200):
            body = json.dumps(obj, separators=(",", ":"), default=float).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path.startswith("/live/session.json"):
                return self._json(robot.session())
            return super().do_GET()

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(n) or b"{}")
            if self.path.startswith("/live/sensors"):
                for k in ("camera", "microphone"):
                    if k in data:
                        robot.enabled[k] = bool(data[k])
                return self._json({"enabled": robot.enabled})
            if self.path.startswith("/live/forget"):
                robot.reset()
                return self._json({"forgotten": True})
            return self._json({"error": "unknown"}, 404)
    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--camera", default="0")
    ap.add_argument("--mic", default="default")
    ap.add_argument("--port", type=int, default=8800)
    ap.add_argument("--asr", default="base", help="faster-whisper size (base on CPU, small/turbo on GPU)")
    ap.add_argument("--language", default=None, help="fixed language chosen at the booth, e.g. en/fr/nl")
    ap.add_argument("--calibration-db", type=float, default=-30.0)
    ap.add_argument("--start-on", action="store_true", help="start with both sensors on (testing only)")
    args = ap.parse_args()
    from robotsees.perception.audio import AudioPerception
    from robotsees.perception.vision import VisionPerception
    robot = LiveRobot(VisionPerception(), AudioPerception(args.asr, language=args.language,
                                                          calibration_db=args.calibration_db))
    if args.start_on:
        robot.enabled = {"camera": True, "microphone": True}
    threading.Thread(target=robot.camera_loop, args=(args.camera,), daemon=True).start()
    threading.Thread(target=robot.mic_loop, args=(args.mic,), daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(robot))
    print(f"Live robot on http://127.0.0.1:{args.port}/local.html#live  (sensors start OFF; Ctrl+C to stop)", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
