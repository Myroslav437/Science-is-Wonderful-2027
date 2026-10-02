# 04 — Audio and speech models for the offline pipeline

**Track:** audio and speech models and tools (VAD, ASR, prosody, audio-language models, sound events, speaker traits, emotion, TTS, small LLMs), all running **locally and offline**.
**Exhibit:** "How does a robot see you?" (TUAI DC5/DC7, Science is Wonderful! 2027, Brussels).
**Date of research:** 2026-10-01/02. Prices are not relevant to this track, since every component is free or open source. Licences and versions were checked on the official pages on these dates.
**Legend:** [Sn] = source in the list at the end. **[LOCAL]** = measured by us on the dev laptop (Intel Core Ultra 7 255U, 12 cores / 14 threads, 32 GB, no NVIDIA GPU, Windows 11, Python 3.12, CPU only); the scripts and raw JSON are in `research/04-audio-bench/`. **UNVERIFIED** = not confirmed from a primary source.

> **Caveat on the [LOCAL] timings.** Other agents' benchmark jobs (session building, image generation) were running at the same time, and Windows reported **100 % CPU load** during our runs. Treat every [LOCAL] latency as **pessimistic, roughly an upper bound**. An earlier run by the team on a quieter machine measured faster-whisper `small` int8 at **2.4 s per 10 s** and `base` at **1.19 s** [LOCAL: `scratch/bench_models.json`; note that it used noise input, which yields few tokens]. **Re-run `bench_audio.py` on the actual exhibition machine with vision running alongside** before freezing the design.

---

## 0. Decisions in one screen

1. **Use a closed task, not open listening.** The robot asks a short question ("What's your favourite animal?"). One 3–8 s answer window then passes through **VAD → ASR with the language forced → closed multilingual lexicon**. The existing prototype (`prototype/robotsees/perception/audio.py`) already works this way. Keep it, and harden it (§11).
2. **VAD:** **Silero VAD 6.2.x** (MIT). v6.2 (Nov 2025) specifically improved **child voices** [S1–S3]. [LOCAL] 0.69 ms per 32 ms chunk, 0.09 s per 10 s clip.
3. **ASR, CPU-only prototype:** **faster-whisper `base` or `small`, int8** (MIT) with `language=` forced from the visitor's flag button. [LOCAL, under load] base 1.15 s, small 4.25 s per 10 s. **Alternative to benchmark properly:** **NVIDIA Parakeet-TDT-0.6B-v3** int8 ONNX via `onnx-asr` (CC-BY-4.0, 25 EU languages incl. PL/NL/FR/DE). [LOCAL, under load] 3.45 s per 10 s. The Parakeet/Canary family beats Whisper zero-shot on child speech [S29], and the Conformer family hallucinates far less on non-speech [S37]. [corrected by verifier: [S29] tested the *English* Parakeet-RNNT and Canary v1, not Parakeet-TDT-0.6B-v3 or Canary-1B-v2, and only on English child speech (MyST/OGI). There is no published child-speech result for the v3/v2 multilingual models, so the A/B test in §12.3 is the actual evidence, not the literature.] [verifier note: Whisper always pads input to a 30 s window, so a short answer costs nearly as much as a 10 s clip. Our GRID run measured faster-whisper small int8 at **2.28 s per ~2.5 s utterance** (RTF ≈0.9, not 0.43) [LOCAL: `audio_grid.json`, `seconds_per_clip_cpu`]. See §2.]
4. **ASR, exhibition laptop with mid-range NVIDIA GPU:** **faster-whisper `large-v3-turbo`** (fp16 / int8_float16) **or Parakeet-TDT-0.6B-v3 / Canary-1B-v2** on CUDA. Keep the CPU model as a hot fallback.
5. **Child speech is the main accuracy risk, not model size.** Zero-shot Whisper-large-v3 gets **12.6 % WER on MyST and 19.9 % on OGI kids' speech** [S29]. On *noisy* Dutch classroom speech even the best model gets **70 % WER** [S32]. Our own babble test (adults, closed colour lexicon) dropped from **79.7 % correct (clean) to 26.6 % at 0 dB SNR** [LOCAL: `prototype/experiments/results/audio_grid.json`]. **The microphone and its placement matter more than the model choice** (§3.5).
6. **Prosody that is safe to show:** loudness relative to a booth calibration, talk time, pause share, and turn count (VAD). **Do not show absolute pitch**, which is mostly an age/sex proxy (the prototype already omits it). Speaking rate is unreliable for children and second-language speakers, so show it at most as a neutral number.
7. **Audio-language models (CLAP etc.) are not reliable "concept scorers" for speech.** MS-CLAP 2023 zero-shot gets **80 % on vocal sounds** (laughter, cough, sigh…) but only **30 % / 31.5 % on CREMA-D / RAVDESS emotion** and **16.4 % on Speech Commands** [S44]. Our probe on adult Lombard speech: see §6.3. Use **sound-event taggers** (EfficientAT / PANNs / YAMNet / AST) with an **allow-list** for "laughter / clapping / music / singing" instead.
8. **Do not build age, gender, child-vs-adult, speaker-ID or emotion-from-voice features.** They are biometric categorisation (age and sex are named in AI Act recital 16), which triggers the Art. 50(3) notice. Emotion inference is prohibited in workplace and education settings under Art. 5(1)(f), and the Commission reads "workplace" broadly. Their accuracy on 12–14-year-olds is also unproven. See `09-ethics-law.md` for the legal analysis. Also **mask the AudioSet classes** "Male speech", "Female speech", "Child speech, kid speaking" and "Child singing" in any tagger output.
9. **TTS:** **pre-render all scripted robot lines** to WAV offline, which removes the runtime risk. For dynamic lines use **Piper** (piper-tts 1.8.0, GPL-3.0 code) with **CC0 / CC-BY voices only**: `nl_BE-nathalie`, `de_DE-thorsten`, `pl_PL-gosia`, `fr_FR-siwis`, and `en_GB-alba` or `en_US-joe`. **Avoid `en_US-lessac`**: its training data is research-only Blizzard 2013 material. Avoid Coqui XTTS-v2 (non-commercial CPML, company closed) and voice cloning entirely. Kokoro and MeloTTS **lack DE/NL/PL**. [corrected by verifier: every recommended voice above (`nl_BE-nathalie`, `de_DE-thorsten` medium and high, `pl_PL-gosia`, `fr_FR-siwis`, `en_GB-alba`, `en_US-joe`) is, according to its own MODEL_CARD, **"Finetuned from U.S. English lessac voice"**. So their weights descend from the research-only Blizzard 2013 data that this document rejects for `en_US-lessac`. The dataset licence (CC0/CC-BY) covers only the fine-tuning recordings. Voices checked as **trained from scratch** without lessac: `nl_NL-mls-medium`, `fr_FR-mls-medium`, `de_DE-mls-medium` (all CC-BY-4.0, MLS/LibriVox) and `en_US-ljspeech-medium` (public domain). No lessac/ryan-free Polish Piper voice was found (`pl_PL-mls_6892` is fine-tuned from `en_US-ryan`, CC BY-NC-SA). Get a decision from the ethics/legal advisor before choosing voices; see §9.1.]
10. **No generative LLM in the child-facing loop.** Deterministic lexicon + fuzzy matching + optional multilingual-e5-small similarity gives explainable slot extraction in about 0.05 s per sentence [LOCAL]. If an LLM is ever used (e.g. Qwen3/Qwen3.5 Apache-2.0, Phi-4-mini MIT), constrain it to grammar-forced JSON over an allow-list, and never let it speak or display free text. CPU speeds: §10.

---

## 1. What the microphone may legitimately contribute

| Allowed output ("robot's ears") | Evidence shown to the visitor (XAI) | Notes |
|---|---|---|
| Spoken answer slots (favourite animal, colour, hobby, from a closed list) | "I heard you say *chien* (confidence 0.82)" plus the word's timestamp on the waveform | Only lexicon words can enter the representation, so hallucinated text never reaches the screen |
| Voice loudness: quiet / normal / loud **relative to the booth calibration** | Live level meter in dB, with a "your voice" band vs. the "hall noise" band | AI Act recital 18 treats "a raised voice or whispering" as readily apparent features, **not** emotion recognition, provided no emotion is inferred [S64] |
| Talk time, number of turns, pause share | VAD timeline (speech bars) | Purely behavioural, no identity information |
| "I can hear music / clapping / laughter around us" (scene context) | Tagger top classes with scores, allow-listed | Describe the scene, not the person ("I heard laughter", never "you are happy") |
| Language the visitor chose / spoke | Flag icon | Prefer the visitor's own button press; ASR language-ID is error-prone on short clips (§3.3) [verifier: AI Act recital 16 lists **"language"** next to sex and age as a biometric-categorisation category [S64], so the button is also the legally cleaner option. Do not present auto-detected language as a fact about the visitor] |
| Signal quality (SNR) to drive uncertainty | "It's noisy here, so I'm less sure" | Feeds the fusion uncertainty, as the prototype already does |

Not allowed (§7–8): age, gender, child-vs-adult, accent or "where you're from", emotion or mood, voiceprint or re-identification, health or "stress".

---

## 2. Local measurements (dev laptop, CPU only)

Input: a 10 s clip made of 4 Lombard-GRID utterances (adult English, CC BY 4.0). int8, `beam_size=1`, `word_timestamps=True`, `condition_on_previous_text=False`. Median of 2–3 runs after warm-up. **The machine was under 100 % concurrent load** (see the caveat above).

| Component | Model / settings | Load time | Time per 10 s of audio | RTF | Notes |
|---|---|---|---|---|---|
| VAD | Silero VAD 6.2.3 (torch JIT) | – | **0.093 s** (0.69 ms per 32 ms chunk) | 0.009 | Streaming-capable |
| ASR | faster-whisper **tiny** int8, `language="en"` | 0.9 s | **0.56 s** (1.12 s with auto language-ID) | 0.06 | Many errors on GRID |
| ASR | faster-whisper **base** int8 | 0.8 s | **1.15 s** (2.84 s auto-LID) | 0.12 | |
| ASR | faster-whisper **small** int8 | 1.9 s | **4.25 s** (6.85 s auto-LID) | 0.43 | Team's earlier run: 2.4 s |
| ASR | faster-whisper **medium** int8 | 7.1 s | **12.4 s** (48 s auto-LID) | 1.24 | Not real-time on this CPU |
| ASR | faster-whisper **large-v3-turbo** int8 | 14.7 s | **15.5 s** (38.6 s auto-LID) | 1.55 | **GPU-only option** |
| ASR | **Parakeet-TDT-0.6B-v3** int8 ONNX (`onnx-asr` 0.12.0) | 7.8 s | **3.45 s** (automatic language) | 0.35 | Output includes punctuation and casing |
| Pitch | librosa 1.0.0 `pyin` (fmin 70, fmax 700, hop 10 ms) | – | **0.88 s** | 0.09 | `yin` takes 0.076 s, but has no voicing probability |
| Loudness | librosa `rms` | – | 0.002 s | ≈0 | |
| Sound events | AST (MIT/ast-finetuned-audioset, 86.6 M params) | – | **8.5 s** (heavily contended) | 0.85 | Top classes on the adult clip: Speech 0.89, …, **"Male speech, man speaking" 0.21**. This shows why an allow-list is needed |
| Text embedding | multilingual-e5-small (4 sentences) | – | **0.18 s** for 4 | – | For paraphrase matching |
| CLAP | see §6.3 | | | | |
| TTS | Piper medium voices, see §9.2 | | | | |
| LLM | llama.cpp CPU, see §10.2 | | | | |

[verifier note on the RTF column: Whisper-family models (incl. faster-whisper) pad every call to a 30 s window [S10, S34], so encoder cost is roughly fixed per call and RTF measured on 10 s clips **understates** the cost of short answers. On single ~2.5 s GRID utterances, faster-whisper small int8 took **2.28 s per clip** clean and 4.91 s at 0 dB babble (longer decoding in noise) [LOCAL: `audio_grid.json`]. Parakeet (FastConformer) does not pad to 30 s, so its per-utterance cost should scale with length. Re-measure both per *utterance*, not per 10 s.]

The team's earlier **noise-robustness experiment** used the same pipeline: faster-whisper small, Lombard GRID (12 talkers × 16 = 192 utterances), closed EN/FR/NL/DE/PL colour lexicon, and 6-talker babble [LOCAL: `prototype/experiments/results/audio_grid.json`; verifier: the JSON confirms 12 talkers × 4 colours × {plain, Lombard} × 2 = 192 and all numbers below, but does **not** record the babble talker count, so "6-talker" is unverifiable from the file]:

| Condition | Colour word correct | Wrong value | Missed | Loud-vs-plain AUROC (absolute level) | s/clip CPU |
|---|---|---|---|---|---|
| Clean, language forced EN | 0.797 | 0.000 | 0.203 | 0.813 | 2.28 |
| Babble 10 dB SNR | 0.714 | 0.000 | 0.286 | 0.818 | 2.91 |
| Babble 5 dB | 0.641 | 0.000 | 0.359 | 0.820 | 3.68 |
| Babble 0 dB | **0.266** | 0.005 | 0.729 | 0.816 | 4.91 |
| Clean, **auto language-ID** | 0.734 | 0.000 | 0.266 | 0.813 | 6.01 (EN detected in only 85.4 % of clips) |

Read-out: (i) the closed lexicon almost never produces a *wrong* value. Errors are *misses*, which fail safely ("I didn't catch that"). (ii) Below about 5 dB SNR the ears become useless. (iii) Forcing the language beats auto-LID on both accuracy and latency. (iv) Loudness ranking works (AUROC ≈ 0.82) and is noise-robust, because VAD selects the speech frames.

---

## 3. (a)+(b) Voice activity detection and speech recognition

### 3.1 VAD

| Tool | Version / date | Licence | Size / speed | Quality evidence | Use |
|---|---|---|---|---|---|
| **Silero VAD** | **6.2.3 (23 Sep 2026)**; v6.0 26 Aug 2025; v6.2 6 Nov 2025 "edge case improvements: child voices, cartoon voices, muted speech"; v6.2.2 (17 Sep 2026) added an offline 16 kHz "sequence" ONNX model [S2, S3] | MIT [S1] | JIT model ≈ 2 MB; "<1 ms per 30+ ms chunk on one CPU thread"; 8 / 16 kHz; `pip install silero-vad` (torchaudio and onnxruntime optional since 6.2.1/6.2.3) [S1–S3] | ROC-AUC on a multi-domain validation set: **v6 0.97, v5 0.91, WebRTC 0.73** [S4] [corrected by verifier: the wiki gives **v5 0.96** (0.91 is v4); v6 0.97, WebRTC 0.73 and TEN 0.93 are correct]. v6.0 release notes listed "small children voices" as a known weakness, fixed in 6.2 [S2] | **Default** |
| WebRTC VAD (`webrtcvad-wheels`) | 2.0.14 (Sep 2024) | MIT [S6] | GMM, 10/20/30 ms frames, aggressiveness 0–3, 8–48 kHz [S6] | 0.73 ROC-AUC (above). Fires on any non-stationary noise | Fallback only |
| TEN VAD | 2025 | **Apache-2.0 "with additional conditions"** (read before use) [S7] [verifier: the LICENSE adds that you may not deploy it "in a way that competes with Agora's offerings", and may deploy it only within your own Application for your direct End Users. That is acceptable for an exhibit, but it is not plain Apache-2.0] | 306–508 KB library; RTF 0.0086 vs Silero 0.0127 on a Xeon (vendor figure); 16 kHz, 10/16 ms hops [S7] | 0.93 multi-domain ROC-AUC in Silero's own table [S4]. Vendor claims faster speech→silence transitions [S7] | Optional, for end-of-turn latency |
| pyannote segmentation-3.0 | pyannote.audio **4.0.7 (30 Jun 2026)** [S9] | MIT, but **gated on HF** (token needed) [S8] | 10 s chunks, 16 kHz; VAD + overlap + speaker change [S8] | Diarization pipelines (community-1) [S9] | **Not needed**: diarization means tracking who is who, which edges toward identification |

**Settings for children in a hall (starting point, to be tuned on recordings from the actual booth):** `threshold=0.5`, `neg_threshold=0.35`, `min_speech_duration_ms=150`, `min_silence_duration_ms=300–500` (children pause mid-answer), `speech_pad_ms=100`. Answer window: start at the end of the robot's prompt (mute the mic while the robot speaks, to avoid echo of its own TTS), close at 8 s or after 0.8 s of silence following speech. faster-whisper exposes the same parameters in `VadOptions` [S12; LOCAL: installed `faster_whisper/vad.py`].

### 3.2 ASR model landscape (verified Oct 2026)

| Model | Params | Licence | Languages relevant to us | CPU latency (source) | GPU | Child-speech / robustness evidence | Verdict |
|---|---|---|---|---|---|---|---|
| **OpenAI Whisper** tiny/base/small/medium/large(-v3)/turbo | 39 M / 74 M / 244 M / 769 M / 1550 M / 809 M [S10] | MIT (code and weights) [S10] | 99 languages incl. EN/FR/NL/DE/PL [S11] | Original PyTorch implementation is slow on CPU. Use faster-whisper or whisper.cpp | VRAM ≈ 1/1/2/5/10/6 GB; turbo ≈ 8× faster than large [S10] | MyST/OGI zero-shot WER: tiny 20.6/53.8, base 16.8/38.0, small 13.4/25.4, medium 13.1/20.8, large-v3 12.6/19.9 [S29] | Reference family |
| **faster-whisper** (CTranslate2) | same weights | MIT; v1.2.1 (31 Oct 2025) [S12, S13] | same | Small model on an i7-12700K (8 threads), 13 min of audio: fp32 2m37s, **int8 1m42s (RTF 0.13)**, batched int8 51 s [S12]. [LOCAL] §2 | large-v2 on an RTX 3070 Ti: fp16 1m03s for 13 min (RTF 0.08); batched 17 s [S12] | Built-in Silero VAD filter, word timestamps, `hotwords`, `hallucination_silence_threshold` [S12; LOCAL] | **Primary** |
| **whisper.cpp** | same, GGML | MIT [S14] | same | tiny ≈ 273 MB RAM … large ≈ 3.9 GB; CPU, **OpenVINO**, Vulkan, CUDA backends; Silero VAD built in [S14]. v1.8.0 (30 Sep 2025) enabled flash attention by default; latest v1.9.4 (11 Sep 2026) [S14] | CUDA, Vulkan | – | Good C++ option; OpenVINO could use the Intel iGPU (not measured) |
| OpenVINO GenAI `WhisperPipeline` | same | Apache-2.0 | same | CPU or Intel GPU; word timestamps need a special export flag [S80] | – | – | Worth one test on the Intel iGPU (**UNVERIFIED** speed) |
| **distil-large-v3.5** | 756 M | MIT | **English only** [S15] | ≈1.5× faster than turbo [S15] | yes | short-form WER 7.08 % (out-of-distribution) [S15] | No: not multilingual |
| **Moonshine** v2 (streaming) | Tiny 34 M / Small 123 M / Medium 245 M [S17] | MIT for streaming models; legacy non-English non-streaming models under a **non-commercial** Moonshine Community License [S16] | **English + 7 (ar, ja, ko, zh, es, uk, vi)**; **no FR/NL/DE/PL** [S16, S18] [verifier: the v2 paper states "Our current models focus exclusively on English ASR" [S17]; the 7 other languages are the legacy non-streaming models under the non-commercial licence. The 7-language list itself comes from a third-party index [S18], unverified on a primary page] | On an Apple M3: Tiny 50 ms, Small 148 ms, Medium 258 ms response latency vs Whisper Small 1,940 ms [S17] | – | Open ASR WER: 12.0 / 7.84 / 6.65 % [S17] | Only for an English-only build |
| **NVIDIA Parakeet-TDT-0.6B-v3** | 600 M | **CC-BY-4.0** (attribution) [S19] | **25 European languages incl. EN/FR/DE/NL/PL**, automatic language detection, word timestamps [S19] | CPU via ONNX: 36 RTFx on a Ryzen 9800X3D (onnx-asr) [S21]. [LOCAL] 3.45 s per 10 s under load | T4 57 RTFx; RTX 5070 Ti + TensorRT 320 RTFx [S21] | FLEURS WER: EN 4.85, FR 5.15, DE 5.04, **NL 7.48, PL 7.31** [S19]. Parakeet-RNNT (English) beat Whisper zero-shot on OGI kids (16.7 vs 19.9) [S29] | **Strong candidate**; test on children |
| **NVIDIA Canary-1B-v2** | 978 M | CC-BY-4.0 [S20] | Same 25 languages; ASR + translation [S20] | GPU-oriented; ONNX supported in onnx-asr [S21] | RTFx 749 [S20] | Canary (v1) was the best zero-shot model on MyST (9.5 % WER) [S29] | GPU option |
| Nemotron Speech Streaming EN 0.6B | 600 M | NVIDIA Open Model License [S27] | English (a 40-locale multilingual variant was reported in Jun 2026, **UNVERIFIED**) [S27] | 80 ms–1.12 s chunks [S27] | NVIDIA GPUs | 6.93 % average WER at 1.12 s [S27] | Not needed (closed turns, not live captions) |
| **Vosk** (Kaldi) | small models ≈ 40–50 MB | Apache-2.0 [S24] | small EN 9.85 / FR 23.95 / DE 13.75 / NL 22.45 / PL 18.36 % WER (vendor) [S24] | Very fast; supports grammar-restricted recognition | – | Python package 0.3.45 is from **Dec 2022** [S24]. Old, weak on FR/NL | Fallback only, for closed vocabularies |
| **Kyutai STT** | 1 B (en_fr), 2.6 B (en) | MIT/Apache code; **CC-BY-4.0** weights [S25] | **EN + FR only** | GPU (PyTorch/Rust) or Apple MLX [S25] | yes; 0.5 s delay, semantic VAD [S25] | – | No: no NL/DE/PL |
| **Voxtral Mini 4B Realtime (2602)** | ≈4 B | Apache-2.0 [S26] | 13 languages incl. EN/FR/DE/NL, **no PL** [S26] | – | **≥16 GB GPU**, vLLM [S26] | 8.72 % average WER at 480 ms delay [S26] | Too heavy for a mid-range GPU |
| Qwen2.5-Omni / Gemma 4 E2B (audio input) | 3–7 B / 2.3 B effective | Apache-2.0 (Omni-7B, Gemma 4); **Qwen Research** licence for Omni-3B [S48, S75] | multilingual | – | Omni-7B needs **31 GB** VRAM for a 15 s video [S48] | LLM-style decoding, so hallucination risk | No (see §6) |

### 3.3 Multilingual operation (EN/FR/NL/DE/PL)

- **Force the language** from a visitor-facing flag button. Auto-LID on short answers was wrong in 14.6 % of clean *native-English adult* clips and cost 6 points of recall [LOCAL]. It also roughly doubled latency (§2). Children's single-word answers ("chien!") are the worst case for LID.
- **Belgian Dutch and French:** Whisper and Parakeet are trained mostly on standard varieties. Parakeet-v3 FLEURS WER is higher for NL (7.48 %) than for FR/DE (≈5 %) [S19]. Run a small booth test with Flemish and Brussels-French children before the fair (**UNVERIFIED** gap).
- Whisper `hotwords` / `initial_prompt` can bias decoding toward lexicon words [S12]. **Test before using:** biasing can raise false "heard *dog*" detections. The lexicon then turns a hallucination into a *wrong* slot value rather than a miss.

### 3.4 Child speech: what the literature says

| Study | Data | Finding |
|---|---|---|
| Fan et al., Interspeech 2024 [S29] | MyST (grades 3–5, ≈240 h), OGI Kids (K–10) | Zero-shot WER: Whisper-tiny 20.6/53.8, small 13.4/25.4, medium 13.1/20.8, large-v3 12.6/19.9; **Canary 9.5/18.2; Parakeet-RNNT 11.1/16.7** (MyST/OGI). Smaller Whisper models degrade sharply on younger children (OGI) |
| Kid-Whisper (Jain et al., AIES 2024) [S30] | MyST, CSLU Kids | Zero-shot WER on CSLU **spontaneous**: medium 37.0, large-v2 29.4 (vs LibriSpeech 2.8). Fine-tuning roughly halves it (16.5) |
| ESPnet child-ASR benchmark (2025) [S31] | MyST (8–10 y) + OGI/CMU Kids, split by age | Zero-shot Whisper-medium WER by age: **4–7 y 39.1 %, 8–10 y 13.5 %, 11–15 y 15.2 %**. Zero-shot Whisper was *worse* for 11–15 than for 8–10. Gains plateau above ≈1 B parameters |
| Dutch child speech (2026) [S32] | JASMIN (7–11 y, clean), DART (3rd grade, **noisy classroom**) | Best fine-tuned model: 5.5 % (clean) vs **70.4 % (noisy, mostly single words)**. Baselines are worse [verifier: confirmed (whisper-medium-FT, 5.46 % / 70.37 %). But DART children are third-graders *learning to read*, so the 70 % mixes noise with beginner reading disfluency. It is not a pure noise effect, and it overstates the difficulty for 8–14-year-olds answering a spoken question] |
| Gao et al., Interspeech 2024 [S33] | Dutch children reading | faster-whisper large-v2 9.8 % WER |

**Implication.** Our target group (8–14 years) is easier than ages 4–7. Still, expect 2–3× adult WER on single words in noise [verifier: this multiplier is an estimate, not taken from any cited source; **unverifiable**]. The design must (1) use a closed vocabulary, (2) ask questions with short, distinctive answers, (3) treat "didn't catch that" as a normal, friendly outcome, and (4) show ASR confidence, which is good XAI material anyway.

### 3.5 Noise and hallucinations in an exhibition hall

- **Speech levels at 1 m:** normal 58 dB, raised 64, loud 70, shouted 76 dB SPL [S78]. Sound drops **6 dB per doubling of distance** in free field [S79]. Assuming a hall background of **≈65–75 dB(A)** (**UNVERIFIED**; measure at a comparable event), a child speaking normally **1 m** from the robot's microphone is at **≈ −7 to −17 dB SNR**. That is far below the ≈5 dB where our pipeline fails (§2). At **10 cm** from a close-talk microphone the same voice gains about 20 dB.
- **Recommendation: do not rely on the robot dog's built-in microphone.** Use a **directional (cardioid/supercardioid) gooseneck or headset-style microphone** at a marked "talk here" spot, or a handheld "microphone prop" that children hold (they enjoy it). Mute it while the robot or its motors make noise. Products are **UNVERIFIED** (outside this track).
- **Whisper hallucinates on non-speech:** "roughly 1 % of transcriptions contained entire hallucinated phrases… 38 % of hallucinations include explicit harms", and hallucinations are more frequent for speakers with longer pauses [S36]. On 301k non-speech clips Whisper output text about 40 % of the time ("thank you", "thanks for watching"…). **Silero VAD pre-filtering plus a "bag of hallucinations" filter** brought WER down to 6.5–9.4 % (AGH Kraków) [S35]. On UrbanSound8K, Whisper-large-v3 hallucinated on **≈100 %** of non-speech clips vs **13.5 % for Conformer-CTC** [S37]. The Whisper paper itself names repeat loops and "complete hallucination" as stubborn failure modes. Under pub noise below 10 dB SNR, all models degrade quickly [S34].
- **Mitigations (all cheap):** VAD-gate before ASR; `condition_on_previous_text=False`; `beam_size=1`; `no_speech_threshold`/`log_prob_threshold` defaults; `hallucination_silence_threshold≈2`; reject segments whose words all have probability < 0.4; **never display raw transcripts on the public screen**, only lexicon hits. Another argument for Parakeet: its transducer architecture is less prone to free-running text.

---

## 4. (c) Non-sensitive prosodic and paralinguistic features in about 10 s windows

| Feature | How (tool, licence) | Compute in a 3–10 s answer window | Reliability notes | Show to visitor? |
|---|---|---|---|---|
| **Loudness** | RMS dBFS over **VAD-speech frames only** (numpy/librosa, ISC [S41]). Optionally LUFS via **pyloudnorm** (MIT, ITU-R BS.1770-4, 400 ms blocks) [S42] | Speech-frame RMS minus booth calibration (prototype default −26 dBFS); map to quiet/normal/loud with soft bins (prototype uses Gaussians at −8/0/+8 dB) | Depends on **mouth-to-mic distance** (−6 dB per doubling) [S79] and mic gain. A fixed talk spot plus calibration is essential. Our Lombard test gives AUROC 0.81–0.82, noise-robust [LOCAL] | **Yes**, as a live meter and "quiet/normal/loud", never "angry/shy" |
| **Voice activity duration / talk time** | Silero VAD [S1] | Sum of speech segments | Robust | Yes ("you talked for 4.2 s") |
| **Pause ratio** | VAD: 1 − speech / (last speech end − first speech start) | Needs ≥2 segments | Depends on the question type; children pause mid-answer | Yes, neutral ("short pauses") |
| **Turn count / response latency** | VAD time from robot prompt end to speech onset | – | Robust | Optional |
| **Speaking rate** | (a) words/s from ASR word timestamps; (b) syllable-nuclei detection (de Jong & Wempe Praat script via **parselmouth, GPL-3.0+** [S39]) | Needs ≥3 s of speech | ASR words/s is biased by misrecognitions, worse for children and L2 speakers. The prototype **deliberately does not judge** rate. Keep it that way | At most a neutral number |
| **Pitch contour (relative)** | **librosa.pyin** (ISC; returns f0, voiced flag, voiced probability; default fmin ≈65 Hz, fmax ≈2093 Hz) [S41]. **torchcrepe** (MIT; "tiny"/"full"; periodicity threshold 0.21 and 15 ms median filter suggested) [S40]. Praat/parselmouth (GPL) [S39] | For children set fmin 80, fmax 700 Hz, hop 10 ms; require ≥1.5 s of voiced frames. Report **semitone range (IQR)** relative to the speaker's own median | pyin 0.88 s per 10 s on our CPU (under load) [LOCAL]. Octave errors in noise. **Absolute F0 is a proxy for age/sex**, so never show Hz or "high/low voice" | Optional, as a "melody line" with no label |
| **eGeMAPS (88 functionals)** | openSMILE / `opensmile` 2.6.0 Python (Jul 2025) [S38] | ≈ real-time | **openSMILE licence: free for "teaching, academic research, public demonstrations"; commercial use needs an audEERING licence** [S37b]. The feature set is designed for emotion and health research | **No**: unnecessary, and it invites emotion inference |

**Robust 10 s recipe:** 16 kHz mono → Silero VAD mask → (i) speech RMS dB with 20 ms frames, 50th and 90th percentiles; (ii) SNR = speech dB − non-speech dB (prototype) → confidence weight; (iii) talk time and pause share; (iv) optional pyin on speech frames, discard if voiced < 1.5 s. Everything except pyin costs < 0.1 s on CPU [LOCAL].

---

## 5. Sound-event context (e)

| Model | Params / cost | AudioSet mAP | Licence | Notes |
|---|---|---|---|---|
| **EfficientAT** mn10_as / dymn04_as / mn40_as | 4.88 M / 0.54 G MACs; 1.97 M / 0.12 G; 68 M / 8 G | 47.1 / 45.0 / 48.4 | MIT [S52] | Best accuracy per FLOP; code from a GitHub repo (no pip package) [S52] |
| **PANNs** CNN14 | ≈80 M (**UNVERIFIED** count) | 43.1 | MIT; `pip install panns_inference` [S54] | Has frame-wise SED variants [S54] |
| **YAMNet** | 3.7 M weights, 69.2 M multiplies per 0.96 s frame | 0.306 (balanced mAP) | Apache-2.0 (tensorflow/models) [S53] | 16 kHz, TFLite; weakest but tiny [S53] |
| **AST** | 86.6 M | 45.9 | BSD-3-Clause [S55] | [LOCAL] 8.5 s per 10 s under load; GPU only |
| **BEATs** | ≈90 M (**UNVERIFIED**) | 50.6 (AS-2M, paper) | MIT (Microsoft unilm) [S56] | GPU |

All use the 527-class **AudioSet ontology**, which includes "Laughter", "Giggle", "Applause", "Clapping", "Cheering", "Crowd", "Chatter", "Hubbub, speech babble", "Music", "Singing", "Whispering", "Shout", "Yell", "Screaming", "Crying, sobbing", **and the person-attribute classes "Male speech, man speaking", "Female speech, woman speaking", "Child speech, kid speaking", "Child singing"** [S57]. **Hard-mask the person-attribute and distress classes** (screaming, crying) before anything reaches the UI or the fusion. Our AST run on adult speech already returned "Male speech, man speaking" in its top 5 [LOCAL].

**Recommended:** EfficientAT `mn10_as` (or `dymn04_as` on CPU) on 1 s hops over 2–3 s windows, allow-list = {Laughter, Giggle, Applause, Clapping, Cheering, Music, Singing, Whistling, Crowd/Hubbub}, display threshold ≥0.3 sustained over 2 windows. Latency is **UNVERIFIED on our CPU**: not measured, but at 0.12–0.54 G MACs it should be far below AST's cost.

---

## 6. (d) Audio-language embedding models as "concept scorers"

### 6.1 Candidates

| Model | Size | Licence | Availability | Fit |
|---|---|---|---|---|
| **LAION-CLAP** (630k-audioset, music_speech, larger_clap_general) | HTSAT + RoBERTa, ≈150–200 M (**UNVERIFIED**) | **CC0-1.0** (code) [S45] | `pip install laion-clap`; HF `ClapModel` [S45] | ESC-50 zero-shot ≈ 90 % [S45]; speech-trait prompts weak (§6.2) |
| **MS-CLAP 2022/2023** | HTSAT-22 + GPT-2 (2023) | **MIT** [S43] | `pip install msclap`; weights on Zenodo / HF [S43] | Best published zero-shot on vocal sounds (80 %) [S44] |
| **ParaCLAP** (Interspeech 2024) | w2v2-emo + BERT | **Licence not stated** in the repository [S47]; its audio backbone is audEERING w2v2-emo, which is CC-BY-NC-SA (**UNVERIFIED** for the exact checkpoint) | GitHub + HF checkpoint [S47] | Built *for* paralinguistics (emotion, gender, age), exactly the categories we must not infer |
| Whisper encoder embeddings | 39 M–1.5 B | MIT | via faster-whisper / transformers | No text side, so no zero-shot; would need a trained probe |
| AudioCLIP, Pengi | – | **UNVERIFIED** (not re-checked; both 2021–2023 research code) | GitHub | Superseded by CLAP |
| **Qwen2-Audio-7B-Instruct** | ≈8 B | Apache-2.0 [S49] | HF | Its own model-card demo outputs "female and in her twenties", i.e. it **volunteers age and gender** [S49] |
| **Qwen2.5-Omni-3B / 7B** | 3 B / 7 B LLM (more in total, with audio/vision encoders and speech "talker") | **qwen-research (3B)** / Apache-2.0 (7B) [S48] | HF | 18–31 GB VRAM for 15 s of video [S48]; does "vocal emotion recognition" [S48] |
| Qwen3-Omni-30B-A3B (+Captioner) | 30 B MoE, 3 B active | Apache-2.0 (from search summary, **UNVERIFIED** on the card) [S50] | HF | Far beyond a mid-range GPU |
| **SALMONN** 7B/13B | Vicuna-based | Apache-2.0 code; Vicuna/LLaMA terms on weights (**UNVERIFIED**) [S51] | GitHub | Research-grade, GPU |

### 6.2 Evidence on speech-related zero-shot classes

- **MS-CLAP 2023 zero-shot** [S44]: Vocal Sound (laughter, sigh, cough, throat-clearing, sneeze, sniff) **80.0 %**; ESC-50 93.9 %; GTZAN music-vs-speech 99.2 %; **CREMA-D emotion 30.0 %, RAVDESS emotion 31.5 %**; Speech Commands keyword spotting 16.4 %; LibriCount speaker counting 24.6 %.
- **Generic CLAP models perform poorly on paralinguistics.** The ParaCLAP and SLAP papers were written because generic CLAP fails there (SLAP reports 62.9 % vs CLAP 42.4 % average zero-shot F1, according to a search summary, **UNVERIFIED** in the paper itself) [S47].
- **CLAP embeddings do encode loudness and reverberation.** These are *linearly recoverable with trained probes*, and amplitude-invariant architectures discard loudness entirely. Text alignment was demonstrated only qualitatively, for RT60 [S46]. So "a loud voice" as a text prompt is not a calibrated loudness meter. **A dB meter is strictly better** for that concept.

### 6.3 Our zero-shot probe (LAION-CLAP, adult Lombard GRID)

TBD_CLAP [verifier: this section was never filled in. `bench_clap.py` exists, but `bench_clap.json` does not, and the CLAP part of `bench_audio.json` failed ("'BaseModelOutputWithPooling' object has no attribute 'norm'", a transformers 5 API change). So the claims elsewhere that rely on "our CLAP probe" (e.g. §7, "CLAP's 'a man speaking' prompt") have **no local evidence**.]

### 6.4 Verdict for (d)

- Use **CLAP only for scene-level, non-personal concepts** where it is known to work: laughter, applause, music, singing, crowd. Even there, a supervised AudioSet tagger (§5) is cheaper and calibrated per class.
- **Do not use text-prompt scoring for "child speaking", "a man/woman speaking", "angry", "excited"**. These are biometric categorisation or emotion inference by another name, and the zero-shot accuracy is poor.
- Prompt-based concepts make a nice **XAI teaching moment, offline**: a pre-recorded demo with actors showing "the AI's guess vs the truth" for *sounds* (clapping vs laughter), not for visitors' voices.
- Large audio-LLMs (Qwen-Omni, Qwen2-Audio, SALMONN) are too big for a mid-range GPU or CPU, have uneven licences, and **volunteer sensitive attributes** in free text [S49]. Exclude them.

---

## 7. (f) Speaker-characteristic models: age, gender, child-vs-adult, voiceprints

| Model | Licence | What it outputs | Reported accuracy | Children |
|---|---|---|---|---|
| audEERING `wav2vec2-large-robust-24-ft-age-gender` | **CC-BY-NC-SA-4.0** [S58] | Age (0–100 regression) plus **female / male / child** probabilities | "at least 91.1 % ACC for gender (female, male, child)"; age MAE **7.1–10.8 years** depending on dataset [S58b] | No child-only metric reported [S58b] |
| SpeechBrain ECAPA-TDNN `spkrec-ecapa-voxceleb` | Apache-2.0 | Speaker embedding (voiceprint) | EER 0.80 % on VoxCeleb1 [S59] | – |
| `bookbot/wav2vec2-adult-child-cls` | **UNVERIFIED** licence | adult vs child | 95.8 % accuracy (model card, via search summary) [S60] | Training data and age ranges **UNVERIFIED** |
| Layer-wise wav2vec2 analysis (WOCCI 2025) | – | Age / gender classification of children | CMU Kids: age 97.1 %, gender 98.2 %; PFSTAR (base-100h): 86.1 % / 95.0 %, in-domain [S31b] | In-domain lab data; ages 4–7 harder [S31] |

**Ethics and law (flag only; see `09-ethics-law.md`):**
- Age and sex are listed in AI Act **recital 16** as biometric-categorisation categories. Any such classifier triggers the **Art. 50(3)** information duty, which also applies to children, and brings fairness and accuracy duties [S64; 09-ethics-law.md §4.4–4.5].
- A **voiceprint** (ECAPA embedding) used to recognise a returning visitor is biometric data processed for unique identification, a **GDPR Art. 9** special category [S65]. **Do not compute one, even transiently.**
- **"Child vs adult voice" is not defensible as a live feature.** (1) Accuracy is weakest exactly where our audience is. Pubertal voice change in the early teens and the overlap between teens and adult women are the hard cases. No published child-only metric exists for the off-the-shelf audEERING model [S58b], so its performance on 12–14-year-olds is **UNVERIFIED**. The published high accuracies come from in-domain clean lab corpora [S31b]. (2) A wrong "you sound like a little child" hurts a 13-year-old. (3) It adds no teaching value beyond a *pre-recorded* demonstration. **If the team wants to teach that "AI can guess your age from your voice and is often wrong", do it with consenting actors' recordings, not live visitors.**
- Our AST and CLAP runs show that **general-purpose models emit these attributes unasked** ("Male speech, man speaking" in the AST top 5; CLAP's "a man speaking" prompt) [corrected by verifier: the AST result is confirmed in `bench_audio.json` (0.208, 4th place). The CLAP result has no local output file (see §6.3), so it is **unverifiable**]. Allow-listing is mandatory.

---

## 8. (g) Speech emotion recognition: flag, do not build

| Model | Licence | Output |
|---|---|---|
| emotion2vec+ large (≈300 M) | "Model-license" (custom; read before any use) [S62] | 9 classes: angry, disgusted, fearful, happy, neutral, other, sad, surprised, unknown [S62] |
| audEERING `wav2vec2-large-robust-12-ft-emotion-msp-dim` | **CC-BY-NC-SA-4.0** [S63] | Arousal / dominance / valence (0–1) [S63] |
| Generic CLAP (zero-shot) | – | 30–31.5 % on CREMA-D/RAVDESS [S44] |

**Legal flags (not resolved here):**
- **AI Act Art. 5(1)(f)** prohibits "the use of AI systems to infer emotions of a natural person in the areas of workplace and education institutions, except where … intended … for medical or safety reasons" [S64]. Whether a science fair visited by school groups falls in "education institutions" is open. Our ethics report notes the Commission reads "workplace" broadly, covering staff and volunteers at temporary sites [09-ethics-law.md §4.3].
- **Recital 18:** emotion recognition "does not include the mere detection of readily apparent expressions, gestures or movements, unless they are used for identifying or inferring emotions", with voice examples "a raised voice or whispering" [S64]. So the **loudness meter is fine**, and "you sound angry/excited" is not.
- **Art. 50(3)** notice duty for any emotion recognition or biometric categorisation (applies from 2 Aug 2026, unchanged by the Digital Omnibus) [09-ethics-law.md].
- **Laughter detection** is a *sound event*. Phrase it as "I heard laughter nearby", never "you are happy". Whether attributing laughter to the specific visitor drifts into emotion inference is **a question for the ethics advisor**.

---

## 9. (h) Offline TTS for the robot voice

### 9.1 Options

| Engine | Licence | Languages we need (EN/FR/NL/DE/PL) | Speed | Verdict |
|---|---|---|---|---|
| **Piper** (`piper-tts` 1.8.0, 4 Sep 2026; repo OHF-Voice/piper1-gpl) | **Code GPL-3.0-or-later** [S66]. Fine for an exhibit we run ourselves; GPL obligations attach to distribution. Voices are MIT-packaged, but **each voice inherits its dataset licence** (see the MODEL_CARD) [S66b] | **All five**: en_US/en_GB, fr_FR, nl_BE/nl_NL, de_DE, pl_PL; quality x_low/low/medium/high [S66b] | Medium voices (63 MB VITS) [LOCAL, §9.2]. On a Raspberry Pi 4, medium voices take ≈1–3 s per sentence; a Pi 5 is real-time (secondary source) [S67] | **Recommended** (with a careful voice choice) |
| **sherpa-onnx** (1.13.8, Sep 2026) | Apache-2.0 [S23] | Runs Piper and Kokoro voice models without the GPL Piper code [S23] | similar | Alternative runtime; also does ASR, VAD and KWS |
| **Kokoro-82M** | Apache-2.0 [S68] | EN (US/UK), ES, **FR (1 voice, <11 h of data, grade B-)**, HI, IT, JA, PT-BR, ZH. **No DE/NL/PL** [S68b] | Fast (82 M) | English and French only, so insufficient alone [verifier: the French voice `ff_siwis` is trained on SIWIS (CC BY 4.0), so it needs attribution. The model card also says the training data includes "synthetic audio from closed commercial TTS systems"] |
| **Coqui XTTS-v2** | **Coqui Public Model License: non-commercial only**; Coqui shut down Jan 2024; code fork by Idiap (MPL-2.0) [S69] | 17 languages incl. PL/NL/FR/DE [S69] | GPU preferred | **Avoid**: licence ambiguity, and **voice cloning** (never clone visitors or staff) |
| **MeloTTS** | MIT [S70] | EN, ES, FR, ZH, JA, KO. **No DE/NL/PL** [S70] | "Fast enough for CPU real-time" [S70] | Insufficient |
| **Windows SAPI 5** (pyttsx3 2.99, MPL-2.0) | Part of Windows [S71] | Standard voices: EN (David/Mark/Zira), FR-FR (Paul/Hortence/Julie), DE (Stefan/Hedda/Katja), **PL (Adam/Paulina)**, **NL (Frank)**. "Natural" voices exist for EN/FR/DE, but **only inside Narrator, not via SAPI**; third-party adapters broke with recent voice versions [S71] | Instant | Zero-install emergency fallback; robotic sound (fine for a robot) |

**Piper voice licences we checked (MODEL_CARD "Dataset licence", Oct 2026)** [S66b]:

| Use ✔ | Avoid ✘ |
|---|---|
| `nl_BE-nathalie` **CC0**, `nl_NL-pim`/`ronnie` CC0, `de_DE-thorsten` **CC0**, `pl_PL-gosia` **CC0**, `pl_PL-darkman`/`mc_speech` CC0, `fr_FR-siwis` **CC-BY-4.0**, `fr_FR-upmc` CC-BY-SA-4.0, `en_GB-alba` **CC-BY-4.0**, `en_US-joe` CC0, `en_US-ljspeech`/`kristin` public domain, `en_GB-northern_english_male` CC-BY-SA-4.0 | `en_US-lessac` (Blizzard 2013 licence: research only, "excludes … any commercial purpose"; the most popular default voice!) [S66c], `en_US-ryan`, `en_US-hfc_female`/`hfc_male` (**CC BY-NC-SA 4.0**), `fr_FR-tom` (**AGPLv3**) |

[corrected by verifier: the "Use ✔" column judges each voice only by its *fine-tuning* dataset. The MODEL_CARDs of `nl_BE-nathalie`, `de_DE-thorsten` (medium and high), `pl_PL-gosia`, `pl_PL-darkman`, `fr_FR-siwis`, `en_GB-alba`, `en_US-joe` and `en_US-libritts_r` all say **"Finetuned from U.S. English lessac voice"**, and `en_US-hfc_female` does as well. The Blizzard licence restricts the data to "Research Purposes" and says nothing explicit about derived models [S66c]. That leaves an unresolved provenance question, and a public exhibit is not research. Voices **trained from scratch** (no lessac parent) per their MODEL_CARDs: `nl_NL-mls-medium`, `fr_FR-mls-medium`, `de_DE-mls-medium` (CC-BY-4.0, multi-speaker MLS; credit them) and `en_US-ljspeech-medium` (public domain). For Polish, none was found: `pl_PL-mls_6892-low` is fine-tuned from `en_US-ryan` (CC BY-NC-SA). The Polish fallback is Windows SAPI (Paulina/Adam), or accepting the gosia/darkman risk after legal review. `nl_NL-pim`/`ronnie`, `fr_FR-upmc`, `en_GB-northern_english_male` and `en_US-kristin` were **not re-checked** by the verifier.]

### 9.2 Piper speed on our CPU

[LOCAL] piper-tts 1.8.0 Python API (`PiperVoice.synthesize_wav`), medium voices (63 MB ONNX each), one sentence per language, median of 3 runs after warm-up, **machine under 100 % concurrent load**. [verifier: **unverifiable**. `research/04-audio-bench/` contains `bench_piper.py`, but no `bench_piper.json`, and no `voices/` folder. The README promises both. Treat the table below as unbacked until the script is re-run and its output saved.]

| Voice (dataset licence) | Load | Synthesis | Audio length | RTF |
|---|---|---|---|---|
| en_US-lessac-medium (research-only; **avoid**) | 8.5 s | 1.53 s | 4.69 s | 0.33 |
| fr_FR-siwis-medium (CC-BY-4.0) | 7.4 s | 1.27 s | 4.47 s | 0.28 |
| nl_BE-nathalie-medium (CC0) | 7.6 s | 1.01 s | 3.55 s | 0.29 |
| de_DE-thorsten-medium (CC0) | 8.1 s | 1.06 s | 4.55 s | 0.23 |
| pl_PL-gosia-medium (CC0) | 8.3 s | 1.00 s | 4.63 s | 0.22 |

So a sentence takes about 1–1.5 s before playback can start, when the whole sentence is synthesised first. That is acceptable but noticeable, and it is another reason to **pre-render**. Load voices once at start-up; 5 voices ≈ 320 MB on disk.

**Recommendation:** the dialogue is scripted, so **pre-render every robot line in all 5 languages to WAV at build time**. Use Piper only for the few dynamic fragments ("I heard *chien*"), or pre-render those too: the lexicon is closed, so it is a finite set. TTS then adds zero runtime risk and its latency becomes irrelevant. Add an Art. 50 disclosure that the voice is synthetic (see `09-ethics-law.md`).

---

## 10. (i) Small local LLMs vs deterministic extraction

### 10.1 Licence and language check (Oct 2026)

| Model | Params | Licence | EU/PL/NL notes |
|---|---|---|---|
| **Qwen3** 0.6B / 1.7B / 4B (Apr–May 2025; 4B-Instruct-2507) | 1.7 B (1.4 B non-embedding) | **Apache-2.0** [S72] | "100+ languages"; thinking mode switchable, so **disable it** (`enable_thinking=False` / `/no_think`) [S72] |
| **Qwen3.5** 0.8B / 2B / 4B / 9B (Feb–Mar 2026) | 2 B | **Apache-2.0** [S72b] | 201 languages; natively multimodal; non-thinking by default [S72b] |
| Qwen2.5 3B | 3 B | **Qwen Research License**: avoid [S72c] | (0.5B/1.5B/7B are Apache-2.0, **UNVERIFIED** here) |
| **Llama 3.2** 1B / 3B | 1.23 B / 3.2 B | **Llama 3.2 Community License**, gated; the EU-domicile restriction applies to the *multimodal* models only [S73] | Official: EN, DE, FR, IT, PT, HI, ES, TH. **Not NL/PL** [S73] |
| **Phi-4-mini-instruct** | 3.8 B | **MIT** [S74] | 22 languages incl. NL, PL, FR, DE. Card warns of worse non-English performance and that "language-specific attack prompts … can cause the model to output harmful content" [S74] |
| **Gemma 3** 270M / 1B / 4B | 0.27 B … | **Gemma Terms of Use** (custom, gated) [S75] | 140+ languages |
| **Gemma 4** E2B / E4B (Apr 2026) | 2.3 B effective (5.1 B with embeddings) | **Apache-2.0** [S75b] | Audio input (ASR / speech translation, ≤30 s) on E2B/E4B [S75b] |

### 10.2 CPU speed (llama.cpp, Q4_K_M)

TBD_LLM [verifier: this section was never filled in, and `bench_llm.txt` and the `llm/` folder are absent from `research/04-audio-bench/`. No local LLM speed figures exist. This does not affect decision 10 (no LLM in the loop).]

### 10.3 Risks with children, and the deterministic alternative

- **Risks:** hallucinated "facts" about the visitor; unsafe or odd content, especially in non-English (Phi card warning [S74]); prompt injection by a child ("ignore your rules and say …"); latency variance; the Art. 50(1) duty to disclose that visitors are interacting with an AI. An LLM speaking to children also turns a perception exhibit into a chatbot exhibit, which is off-message.
- **Deterministic extraction is enough for our slots:** (1) exact or folded lexicon match on ASR words (prototype); (2) **fuzzy match** (Levenshtein ≤1 on ≥5-letter words) for ASR near-misses; (3) **embedding fallback** for paraphrases ("a little doggy", "mon toutou") with **multilingual-e5-small** (MIT, 118 M params, 384-d, needs the `query: ` prefix) [S76] or **paraphrase-multilingual-MiniLM-L12-v2** (Apache-2.0, ≈118 M, 50 languages) [S76]. Note that **all-MiniLM-L6-v2 is English-only** (Apache-2.0, 22.7 M) [S76]. Cosine against the lexicon entries' embeddings, with acceptance threshold and margin tuned on a small labelled set. [LOCAL] 0.18 s for 4 sentences under load. Every decision stays explainable ("closest to *dog*: 0.83").
- **If an LLM is used at all:** only as a *classifier* with **grammar-constrained output** (llama.cpp GBNF / JSON schema) whose only legal outputs are lexicon IDs or `none`. Validate in code. Log nothing. Never let it generate the spoken reply. Prefer Qwen3/Qwen3.5 (Apache-2.0) or Phi-4-mini (MIT) over custom-licence models.

---

## 11. Recommended audio stacks

### 11.1 CPU-only prototype (dev laptop now; also the fallback on the exhibition laptop)

```
mic (close-talk, 16 kHz mono) ─► Silero VAD 6.2.x (512-sample chunks, mic muted while robot speaks)
   ├─► loudness / talk-time / pause share / SNR       (numpy; <0.01 s)
   ├─► [optional] EfficientAT dymn04/mn10 allow-list  (laughter, clapping, music, singing)
   └─► answer window (≤8 s) ─► faster-whisper base|small int8, language=<flag button>,
                               beam 1, word_timestamps, vad_filter, condition_on_previous_text=False
                               (A/B: Parakeet-TDT-0.6B-v3 int8 via onnx-asr)
                          ─► closed lexicon (+fuzzy, +me5-small fallback) ─► slot + confidence + evidence
robot voice: pre-rendered Piper WAVs (CC0/CC-BY voices); Windows SAPI as emergency fallback
no LLM, no age/gender/emotion/speaker models
```

- Latency budget on this CPU (under load): VAD 0.1 s + ASR base 1.2 s or small ≈2.4–4.3 s + lexicon <0.05 s. [verifier: for a *short* answer the small-model cost does not shrink much, because of Whisper's 30 s padding: 2.28 s per ~2.5 s GRID utterance clean, 2.9–4.9 s in babble, and 6.0 s with auto-LID [LOCAL: `audio_grid.json`]. Budget ≈2.3–5 s per answer for `small`, regardless of answer length.] Fill the gap with a robot "thinking" animation, which is honest XAI ("I'm working out what I heard").
- Threads: give ASR 4–6 threads (`cpu_threads`) so vision keeps its share. Measure with everything running.

### 11.2 Exhibition laptop with a mid-range NVIDIA GPU (e.g. 8 GB laptop RTX class)

- **ASR:** faster-whisper **large-v3-turbo**, `compute_type="float16"` or `"int8_float16"`, language forced. Turbo needs ≈6 GB VRAM in the reference implementation; CTranslate2 int8 needs less [S10, S12]. **Or Parakeet-TDT-0.6B-v3 / Canary-1B-v2** on CUDA (onnx-asr: Parakeet 57 RTFx even on an old T4 [S21]). Pick the winner on **recordings of real children at a booth**, not on benchmarks. Per-utterance latency on a mid-range GPU is **UNVERIFIED** (expected well under 1 s for 10 s of audio, based on [S12, S21]).
- **Keep the CPU path hot** (base/Parakeet int8) and fall back automatically if CUDA errors or VRAM contention appear (vision and image generation share the GPU; see `05`/`06`).
- Optional on the GPU: AST/BEATs for richer scene tags (allow-listed). **Still no LLM, emotion or speaker models.**
- Not recommended even with a GPU: Voxtral Realtime (≥16 GB) [S26], Qwen-Omni (18–31 GB) [S48], Kyutai (EN/FR only) [S25].

---

## 12. Recommendations for our demonstrator

1. **Keep the prototype's architecture** (VAD → forced-language ASR → closed lexicon → loudness/SNR). It is the right one for feasibility, robustness and explainability.
2. **Add a language-flag button**, pass `language=` to ASR, and remove auto-LID from the default path [LOCAL evidence].
3. **Run an A/B test of faster-whisper small vs Parakeet-TDT-0.6B-v3** on 30–50 consented child recordings in EN/FR/NL (plus a few PL/DE), recorded **at the booth microphone in hall-like noise**. Report lexicon hit / miss / wrong per language. This is a 1–2 day task and the single most informative experiment for the audio track.
4. **Hardware first:** a directional close-talk microphone at a marked spot, an on-screen SNR indicator, and the mic muted during robot speech and motor movement. Measure hall noise at a comparable fair.
5. **Design questions for ASR:** short, distinctive, closed-set answers ("dog / cat / horse…", colours). Prefer words that are acoustically distinct across the five languages, and avoid homophones (e.g. EN "chat" vs FR "chat"). The prototype handles that by matching per detected language.
6. **Show uncertainty honestly:** per-word ASR probability, SNR-based quality, and "I didn't catch that" as a first-class outcome. Display lexicon hits, not raw transcripts.
7. **Loudness as the flagship paralinguistic feature:** calibrate per booth (play a reference tone or speak at a fixed SPL), fix the talking distance, and display relative dB with three soft bins.
8. **Scene sounds (optional, adds wonder):** an EfficientAT allow-list for laughter, clapping, music and singing, framed as "what's happening around us".
9. **Robot voice:** pre-rendered Piper CC0/CC-BY voices; credit the CC-BY voices (fr_FR-siwis, en_GB-alba) on the attribution panel; keep a SAPI fallback. [corrected by verifier: these voices are fine-tuned from lessac (see §9.1). Prefer the from-scratch `*-mls-medium` voices (NL/FR/DE, CC-BY-4.0, credit required) and `en_US-ljspeech`, and resolve Polish with the legal advisor.]
10. **Licence hygiene:** list every model's licence on the exhibit's "credits" screen. Parakeet/Canary (CC-BY-4.0) need attribution, Piper code is GPL-3.0 (keep the source available if we ever distribute the software), and the openSMILE research licence is not needed.
11. **Document the exclusions** (age, gender, child-vs-adult, emotion, voiceprint) in the DPIA, with the AudioSet mask list, as "privacy by design" evidence.

---

## 13. Pitfalls / what not to do

- **Do not use the robot dog's onboard microphone** as the primary ear in a hall: distance, motor noise and fan noise push SNR far below the ≈5 dB where recognition collapses [LOCAL; S78, S79].
- **Do not run Whisper on non-speech or long silences.** Without VAD gating it invents text ("thank you", "thanks for watching", sometimes harmful phrases) [S35, S36, S37]. Never display raw transcripts.
- **Do not trust auto language-ID on short child utterances.** Force the language.
- **Do not pick `medium`/`turbo` on CPU**: RTF > 1 on this laptop [LOCAL].
- **Do not use distil-whisper or Moonshine** for a multilingual Brussels exhibit (English-only, or no FR/NL/DE/PL) [S15, S16].
- **Do not trust zero-shot CLAP for person-level concepts** ("a child speaking", "an angry voice"). Accuracy is poor [S44], and it is biometric categorisation or emotion inference anyway.
- **Do not let general taggers leak attributes:** mask the AudioSet "Male / Female / Child speech", "Child singing", "Screaming", "Crying" classes.
- **Do not show absolute pitch or "high/low voice"**: it is an age/sex proxy.
- **Do not build speaker embeddings** for "welcome back!" re-identification (GDPR Art. 9 biometric identification).
- **Do not use `en_US-lessac`, `ryan`, `hfc_*` or `fr_FR-tom` Piper voices**, nor XTTS-v2, nor any voice cloning [S66c, S69]. [corrected by verifier: most "clean" Piper voices are fine-tuned from lessac too; see §9.1.]
- **Do not use non-commercial models without checking** whether SiW/MSCA outreach counts as non-commercial: audEERING CC-BY-NC-SA, the openSMILE research licence, the Qwen Research licence. Avoiding them is simpler.
- **Do not put a generative LLM between children and the speaker.**
- **Do not freeze latency numbers measured on a busy dev laptop.** Re-benchmark on the exhibition machine with vision running.

---

## 14. Open / UNVERIFIED items

- Real hall noise level at SiW 2027 (assumed 65–75 dB(A)).
- Parakeet-v3 and Whisper accuracy on **Flemish / Brussels-French children aged 8–14** (no published benchmark found).
- Per-utterance GPU latency of turbo / Parakeet on the actual exhibition GPU.
- Whisper via OpenVINO on the Intel iGPU/NPU of the dev laptop (not tested).
- EfficientAT and YAMNet CPU latency on our laptop (not measured).
- ParaCLAP, AudioCLIP, Pengi and SALMONN weight licences (not confirmed).
- `bookbot/wav2vec2-adult-child-cls` licence and data (search summary only); SLAP numbers (search summary only).
- Nemotron multilingual streaming variant (mentioned on the model card, not inspected).
- Piper Raspberry Pi timing (secondary source).

---

## Sources

All accessed 2026-10-01/02.

**Local evidence**
- [LOCAL] `research/04-audio-bench/` (bench_audio.py / .json, bench_clap.py / .json, bench_piper.py / .json, bench_llm.txt). Earlier team runs: `prototype/experiments/results/audio_grid.json`, `scratch/bench_models.json`. Prototype code: `prototype/robotsees/perception/audio.py`, `lexicon.py`.

**VAD**
- [S1] Silero VAD repository (MIT, ≈2 MB, <1 ms per chunk, 8/16 kHz): https://github.com/snakers4/silero-vad
- [S2] Silero VAD releases (v6.0 26 Aug 2025; v6.2 "child voices" 6 Nov 2025; v6.2.1–6.2.3 2026): https://github.com/snakers4/silero-vad/releases ; v6.0 discussion: https://github.com/snakers4/silero-vad/discussions/678
- [S3] silero-vad on PyPI (6.2.3, 23 Sep 2026, MIT): https://pypi.org/project/silero-vad/
- [S4] Silero VAD quality metrics (ROC-AUC table incl. WebRTC, TEN, FireRed): https://github.com/snakers4/silero-vad/wiki/Quality-Metrics
- [S6] webrtcvad-wheels on PyPI: https://pypi.org/project/webrtcvad-wheels/
- [S7] TEN VAD model card: https://huggingface.co/TEN-framework/ten-vad
- [S8] pyannote/segmentation-3.0: https://huggingface.co/pyannote/segmentation-3.0
- [S9] pyannote.audio on PyPI (4.0.7, 30 Jun 2026): https://pypi.org/project/pyannote.audio/

**ASR**
- [S10] OpenAI Whisper repository (sizes, VRAM, relative speed, MIT): https://github.com/openai/whisper
- [S11] whisper-large-v3-turbo model card (809 M, 4 decoder layers, 99 languages, MIT): https://huggingface.co/openai/whisper-large-v3-turbo
- [S12] faster-whisper repository (benchmarks, VAD filter, options): https://github.com/SYSTRAN/faster-whisper
- [S13] faster-whisper on PyPI (1.2.1, 31 Oct 2025): https://pypi.org/project/faster-whisper/
- [S14] whisper.cpp repository and releases: https://github.com/ggml-org/whisper.cpp , https://github.com/ggml-org/whisper.cpp/releases
- [S15] distil-whisper/distil-large-v3.5 model card: https://huggingface.co/distil-whisper/distil-large-v3.5
- [S16] Moonshine repository (licence statement, platforms): https://github.com/moonshine-ai/moonshine
- [S17] Moonshine v2 paper (Table 2 latency on an M3, WER): https://arxiv.org/html/2602.12241
- [S18] STT Index Moonshine entry (English + 7 languages): https://speechtotext.dev/model/moonshine/
- [S19] NVIDIA Parakeet-TDT-0.6B-v3 model card: https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3
- [S20] NVIDIA Canary-1B-v2 model card: https://huggingface.co/nvidia/canary-1b-v2
- [S21] onnx-asr repository (CPU/GPU RTFx benchmarks, MIT): https://github.com/istupakov/onnx-asr
- [S23] sherpa-onnx on PyPI (1.13.8, Apache-2.0): https://pypi.org/project/sherpa-onnx/
- [S24] Vosk models list and PyPI: https://alphacephei.com/vosk/models , https://pypi.org/project/vosk/
- [S25] Kyutai delayed-streams-modeling (STT 1B en_fr, 2.6B en): https://github.com/kyutai-labs/delayed-streams-modeling
- [S26] Voxtral-Mini-4B-Realtime-2602 model card: https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602
- [S27] NVIDIA Nemotron Speech Streaming EN 0.6B model card: https://huggingface.co/nvidia/nemotron-speech-streaming-en-0.6b
- [S80] OpenVINO GenAI speech recognition docs: https://openvinotoolkit.github.io/openvino.genai/docs/use-cases/speech-recognition/

**Child speech, noise, hallucination**
- [S29] Fan et al., "Benchmarking Children's ASR with Supervised and Self-supervised Speech Foundation Models", Interspeech 2024 (Table 2): https://arxiv.org/html/2406.10507
- [S30] Jain et al., "Kid-Whisper", AIES 2024: https://arxiv.org/html/2309.07927
- [S31] "Benchmarking Training Paradigms, Dataset Composition, and Model Scaling for Child ASR in ESPnet" (2025): https://arxiv.org/html/2508.16576
- [S31b] "Layer-Wise Analysis of Self-Supervised Representations for Age and Gender Classification in Children's Speech", WOCCI 2025: https://arxiv.org/abs/2508.10332
- [S32] "Transcribing Children's Speech: ASR Performance and Obtaining Reliable Orthographic Transcriptions" (JASMIN, DART; 2026): https://arxiv.org/html/2605.28833v1
- [S33] Gao et al., "Reading Miscue Detection in Primary School through ASR", Interspeech 2024: https://arxiv.org/abs/2406.07060
- [S34] Radford et al., Whisper paper (noise robustness §3.7, failure modes §6): https://ar5iv.labs.arxiv.org/html/2212.04356
- [S35] "Investigation of Whisper ASR Hallucinations Induced by Non-Speech Audio" (AGH Kraków, 2025): https://arxiv.org/html/2501.11378v1
- [S36] Koenecke et al., "Careless Whisper: Speech-to-Text Hallucination Harms", FAccT 2024: https://talkbank.org/aphasia/publications/2024/Koenecke24.pdf (DOI 10.1145/3630106.3658996)
- [S37] "Calm-Whisper: Reduce Whisper Hallucination on Non-Speech" (Interspeech 2025; UrbanSound8K): https://arxiv.org/html/2505.12969v1
- [S78] DPA Microphones, "Facts about speech intelligibility" (speech levels at 1 m: 58/64/70/76 dB): https://www.dpamicrophones.com/mic-university/background-knowledge/facts-about-speech-intelligibility/
- [S79] Engineering ToolBox, inverse-square law (−6 dB per doubling of distance): https://www.engineeringtoolbox.com/inverse-square-law-d_890.html

**Prosody**
- [S37b] openSMILE licence (non-commercial; "teaching, academic research, public demonstrations"): https://github.com/audeering/opensmile/blob/master/LICENSE
- [S38] opensmile on PyPI (2.6.0, 31 Jul 2025): https://pypi.org/project/opensmile/
- [S39] praat-parselmouth on PyPI (0.4.7, GPL-3.0+): https://pypi.org/project/praat-parselmouth/
- [S40] torchcrepe repository (MIT): https://github.com/maxrmorrison/torchcrepe
- [S41] librosa.pyin docs and librosa on PyPI (1.0.0, 11 Aug 2026, ISC, Python ≥3.12): https://librosa.org/doc/main/api/generated/librosa.pyin.html , https://pypi.org/project/librosa/
- [S42] pyloudnorm repository (MIT, BS.1770-4): https://github.com/csteinmetz1/pyloudnorm

**Audio-language models and sound events**
- [S43] Microsoft CLAP repository (MIT, msclap): https://github.com/microsoft/CLAP
- [S44] Elizalde et al., "Natural Language Supervision for General-Purpose Audio Representations" (MS-CLAP 2023, Table 2): https://arxiv.org/html/2309.05767v2
- [S45] LAION-CLAP repository (CC0-1.0): https://github.com/LAION-AI/CLAP
- [S46] Martel et al., "Probing Low-Level Acoustic Attribute Encoding in CLAP Audio Embeddings", DAFx26: https://arxiv.org/pdf/2607.03806
- [S47] ParaCLAP repository and paper: https://github.com/KeiKinn/ParaCLAP , https://www.isca-archive.org/interspeech_2024/jing24b_interspeech.pdf
- [S48] Qwen2.5-Omni-3B (qwen-research) and -7B (Apache-2.0 LICENSE): https://huggingface.co/Qwen/Qwen2.5-Omni-3B , https://huggingface.co/Qwen/Qwen2.5-Omni-7B , https://huggingface.co/Qwen/Qwen2.5-Omni-7B/blob/main/LICENSE
- [S49] Qwen2-Audio-7B-Instruct: https://huggingface.co/Qwen/Qwen2-Audio-7B-Instruct
- [S50] Qwen3-Omni-30B-A3B-Captioner: https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Captioner
- [S51] SALMONN repository: https://github.com/bytedance/SALMONN
- [S52] EfficientAT repository (MIT; mn/dymn mAP table): https://github.com/fschmid56/EfficientAT
- [S53] YAMNet (tensorflow/models): https://github.com/tensorflow/models/tree/master/research/audioset/yamnet
- [S54] PANNs repository (MIT; CNN14 mAP 0.431): https://github.com/qiuqiangkong/audioset_tagging_cnn
- [S55] AST AudioSet model card (BSD-3, 86.6 M): https://huggingface.co/MIT/ast-finetuned-audioset-10-10-0.4593
- [S56] BEATs paper and code: https://arxiv.org/abs/2212.09058 , https://github.com/microsoft/unilm/tree/master/beats
- [S57] AudioSet ontology (632 nodes incl. person-attribute speech classes): https://github.com/audioset/ontology

**Speaker traits, emotion, law**
- [S58] audeering/wav2vec2-large-robust-24-ft-age-gender (CC-BY-NC-SA-4.0): https://huggingface.co/audeering/wav2vec2-large-robust-24-ft-age-gender
- [S58b] Burkhardt et al., "Speech-based Age and Gender Prediction with Transformers" (2023): https://arxiv.org/abs/2306.16962
- [S59] speechbrain/spkrec-ecapa-voxceleb: https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb
- [S60] bookbot/wav2vec2-adult-child-cls (seen in search results only): https://huggingface.co/bookbot/wav2vec2-adult-child-cls
- [S62] emotion2vec+ large: https://huggingface.co/emotion2vec/emotion2vec_plus_large
- [S63] audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim (CC-BY-NC-SA-4.0): https://huggingface.co/audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim
- [S64] EU AI Act, Reg. (EU) 2024/1689: Art. 5 https://artificialintelligenceact.eu/article/5/ ; Recital 18 https://artificialintelligenceact.eu/recital/18/ ; official text https://eur-lex.europa.eu/eli/reg/2024/1689/oj
- [S65] GDPR Art. 9(1) ("biometric data for the purpose of uniquely identifying a natural person"): https://gdpr-info.eu/art-9-gdpr/
- Project ethics/legal analysis: `research/09-ethics-law.md` (Art. 5(1)(f), Art. 50(3), Digital Omnibus timeline).

**TTS**
- [S66] Piper (OHF-Voice/piper1-gpl, GPL-3.0) and piper-tts on PyPI (1.8.0, 4 Sep 2026): https://github.com/OHF-Voice/piper1-gpl , https://pypi.org/project/piper-tts/
- [S66b] rhasspy/piper-voices (per-voice MODEL_CARD dataset licences): https://huggingface.co/rhasspy/piper-voices
- [S66c] Lessac / Blizzard 2013 data licence: https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html
- [S67] Secondary: Piper on Raspberry Pi 4/5 timing: https://www.promptquorum.com/power-local-llm/best-local-tts-raspberry-pi
- [S68] Kokoro-82M model card and VOICES.md: https://huggingface.co/hexgrad/Kokoro-82M , https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md
- [S69] Coqui XTTS-v2 card and CPML licence; Idiap fork: https://huggingface.co/coqui/XTTS-v2 , https://huggingface.co/coqui/XTTS-v2/blob/main/LICENSE.txt , https://github.com/idiap/coqui-ai-TTS , https://github.com/coqui-ai/TTS/discussions/4145
- [S70] MeloTTS repository (MIT): https://github.com/myshell-ai/MeloTTS
- [S71] Windows TTS voices; pyttsx3; NaturalVoiceSAPIAdapter: https://support.microsoft.com/en-us/windows/appendix-a-supported-languages-and-voices-4486e345-7730-53da-fcfe-55cc64300f01 , https://pypi.org/project/pyttsx3/ , https://github.com/gexgd0419/NaturalVoiceSAPIAdapter

**LLMs and embeddings**
- [S72] Qwen3-1.7B (Apache-2.0): https://huggingface.co/Qwen/Qwen3-1.7B
- [S72b] Qwen3.5-2B (Apache-2.0): https://huggingface.co/Qwen/Qwen3.5-2B
- [S72c] Qwen2.5-3B-Instruct (Qwen Research License): https://huggingface.co/Qwen/Qwen2.5-3B-Instruct
- [S73] Llama-3.2-1B-Instruct (Llama 3.2 Community License): https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct
- [S74] Phi-4-mini-instruct (MIT): https://huggingface.co/microsoft/Phi-4-mini-instruct
- [S75] Gemma 3 270M (Gemma Terms of Use): https://huggingface.co/google/gemma-3-270m
- [S75b] Gemma 4 E2B-it (Apache-2.0, audio input): https://huggingface.co/google/gemma-4-E2B-it
- [S76] Sentence embedding models: https://huggingface.co/intfloat/multilingual-e5-small (MIT, 117.7 M params via HF API) , https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 , https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- [S77] llama.cpp releases (build b11327, 1 Oct 2026, Windows CPU x64 binary used): https://github.com/ggml-org/llama.cpp/releases ; GGUFs used: https://huggingface.co/unsloth/gemma-3-1b-it-GGUF , https://huggingface.co/unsloth/Qwen3-1.7B-GGUF , https://huggingface.co/unsloth/Qwen3.5-2B-GGUF , https://huggingface.co/unsloth/gemma-4-E2B-it-GGUF , https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF , https://huggingface.co/unsloth/Phi-4-mini-instruct-GGUF , https://huggingface.co/unsloth/Qwen3-4B-Instruct-2507-GGUF

---

## Verification log

Adversarial re-check on 2026-10-02 against primary sources (model cards, repos, PyPI, papers, the AI Act text) and the local result files. Verdicts: **verified**, **corrected** (fixed inline above), **partly verified**, or **unverifiable** (no primary source, or no local file).

| # | Claim | Verdict | Source |
|---|---|---|---|
| 1 | Whisper code and weights MIT; 39/74/244/769/1550/809 M params; VRAM ≈1/1/2/5/10/6 GB; turbo ≈8× vs large | verified | https://github.com/openai/whisper (README table and licence line) |
| 2 | faster-whisper MIT, v1.2.1 (31 Oct 2025); small on i7-12700K 8 threads, 13 min: fp32 2m37s, int8 1m42s, batched int8 51 s; large-v2 RTX 3070 Ti fp16 1m03s, batched 17 s | verified | https://github.com/SYSTRAN/faster-whisper ; https://pypi.org/project/faster-whisper/ |
| 3 | Silero VAD MIT; 6.0.0 26 Aug 2025; 6.2.0 6 Nov 2025 (child voices); 6.2.2 17 Sep 2026; 6.2.3 23 Sep 2026; v6.0 listed small children as a known weakness | verified | https://pypi.org/project/silero-vad/#history ; https://github.com/snakers4/silero-vad/releases |
| 4 | Silero ROC-AUC v6 0.97 / **v5 0.91** / WebRTC 0.73 / TEN 0.93 | **corrected** (v5 = 0.96; 0.91 is v4) | https://github.com/snakers4/silero-vad/wiki/Quality-Metrics |
| 5 | TEN VAD "Apache-2.0 with additional conditions"; RTF 0.0086 vs Silero 0.0127 (Xeon) | verified (Xeon Gold 6348); conditions spelled out inline | https://github.com/TEN-framework/ten-vad (README, LICENSE) |
| 6 | Parakeet-TDT-0.6B-v3: CC-BY-4.0, 600 M, 25 EU languages incl. NL/PL, auto LID, word timestamps; FLEURS EN 4.85 / FR 5.15 / DE 5.04 / NL 7.48 / PL 7.31 | verified | https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3 |
| 7 | Canary-1B-v2: CC-BY-4.0, 978 M, 25 languages, RTFx 749 | verified | https://huggingface.co/nvidia/canary-1b-v2 |
| 8 | onnx-asr MIT; Parakeet v3 36 RTFx on 9800X3D, 57 on T4, 320 on RTX 5070 Ti TensorRT | verified | https://github.com/istupakov/onnx-asr |
| 9 | Moonshine v2 Tiny/Small/Medium 34/123/245 M; M3 latency 50/148/258 ms; WER 12.0/7.84/6.65; MIT except legacy non-English non-streaming (non-commercial) | verified; "English + 7" refined inline (v2 is English-only) | https://arxiv.org/html/2602.12241 ; https://github.com/moonshine-ai/moonshine |
| 10 | Fan et al. zero-shot WER MyST/OGI: tiny 20.6/53.8, base 16.8/38.0, small 13.4/25.4, medium 13.1/20.8, large-v3 12.6/19.9, Canary 9.5/18.2, Parakeet-RNNT 11.1/16.7 | verified; "Parakeet/Canary family" generalisation in §0 **corrected** (models tested are not v3/v2) | https://arxiv.org/html/2406.10507 (Table 2) |
| 11 | Kid-Whisper CSLU spontaneous zero-shot medium 37.0, large-v2 29.4; fine-tuned 16.5; LibriSpeech 2.8 | verified | https://arxiv.org/html/2309.07927 |
| 12 | ESPnet child ASR: Whisper-medium zero-shot 39.1 / 13.5 / 15.2 % (ages 4–7 / 8–10 / 11–15); plateau ≈1 B params | verified | https://arxiv.org/html/2508.16576 (Table 5) |
| 13 | Dutch children JASMIN 5.5 % vs DART 70.4 % | verified; context added (DART = beginning readers) | https://arxiv.org/html/2605.28833v1 |
| 14 | "Expect 2–3× adult WER on single words in noise" | unverifiable (author estimate) | – |
| 15 | Whisper hallucination: ≈1 % of transcripts with hallucinated phrases, 38 % harmful (Koenecke); 40.3 % of 301k non-speech clips, top "thank you"/"thanks for watching", WER 6.5/9.4 % after VAD + BoH (AGH); UrbanSound8K large-v3 99.97 % vs Conformer-CTC 13.52 % | verified | https://arxiv.org/pdf/2402.08021 (abstract, via search); https://arxiv.org/html/2501.11378v1 ; https://arxiv.org/html/2505.12969v1 |
| 16 | Voxtral Mini 4B Realtime: Apache-2.0, 13 languages, no PL, ≥16 GB GPU, 8.72 % WER at 480 ms | verified | https://huggingface.co/mistralai/Voxtral-Mini-4B-Realtime-2602 |
| 17 | Piper code GPL-3.0 (OHF-Voice/piper1-gpl); voices repo MIT-packaged, each voice with its own dataset licence | verified (repo licence GPL-3.0; piper-voices metadata "mit"; per-voice dataset licence in MODEL_CARD) | https://github.com/OHF-Voice/piper1-gpl ; https://huggingface.co/rhasspy/piper-voices |
| 18 | Recommended Piper voices `nl_BE-nathalie`, `de_DE-thorsten`, `pl_PL-gosia`, `fr_FR-siwis`, `en_GB-alba`, `en_US-joe` are clean CC0/CC-BY, unlike lessac | **corrected**: dataset licences are as stated, but all are "Finetuned from U.S. English lessac voice" | MODEL_CARD files under https://huggingface.co/rhasspy/piper-voices/tree/main (nl_BE/nathalie/medium, de_DE/thorsten/medium+high, pl_PL/gosia/medium, pl_PL/darkman/medium, fr_FR/siwis/medium, en_GB/alba/medium, en_US/joe/medium) |
| 19 | `en_US-lessac` research-only Blizzard 2013 data, commercial use excluded; `en_US-ryan` and `hfc_female` CC BY-NC-SA | verified | https://www.cstr.ed.ac.uk/projects/blizzard/2013/lessac_blizzard2013/license.html ; ryan and hfc_female MODEL_CARDs |
| 20 | Kokoro-82M Apache-2.0; languages EN/ES/FR/HI/IT/JA/PT-BR/ZH; FR = 1 voice (<11 h, grade B-); no DE/NL/PL | verified | https://huggingface.co/hexgrad/Kokoro-82M ; .../VOICES.md |
| 21 | XTTS-v2 under the Coqui Public Model License, 17 languages incl. PL/NL/FR/DE | verified (the licence name; its "non-commercial" scope and the Jan 2024 shutdown were not re-checked) | https://huggingface.co/coqui/XTTS-v2 |
| 22 | MeloTTS MIT; EN/ES/FR/ZH/JA/KO; "fast enough for CPU real-time inference" | verified | https://github.com/myshell-ai/MeloTTS |
| 23 | Qwen3-1.7B Apache-2.0, 1.4 B non-embedding, 100+ languages, `enable_thinking=False` | verified | https://huggingface.co/Qwen/Qwen3-1.7B |
| 24 | Qwen3.5-2B Apache-2.0, 201 languages, non-thinking by default, Feb 2026 | verified | https://huggingface.co/Qwen/Qwen3.5-2B |
| 25 | Phi-4-mini-instruct MIT, 3.8 B, 22 languages incl. NL/PL/FR/DE, non-English and attack-prompt warnings | verified | https://huggingface.co/microsoft/Phi-4-mini-instruct |
| 26 | Llama 3.2 Community License; official languages EN/DE/FR/IT/PT/HI/ES/TH; the EU restriction applies to multimodal models only | verified | https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct |
| 27 | Gemma 4 E2B Apache-2.0, 2.3 B effective / 5.1 B with embeddings, audio input ≤30 s | verified | https://huggingface.co/google/gemma-4-E2B-it |
| 28 | AI Act Art. 5(1)(f) text (emotion inference in workplace/education, medical/safety exception) | verified | https://artificialintelligenceact.eu/article/5/ |
| 29 | Recital 18: "raised voice or whispering" is not emotion recognition unless used to infer emotion | verified | https://artificialintelligenceact.eu/recital/18/ |
| 30 | Recital 16 names age and sex as biometric-categorisation categories | verified (it also lists **language**; see Omissions) | https://artificialintelligenceact.eu/recital/16/ |
| 31 | Art. 50 applies from 2 Aug 2026, unchanged by the Digital Omnibus | verified for Art. 50 generally (only the Art. 50(2) marking duty gets a grace period to 2 Dec 2026); the Omnibus did not touch the emotion-recognition prohibition | https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act ; https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ (secondary) |
| 32 | [LOCAL] VAD 0.093 s; fw tiny/base/small/medium/turbo 0.56/1.15/4.25/12.36/15.51 s per 10 s; Parakeet 3.45 s; pyin 0.88 s; AST 8.5 s with "Male speech" 0.208; me5-small 0.18 s | verified against the file | `research/04-audio-bench/bench_audio.json` |
| 33 | [LOCAL] GRID colour words 79.7 % clean, 71.4 / 64.1 / 26.6 % at 10 / 5 / 0 dB, wrong value 0.5 % at 0 dB; auto-LID 73.4 % with EN detected in 85.4 %; AUROC 0.813–0.820; 2.28 s per clip | verified against the file | `prototype/experiments/results/audio_grid.json` |
| 34 | [LOCAL] earlier run: base 1.19 s, small 2.4 s per 10 s (noise input) | verified against the file | `scratch/bench_models.json` |
| 35 | [LOCAL] Piper synthesis table (§9.2), CLAP probe (§6.3), LLM speeds (§10.2) | **unverifiable**: output files are missing (`bench_piper.json`, `bench_clap.json`, `bench_llm.txt`), and the CLAP run in `bench_audio.json` errored | `research/04-audio-bench/` listing |
| 36 | [LOCAL, team-reported] Whisper small and large-v3-turbo both missed "my dog" on a far-field recording | **unverifiable from files**: not present in `audio_grid.json` or any other project file found; reported by the team | – |

Not re-checked (left as the author wrote them): EfficientAT/PANNs/YAMNet/AST/BEATs mAP figures, LAION-CLAP and MS-CLAP numbers, audEERING and emotion2vec licences, Vosk WERs, Kyutai, Nemotron, pyannote, the speech-level and inverse-square figures [S78, S79], Windows SAPI voice lists, sherpa-onnx, openSMILE licence, multilingual-e5-small, and Piper on Raspberry Pi.

## Omissions added by verifier

1. **Whisper's 30 s padding makes per-utterance latency nearly constant.** Whisper processes fixed 30 s windows, so a 2.5 s answer costs almost as much as a 10 s clip. Our own data show 2.28 s per ~2.5 s GRID utterance for faster-whisper small int8 [LOCAL: `audio_grid.json`], versus 4.25 s per 10 s in `bench_audio.json`. The RTF column in §2 therefore flatters Whisper for this use case. Parakeet (FastConformer-TDT) does not pad, which is another reason for the §12.3 A/B test. Benchmark per *utterance* on the exhibition machine.
2. **Far-field failure (team observation).** The team reports that Whisper small **and** large-v3-turbo both missed "my dog" on a far-field recording. If true, a bigger model does not fix distance, which supports §3.5 and §13 (close-talk microphone first). The recording and output are not in the repo. Save them (with consent) so the result can be cited and re-run.
3. **Piper voice provenance.** Almost every popular Piper voice is fine-tuned from `en_US-lessac`, whose data are research-only. From-scratch alternatives: `nl_NL-mls-medium`, `fr_FR-mls-medium`, `de_DE-mls-medium` (CC-BY-4.0) and `en_US-ljspeech-medium` (PD). No clean Polish voice was found. Options are SAPI Paulina/Adam, a commercial offline voice with a clear licence, or a legal sign-off on gosia/darkman. Pre-rendering does not remove the question, because the WAVs are still model output.
4. **"Language" is a recital 16 category.** The AI Act lists language among biometric-categorisation categories. Inferring a visitor's language from their voice (auto-LID) and displaying it is a weak but real argument for Art. 50(3) applicability. The flag button avoids it.
5. **TEN VAD licence conditions** (no deployment competing with Agora; only in your own application for your direct end users) are spelled out inline. They are harmless for the exhibit but make it unsuitable for code we might later release as a reusable toolkit.
6. **Kokoro provenance.** Its French voice requires CC BY attribution (SIWIS), and the training set includes synthetic audio from closed commercial TTS systems, whose terms we cannot check.
7. **The child-speech evidence does not cover the candidate models.** No published child-speech WER exists for Parakeet-TDT-0.6B-v3 or Canary-1B-v2, nor for any model on Flemish/Brussels-French children aged 8–14. The A/B on our own child recordings is the only evidence that would count.
8. **Missing local artefacts.** `bench_clap.json`, `bench_piper.json`, `bench_llm.txt`, and the `pylib/`, `ttslib/`, `voices/` and `llm/` folders named in `research/04-audio-bench/README.txt` are absent. §6.3 and §10.2 still hold the placeholders `TBD_CLAP` / `TBD_LLM`. Re-run the scripts and save their outputs, or delete the claims that depend on them.
