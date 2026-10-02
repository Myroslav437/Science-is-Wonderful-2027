"""Camera -> observations.

Per sampled frame (2-4 fps is plenty):
  MediaPipe face detector  -> head box (no landmarks, no identity, no embedding kept)
  MediaPipe pose landmarker -> torso box + body keypoints for motion energy
  clothing colour           -> k-means in CIELAB over a torso region starting
                               well below the shoulders (clothes, not skin),
                               named with 11 basic colour terms
  CLIP contrast prompts     -> glasses on the head crop, calibrated with
                               per-concept Platt scaling (fitted on Open Images)
  CLIP animal prompts       -> an animal picture card / toy shown to the robot
  keypoint speed            -> still / moving / very active (a momentary reading)

What is deliberately NOT computed: face recognition, face embeddings, age,
gender, skin tone, hair, headwear (can reveal religion), emotion/expression,
attractiveness, body shape, height.
"""
from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass, field

import numpy as np

from ..config import ANIMALS, CAMERA, COLOURS
from ..fusion import Observation

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
MP_MODELS = {
    "face": ("blaze_face_short_range.tflite",
             "https://mediapipe-models.storage.googleapis.com/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite"),
    "pose": ("pose_landmarker_lite.task",
             "https://mediapipe-models.storage.googleapis.com/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"),
}

# Contrast prompts (positive set vs. contrast set), as recommended for CLIP.
CONCEPT_PROMPTS = {
    "glasses": (["a photo of a person wearing glasses", "a photo of a person wearing sunglasses",
                 "a close-up photo of a face with eyeglasses"],
                ["a close-up photo of a person's bare eyes", "a photo of a face with nothing over the eyes",
                 "a close-up photo of a person's eyes and eyebrows"]),
}
ANIMAL_TEMPLATES = ["a photo of a {} toy", "a drawing of a {}", "a picture card showing a {}",
                    "a person holding a picture of a {}"]
BACKGROUND_PROMPTS = ["a photo of a person", "a close-up photo of a person's face",
                      "a photo of a person in a room", "a photo of a person's shoulders and t-shirt",
                      "a plain wall"]

# Basic colour terms as CIELAB prototypes (L*, a*, b*), several per name
# (dark / mid / light variants) -- sRGB D65 approximations.
COLOUR_LAB = {
    "red": [(45, 65, 45), (32, 48, 28), (55, 60, 35)],
    "orange": [(65, 40, 65), (58, 35, 55)],
    "yellow": [(88, -5, 80), (80, 0, 60)],
    "green": [(50, -45, 35), (32, -28, 15), (70, -35, 25), (60, -30, 5), (45, -30, 5)],
    "blue": [(40, 15, -55), (25, 5, -30), (60, -5, -35), (45, -10, -25), (35, -12, -12)],
    "purple": [(35, 45, -40), (55, 30, -30), (28, 25, -25)],
    "pink": [(72, 35, 0), (60, 55, -5), (80, 20, 5)],
    "brown": [(35, 18, 25), (45, 15, 30), (28, 10, 15)],
    "black": [(10, 0, 0), (20, 0, 0)],
    "white": [(95, 0, 0), (85, -2, 2)],
    "grey": [(40, 0, 0), (55, 0, 0), (70, 0, 0)],
}


def _ensure_model(key: str) -> str:
    fname, url = MP_MODELS[key]
    os.makedirs(MODEL_DIR, exist_ok=True)
    path = os.path.join(MODEL_DIR, fname)
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)
    return path


def _softmax(x, temp=1.0):
    x = np.asarray(x, float) / temp
    e = np.exp(x - x.max())
    return e / e.sum()


def name_colour(rgb_pixels: np.ndarray) -> tuple[dict[str, float], np.ndarray, float]:
    """Dominant colour of a pixel set -> (likelihood over COLOURS, swatch RGB, cluster share)."""
    import cv2
    px = rgb_pixels.reshape(-1, 3).astype(np.uint8)
    if len(px) < 50:
        return {}, np.zeros(3), 0.0
    if len(px) > 4000:
        px = px[np.random.default_rng(0).choice(len(px), 4000, replace=False)]
    lab = cv2.cvtColor(px.reshape(-1, 1, 3), cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)
    lab[:, 0] *= 100 / 255
    lab[:, 1:] -= 128
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centres = cv2.kmeans(lab, 3, None, crit, 2, cv2.KMEANS_PP_CENTERS)
    counts = np.bincount(labels.ravel(), minlength=3)
    k = int(np.argmax(counts))
    c = centres[k]
    names = list(COLOUR_LAB)
    d = []
    for n in names:
        p = np.array(COLOUR_LAB[n], float)
        # Lightness matters less than hue for colour names.
        d.append(np.sqrt(0.5 * (p[:, 0] - c[0]) ** 2 + (p[:, 1] - c[1]) ** 2 + (p[:, 2] - c[2]) ** 2).min())
    lik = _softmax(-np.array(d) / 8.0)
    swatch = px[labels.ravel() == k].mean(0)
    return dict(zip(names, lik)), swatch, float(counts[k] / counts.sum())


@dataclass
class FrameResult:
    t: float
    observations: list[Observation]
    person: bool = False
    head_box: tuple | None = None       # x0, y0, x1, y1 in pixels
    torso_box: tuple | None = None
    swatch: list | None = None
    scores: dict = field(default_factory=dict)
    quality: float = 0.0


class VisionPerception:
    def __init__(self, clip_name: str = "ViT-B-32", clip_pretrained: str = "laion2b_s34b_b79k",
                 calibration: str | dict | None = None, device: str = "cpu"):
        import mediapipe as mp
        import open_clip
        import torch
        from mediapipe.tasks import python as mpt
        from mediapipe.tasks.python import vision as mpv
        self.torch = torch
        self.mp = mp
        self.face = mpv.FaceDetector.create_from_options(mpv.FaceDetectorOptions(
            base_options=mpt.BaseOptions(model_asset_path=_ensure_model("face")),
            min_detection_confidence=0.5))
        self.pose = mpv.PoseLandmarker.create_from_options(mpv.PoseLandmarkerOptions(
            base_options=mpt.BaseOptions(model_asset_path=_ensure_model("pose")),
            num_poses=1, min_pose_detection_confidence=0.5))
        self.device = device
        self.clip, _, self.preprocess = open_clip.create_model_and_transforms(
            clip_name, pretrained=clip_pretrained, device=device)
        self.clip.eval()
        self.tok = open_clip.get_tokenizer(clip_name)
        with torch.no_grad():
            self.concept_txt = {k: (self._enc(p), self._enc(n)) for k, (p, n) in CONCEPT_PROMPTS.items()}
            self.animal_txt = torch.stack([self._enc([t.format(a) for t in ANIMAL_TEMPLATES]).mean(0)
                                           for a in ANIMALS])
            self.animal_txt = self.animal_txt / self.animal_txt.norm(dim=-1, keepdim=True)
            self.bg_txt = self._enc(BACKGROUND_PROMPTS)
        if calibration is None and os.path.exists(os.path.join(MODEL_DIR, "vision_calibration.json")):
            calibration = os.path.join(MODEL_DIR, "vision_calibration.json")
        if isinstance(calibration, str) and os.path.exists(calibration):
            calibration = json.load(open(calibration))
        # Platt parameters per concept: p = sigmoid(a * score + b). Defaults are
        # placeholders until experiments/calibrate_vision.py has been run.
        self.calib = calibration or {"glasses": {"a": 8.0, "b": 0.0}}
        self.prev_kp = None
        self.prev_t = None

    def _enc(self, texts):
        t = self.clip.encode_text(self.tok(texts).to(self.device))
        return t / t.norm(dim=-1, keepdim=True)

    def reset(self):
        self.prev_kp, self.prev_t = None, None

    def image_features(self, images: list) -> "np.ndarray":
        from PIL import Image
        torch = self.torch
        batch = torch.stack([self.preprocess(Image.fromarray(im)) for im in images]).to(self.device)
        with torch.no_grad():
            f = self.clip.encode_image(batch)
        return f / f.norm(dim=-1, keepdim=True)

    def concept_score(self, feats, concept: str) -> np.ndarray:
        """Raw contrast score: mean cosine to positive prompts minus contrast prompts."""
        pos, neg = self.concept_txt[concept]
        return ((feats @ pos.T).mean(-1) - (feats @ neg.T).mean(-1)).cpu().numpy()

    def calibrated(self, concept: str, score: float) -> float:
        c = self.calib[concept]
        return float(1 / (1 + np.exp(-(c["a"] * score + c["b"]))))

    # ------------------------------------------------------------------
    def analyse_frame(self, frame: np.ndarray, t: float) -> FrameResult:
        """frame: HxWx3 uint8 RGB."""
        import cv2
        h, w = frame.shape[:2]
        mp_img = self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=np.ascontiguousarray(frame))
        faces = self.face.detect(mp_img).detections
        pose = self.pose.detect(mp_img).pose_landmarks

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        brightness = float(gray.mean()) / 255
        sharp = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        img_q = float(np.clip((brightness - 0.08) / 0.2, 0, 1) * np.clip(sharp / 60.0, 0.15, 1))

        res = FrameResult(t=t, observations=[], quality=img_q)
        if not faces and not pose:
            self.prev_kp = None
            return res
        res.person = True

        face = max(faces, key=lambda d: d.bounding_box.width * d.bounding_box.height) if faces else None
        if face is not None:
            bb = face.bounding_box
            fx0, fy0, fw, fh = bb.origin_x, bb.origin_y, bb.width, bb.height
            fq = float(face.categories[0].score)
        elif pose:
            lm = pose[0]
            xs = [lm[i].x * w for i in (0, 2, 5, 7, 8)]
            ys = [lm[i].y * h for i in (0, 2, 5, 7, 8)]
            fw = max(xs) - min(xs) + 1e-3
            fx0, fy0, fh = min(xs), min(ys) - 0.4 * fw, 1.3 * fw
            fq = 0.6
        head = (int(max(0, fx0 - 0.3 * fw)), int(max(0, fy0 - 0.7 * fh)),
                int(min(w, fx0 + 1.3 * fw)), int(min(h, fy0 + 1.15 * fh)))
        res.head_box = head
        # A face only a few dozen pixels wide is too small to judge glasses:
        # evidence quality falls with face size (robot far away = less sure).
        size_q = float(np.clip(fw / 80.0, 0.05, 1.0))
        q = img_q * fq * size_q

        # Torso: from pose shoulders/hips if visible, else a box below the face.
        torso = None
        if pose:
            lm = pose[0]
            ls, rs, lh, rh = lm[11], lm[12], lm[23], lm[24]
            if min(ls.visibility, rs.visibility) > 0.5:
                sx0, sx1 = sorted([ls.x * w, rs.x * w])
                sy = max(ls.y, rs.y) * h
                sw = sx1 - sx0
                hip_y = max(lh.y, rh.y) * h if min(lh.visibility, rh.visibility) > 0.5 else sy + 1.2 * sw
                # Upper chest only: below the collar, above the waistband.
                torso = (sx0 + 0.2 * sw, sy + 0.15 * (hip_y - sy), sx1 - 0.2 * sw, sy + 0.6 * (hip_y - sy))
        if torso is None and face is not None:
            torso = (fx0 - 0.2 * fw, fy0 + 2.0 * fh, fx0 + 1.2 * fw, fy0 + 3.4 * fh)
        if torso is not None:
            x0, y0, x1, y1 = (int(np.clip(v, 0, lim)) for v, lim in zip(torso, (w, h, w, h)))
            if (x1 - x0) * (y1 - y0) > 0.01 * w * h:
                res.torso_box = (x0, y0, x1, y1)
                lik, swatch, share = name_colour(frame[y0:y1, x0:x1])
                if lik:
                    best = max(lik, key=lik.get)
                    res.swatch = [int(v) for v in swatch]
                    common = dict(t=t, modality=CAMERA, likelihood=lik, weight=0.25,
                                  detail={"swatch": res.swatch, "box": res.torso_box, "share": round(share, 2)})
                    res.observations.append(Observation(slot="shirt", quality=img_q * min(1, share * 1.5),
                                                        evidence=f"saw {best} clothes", **common))
                    res.observations.append(Observation(slot="colour", quality=img_q * min(1, share * 1.5),
                                                        evidence=f"saw {best} clothes (a clue, not proof)", **common))

        # CLIP: hat / glasses on the head crop, animal card on the whole frame.
        x0, y0, x1, y1 = head
        crops = [frame[y0:y1, x0:x1], frame]
        feats = self.image_features(crops)
        for concept in ("glasses",):
            s = float(self.concept_score(feats[:1], concept)[0])
            p = self.calibrated(concept, s)
            res.scores[concept] = {"raw": round(s, 4), "p": round(p, 3)}
            yes, no = concept, f"no {concept}"
            res.observations.append(Observation(
                t=t, modality=CAMERA, slot=concept, likelihood={yes: p, no: 1 - p},
                quality=q, weight=0.3,
                evidence="saw something like glasses" if p > 0.5 else "saw no glasses",
                detail={"box": head, "raw_score": round(s, 4), "p": round(p, 3)}))
        sims_animal = (feats[1:] @ self.animal_txt.T).cpu().numpy()[0]
        sims_bg = (feats[1:] @ self.bg_txt.T).cpu().numpy()[0]
        probs = _softmax(np.concatenate([sims_animal, [sims_bg.max()]]) * 100)
        res.scores["animal_bg"] = round(float(probs[-1]), 3)
        if probs[-1] < 0.5:
            pa = probs[:-1] / probs[:-1].sum()
            k = int(np.argmax(pa))
            res.observations.append(Observation(
                t=t, modality=CAMERA, slot="animal", likelihood=dict(zip(ANIMALS, pa)),
                quality=img_q * (1 - float(probs[-1])), weight=0.5,
                evidence=f"saw a picture or toy that looks like a {ANIMALS[k]}",
                detail={"p_background": round(float(probs[-1]), 3), "top": ANIMALS[k]}))

        # Motion energy from body keypoints (normalised by face width).
        # Only keypoints that are really visible and inside the frame (MediaPipe
        # guesses off-screen limbs in close-ups and those guesses jitter).
        kp = {}
        if pose:
            lm = pose[0]
            for i in (0, 11, 12, 13, 14, 15, 16):
                if lm[i].visibility > 0.7 and 0 <= lm[i].x <= 1 and 0 <= lm[i].y <= 1:
                    kp[i] = (lm[i].x * w, lm[i].y * h)
        if len(kp) < 2 and face is not None:
            kp = {-1: (fx0 + fw / 2, fy0 + fh / 2)}
        common_ids = sorted(set(kp) & set(self.prev_kp or {}))
        if common_ids and t > self.prev_t:
            a = np.array([kp[i] for i in common_ids]); b = np.array([self.prev_kp[i] for i in common_ids])
            speed = float(np.linalg.norm(a - b, axis=1).mean() / fw / (t - self.prev_t))
            z = np.log2(max(speed, 1e-3) / 0.25)
            lik = _softmax([-(z - c) ** 2 / 2 for c in (-1.5, 0.5, 2.5)])
            word = ("little", "some", "lots of")[int(np.argmax(lik))]
            res.scores["motion"] = round(speed, 3)
            res.observations.append(Observation(
                t=t, modality=CAMERA, slot="energy", likelihood=dict(zip(("still", "moving", "very active"), lik)),
                quality=q, weight=0.2, evidence=f"saw {word} movement ({speed:.2f} head-widths per second)",
                detail={"speed": round(speed, 3)}))
        self.prev_kp, self.prev_t = kp, t
        return res


def degrade(frame: np.ndarray, level: float, seed: int = 0) -> np.ndarray:
    """'Foggy lens' manipulation: blur + darken + sensor noise (level 0..1)."""
    import cv2
    if level <= 0:
        return frame
    k = int(1 + 2 * round(10 * level)) | 1
    out = cv2.GaussianBlur(frame, (k, k), 0).astype(np.float32)
    out *= (1 - 0.7 * level)
    out += np.random.default_rng(seed).normal(0, 40 * level, out.shape)
    return np.clip(out, 0, 255).astype(np.uint8)
