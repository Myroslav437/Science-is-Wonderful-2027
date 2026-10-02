"""Modality-ablation analysis over all built visitor sessions.

For every visitor x variant (clean / noisy-ears / foggy-eyes) x sensor
configuration (eyes+ears / eyes only / ears only) we read the robot's final
belief and compare it with the hand-annotated ground truth in visitors.json.

  claim     = the value shown with certainty guess/think/sure
  confident = certainty think/sure
  correct   = claim is in the truth set; for "favourite colour" nobody stated
              one, so any claim there is unsupported (counted as wrong)

Writes experiments/results/ablation.json, ablation_table.md and figures.
"""
from __future__ import annotations

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
SES = os.path.join(RES, "sessions")
CONFIGS = [("camera+microphone", "Eyes + ears"), ("camera", "Eyes only"), ("microphone", "Ears only")]
VARIANTS = [("clean", "Clean"), ("noisy-ears", "Noisy room (ears)"), ("foggy-eyes", "Foggy lens (eyes)")]
SLOTS = ["animal", "colour", "shirt", "glasses", "energy", "voice"]
GT_SLOTS = ["animal", "colour", "shirt", "glasses"]
COL = {"camera+microphone": "#7a5cc7", "camera": "#2f7de1", "microphone": "#f08a24"}
INK, INK2, GRID = "#1f2430", "#5b6170", "#e3e5ea"
GOOD, BAD = "#1f8a4c", "#c8352b"


def truth_of(truth, slot):
    t = truth.get(slot)
    if slot == "colour":
        return None if t is None else [t]
    return t if isinstance(t, list) else ([t] if t else None)


def judge(slot, belief, truth):
    level = belief["certainty"]
    if level == "unknown":
        return None
    t = truth_of(truth, slot)
    if slot == "colour" and t is None:
        return False            # favourite colour was never stated: any claim is unsupported
    if t is None:
        return None
    return belief["best"] in t


def main():
    visitors = json.load(open(os.path.join(HERE, "visitors.json"), encoding="utf-8"))["visitors"]
    rows, per_visitor = [], {}
    for v in visitors:
        for var, _ in VARIANTS:
            p = os.path.join(SES, f"{v['id']}-{var}.json")
            if not os.path.exists(p):
                continue
            s = json.load(open(p, encoding="utf-8"))
            for cfg, _ in CONFIGS:
                fin = s["final"][cfg]["slots"]
                for slot in SLOTS:
                    b = fin[slot]
                    ok = judge(slot, b, v["truth"])
                    rows.append({"visitor": v["id"], "variant": var, "config": cfg, "slot": slot,
                                 "value": b["best"] if b["certainty"] != "unknown" else None,
                                 "certainty": b["certainty"], "score": b["certainty_score"], "correct": ok})
                # time to the first confident animal claim (progressive interaction)
                tt = next((step["t"] for step in s["timeline"]
                           if step["configs"][cfg]["slots"]["animal"]["certainty"] in ("think", "sure")), None)
                per_visitor.setdefault((v["id"], var, cfg), {})["t_animal_confident"] = tt
    summary = {}
    for var, _ in VARIANTS:
        for cfg, _ in CONFIGS:
            R = [r for r in rows if r["variant"] == var and r["config"] == cfg]
            if not R:
                continue
            nv = len({r["visitor"] for r in R})
            claims = [r for r in R if r["slot"] in GT_SLOTS and r["correct"] is not None]
            conf = [r for r in claims if r["certainty"] in ("think", "sure")]
            summary[f"{var}|{cfg}"] = {
                "visitors": nv,
                "slots_known_per_visitor": round(sum(r["certainty"] != "unknown" for r in R) / nv, 2),
                "mean_certainty": round(float(np.mean([r["score"] for r in R])), 3),
                "claims_checked": len(claims),
                "claims_correct": round(float(np.mean([r["correct"] for r in claims])), 3) if claims else None,
                "confident_claims": len(conf),
                "confident_correct": round(float(np.mean([r["correct"] for r in conf])), 3) if conf else None,
                "animal_correct": sum(1 for r in R if r["slot"] == "animal" and r["correct"]),
                "shirt_correct": sum(1 for r in R if r["slot"] == "shirt" and r["correct"]),
                "glasses_correct": sum(1 for r in R if r["slot"] == "glasses" and r["correct"]),
                "unsupported_colour_claims": sum(1 for r in R if r["slot"] == "colour" and r["correct"] is False),
            }
    os.makedirs(RES, exist_ok=True)
    json.dump({"definitions": __doc__, "summary": summary, "rows": rows,
               "time_to_confident_animal": {"|".join(k): v["t_animal_confident"] for k, v in per_visitor.items()}},
              open(os.path.join(RES, "ablation.json"), "w"), indent=1)

    # Markdown table
    lines = ["| Condition | Sensors | Visitors | Things known (of 6) | Mean certainty | Checkable claims correct | Confident claims correct | Animal right | Clothes colour right | Glasses right | Unsupported fav.-colour claims |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for var, vl in VARIANTS:
        for cfg, cl in CONFIGS:
            s = summary.get(f"{var}|{cfg}")
            if not s:
                continue
            pct = lambda x: "-" if x is None else f"{100 * x:.0f}%"
            lines.append(f"| {vl} | {cl} | {s['visitors']} | {s['slots_known_per_visitor']} | {s['mean_certainty']:.2f} | "
                         f"{pct(s['claims_correct'])} ({s['claims_checked']}) | {pct(s['confident_correct'])} ({s['confident_claims']}) | "
                         f"{s['animal_correct']}/{s['visitors']} | {s['shirt_correct']}/{s['visitors']} | {s['glasses_correct']}/{s['visitors']} | "
                         f"{s['unsupported_colour_claims']} |")
    open(os.path.join(RES, "ablation_table.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    figures(rows, summary, visitors)


def figures(rows, summary, visitors):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK})

    # 1) Representation matrix (clean): what each configuration concluded.
    vids = [v["id"] for v in visitors]
    labels = {v["id"]: v["label"] for v in visitors}
    fig, axes = plt.subplots(1, 3, figsize=(17, 0.62 * len(vids) + 1.6), sharey=True)
    short = {"no glasses": "no", "glasses": "yes", "very active": "v. active"}
    cmap = matplotlib.colormaps["Greys"]
    for ax, (cfg, cl) in zip(axes, CONFIGS):
        ax.set_title(cl, color=COL[cfg], fontsize=12, fontweight="bold", loc="left")
        for i, vid in enumerate(vids):
            for j, slot in enumerate(SLOTS):
                r = next((r for r in rows if r["visitor"] == vid and r["variant"] == "clean"
                          and r["config"] == cfg and r["slot"] == slot), None)
                if r is None:
                    continue
                sc = r["score"] if r["certainty"] != "unknown" else 0
                ax.add_patch(plt.Rectangle((j + 0.04, i + 0.06), 0.92, 0.88, color=cmap(0.08 + 0.5 * sc), lw=0))
                txt = "?" if r["value"] is None else short.get(r["value"], r["value"])
                fg = "white" if sc > 0.62 else INK
                mark = "" if r["correct"] is None else (" ✓" if r["correct"] else " ✗")
                ax.text(j + 0.5, i + 0.42, txt + mark, ha="center", va="center", fontsize=8 if len(txt) < 8 else 7, color=fg,
                        fontweight="bold" if r["value"] else "normal")
                ax.text(j + 0.5, i + 0.74, r["certainty"] if r["certainty"] != "unknown" else "don't know",
                        ha="center", va="center", fontsize=7, color=fg)
                if r["correct"] is False:
                    ax.add_patch(plt.Rectangle((j + 0.04, i + 0.06), 0.92, 0.88, fill=False, ec=BAD, lw=1.6))
        ax.set_xlim(0, len(SLOTS)); ax.set_ylim(len(vids), 0)
        ax.set_xticks(np.arange(len(SLOTS)) + 0.5, ["fav. animal", "fav. colour", "clothes", "glasses?", "action now", "voice now"], fontsize=8)
        ax.xaxis.tick_top(); ax.tick_params(length=0)
        ax.set_yticks(np.arange(len(vids)) + 0.5, [labels[v] for v in vids])
        for sp in ax.spines.values():
            sp.set_visible(False)
    fig.text(0.01, 0.01, "Cell shade = how sure the robot is.  ✓ matches the annotated truth, ✗ wrong or unsupported "
             "(red box).  '?' = the robot says it doesn't know.  Real people from Seamless Interaction (CC BY-NC 4.0), real models.",
             fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(RES, "fig_ablation_matrix.png"), dpi=140)
    plt.close(fig)

    # 2) Conditions: things known and claim accuracy (two charts, one measure each).
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    x = np.arange(len(VARIANTS))
    w = 0.26
    for k, (cfg, cl) in enumerate(CONFIGS):
        known = [summary.get(f"{var}|{cfg}", {}).get("slots_known_per_visitor", 0) for var, _ in VARIANTS]
        acc = [summary.get(f"{var}|{cfg}", {}).get("claims_correct") or 0 for var, _ in VARIANTS]
        for ax, vals, fmt in ((axes[0], known, "{:.1f}"), (axes[1], [100 * a for a in acc], "{:.0f}%")):
            bars = ax.bar(x + (k - 1) * (w + 0.02), vals, w, color=COL[cfg], label=cl, edgecolor="white", linewidth=1)
            for b, val in zip(bars, vals):
                ax.text(b.get_x() + b.get_width() / 2, b.get_height() + (0.08 if ax is axes[0] else 1.5),
                        fmt.format(val), ha="center", va="bottom", fontsize=7.5, color=INK2)
    axes[0].set_title("Things the robot claims to know (of 6), per visitor", loc="left", fontsize=10)
    axes[0].set_ylim(0, 6.5)
    axes[1].set_title("Checkable claims that are correct", loc="left", fontsize=10)
    axes[1].set_ylim(0, 112)
    for ax in axes:
        ax.set_xticks(x, [vl for _, vl in VARIANTS])
        ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.tick_params(length=0)
    axes[0].legend(frameon=False, fontsize=8, loc="upper right", ncol=3)
    fig.tight_layout()
    fig.savefig(os.path.join(RES, "fig_conditions.png"), dpi=140)
    plt.close(fig)

    # 3) Progressive interaction for one visitor: certainty over time, per slot, per configuration.
    vid = "v02"
    p = os.path.join(SES, f"{vid}-clean.json")
    if os.path.exists(p):
        s = json.load(open(p, encoding="utf-8"))
        fig, axes = plt.subplots(2, 3, figsize=(12, 5.2), sharex=True, sharey=True)
        names = {"animal": "Favourite animal", "colour": "Favourite colour", "shirt": "Clothes colour",
                 "glasses": "Glasses", "energy": "Action right now", "voice": "Voice right now"}
        ts = [step["t"] for step in s["timeline"]]
        for ax, slot in zip(axes.ravel(), SLOTS):
            style = {"camera+microphone": dict(lw=5, alpha=0.45), "camera": dict(lw=1.8), "microphone": dict(lw=1.8, ls="--")}
            for cfg, cl in CONFIGS:
                ys = [step["configs"][cfg]["slots"][slot]["certainty_score"] if
                      step["configs"][cfg]["slots"][slot]["certainty"] != "unknown" else 0 for step in s["timeline"]]
                ax.plot(ts, ys, color=COL[cfg], label=cl, **style[cfg])
                last = s["timeline"][-1]["configs"][cfg]["slots"][slot]
                if last["certainty"] != "unknown" and ys[-1] > 0.02:
                    ax.text(ts[-1] + 0.5, ys[-1], last["best"], color=INK2, fontsize=7.5, va="center")
            groups = []
            for a in s["audio"]:
                for kw in a["keywords"]:
                    if kw["slot"] == slot:
                        if groups and kw["t"] - groups[-1][0] < 1.2:
                            if kw["value"].lower() not in groups[-1][1]:
                                groups[-1][1].append(kw["value"].lower())
                        else:
                            groups.append([kw["t"], [kw["value"].lower()]])
            for t_kw, ws in groups:
                ax.axvline(t_kw, color=COL["microphone"], lw=0.8, ls=":", alpha=0.8)
                ax.text(t_kw, 1.03, "/".join(ws), rotation=90, fontsize=6.5, color=INK2, va="bottom", ha="center")
            for thr, lab in ((0.25, "guess"), (0.5, "think"), (0.75, "sure")):
                ax.axhline(thr, color=GRID, lw=0.8)
                ax.text(-0.5, thr, lab, fontsize=6.5, color=INK2, ha="right", va="center")
            ax.set_title(names[slot], loc="left", fontsize=9.5, pad=40)
            ax.set_ylim(0, 1.0); ax.set_xlim(0, ts[-1] + 6)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
            ax.set_yticks([])
        axes[1, 0].set_xlabel("seconds of interaction"); axes[1, 1].set_xlabel("seconds of interaction")
        axes[1, 2].set_xlabel("seconds of interaction")
        axes[0, 0].legend(frameon=False, fontsize=7.5, loc="center right")
        fig.suptitle("Visitor B: the robot's certainty builds up over time (dotted lines = words from its word list)",
                     x=0.01, ha="left", fontsize=10.5)
        fig.tight_layout()
        fig.savefig(os.path.join(RES, "fig_progressive_v02.png"), dpi=140)
        plt.close(fig)


if __name__ == "__main__":
    main()
