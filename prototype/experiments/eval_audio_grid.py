"""Evaluate the microphone pipeline on Lombard GRID (CC BY 4.0).

Ground truth from the file name s<talker>_<l|p>_<code>:
  * colour word spoken (code[1]: b=blue g=green r=red w=white) -> "favourite colour" keyword path
  * l = Lombard (loud, effortful) vs p = plain speech         -> "voice loudness" path

Conditions: clean, and "crowded hall" babble made by summing 6 other talkers'
plain utterances, at SNR 10 / 5 / 0 dB. Also one clean run with automatic
language identification (as at a multilingual booth).

Writes experiments/results/audio_grid.json and fig_audio_grid.png
"""
from __future__ import annotations

import glob
import json
import os
import random
import sys
import time

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from robotsees.perception.audio import AudioPerception, add_noise  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(os.path.dirname(__file__), "results")
COL = {"b": "blue", "g": "green", "r": "red", "w": "white"}


def load(f):
    y, sr = sf.read(f, dtype="float32")
    return (y.mean(1) if y.ndim > 1 else y), sr


def main():
    from sklearn.metrics import roc_auc_score
    files = sorted(glob.glob(os.path.join(ROOT, "data", "grid", "audio", "*.wav")))
    meta = []
    for f in files:
        spk, cond, code = os.path.basename(f)[:-4].split("_")
        meta.append({"file": f, "talker": spk, "lombard": int(cond == "l"), "colour": COL[code[1]]})
    rng = random.Random(0)
    plain = [m["file"] for m in meta if not m["lombard"]]

    def babble(exclude_talker, n):
        picks = [f for f in plain if f"{os.sep}{exclude_talker}_" not in f and not os.path.basename(f).startswith(exclude_talker + "_")]
        mix = np.zeros(n, np.float32)
        for f in rng.sample(picks, 6):
            y, _ = load(f)
            y = np.resize(y, n)
            mix += y / (np.sqrt(np.mean(y ** 2)) + 1e-9)
        return mix

    ap_en = AudioPerception("small", language="en")
    ap_auto = AudioPerception("small", language=None)
    conditions = [("clean", None, ap_en), ("babble_10dB", 10, ap_en), ("babble_5dB", 5, ap_en),
                  ("babble_0dB", 0, ap_en), ("clean_auto_language", None, ap_auto)]
    results = {}
    for name, snr, ap in conditions:
        rows = []
        t0 = time.time()
        for m in meta:
            y, sr = load(m["file"])
            if snr is not None:
                y = add_noise(y, snr, noise=babble(m["talker"], len(y)))
            r = ap.analyse(y, sr)
            heard = [o for o in r.observations if o.slot == "colour"]
            rows.append({"talker": m["talker"], "lombard": m["lombard"], "gt": m["colour"],
                         "heard": [next(iter(o.likelihood)) for o in heard],
                         "speech_db": None if r.loudness_db is None else r.loudness_db + ap.calibration_db,
                         "language": r.language, "transcript": r.transcript})
        secs = (time.time() - t0) / len(meta)
        correct = np.mean([row["gt"] in row["heard"] for row in rows])
        wrong = np.mean([any(h != row["gt"] for h in row["heard"]) for row in rows])
        missed = np.mean([len(row["heard"]) == 0 for row in rows])
        lv = [(row["speech_db"], row["lombard"]) for row in rows if row["speech_db"] is not None]
        auroc = roc_auc_score([l for _, l in lv], [d for d, _ in lv]) if lv else None
        # Within-talker loudness difference (Lombard minus plain), in dB.
        diffs = []
        for t in {row["talker"] for row in rows}:
            l = [row["speech_db"] for row in rows if row["talker"] == t and row["lombard"] and row["speech_db"] is not None]
            p = [row["speech_db"] for row in rows if row["talker"] == t and not row["lombard"] and row["speech_db"] is not None]
            if l and p:
                diffs.append(np.mean(l) - np.mean(p))
        results[name] = {
            "n": len(rows), "snr_db": snr,
            "colour_word_correct": round(float(correct), 3),
            "colour_word_wrong_value": round(float(wrong), 3),
            "colour_word_missed": round(float(missed), 3),
            "loud_vs_plain_auroc_absolute_level": None if auroc is None else round(float(auroc), 3),
            "lombard_minus_plain_db_within_talker": round(float(np.mean(diffs)), 2) if diffs else None,
            "language_detected_en": round(float(np.mean([row["language"] == "en" for row in rows])), 3),
            "seconds_per_clip_cpu": round(secs, 2),
            "examples_wrong": [row["transcript"] for row in rows if row["heard"] and row["gt"] not in row["heard"]][:5],
        }
        print(name, json.dumps(results[name]), flush=True)
    os.makedirs(OUT, exist_ok=True)
    json.dump({"data": "Lombard GRID (CC BY 4.0), 12 talkers x 4 colours x {plain, Lombard} x 2 = 192 utterances",
               "asr": "faster-whisper small int8, CPU, beam 1, word timestamps; closed EN/FR/NL/DE/PL lexicon",
               "results": results}, open(os.path.join(OUT, "audio_grid.json"), "w"), indent=1)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = [n for n in results if n.startswith(("clean", "babble")) and n != "clean_auto_language"]
    fig, ax = plt.subplots(figsize=(6, 3.6))
    x = np.arange(len(names))
    ax.bar(x - 0.2, [results[n]["colour_word_correct"] for n in names], 0.4, label="heard the right colour", color="#f08a24")
    ax.bar(x + 0.2, [results[n]["colour_word_wrong_value"] for n in names], 0.4, label="heard a wrong colour", color="#888")
    ax.set_xticks(x, [n.replace("babble_", "babble ") for n in names])
    ax.set_ylim(0, 1); ax.set_ylabel("fraction of utterances"); ax.legend(fontsize=8)
    ax.set_title("Ears: colour words in clean vs. crowded-hall noise (GRID, n=192)")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "fig_audio_grid.png"), dpi=130)


if __name__ == "__main__":
    main()
