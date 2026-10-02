"""Closed, child-safe concept vocabulary ("slots") and per-sensor reliabilities.

The robot's internal representation of a visitor is a belief state over a small
set of slots. Every slot is something a child can check ("Do I wear glasses?"),
and none of them is a sensitive or protected characteristic: no age, gender,
emotion, ethnicity, identity, health or attractiveness, and no headwear
(it can reveal religion). That is a design constraint, not an omission
(see research/09-ethics-law.md, attribute register).
"""
from __future__ import annotations

from dataclasses import dataclass, field

CAMERA = "camera"
MICROPHONE = "microphone"
MODALITIES = (CAMERA, MICROPHONE)

# Display metadata used by every UI (kid-facing names, icons, colours).
MODALITY_META = {
    CAMERA: {"label": "Eyes (camera)", "short": "Eyes", "icon": "eye", "colour": "#2f7de1"},
    MICROPHONE: {"label": "Ears (microphone)", "short": "Ears", "icon": "ear", "colour": "#f08a24"},
}


@dataclass(frozen=True)
class Slot:
    key: str
    question: str                  # what the robot is trying to find out (kid language)
    values: tuple[str, ...]
    # How relevant each sensor is *for this slot* (0..1): the probability that
    # the cue actually says something about the slot.
    # These are design decisions and are shown to visitors ("eyes can only guess
    # your favourite colour from your clothes; ears hear you say it").
    reliability: dict[str, float] = field(default_factory=dict)
    # How the evidence is obtained, per sensor (used in explanations).
    how: dict[str, str] = field(default_factory=dict)

    @property
    def sensors(self) -> tuple[str, ...]:
        return tuple(m for m in MODALITIES if self.reliability.get(m, 0) > 0)


COLOURS = ("red", "orange", "yellow", "green", "blue", "purple", "pink",
           "brown", "black", "white", "grey")

ANIMALS = ("dog", "cat", "horse", "rabbit", "bird", "fish", "lion",
           "elephant", "bear", "monkey", "turtle", "dinosaur")

SLOTS: dict[str, Slot] = {s.key: s for s in [
    Slot("animal", "What is your favourite animal?", ANIMALS,
         reliability={MICROPHONE: 1.0, CAMERA: 0.6},
         how={MICROPHONE: "heard the animal's name in what you said",
              CAMERA: "saw an animal picture or toy you showed"}),
    Slot("colour", "What is your favourite colour?", COLOURS,
         reliability={MICROPHONE: 1.0, CAMERA: 0.35},
         how={MICROPHONE: "heard you say a colour",
              CAMERA: "guessed from the colour of your clothes"}),
    Slot("shirt", "What colour are your clothes?", COLOURS,
         reliability={CAMERA: 1.0},
         how={CAMERA: "measured the colours of the pixels on your top"}),
    Slot("glasses", "Are you wearing glasses?", ("glasses", "no glasses"),
         reliability={CAMERA: 1.0},
         how={CAMERA: "compared your face area with pictures of glasses"}),
    # Momentary readings, never traits ("you are moving a lot right now",
    # not "you are a bouncy person"): trait labels edge towards behaviour or
    # health profiling of children.
    Slot("energy", "How much is happening right now?", ("still", "moving", "very active"),
         reliability={CAMERA: 0.9, MICROPHONE: 0.6},
         how={CAMERA: "measured how fast your body moves",
              MICROPHONE: "measured how much sound you make"}),
    Slot("voice", "How loud is the voice I hear right now?", ("quiet", "normal", "loud"),
         reliability={MICROPHONE: 1.0},
         how={MICROPHONE: "measured the loudness of the voice"}),
]}

# Confidence language shown to children (max posterior probability thresholds).
CERTAINTY_LEVELS = (
    (0.75, "sure", "I'm sure"),
    (0.50, "think", "I think"),
    (0.25, "guess", "I'm guessing"),
    (0.00, "unknown", "I don't know yet"),
)

# Evidence accumulation: how many "good observations" until a sensor's opinion
# reaches ~63% of its full weight (saturating, so 100 video frames are not
# treated as 100 independent proofs).
SATURATION_TAU = 1.5
# Floor mixed into every likelihood so no single observation is ever "certain".
LIKELIHOOD_FLOOR = 0.05

# Shown on screen: what the robot will never try to find out, and why.
NEVER_GUESS = (
    ("who you are", "I don't recognise faces or voices. I forget you when you leave."),
    ("how you feel", "Faces and voices don't reliably show feelings, and guessing them is not allowed here."),
    ("your age or gender", "Machines often get these wrong, and it is not my business."),
    ("where you come from", "Skin, hair or accent say nothing about who you are."),
    ("anything about your health", "Glasses help eyes; they tell me nothing else."),
)
