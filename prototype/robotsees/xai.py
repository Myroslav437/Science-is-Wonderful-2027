"""Explanations computed from the same fusion the robot uses.

For every slot we produce:
  * the belief (best value, probabilities, certainty phrase)
  * exact Shapley contributions of each enabled sensor to that answer
  * each sensor's own opinion (what it would conclude alone) -> disagreement
  * the strongest pieces of evidence (with timestamps) -> "because ..."
  * counterfactuals for every sensor configuration ("with only my ears ...")
  * a short kid-language explanation built from templates (no LLM, so the
    text can only say what the numbers say)
"""
from __future__ import annotations

import numpy as np

from .config import MODALITY_META, MODALITIES, SLOTS
from .fusion import (EvidenceMemory, all_configs, fuse_slot, sensor_clues,
                     shapley_sensors)

NOUN = {"animal": "favourite animal", "colour": "favourite colour",
        "shirt": "clothes colour", "glasses": "glasses",
        "energy": "action right now", "voice": "voice right now"}


def _statement(slot: str, value: str) -> str:
    if slot == "animal":
        return f"your favourite animal is a {value.upper()}"
    if slot == "colour":
        return f"your favourite colour is {value.upper()}"
    if slot == "shirt":
        return f"you are wearing {value.upper()} clothes"
    if slot == "glasses":
        return "you are wearing glasses" if value == "glasses" else "you are NOT wearing glasses"
    if slot == "energy":
        return {"still": "you are standing STILL right now", "moving": "you are MOVING right now",
                "very active": "you are VERY ACTIVE right now"}[value]
    if slot == "voice":
        return f"I hear a {value.upper()} voice right now"
    return f"{slot} = {value}"


def evidence_ranking(memory: EvidenceMemory, slot: str, enabled: tuple[str, ...],
                     target: str, k: int = 3) -> list[dict]:
    """Rank individual observations by how much they pushed towards `target`."""
    spec = SLOTS[slot]
    ti = spec.values.index(target)
    rows = []
    for m in enabled:
        w = spec.reliability.get(m, 0.0)
        if w <= 0:
            continue
        _, kappa, obs = memory.modality_evidence(slot, m)
        qsum = sum(o.quality * o.weight for o in obs) or 1.0
        for o in obs:
            le = o.log_evidence()
            push = kappa * o.quality * o.weight / qsum * (le[ti] - le.mean())
            rows.append({"t": round(o.t, 2), "sensor": m, "evidence": o.evidence,
                         "push": float(push), "quality": round(o.quality, 2),
                         "detail": o.detail})
    # Merge identical evidence strings (e.g. the same colour seen in 40 frames).
    merged: dict[tuple, dict] = {}
    for r in rows:
        key = (r["sensor"], r["evidence"])
        if key in merged:
            merged[key]["push"] += r["push"]
            merged[key]["count"] += 1
        else:
            merged[key] = {**r, "count": 1}
    out = sorted(merged.values(), key=lambda r: -r["push"])
    return [r for r in out if r["push"] > 1e-4][:k]


def explain_slot(memory: EvidenceMemory, slot: str, enabled: tuple[str, ...]) -> dict:
    spec = SLOTS[slot]
    belief = fuse_slot(memory, slot, enabled)
    level, phrase = belief.certainty
    best = belief.best

    # Each enabled sensor's own opinion.
    alone = {}
    for m in spec.sensors:
        b = fuse_slot(memory, slot, (m,))
        _, kappa, obs = memory.modality_evidence(slot, m)
        alone[m] = {"best": b.best, "certainty": b.certainty[0],
                    "certainty_score": round(b.certainty_score, 3),
                    "n_obs": len(obs), "strength": round(kappa, 3),
                    "enabled": m in enabled}

    clues = sensor_clues(memory, slot, enabled, best)
    phi = shapley_sensors(memory, slot, enabled, best) if level != "unknown" else {}
    evidence = evidence_ranking(memory, slot, enabled, best, k=4) if level != "unknown" else []
    # Ignorance vs conflict: how much evidence is on the scale at all.
    volume = {}
    for m in enabled:
        if spec.reliability.get(m, 0) > 0:
            e, _, _ = memory.modality_evidence(slot, m)
            volume[m] = float(np.abs(e - e.mean()).sum())

    # Counterfactuals: what would I believe with each sensor configuration?
    counterfactuals = {}
    for cfg in all_configs():
        b = fuse_slot(memory, slot, cfg)
        counterfactuals["+".join(cfg) or "none"] = {
            "best": b.best, "certainty": b.certainty[0],
            "certainty_score": round(b.certainty_score, 3),
            "probs": [round(float(p), 4) for p in b.probs]}

    # Kid-language explanation (templates only).
    lines = []
    if level == "unknown":
        missing = [m for m in spec.sensors if m not in enabled]
        hinted = [m for m in spec.sensors if m in enabled and alone[m]["n_obs"] > 0]
        if hinted and belief.certainty_score > 0.05:
            lines.append(f"I only have a tiny hint that it might be {best.upper()} - not enough to guess yet.")
        elif missing and not hinted:
            lines.append(f"I can't tell: my {' and '.join(MODALITY_META[m]['short'].lower() for m in missing)} "
                         f"{'is' if len(missing) == 1 else 'are'} switched off.".replace("ears is", "ears are")
                         .replace("eyes is", "eyes are"))
        else:
            lines.append("I haven't noticed anything about this yet.")
    else:
        lines.append(f"{phrase} {_statement(slot, best)}.")
        for ev in evidence[:2]:
            lines.append(f"Because my {MODALITY_META[ev['sensor']]['short'].lower()} {ev['evidence']}.")
        opinions = {m: a["best"] for m, a in alone.items()
                    if a["enabled"] and a["certainty"] != "unknown"}
        if len(set(opinions.values())) > 1:
            parts = [f"my {MODALITY_META[m]['short'].lower()} say {v.upper()}" for m, v in opinions.items()]
            trusted = max(opinions, key=lambda m: spec.reliability[m] * alone[m]["strength"])
            lines.append(f"My senses disagree: {' but '.join(parts)}. "
                         f"For this question I trust my {MODALITY_META[trusted]['short'].lower()} more.")
        for m in spec.sensors:
            if m not in enabled:
                lines.append(f"My {MODALITY_META[m]['short'].lower()} are switched off, "
                             f"so I could not use them here.")

    return {
        "slot": slot, "question": spec.question, "noun": NOUN[slot],
        "values": list(spec.values),
        "probs": [round(float(p), 4) for p in belief.probs],
        "best": best, "confidence": round(belief.confidence, 4),
        "certainty": level, "certainty_phrase": phrase,
        "certainty_score": round(belief.certainty_score, 3),
        "clues": {m: round(v, 4) for m, v in clues.items()},
        "evidence_volume": {m: round(v, 3) for m, v in volume.items()},
        "shapley_prob": {m: round(v, 4) for m, v in phi.items()},
        "alone": alone, "evidence": evidence,
        "counterfactuals": counterfactuals,
        "explanation": lines,
    }


def snapshot(memory: EvidenceMemory, enabled: tuple[str, ...], t: float | None = None) -> dict:
    """Full robot state for one sensor configuration at time t (JSON-ready)."""
    mem = memory.upto(t) if t is not None else memory
    slots = {k: explain_slot(mem, k, enabled) for k in SLOTS}
    known = [s for s in slots.values() if s["certainty"] != "unknown"]
    # Overall share of each sensor in everything the robot currently believes.
    share = {m: 0.0 for m in MODALITIES}
    for s in known:
        for m, v in s["clues"].items():
            share[m] += max(v, 0.0)
    tot = sum(share.values()) or 1.0
    return {
        "t": t, "enabled": list(enabled),
        "slots": slots,
        "summary": {
            "known": len(known), "total": len(slots),
            "mean_certainty": round(float(np.mean([s["certainty_score"] for s in slots.values()])), 3),
            "sensor_share": {m: round(v / tot, 3) for m, v in share.items()},
        },
    }
