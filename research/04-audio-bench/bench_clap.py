"""Zero-shot CLAP probe on Lombard GRID (12 adult talkers, plain vs Lombard speech) + CPU latency.
Writes bench_clap.json next to this script."""
import glob, json, os, time, statistics as st
import numpy as np, soundfile as sf, librosa, torch
from sklearn.metrics import roc_auc_score
from transformers import ClapModel, ClapProcessor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = r"C:\Users\myros\projects\Science Is Wonderful 2027"
files = sorted(glob.glob(os.path.join(ROOT, "data", "grid", "audio", "*.wav")))
torch.set_num_threads(os.cpu_count())

def load(f):
    y, sr = sf.read(f, dtype="float32"); y = y if y.ndim == 1 else y.mean(1)
    return librosa.resample(y, orig_sr=sr, target_sr=48000)

prompts = {
    "loud": "a person shouting loudly", "quiet": "a person speaking quietly",
    "whisper": "a person whispering", "child": "a child speaking", "adult": "an adult speaking",
    "man": "a man speaking", "woman": "a woman speaking", "laugh": "a person laughing",
    "sing": "a person singing", "applause": "applause", "crowd": "a noisy crowd", "speech": "speech",
}
keys = list(prompts)
res = {}
for rid in ["laion/clap-htsat-unfused", "laion/larger_clap_general"]:
    cm = ClapModel.from_pretrained(rid).eval(); cp = ClapProcessor.from_pretrained(rid)
    with torch.no_grad():
        ti = cp(text=[prompts[k] for k in keys], return_tensors="pt", padding=True)
        T = cm.get_text_features(**ti).pooler_output  # already L2-normalised
        def A(y):
            return cm.get_audio_features(**cp(audio=[y], sampling_rate=48000, return_tensors="pt")).pooler_output
        y10 = np.concatenate([load(f) for f in files[:4]])[: 48000 * 10]
        A(y10); ts = []
        for _ in range(3):
            t = time.perf_counter(); A(y10); ts.append(time.perf_counter() - t)
        S_raw, S_norm, lab, spk = [], [], [], []
        for f in files:
            y = load(f)
            S_raw.append((A(y) @ T.T)[0].numpy())
            S_norm.append((A(y / (np.abs(y).max() + 1e-9) * 0.5) @ T.T)[0].numpy())
            b = os.path.basename(f); lab.append(int("_l_" in b)); spk.append(b.split("_")[0])
    S_raw, S_norm, lab = np.array(S_raw), np.array(S_norm), np.array(lab)
    k = {n: i for i, n in enumerate(keys)}
    def auc(S, a, b):
        return round(float(roc_auc_score(lab, S[:, k[a]] - S[:, k[b]])), 3)
    top1 = {}
    for row in S_norm:
        n = keys[int(np.argmax(row))]; top1[n] = top1.get(n, 0) + 1
    res[rid] = {
        "audio_embed_s_per_10s_cpu": round(st.median(ts), 3),
        "n_utts": len(files), "n_talkers": len(set(spk)),
        "lombard_vs_plain_AUROC_loud_minus_quiet_raw_level": auc(S_raw, "loud", "quiet"),
        "lombard_vs_plain_AUROC_loud_minus_quiet_peak_normalised": auc(S_norm, "loud", "quiet"),
        "share_adult_utts_where_child_prompt_beats_adult_prompt": round(float(np.mean(S_norm[:, k["child"]] > S_norm[:, k["adult"]])), 3),
        "share_utts_where_laugh_beats_speech": round(float(np.mean(S_norm[:, k["laugh"]] > S_norm[:, k["speech"]])), 3),
        "share_utts_where_sing_beats_speech": round(float(np.mean(S_norm[:, k["sing"]] > S_norm[:, k["speech"]])), 3),
        "top1_prompt_counts_peak_normalised": top1,
        "mean_cosine_by_prompt": {n: round(float(S_norm[:, k[n]].mean()), 3) for n in keys},
    }
    print(rid, json.dumps(res[rid]), flush=True)
    json.dump(res, open(os.path.join(HERE, "bench_clap.json"), "w"), indent=1)
    del cm
print("DONE")
