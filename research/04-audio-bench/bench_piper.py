"""Piper TTS (piper-tts 1.8.0, GPL-3.0) CPU latency on the dev laptop: first-sentence latency and RTF."""
import json, os, sys, time, wave, io
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "ttslib"))
from piper import PiperVoice
texts = {
    "en_US-lessac-medium": "Hello! I am a robot dog. I can hear that you are speaking quite loudly right now.",
    "fr_FR-siwis-medium": "Bonjour ! Je suis un chien robot. J'entends que tu parles assez fort en ce moment.",
    "nl_BE-nathalie-medium": "Hallo! Ik ben een robothond. Ik hoor dat je nu vrij luid praat.",
    "de_DE-thorsten-medium": "Hallo! Ich bin ein Roboterhund. Ich höre, dass du gerade ziemlich laut sprichst.",
    "pl_PL-gosia-medium": "Cześć! Jestem psem robotem. Słyszę, że mówisz teraz dość głośno.",
}
res = {}
for v, txt in texts.items():
    t = time.perf_counter()
    voice = PiperVoice.load(os.path.join(HERE, "voices", v + ".onnx"))
    load_s = time.perf_counter() - t
    def synth():
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            voice.synthesize_wav(txt, w)
        buf.seek(0)
        with wave.open(buf, "rb") as r:
            return r.getnframes() / r.getframerate()
    synth()
    ts = []
    for _ in range(3):
        t = time.perf_counter(); dur = synth(); ts.append(time.perf_counter() - t)
    ts.sort(); s = ts[1]
    res[v] = {"load_s": round(load_s, 2), "synth_s": round(s, 3), "audio_s": round(dur, 2), "rtf": round(s / dur, 3)}
    print(v, res[v], flush=True)
json.dump(res, open(os.path.join(HERE, "bench_piper.json"), "w"), indent=1)
