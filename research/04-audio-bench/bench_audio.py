"""Audio-stack latency micro-benchmark on the dev laptop (Intel Core Ultra 7 255U, CPU only).
Uses already-cached models only. Writes bench_audio.json next to this script."""
import glob, json, os, sys, time, statistics as st
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "pylib"))
ROOT = r"C:\Users\myros\projects\Science Is Wonderful 2027"
files = sorted(glob.glob(os.path.join(ROOT, "data", "grid", "audio", "*.wav")))
SR = 16000
res = {"cpu": "Intel Core Ultra 7 255U (12C/14T), Windows 11, battery/AC unknown"}

def load(f):
    y, sr = sf.read(f, dtype="float32")
    return y if y.ndim == 1 else y.mean(1)

# ~10 s clip: 4 GRID utterances separated by 0.3 s silence
parts = []
for f in files[:4]:
    parts += [load(f), np.zeros(int(0.3 * SR), np.float32)]
clip = np.concatenate(parts)[: 10 * SR]
if len(clip) < 10 * SR:
    clip = np.pad(clip, (0, 10 * SR - len(clip)))
res["clip_s"] = len(clip) / SR

def timeit(fn, n=3):
    fn()  # warm-up
    ts = []
    for _ in range(n):
        t = time.perf_counter(); out = fn(); ts.append(time.perf_counter() - t)
    return st.median(ts), out

def log(k, v):
    res[k] = v; print(k, v, flush=True)
    json.dump(res, open(os.path.join(HERE, "bench_audio.json"), "w"), indent=1)

import torch
torch.set_num_threads(os.cpu_count())

# 1. Silero VAD
from silero_vad import load_silero_vad, get_speech_timestamps
vad = load_silero_vad()
x = torch.from_numpy(clip)
chunk = torch.from_numpy(clip[:512].copy())
vad.reset_states()
t = time.perf_counter()
for i in range(0, 512 * 300, 512):
    vad(torch.from_numpy(clip[i:i + 512].copy()), SR)
per_chunk_ms = (time.perf_counter() - t) / 300 * 1000
m, ts = timeit(lambda: get_speech_timestamps(x, vad, sampling_rate=SR))
log("silero_vad", {"ms_per_32ms_chunk": round(per_chunk_ms, 3), "s_per_10s_clip": round(m, 3),
                   "segments": len(ts)})

# 2. faster-whisper
from faster_whisper import WhisperModel
for size, rid in [("tiny", "tiny"), ("base", "base"), ("small", "small"), ("medium", "medium"),
                  ("turbo", "mobiuslabsgmbh/faster-whisper-large-v3-turbo")]:
    try:
        t = time.perf_counter(); wm = WhisperModel(rid, device="cpu", compute_type="int8"); load_s = time.perf_counter() - t
        def run(lang="en", wt=True):
            segs, info = wm.transcribe(clip, language=lang, beam_size=1, word_timestamps=wt,
                                       condition_on_previous_text=False)
            return " ".join(s.text.strip() for s in segs), info.language
        m, (txt, lang) = timeit(lambda: run("en"), n=2)
        m2, (txt2, lang2) = timeit(lambda: run(None), n=1)
        log("fw_" + size, {"load_s": round(load_s, 1), "s_per_10s_en_wordts": round(m, 2),
                           "s_per_10s_autolang": round(m2, 2), "lang_detected": lang2, "text": txt[:120]})
        del wm
    except Exception as e:
        log("fw_" + size, "ERROR " + str(e)[:200])

# 3. Parakeet TDT 0.6B v3 int8 via onnx-asr
try:
    import onnx_asr
    t = time.perf_counter(); pm = onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v3", quantization="int8"); load_s = time.perf_counter() - t
    m, out = timeit(lambda: pm.recognize(clip, sample_rate=SR), n=3)
    log("parakeet_v3_int8_onnx", {"load_s": round(load_s, 1), "s_per_10s": round(m, 2), "text": str(out)[:120]})
except Exception as e:
    log("parakeet_v3_int8_onnx", "ERROR " + str(e)[:300])

# 4. Prosody
import librosa
m, (f0, vf, vp) = timeit(lambda: librosa.pyin(clip, fmin=70, fmax=700, sr=SR, frame_length=1024, hop_length=160), n=2)
m2, _ = timeit(lambda: librosa.yin(clip, fmin=70, fmax=700, sr=SR, frame_length=1024, hop_length=160), n=3)
m3, _ = timeit(lambda: librosa.feature.rms(y=clip, frame_length=400, hop_length=160), n=3)
log("prosody", {"pyin_s_per_10s": round(m, 3), "yin_s_per_10s": round(m2, 4), "rms_s_per_10s": round(m3, 5),
                "median_f0_hz": float(np.nanmedian(f0)), "voiced_frac": float(np.mean(vf))})

# 5. CLAP zero-shot (latency + Lombard-vs-plain AUROC with text prompts)
from transformers import ClapModel, ClapProcessor
from sklearn.metrics import roc_auc_score
prompts = ["a person shouting loudly", "a person speaking quietly", "a person whispering",
           "a child speaking", "an adult man speaking", "an adult woman speaking",
           "laughter", "singing", "applause", "crowd noise"]
for rid in ["laion/clap-htsat-unfused", "laion/larger_clap_general"]:
    try:
        cm = ClapModel.from_pretrained(rid).eval(); cp = ClapProcessor.from_pretrained(rid)
        with torch.no_grad():
            ti = cp(text=prompts, return_tensors="pt", padding=True)
            temb = cm.get_text_features(**ti); temb = torch.nn.functional.normalize(temb, dim=-1)
            def aemb(y):
                ai = cp(audio=[y], sampling_rate=48000, return_tensors="pt")
                e = cm.get_audio_features(**ai); return torch.nn.functional.normalize(e, dim=-1)
            y48 = librosa.resample(clip, orig_sr=SR, target_sr=48000)
            m, _ = timeit(lambda: aemb(y48), n=3)
            # Lombard (loud) vs plain on all GRID files, peak-normalised so only voice quality differs
            labels, s_loud, top1 = [], [], {}
            for f in files:
                y = load(f); y = y / (np.abs(y).max() + 1e-9) * 0.5
                e = aemb(librosa.resample(y, orig_sr=SR, target_sr=48000))
                sims = (e @ temb.T)[0].numpy()
                labels.append(int("_l_" in os.path.basename(f)))
                s_loud.append(sims[0] - sims[1])
                k = prompts[int(np.argmax(sims))]; top1[k] = top1.get(k, 0) + 1
            auc = roc_auc_score(labels, s_loud)
        log("clap_" + rid.split("/")[1], {"audio_embed_s_per_10s": round(m, 3),
            "lombard_vs_plain_auroc_peaknorm": round(float(auc), 3), "n": len(files),
            "top1_prompt_counts_on_adult_GRID": top1})
        del cm
    except Exception as e:
        log("clap_" + rid.split("/")[1], "ERROR " + str(e)[:300])

# 6. AST AudioSet tagger latency
try:
    from transformers import ASTForAudioClassification, ASTFeatureExtractor
    rid = "MIT/ast-finetuned-audioset-10-10-0.4593"
    am = ASTForAudioClassification.from_pretrained(rid).eval(); fe = ASTFeatureExtractor.from_pretrained(rid)
    with torch.no_grad():
        def tag():
            return am(**fe(clip, sampling_rate=SR, return_tensors="pt")).logits[0]
        m, lg = timeit(tag, n=3)
    top = torch.sigmoid(lg).topk(5)
    log("ast_audioset", {"s_per_10s": round(m, 3),
        "top5": [(am.config.id2label[int(i)], round(float(p), 3)) for p, i in zip(top.values, top.indices)]})
except Exception as e:
    log("ast_audioset", "ERROR " + str(e)[:300])

# 7. multilingual-e5-small sentence embedding latency
try:
    from transformers import AutoTokenizer, AutoModel
    rid = "intfloat/multilingual-e5-small"
    tok = AutoTokenizer.from_pretrained(rid); em = AutoModel.from_pretrained(rid).eval()
    sents = ["query: mon animal préféré est le chat", "query: mijn lievelingsdier is een hond",
             "query: moje ulubione zwierzę to kot", "query: my favourite animal is a cat"]
    with torch.no_grad():
        def enc():
            b = tok(sents, padding=True, return_tensors="pt"); o = em(**b).last_hidden_state
            msk = b["attention_mask"].unsqueeze(-1); return (o * msk).sum(1) / msk.sum(1)
        m, _ = timeit(enc, n=5)
    log("me5_small", {"s_per_4_sentences": round(m, 4)})
except Exception as e:
    log("me5_small", "ERROR " + str(e)[:300])
print("DONE")
