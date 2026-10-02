"""Calibrate and evaluate the zero-shot hat / glasses detectors on Open Images V7.

Data: human-verified Open Images validation labels (see scratch/fetch_openimages.py).
Positives = faces overlapped by a Hat-family / Glasses-family box in images where
the label is verified present; negatives = faces in images where it is verified
absent. Images labelled Boy/Girl were excluded (no evaluation on minors).

For each backbone we compute the raw contrast score on a head crop (the same
crop geometry the live pipeline uses), then fit per-concept Platt scaling with
5-fold stratified cross-validation and report AUROC, accuracy, ECE, Brier and
the precision of "I'm sure" claims (calibrated p >= 0.8 or <= 0.2).

Usage: python experiments/calibrate_vision.py
Writes: experiments/results/vision_calibration.json, models/vision_calibration.json,
        experiments/results/fig_reliability.png
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from robotsees.perception.vision import CONCEPT_PROMPTS  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OI = os.path.join(ROOT, "data", "openimages")
OUT = os.path.join(os.path.dirname(__file__), "results")
BACKBONES = [("ViT-B-32", "laion2b_s34b_b79k"), ("ViT-B-16-SigLIP2", "webli")]


def head_crop(img: Image.Image, box) -> Image.Image:
    w, h = img.size
    x0, y0, x1, y1 = box[0] * w, box[1] * h, box[2] * w, box[3] * h
    fw, fh = x1 - x0, y1 - y0
    return img.crop((max(0, x0 - 0.3 * fw), max(0, y0 - 0.7 * fh), min(w, x1 + 0.3 * fw), min(h, y1 + 0.15 * fh)))


def ece(p, y, bins=10):
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        m = (p >= a) & (p < b if b < 1 else p <= b)
        if m.any():
            e += m.mean() * abs(p[m].mean() - y[m].mean())
    return float(e)


def main():
    import open_clip
    import torch
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import brier_score_loss, roc_auc_score
    from sklearn.model_selection import StratifiedKFold

    rows = [r for r in json.load(open(os.path.join(OI, "headcrops.json")))
            if os.path.exists(os.path.join(OI, "img", r["image"] + ".jpg"))]
    crops = [head_crop(Image.open(os.path.join(OI, "img", r["image"] + ".jpg")).convert("RGB"), r["box"])
             for r in rows]
    results, calib, curves = {}, {}, {}
    for name, pre in BACKBONES:
        model, _, preprocess = open_clip.create_model_and_transforms(name, pretrained=pre)
        model.eval()
        tok = open_clip.get_tokenizer(name)
        with torch.no_grad():
            feats = []
            for i in range(0, len(crops), 32):
                f = model.encode_image(torch.stack([preprocess(c) for c in crops[i:i + 32]]))
                feats.append(f / f.norm(dim=-1, keepdim=True))
            feats = torch.cat(feats)
            res = {}
            for concept, (pos, neg) in CONCEPT_PROMPTS.items():
                tp = model.encode_text(tok(pos)); tp = tp / tp.norm(dim=-1, keepdim=True)
                tn = model.encode_text(tok(neg)); tn = tn / tn.norm(dim=-1, keepdim=True)
                idx = [i for i, r in enumerate(rows) if r["attr"] == concept]
                s = ((feats[idx] @ tp.T).mean(-1) - (feats[idx] @ tn.T).mean(-1)).numpy()
                y = np.array([rows[i]["label"] for i in idx])
                # 5-fold CV Platt scaling
                p_cv = np.zeros(len(y))
                for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(s, y):
                    lr = LogisticRegression(C=100.0).fit(s[tr, None], y[tr])
                    p_cv[te] = lr.predict_proba(s[te, None])[:, 1]
                sure = (p_cv >= 0.8) | (p_cv <= 0.2)
                # Upgrade path: a linear probe on the image embedding (post-hoc concept bottleneck).
                Xf = feats[idx].numpy()
                p_probe = np.zeros(len(y))
                for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(Xf, y):
                    p_probe[te] = LogisticRegression(C=1.0, max_iter=2000).fit(Xf[tr], y[tr]).predict_proba(Xf[te])[:, 1]
                res[concept] = {
                    "n_pos": int(y.sum()), "n_neg": int((1 - y).sum()),
                    "auroc": round(float(roc_auc_score(y, s)), 3),
                    "accuracy_cv": round(float(((p_cv > 0.5) == y).mean()), 3),
                    "ece_cv": round(ece(p_cv, y), 3),
                    "brier_cv": round(float(brier_score_loss(y, p_cv)), 3),
                    "sure_fraction": round(float(sure.mean()), 3),
                    "sure_precision": round(float(((p_cv > 0.5) == y)[sure].mean()), 3) if sure.any() else None,
                    "linear_probe_auroc_cv": round(float(roc_auc_score(y, p_probe)), 3),
                }
                lr = LogisticRegression(C=100.0).fit(s[:, None], y)
                calib.setdefault(name, {})[concept] = {"a": float(lr.coef_[0][0]), "b": float(lr.intercept_[0])}
                curves[(name, concept)] = (p_cv, y)
        results[name] = res
        print(name, json.dumps(res, indent=1), flush=True)

    os.makedirs(OUT, exist_ok=True)
    json.dump({"data": "Open Images V7 validation, human-verified labels, adults only (Boy/Girl images excluded)",
               "protocol": "contrast-prompt score on head crop; Platt scaling; 5-fold stratified CV",
               "results": results}, open(os.path.join(OUT, "vision_calibration.json"), "w"), indent=1)
    best = max(results, key=lambda n: np.mean([results[n][c]["auroc"] for c in results[n]]))
    os.makedirs(os.path.join(ROOT, "prototype", "models"), exist_ok=True)
    json.dump({"backbone": best, **calib[best]},
              open(os.path.join(ROOT, "prototype", "models", "vision_calibration.json"), "w"), indent=1)
    json.dump(calib, open(os.path.join(OUT, "platt_all_backbones.json"), "w"), indent=1)
    print("best backbone by mean AUROC:", best)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, concept in zip(axes, CONCEPT_PROMPTS):
        ax.plot([0, 1], [0, 1], color="#999", lw=1, ls="--")
        for (name, c), (p, y) in curves.items():
            if c != concept:
                continue
            edges = np.linspace(0, 1, 6)
            xs, ys = [], []
            for a, b in zip(edges[:-1], edges[1:]):
                m = (p >= a) & (p <= b)
                if m.sum() >= 5:
                    xs.append(p[m].mean()); ys.append(y[m].mean())
            ax.plot(xs, ys, marker="o", label=f"{name} (AUROC {results[name][concept]['auroc']})")
        ax.set_title(f"'{concept}' - calibrated (5-fold CV)")
        ax.set_xlabel("predicted probability"); ax.set_ylabel("observed frequency")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_reliability.png"), dpi=130)


if __name__ == "__main__":
    main()
