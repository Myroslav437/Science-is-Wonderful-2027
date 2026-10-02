"""Evidence memory and late fusion.

Representation = for every slot, a probability distribution over its values.

Each perception module emits `Observation`s: a likelihood vector over a slot's
values (the module's opinion), a quality in [0, 1] (how usable the signal was:
dark frame, no face found, low SNR, ASR unsure...) and human-readable evidence.

Fusion is a tempered logarithmic opinion pool (product of experts):

    score(v) = log prior(v) + sum_{m in enabled} E_m(v)
    P(v)     = softmax(score)

    E_m(v)   = kappa_m * mean_k[ log(r L_k(v) + (1-r)/|V|) - log(1/|V|) ]   (quality-weighted)
    kappa_m  = 1 - exp(-sum_k q_k w_k / tau)

    r = relevance of sensor m for the slot. It is a mixture with "uninformative":
        with probability r the cue says something about the slot, otherwise it
        says nothing. So red clothes make "favourite colour = red" a bit more
        likely without strongly ruling out blue.
    w = how many independent observations one observation is worth (one video
        frame is worth little -- frames are correlated; one spoken word is
        worth a lot).

* A disabled or silent sensor contributes nothing, so the belief falls back to
  the prior (flat), which is exactly "I don't know" -- no imputation.
* kappa saturates, so a sensor gets more convincing with more good observations
  but 100 correlated video frames are not 100 independent proofs.
* r encodes how relevant a sensor is for a slot (e.g. clothes colour is only a
  weak hint about a favourite colour).

Because every sensor configuration is just a different `enabled` set, the
counterfactuals ("what would I think with only my ears?") and the exact
Shapley values over sensors are computed with the very same function the robot
uses -- the explanation is faithful by construction.
"""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field

import numpy as np

from .config import (CERTAINTY_LEVELS, LIKELIHOOD_FLOOR, MODALITIES,
                     SATURATION_TAU, SLOTS)


@dataclass
class Observation:
    t: float                       # seconds since the interaction started
    modality: str
    slot: str
    likelihood: dict[str, float]   # module's opinion over slot values (need not be normalised)
    quality: float                 # 0..1
    evidence: str                  # kid-readable "what I noticed"
    detail: dict = field(default_factory=dict)  # technical detail (scores, crop box, words...)
    weight: float = 1.0            # independent-evidence units (frame << spoken word)

    def log_evidence(self) -> np.ndarray:
        spec = SLOTS[self.slot]
        values = spec.values
        lik = np.array([max(self.likelihood.get(v, 0.0), 0.0) for v in values], float)
        lik = lik / lik.sum() if lik.sum() > 0 else np.full(len(values), 1 / len(values))
        n = len(values)
        lik = (1 - LIKELIHOOD_FLOOR) * lik + LIKELIHOOD_FLOOR / n
        r = spec.reliability.get(self.modality, 0.0)
        lik = r * lik + (1 - r) / n
        return np.log(lik) - math.log(1 / n)


class EvidenceMemory:
    """Per-visitor, in-RAM evidence ledger. Cleared when the visitor leaves.

    This is the robot's whole "memory" -- a list of observations plus running
    sums. No images, audio or embeddings are kept, only the per-slot evidence
    the modules produced.
    """

    def __init__(self) -> None:
        self.observations: list[Observation] = []

    def add(self, obs: Observation | list[Observation]) -> None:
        if isinstance(obs, Observation):
            obs = [obs]
        for o in obs:
            if o.slot in SLOTS and o.modality in SLOTS[o.slot].reliability:
                self.observations.append(o)

    def clear(self) -> None:
        self.observations.clear()

    def upto(self, t: float) -> "EvidenceMemory":
        m = EvidenceMemory()
        m.observations = [o for o in self.observations if o.t <= t]
        return m

    def modality_evidence(self, slot: str, modality: str) -> tuple[np.ndarray, float, list[Observation]]:
        """Return (E_m vector, kappa, observations) for one slot and sensor."""
        obs = [o for o in self.observations if o.slot == slot and o.modality == modality]
        n = len(SLOTS[slot].values)
        q = np.array([o.quality * o.weight for o in obs], float)
        if len(obs) == 0 or q.sum() <= 1e-9:
            return np.zeros(n), 0.0, obs
        logs = np.stack([o.log_evidence() for o in obs])
        mean = (q[:, None] * logs).sum(0) / q.sum()
        kappa = 1 - math.exp(-q.sum() / SATURATION_TAU)
        return kappa * mean, kappa, obs


@dataclass
class SlotBelief:
    slot: str
    values: tuple[str, ...]
    probs: np.ndarray
    enabled: tuple[str, ...]

    @property
    def best(self) -> str:
        return self.values[int(np.argmax(self.probs))]

    @property
    def confidence(self) -> float:
        return float(np.max(self.probs))

    @property
    def entropy(self) -> float:
        p = np.clip(self.probs, 1e-12, 1)
        return float(-(p * np.log(p)).sum() / math.log(len(p)))

    @property
    def certainty(self) -> tuple[str, str]:
        # With few values (glasses / no glasses) a flat belief is already 0.5, so rescale
        # confidence to [0, 1] between "uniform" and "one-hot" first.
        n = len(self.values)
        c = (self.confidence - 1 / n) / (1 - 1 / n)
        for thr, key, phrase in CERTAINTY_LEVELS:
            if c >= thr:
                return key, phrase
        return CERTAINTY_LEVELS[-1][1:]

    @property
    def certainty_score(self) -> float:
        n = len(self.values)
        return float((self.confidence - 1 / n) / (1 - 1 / n))


def fuse_slot(memory: EvidenceMemory, slot: str, enabled: tuple[str, ...],
              prior: np.ndarray | None = None) -> SlotBelief:
    spec = SLOTS[slot]
    n = len(spec.values)
    score = np.log(prior) if prior is not None else np.full(n, -math.log(n))
    for m in enabled:
        if spec.reliability.get(m, 0.0) <= 0:
            continue
        e, _, _ = memory.modality_evidence(slot, m)
        score = score + e
    p = np.exp(score - score.max())
    return SlotBelief(slot, spec.values, p / p.sum(), tuple(enabled))


def fuse_all(memory: EvidenceMemory, enabled: tuple[str, ...]) -> dict[str, SlotBelief]:
    return {k: fuse_slot(memory, k, enabled) for k in SLOTS}


def all_configs(modalities: tuple[str, ...] = MODALITIES) -> list[tuple[str, ...]]:
    out = []
    for r in range(len(modalities), -1, -1):
        out.extend(itertools.combinations(modalities, r))
    return out


def sensor_clues(memory: EvidenceMemory, slot: str, enabled: tuple[str, ...],
                 target: str) -> dict[str, float]:
    """Each sensor's "clues" for `target`, in log-odds units.

    clue_m = E_m(target) - mean_v E_m(v). The fused centred score of `target`
    is exactly prior_term + sum_m clue_m, so the game v(S) = centred score with
    sensors S is additive: clue_m is simultaneously (a) the exact Shapley value
    of sensor m, (b) the leave-one-sensor-out change and (c) the sum of that
    sensor's individual clue cards (see xai.evidence_ranking). These are the
    numbers the visitor sees on the balance scale.
    """
    ti = SLOTS[slot].values.index(target)
    out = {}
    for m in enabled:
        if SLOTS[slot].reliability.get(m, 0) <= 0:
            continue
        e, _, _ = memory.modality_evidence(slot, m)
        out[m] = float(e[ti] - e.mean())
    return out


def shapley_sensors(memory: EvidenceMemory, slot: str, enabled: tuple[str, ...],
                    target: str | None = None) -> dict[str, float]:
    """Exact Shapley value of each enabled sensor for P(target) (probability space).

    Kept for comparison; probability-space values depend on the softmax
    curvature and on the other sensors, which is why the exhibit displays
    `sensor_clues` (log-odds space) instead.

    Players are the enabled sensors; the value of a coalition S is the
    probability the robot itself would give `target` if only S were switched
    on. With 2-3 sensors this is 4-8 cheap re-fusions (no model re-runs),
    and it is literally what the visitor sees when flipping the switches.
    """
    full = fuse_slot(memory, slot, enabled)
    target = target or full.best
    ti = SLOTS[slot].values.index(target)
    players = [m for m in enabled if SLOTS[slot].reliability.get(m, 0) > 0]
    n = len(players)
    cache: dict[frozenset, float] = {}

    def v(S: frozenset) -> float:
        if S not in cache:
            cache[S] = float(fuse_slot(memory, slot, tuple(S)).probs[ti])
        return cache[S]

    phi = {}
    for p in players:
        others = [o for o in players if o != p]
        total = 0.0
        for r in range(len(others) + 1):
            for S in itertools.combinations(others, r):
                S = frozenset(S)
                wgt = math.factorial(len(S)) * math.factorial(n - len(S) - 1) / math.factorial(n)
                total += wgt * (v(S | {p}) - v(S))
        phi[p] = total
    return phi
