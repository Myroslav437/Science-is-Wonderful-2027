"""Render the partner demo video from the real prototype UI.

The exhibition screen (demo/local.html) is driven through its window.demo API
by a shot list, captured frame by frame with Playwright (headless Chromium),
and combined with the robot's lines spoken by an offline TTS voice (Piper) and
the visitors' own recorded voices (the same audio the pipeline analysed; for the
"noisy room" scenes the exact crowd-babble mix the robot heard). Everything on
screen is the real pipeline output for real dataset recordings; only the stage
titles and captions are added for the video.

Usage (from prototype/):  python video/render_video.py [--fps 12] [--only A,B] [--keep-frames]
Output: video/out/how_does_a_robot_see_you.mp4  +  video/out/storyboard.md
"""
from __future__ import annotations

import argparse
import contextlib
import http.server
import json
import os
import shutil
import socketserver
import subprocess
import threading
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEMO = os.path.join(HERE, "..", "demo")
OUT = os.path.join(HERE, "out")
VOICE = os.path.join(HERE, "..", "..", "models", "tts", "en_US-amy-medium.onnx")
W, H = 1920, 1080

BOTH = {"camera": True, "microphone": True}
EYES = {"camera": True, "microphone": False}
EARS = {"camera": False, "microphone": True}
NONE = {"camera": False, "microphone": False}

# Each scene: duration (s), optional playback of a session, and timed actions.
# Action tuples: (t_in_scene, method, *args)  -> window.demo[method](*args)
#                (t, "say", text)            -> robot speech bubble + TTS audio
# "voice": [(t_in_scene, visitor, variant, from_s, to_s)] -> the visitor's recorded
#          speech (seconds relative to that visitor's segment) mixed into the soundtrack
SHOTS = [
    {"id": "title", "dur": 7, "load": ("v01", "clean"), "seek": 0, "actions": [
        (0, "setSensors", NONE), (0, "setChrome", False),
        (0, "setStage", "How does a robot see you?",
         "Booth prototype for Science is Wonderful! 2027 - real recordings, real AI models"),
        (0.5, "setCaption", "A small robot dog builds a picture of a visitor from its senses - and explains itself."),
    ]},
    {"id": "meet", "dur": 9, "actions": [
        (0, "setStage", None, None),
        (0.3, "say", "Hi! I'm a robot dog. I'm a computer program, not alive. Let's see what I can learn about you."),
        (0.3, "setCaption", "The robot's camera and microphone stay OFF until the visitor switches them on."),
    ]},
    {"id": "A", "dur": 34, "play": (0, 1.0), "voice": [(0, "v01", "clean", 0, 33)], "actions": [
        (0, "setSensors", BOTH), (0, "setStage", "Demo A - Eyes + ears", "camera and microphone both on"),
        (0.2, "say", "Thank you! My eyes and ears are on."),
        (3, "setCaption", "On the screen the picture is pixelated. The robot looks, then forgets each picture."),
        (9, "highlightSlot", "animal"),
        (9, "setCaption", "The ears pick out 'horse' from what the visitor says: favourite animal - horse."),
        (18, "highlightSlot", "shirt"),
        (18, "setCaption", "The eyes measure the colours of the top: white clothes - but only a guess."),
        (27, "highlightSlot", None),
        (27, "setCaption", "Every answer comes with how sure the robot is, and why."),
    ]},
    {"id": "B", "dur": 11, "load": ("v01", "clean"), "seek": "end", "actions": [
        (0, "setStage", "Demo B - Eyes only", "the visitor switches the ears off"),
        (0.3, "setSensors", EYES), (0.5, "say", "OK. I'll only use my eyes."),
        (2, "highlightSlot", "animal"),
        (2, "setCaption", "Ears off: the favourite animal turns into a question mark. The clothes colour stays."),
    ]},
    {"id": "C", "dur": 11, "seek": "end", "actions": [
        (0, "setStage", "Demo C - Ears only", "eyes off, ears on"),
        (0.3, "setSensors", EARS), (0.5, "say", "OK. I'll only use my ears."),
        (2, "highlightSlot", "shirt"),
        (2, "setCaption", "Eyes off: it still heard 'horse', but it cannot know what the visitor is wearing."),
    ]},
    {"id": "D", "dur": 32, "load": ("v02", "clean"), "seek": "end",
     "voice": [(1.0, "v02", "clean", 2.8, 13.4), (12.3, "v02", "clean", 26.0, 31.5)], "actions": [
        (0, "setSensors", BOTH), (0, "highlightSlot", None),
        (0, "setStage", "Demo D - Why does the robot think this?", "explanations from the robot's own evidence"),
        (1, "highlightSlot", "animal"),
        (1, "setCaption", "Clue balance: 'bunny' and 'rabbit' many times. Even 'not a cat or a dog' adds small cat and dog clues."),
        (12, "highlightSlot", "colour"),
        (12, "setCaption", "Favourite colour BROWN? Listen: she said 'ginger brown' about her rabbit's fur."),
        (18.3, "say", "I heard 'brown' twice, so I think your favourite colour is brown. Was I right?"),
        (25, "setCaption", "The robot spots words but does not understand them. AI can be sure - and still wrong."),
    ]},
    {"id": "noisy", "dur": 13, "load": ("v06", "noisy-ears"), "seek": "end",
     "voice": [(1.5, "v06", "noisy-ears", 20.0, 26.5)], "actions": [
        (0, "highlightSlot", "animal"),
        (0, "setStage", "Trouble 1 - Noisy room", "crowd noise mixed into the microphone"),
        (1, "setCaption", "Listen to what the robot heard: she says 'elephant', but the crowd drowns it - so the robot says it doesn't know."),
    ]},
    {"id": "crowd", "dur": 12, "load": ("v05", "noisy-ears"), "seek": "end",
     "voice": [(1.5, "v05", "noisy-ears", 12.0, 18.0)], "actions": [
        (0, "highlightSlot", "colour"),
        (0, "setStage", "Trouble 1b - Other voices", "in a hall, other people talk too"),
        (1, "setCaption", "Now the robot is SURE her favourite colour is white. Listen: the 'white' comes from other people in the crowd, not from her."),
    ]},
    {"id": "foggy", "dur": 11, "load": ("v01", "foggy-eyes"), "seek": "end", "actions": [
        (0, "highlightSlot", "shirt"),
        (0, "setStage", "Trouble 2 - Foggy lens", "blurred, dark, noisy camera"),
        (1, "setCaption", "Foggy lens: the white top now looks dark, so the robot guesses BLACK. A bad sensor can fool the robot, not only make it unsure."),
    ]},
    {"id": "E", "dur": 31, "load": ("v06", "clean"), "seek": 0, "play": (0, 1.0), "voice": [(0, "v06", "clean", 0, 30)], "actions": [
        (0, "highlightSlot", None),
        (0, "setStage", "Demo E - The picture builds up", "a new visitor, from the first second"),
        (1, "setCaption", "At first the robot knows nothing. Clue by clue its picture fills in: glasses, clothes, words."),
        (15, "highlightSlot", "glasses"),
        (15, "setCaption", "Each part of the drawing shows which sense found it - eyes or ears."),
    ]},
    {"id": "imagination", "dur": 11, "load": ("v01", "clean"), "seek": "end", "actions": [
        (0, "highlightSlot", None),
        (0, "setStage", "The robot's imagination", "an AI-generated picture"),
        (1, "setCaption", "An image generator restyles the robot's own drawing into a robot friend - using only the words the robot believes, never a photo."),
    ]},
    {"id": "never", "dur": 10, "actions": [
        (0, "setStage", "Things the robot will never guess", None),
        (0.5, "say", "I will never guess who you are, how you feel, your age, your gender, or where you come from."),
        (0.5, "setCaption", "Faces and voices don't reveal these reliably - and guessing them about children is not OK."),
    ]},
    {"id": "card", "dur": 10, "actions": [
        (0, "showCard", True), (0, "setStage", None, None),
        (0.5, "setCaption", "The take-home card has no photo and no name. When the visitor leaves, the robot forgets everything."),
        (1, "say", "Here is how I saw you. Now I will forget everything. Bye!"),
    ]},
    {"id": "credits", "dur": 9, "actions": [
        (0, "showCard", False),
        (0, "setStage", "TUAI doctoral network - DC5 sensor fusion & DC7 explainable AI",
         "Silesian University of Technology - Marie Sklodowska-Curie Actions"),
        (0.5, "setCaption", "Recordings: Seamless Interaction (Meta, CC BY-NC 4.0, pixelated). Models: MediaPipe, CLIP ViT-B/32, "
                            "Silero VAD, Whisper small, LCM-Dreamshaper. All on one laptop, offline."),
    ]},
]


@contextlib.contextmanager
def serve(directory: str, port: int = 8791):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=directory, **k)  # noqa: E731
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        th = threading.Thread(target=httpd.serve_forever, daemon=True)
        th.start()
        try:
            yield f"http://127.0.0.1:{port}"
        finally:
            httpd.shutdown()


class Voice:
    def __init__(self):
        self.v = None
        if os.path.exists(VOICE):
            from piper import PiperVoice
            self.v = PiperVoice.load(VOICE)

    def say(self, text: str) -> tuple[np.ndarray, int]:
        if self.v is None:
            return np.zeros(1, np.float32), 22050
        path = os.path.join(OUT, "_tts.wav")
        with wave.open(path, "wb") as w:
            self.v.synthesize_wav(text, w)
        with wave.open(path, "rb") as r:
            sr = r.getframerate()
            y = np.frombuffer(r.readframes(r.getnframes()), np.int16).astype(np.float32) / 32768
        return y, sr


class VisitorAudio:
    """The visitors' recorded speech, exactly as the pipeline received it."""

    def __init__(self, sr: int = 22050):
        import importlib.util
        import sys
        sys.path.insert(0, os.path.join(HERE, ".."))
        spec = importlib.util.spec_from_file_location(
            "build_sessions", os.path.join(HERE, "..", "experiments", "build_sessions.py"))
        self.bs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.bs)
        cfg = json.load(open(os.path.join(HERE, "..", "experiments", "visitors.json"), encoding="utf-8"))
        self.visitors = {v["id"]: v for v in cfg["visitors"]}
        self.sr = sr
        self.cache = {}

    def segment(self, vid: str, variant: str) -> np.ndarray:
        key = (vid, variant)
        if key not in self.cache:
            import librosa
            from robotsees.perception.audio import add_noise
            from robotsees.session import load_audio
            v = self.visitors[vid]
            wav = os.path.join(self.bs.SEAM, "audio", v["file"] + ".wav")
            y = load_audio(wav, v["start"], v["end"])                     # 16 kHz, what the robot analysed
            if variant == "noisy-ears":                                     # same mix as build_sessions.py
                y = add_noise(y, 0.0, seed=1, noise=self.bs.babble(v["end"] - v["start"] + 1, seed=int(vid[1:])))
            self.cache[key] = librosa.resample(y.astype(np.float32), orig_sr=16000, target_sr=self.sr)
        return self.cache[key]

    def snippet(self, vid: str, variant: str, a: float, b: float, target_db: float = -25.0) -> np.ndarray:
        y = self.segment(vid, variant)[int(a * self.sr):int(b * self.sr)].copy()
        if not len(y):
            return y
        frame = int(0.05 * self.sr)
        e = np.array([np.sqrt(np.mean(y[i:i + frame] ** 2) + 1e-12) for i in range(0, len(y), frame)])
        speech_rms = np.sqrt(np.mean(np.sort(e)[len(e) // 2:] ** 2)) + 1e-9   # louder half = speech
        y *= 10 ** (target_db / 20) / speech_rms                               # recordings differ by up to 33 dB
        peak = np.max(np.abs(y))
        if peak > 0.85:
            y *= 0.85 / peak
        fade = min(len(y) // 4, int(0.08 * self.sr))
        if fade:
            y[:fade] *= np.linspace(0, 1, fade)
            y[-fade:] *= np.linspace(1, 0, fade)
        return y.astype(np.float32)


def storyboard_md(shots) -> str:
    lines = ["# Demo video - storyboard and script", "",
             "Rendered automatically by `prototype/video/render_video.py` from the real prototype UI "
             "(real recordings, real model outputs). Stage titles and captions are added for the video; "
             "the robot's lines are spoken by an offline TTS voice (Piper, en_US-amy); the visitors' own recorded voices are "
             "mixed in (loudness-matched, lowered while the robot speaks).", "",
             "| # | Scene | Time | On screen | Visitor audio | Robot says | Caption |", "|---|---|---|---|---|---|---|"]
    t = 0.0
    for i, s in enumerate(shots, 1):
        stage = next((a[2] for a in s["actions"] if a[1] == "setStage" and a[2]), "")
        says = " / ".join(a[2] for a in s["actions"] if a[1] == "say")
        caps = " / ".join(a[2] for a in s["actions"] if a[1] == "setCaption" and a[2])
        view = []
        if "load" in s:
            view.append(f"visitor {s['load'][0]} ({s['load'][1]})")
        sens = [a[2] for a in s["actions"] if a[1] == "setSensors"]
        if sens:
            v = sens[-1]
            view.append("sensors: " + ("eyes+ears" if v["camera"] and v["microphone"] else
                                       "eyes only" if v["camera"] else "ears only" if v["microphone"] else "off"))
        if "play" in s:
            view.append(f"playing x{s['play'][1]}")
        va = "; ".join(f"{vv[1]} {vv[2]} {vv[3]:g}-{vv[4]:g} s" for vv in s.get("voice", []))
        lines.append(f"| {i} | {stage or s['id']} | {int(t // 60)}:{int(t % 60):02d}-{int((t + s['dur']) // 60)}:{int((t + s['dur']) % 60):02d} "
                     f"| {', '.join(view)} | {va} | {says} | {caps} |")
        t += s["dur"]
    lines += ["", f"Total length: {int(t // 60)} min {int(t % 60)} s."]
    return "\n".join(lines) + "\n"


def build_soundtrack(shots, audio_sr: int = 22050) -> np.ndarray:
    """Robot TTS lines + visitor voices, with the visitors ducked under the robot."""
    voice = Voice()
    vaudio = VisitorAudio(audio_sr)
    total = sum(s["dur"] for s in shots)
    track = np.zeros(int((total + 2) * audio_sr), np.float32)
    vtrack = np.zeros_like(track)
    t0 = 0.0
    for s in shots:
        for (ts, vid, var, a_s, b_s) in s.get("voice", []):
            y = vaudio.snippet(vid, var, a_s, b_s)
            i0 = int((t0 + ts) * audio_sr)
            n_ = max(0, min(len(y), len(vtrack) - i0))
            vtrack[i0:i0 + n_] += y[:n_]
        for a in s["actions"]:
            if a[1] == "say":
                y, sr = voice.say(a[2])
                if sr != audio_sr:
                    y = np.interp(np.arange(0, len(y), sr / audio_sr), np.arange(len(y)), y)
                i0 = int((t0 + a[0]) * audio_sr)
                n_ = max(0, min(len(y), len(track) - i0))
                track[i0:i0 + n_] += y[:n_]
        t0 += s["dur"]
    win = int(0.08 * audio_sr)
    env = np.convolve(np.abs(track), np.ones(win) / win, mode="same")
    robot_on = np.convolve((env > 0.01).astype(np.float32), np.ones(win * 3) / (win * 3), mode="same")
    return track + vtrack * (1.0 - 0.7 * np.clip(robot_on, 0, 1))


def remux_audio(mp4: str, audio_sr: int = 22050) -> None:
    import imageio_ffmpeg
    mix = build_soundtrack(SHOTS, audio_sr)
    wav = os.path.join(OUT, "_audio.wav")
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(audio_sr)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    tmp = mp4 + ".tmp.mp4"
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-i", mp4, "-i", wav, "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, mp4)
    for f in ("_audio.wav", "_tts.wav"):
        try:
            os.remove(os.path.join(OUT, f))
        except OSError:
            pass
    print("re-muxed audio into", mp4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fps", type=int, default=12)
    ap.add_argument("--only", default="")
    ap.add_argument("--keep-frames", action="store_true")
    ap.add_argument("--audio-only", action="store_true", help="rebuild only the soundtrack of the existing video")
    args = ap.parse_args()
    if args.audio_only:
        open(os.path.join(OUT, "storyboard.md"), "w", encoding="utf-8").write(storyboard_md(SHOTS))
        remux_audio(os.path.join(OUT, "how_does_a_robot_see_you.mp4"))
        return
    from playwright.sync_api import sync_playwright
    import imageio_ffmpeg

    shots = [s for s in SHOTS if not args.only or s["id"] in args.only.split(",")]
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "storyboard.md"), "w", encoding="utf-8").write(storyboard_md(SHOTS))
    frames_dir = os.path.join(OUT, "_frames")
    shutil.rmtree(frames_dir, ignore_errors=True)
    os.makedirs(frames_dir)
    voice = Voice()
    total = sum(s["dur"] for s in shots)
    audio_sr = 22050
    track = np.zeros(int((total + 2) * audio_sr), np.float32)
    vtrack = np.zeros_like(track)
    vaudio = VisitorAudio(audio_sr)

    with serve(DEMO) as base, sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        page.emulate_media(color_scheme="light", reduced_motion="no-preference")
        page.goto(base + "/local.html")
        page.wait_for_function("window.demo && window.demo.ready")
        page.evaluate("window.demo.ready")

        n = 0
        t0 = 0.0
        for s in shots:
            if "load" in s:
                page.evaluate("([v, vr]) => window.demo.load(v, vr)", list(s["load"]))
            state = page.evaluate("window.demo.getState()")
            sess_dur = state.get("duration") or 30
            if "seek" in s:
                page.evaluate("t => window.demo.seek(t)", sess_dur if s["seek"] == "end" else s["seek"])
            page.evaluate("window.demo.pause()")
            for (ts, vid, var, a_s, b_s) in s.get("voice", []):
                y = vaudio.snippet(vid, var, a_s, b_s)
                i0 = int((t0 + ts) * audio_sr)
                n_ = max(0, min(len(y), len(vtrack) - i0))
                vtrack[i0:i0 + n_] += y[:n_]
            pending = sorted(s["actions"], key=lambda a: a[0])
            nf = int(round(s["dur"] * args.fps))
            for f in range(nf):
                t = f / args.fps
                while pending and pending[0][0] <= t + 1e-9:
                    a = pending.pop(0)
                    if a[1] == "say":
                        page.evaluate("txt => window.demo.robotSay(txt)", a[2])
                        y, sr = voice.say(a[2])
                        if sr != audio_sr:
                            y = np.interp(np.arange(0, len(y), sr / audio_sr), np.arange(len(y)), y)
                        i0 = int((t0 + a[0]) * audio_sr)
                        track[i0:i0 + len(y)] += y[:max(0, len(track) - i0)]
                    elif a[1] == "setStage":
                        page.evaluate("([a, b]) => window.demo.setStage(a, b)", [a[2], a[3] if len(a) > 3 else None])
                    else:
                        page.evaluate(f"x => window.demo.{a[1]}(x)", a[2] if len(a) > 2 else None)
                if "play" in s:
                    start, rate = s["play"]
                    page.evaluate("t => window.demo.seek(t)", min(sess_dur, start + t * rate))
                page.wait_for_timeout(30)
                page.screenshot(path=os.path.join(frames_dir, f"{n:05d}.jpg"), type="jpeg", quality=92)
                n += 1
            # clear the robot bubble at the end of each scene unless the next scene speaks immediately
            page.evaluate("window.demo.robotSay(null)")
            t0 += s["dur"]
            print(f"scene {s['id']}: {nf} frames", flush=True)
        browser.close()

    # duck the visitors while the robot speaks (smoothed envelope of the robot track)
    win = int(0.08 * audio_sr)
    env = np.convolve(np.abs(track), np.ones(win) / win, mode="same")
    robot_on = np.convolve((env > 0.01).astype(np.float32), np.ones(win * 3) / (win * 3), mode="same")
    mix = track + vtrack * (1.0 - 0.7 * np.clip(robot_on, 0, 1))
    wav = os.path.join(OUT, "_audio.wav")
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
    with wave.open(wav, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(audio_sr); w.writeframes(pcm.tobytes())
    mp4 = os.path.join(OUT, "how_does_a_robot_see_you.mp4" if not args.only else f"preview_{args.only.replace(',', '_')}.mp4")
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, "-y", "-v", "error", "-framerate", str(args.fps), "-i", os.path.join(frames_dir, "%05d.jpg"),
                    "-i", wav, "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-r", "30", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", mp4], check=True)
    if not args.keep_frames:
        shutil.rmtree(frames_dir, ignore_errors=True)
        for tmp in ("_audio.wav", "_tts.wav"):
            try:
                os.remove(os.path.join(OUT, tmp))
            except OSError:
                pass
    print("wrote", mp4, round(os.path.getsize(mp4) / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
