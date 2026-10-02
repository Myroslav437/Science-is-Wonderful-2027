"""Microphone -> observations.

Pipeline per audio window (a few seconds, e.g. one answer):
  Silero VAD -> speech segments
  faster-whisper (multilingual, word timestamps) -> words + per-word confidence
  closed lexicon -> favourite animal / favourite colour observations
  loudness (dBFS of speech samples, relative to a booth calibration level)
  speaking rate (words per second of speech)
  SNR estimate (speech vs. non-speech level) -> observation quality

Nothing about *who* is speaking is computed: no speaker embedding, no age,
gender, accent or emotion model. Pitch is not used either, because absolute
pitch mostly reflects age and sex.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..config import MICROPHONE
from ..fusion import Observation
from .lexicon import find_keywords

SR = 16000


@dataclass
class AudioResult:
    observations: list[Observation]
    transcript: str = ""
    language: str | None = None
    words: list[dict] = field(default_factory=list)
    speech_seconds: float = 0.0
    loudness_db: float | None = None      # relative to calibration level
    words_per_second: float | None = None
    snr_db: float | None = None
    quality: float = 0.0


def _softmax(x):
    x = np.asarray(x, float)
    e = np.exp(x - x.max())
    return e / e.sum()


def _db(x: np.ndarray) -> float:
    return float(20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9))


class AudioPerception:
    def __init__(self, asr_size: str = "small", compute_type: str = "int8",
                 device: str = "cpu", calibration_db: float = -26.0,
                 language: str | None = None, cpu_threads: int = 0):
        from faster_whisper import WhisperModel
        from silero_vad import load_silero_vad
        self.vad = load_silero_vad()
        self.asr = WhisperModel(asr_size, device=device, compute_type=compute_type,
                                cpu_threads=cpu_threads)
        self.calibration_db = calibration_db
        self.language = language

    # -- helpers -------------------------------------------------------------
    def speech_mask(self, audio: np.ndarray) -> tuple[np.ndarray, list[dict]]:
        import torch
        from silero_vad import get_speech_timestamps
        ts = get_speech_timestamps(torch.from_numpy(audio), self.vad, sampling_rate=SR,
                                   min_speech_duration_ms=150, min_silence_duration_ms=150)
        mask = np.zeros(len(audio), bool)
        for seg in ts:
            mask[seg["start"]:seg["end"]] = True
        return mask, ts

    # -- main ----------------------------------------------------------------
    def analyse(self, audio: np.ndarray, sr: int = SR, t0: float = 0.0) -> AudioResult:
        if sr != SR:
            import librosa
            audio = librosa.resample(audio.astype(np.float32), orig_sr=sr, target_sr=SR)
        audio = audio.astype(np.float32)
        mask, segs = self.speech_mask(audio)
        speech_s = mask.sum() / SR
        if speech_s < 0.25:
            return AudioResult([], speech_seconds=float(speech_s))

        speech_db = _db(audio[mask])
        noise = audio[~mask]
        noise_db = _db(noise) if len(noise) > SR * 0.2 else speech_db - 30
        snr = speech_db - noise_db
        q = float(np.clip((snr - 3) / 12, 0.05, 1.0))

        segments, info = self.asr.transcribe(audio, language=self.language, beam_size=1,
                                             word_timestamps=True, vad_filter=True,
                                             condition_on_previous_text=False)
        words = []
        for s in segments:
            for w in (s.words or []):
                words.append({"word": w.word.strip(), "start": round(t0 + w.start, 2),
                              "end": round(t0 + w.end, 2), "prob": round(float(w.probability), 3)})
        transcript = " ".join(w["word"] for w in words)
        rate = len(words) / speech_s if speech_s > 0 else 0.0
        rel_db = speech_db - self.calibration_db

        obs: list[Observation] = []
        # 1. Words from the closed lexicon (favourite animal / colour).
        for slot, value, spoken, start, prob in find_keywords(
                [(w["word"], w["start"], w["end"], w["prob"]) for w in words], info.language):
            obs.append(Observation(
                t=start, modality=MICROPHONE, slot=slot, likelihood={value: 1.0},
                quality=float(prob) * q ** 0.5, weight=2.0,
                evidence=f'heard you say "{spoken.strip(".,!?;:")}"',
                detail={"word": spoken.strip(".,!?;:"), "asr_prob": prob, "language": info.language}))

        t_mid = t0 + float(np.mean([seg["start"] + seg["end"] for seg in segs])) / 2 / SR
        # 2. Voice loudness (relative to the booth calibration level).
        vl = _softmax([-(rel_db - c) ** 2 / (2 * 4.0 ** 2) for c in (-8.0, 0.0, 8.0)])
        word = ("quiet", "normal", "loud")[int(np.argmax(vl))]
        obs.append(Observation(
            t=t_mid, modality=MICROPHONE, slot="voice",
            likelihood=dict(zip(("quiet", "normal", "loud"), vl)), quality=q,
            weight=min(1.0, speech_s / 2.0),
            evidence=f"heard a {word} voice ({rel_db:+.0f} dB)",
            detail={"loudness_rel_db": round(rel_db, 1), "snr_db": round(snr, 1)}))
        # 3. Activity from sound: how much sound there is right now (loudness only;
        #    speaking speed is deliberately not used -- stuttering and second-language
        #    speakers would be judged unfairly).
        el = _softmax([-(rel_db - c) ** 2 / (2 * 5.0 ** 2) for c in (-8.0, 0.0, 9.0)])
        eword = ("little", "some", "lots of")[int(np.argmax(el))]
        obs.append(Observation(
            t=t_mid, modality=MICROPHONE, slot="energy",
            likelihood=dict(zip(("still", "moving", "very active"), el)), quality=q,
            weight=min(1.0, speech_s / 2.0),
            evidence=f"heard {eword} sound ({rel_db:+.0f} dB)",
            detail={"loudness_rel_db": round(rel_db, 1)}))

        return AudioResult(obs, transcript=transcript, language=info.language, words=words,
                           speech_seconds=float(speech_s), loudness_db=round(rel_db, 1),
                           words_per_second=round(rate, 2), snr_db=round(snr, 1), quality=q)


def add_noise(audio: np.ndarray, snr_db: float, seed: int = 0,
              noise: np.ndarray | None = None) -> np.ndarray:
    """Degrade audio to a target SNR (white noise or a supplied babble track)."""
    rng = np.random.default_rng(seed)
    if noise is None:
        noise = rng.standard_normal(len(audio)).astype(np.float32)
    else:
        noise = np.resize(noise, len(audio)).astype(np.float32)
    p_sig = np.mean(audio ** 2) + 1e-12
    p_noise = np.mean(noise ** 2) + 1e-12
    noise = noise * np.sqrt(p_sig / (p_noise * 10 ** (snr_db / 10)))
    return (audio + noise).astype(np.float32)
