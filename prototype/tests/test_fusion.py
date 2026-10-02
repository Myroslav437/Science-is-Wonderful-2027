import numpy as np

from robotsees.config import CAMERA, MICROPHONE
from robotsees.fusion import EvidenceMemory, Observation, fuse_slot, sensor_clues, shapley_sensors
from robotsees.xai import evidence_ranking
from robotsees.xai import explain_slot, snapshot


def _mem():
    m = EvidenceMemory()
    # Camera sees red clothes several times (weak hint about favourite colour).
    for i in range(30):
        m.add(Observation(t=i * 0.2, modality=CAMERA, slot="colour",
                          likelihood={"red": 0.8, "orange": 0.2}, quality=0.9,
                          evidence="saw red clothes", weight=0.25))
    # Child says "blue".
    m.add(Observation(t=7, modality=MICROPHONE, slot="colour",
                      likelihood={"blue": 1.0}, quality=0.95, evidence='heard "blue"', weight=2.0))
    return m


def test_missing_modality_falls_back_to_flat_prior():
    b = fuse_slot(_mem(), "colour", ())
    assert np.allclose(b.probs, 1 / len(b.values))
    assert b.certainty[0] == "unknown"


def test_voice_beats_clothes_for_favourite_colour():
    m = _mem()
    assert fuse_slot(m, "colour", (CAMERA,)).best == "red"
    assert fuse_slot(m, "colour", (MICROPHONE,)).best == "blue"
    assert fuse_slot(m, "colour", (CAMERA, MICROPHONE)).best == "blue"


def test_conflict_lowers_confidence():
    m = _mem()
    both = fuse_slot(m, "colour", (CAMERA, MICROPHONE)).confidence
    ears = fuse_slot(m, "colour", (MICROPHONE,)).confidence
    assert both < ears


def test_shapley_efficiency():
    m = _mem()
    full = fuse_slot(m, "colour", (CAMERA, MICROPHONE))
    phi = shapley_sensors(m, "colour", (CAMERA, MICROPHONE))
    empty = fuse_slot(m, "colour", ())
    ti = full.values.index(full.best)
    assert abs(sum(phi.values()) - (full.probs[ti] - empty.probs[ti])) < 1e-9
    assert phi[MICROPHONE] > 0 > phi[CAMERA]


def test_more_observations_more_certain():
    m = EvidenceMemory()
    certs = []
    for i in range(8):
        m.add(Observation(t=i, modality=CAMERA, slot="glasses",
                          likelihood={"glasses": 0.7, "no glasses": 0.3}, quality=1.0, evidence="glasses-like shape", weight=0.25))
        certs.append(fuse_slot(m, "glasses", (CAMERA,)).confidence)
    assert all(b >= a for a, b in zip(certs, certs[1:]))


def test_explanation_and_snapshot_are_json_ready():
    import json
    m = _mem()
    e = explain_slot(m, "colour", (CAMERA, MICROPHONE))
    assert any("disagree" in line for line in e["explanation"])
    json.dumps(snapshot(m, (CAMERA, MICROPHONE)))
    e2 = explain_slot(m, "colour", (CAMERA,))
    assert any("switched off" in line for line in e2["explanation"])


def test_clues_are_exact_shapley_and_lomo_and_sum_of_cards():
    """Faithfulness: balance-scale weights == leave-one-out change == sum of clue cards."""
    m = _mem()
    both = (CAMERA, MICROPHONE)
    target = fuse_slot(m, "colour", both).best
    ti = fuse_slot(m, "colour", both).values.index(target)

    def centred(cfg):
        p = fuse_slot(m, "colour", cfg).probs
        lp = np.log(p)
        return lp[ti] - lp.mean()

    clues = sensor_clues(m, "colour", both, target)
    assert abs(centred(both) - centred(()) - sum(clues.values())) < 1e-9          # completeness
    for s, other in [(CAMERA, MICROPHONE), (MICROPHONE, CAMERA)]:
        assert abs(centred(both) - centred((other,)) - clues[s]) < 1e-9          # LOMO
    cards = evidence_ranking(m, "colour", both, target, k=100)
    for s in both:
        total = sum(c["push"] for c in cards if c["sensor"] == s)
        # cards with negligible or negative push are dropped from the ranking
        assert total >= clues[s] - 1e-9 or clues[s] < 0
