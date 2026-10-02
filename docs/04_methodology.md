# Prototype methodology and results

Purpose: this document records how the working prototype was built and tested before any robot was bought. It covers the data, models, preprocessing, sensor fusion, representation, explanations and image generator, and how we evaluated them. It is meant for TUAI partners.

## Key points

- The pipeline is implemented end to end and runs offline on a laptop CPU. It uses real models on recordings of **real people** (6 adults from Meta's Seamless Interaction dataset). Each visitor is replayed with every sensor configuration (eyes + ears, eyes only, ears only, none) and with two sensor problems: a noisy room and a foggy lens.
- The representation is a **belief over 6 child-safe concept slots**. The fusion is a tempered logarithmic opinion pool, so a missing sensor is handled by marginalisation. That design makes the explanation exact: each sensor's "clues" for an answer are at once its exact Shapley value, its leave-one-sensor-out effect and the sum of its evidence cards. This is unit-tested.
- The prototype reproduces the exhibit's message on real data. Eyes and ears together know 4.5 of 6 things per visitor, with 94% of checkable claims correct. Eyes alone know 2.3 (clothes 6/6, animal 0/6) and ears alone 1.8 (animal 5/6, clothes 0/6). A noisy room costs the animal for 2 more visitors. A foggy lens wipes out the clothes colour and even misleads. And the robot can be confidently wrong: Visitor B's "brown".
- Component evaluations on public data:
  - Lombard GRID, 192 utterances: colour words correct in 80% of clean utterances with 0% wrong colours, falling to 27% correct with 0.5% wrong at 0 dB crowd babble. Plain vs loud speech separates with AUROC 0.81.
  - Open Images, 219 verified head crops: glasses AUROC 0.91, calibration error 0.08, and 93% of "I'm sure" claims are correct.

## 1. Pipeline

```
camera frames (2 fps) -> MediaPipe face + pose -> head box / upper-chest box / keypoints
                      -> glasses: CLIP ViT-B/32 contrast prompts + Platt calibration
                      -> clothes colour: k-means (k=3) in CIELAB -> 11 basic colour names
                      -> movement: keypoint speed in head-widths per second
                      -> animal picture card/toy: CLIP prompts vs. background prompts
microphone (6 s windows) -> Silero VAD -> faster-whisper small (multilingual, word timestamps)
                      -> closed EN/FR/NL/DE/PL lexicon -> favourite animal / colour words
                      -> loudness of speech vs booth calibration, SNR -> evidence quality
          all -> Observation(t, sensor, slot, likelihood over values, quality, weight, evidence text)
              -> EvidenceMemory (in RAM, per visitor) -> fusion per sensor configuration
              -> belief per slot -> explanations -> avatar + "why" cards + what-if + imagination
```

Code: `prototype/robotsees/` (`perception/vision.py`, `perception/audio.py`, `perception/lexicon.py`, `fusion.py`, `xai.py`, `session.py`).

## 2. Data

| Use | Dataset | Licence and access | What we used |
|---|---|---|---|
| End-to-end "visitors" | **Seamless Interaction** (Meta, 2025), naturalistic/dev | CC BY-NC 4.0, ungated per-file download | 6 people, standing full-body views, 23–38 s segments in which they mention an animal. We chose segments by searching the dataset's transcripts for our word list. We annotated ground truth by hand (animal, clothes colour, glasses). Faces are pixelated on every screen |
| Audio evaluation, crowd noise | **Lombard GRID** | CC BY 4.0, Zenodo | 192 utterances: 12 talkers × 4 colour words × plain/Lombard (loud) × 2. Fetched with HTTP range requests (only the needed files). Babble = 6 overlapping streams of other talkers |
| Glasses (and hat) calibration | **Open Images V7** validation set | Annotations CC BY 4.0, images CC BY 2.0 | Human-verified labels: 120/99 glasses faces, 79/52 hat faces. **Images labelled Boy/Girl were excluded**: no evaluation on minors |
| Considered, not used | RAVDESS, CREMA-D | CC BY-NC-SA / ODbL | Head-and-shoulder studio shots with uniform black T-shirts and scripted sentences. They are emotion corpora, which we must not train on |
| Rejected | VoxCeleb, LRS3, AVSpeech, CelebA, FairFace, MEAD, IEMOCAP, children's corpora | Withdrawn, scraped, restricted or sensitive labels | See `research/08-datasets.md` |

No public dataset matches the real setting: children seen from a low robot viewpoint, in a noisy hall, speaking FR/NL. Before the fair we will record a small consented set of **adult researchers** at the booth to calibrate on site (protocol in `research/08-datasets.md` §5c). We will not record children.

## 3. Models and preprocessing

| Function | Model / method | Licence | Measured on dev laptop CPU (Core Ultra 7 255U) |
|---|---|---|---|
| Face box (crop location only) | MediaPipe BlazeFace short-range | Apache-2.0 | part of 250–450 ms per frame (all vision) |
| Body keypoints | MediaPipe Pose Landmarker lite; only keypoints with visibility > 0.7 inside the frame | Apache-2.0 | (same) |
| Glasses | OpenCLIP ViT-B/32 (LAION-2B), contrast prompts (e.g. "a photo of a person wearing glasses" vs "a close-up photo of a person's bare eyes"), per-concept Platt scaling | MIT code | 94–128 ms per crop |
| Clothes colour | k-means in CIELAB on the upper chest (15–60% of the shoulder-to-hip span, inner 60% width); nearest of 2–5 Lab prototypes per colour name | own code | < 5 ms |
| Voice activity | Silero VAD | MIT | < 50 ms per window |
| Speech to words | faster-whisper `small` int8, multilingual, word timestamps, beam 1 | MIT | 2.3 s per ~2.5 s utterance; 2.4 s per 10 s |
| Words to slots | closed lexicon of 11 colours and 12 animals in EN/FR/NL/DE/PL, language-aware (English "chat" is not a cat) | own code | < 1 ms |
| Loudness | RMS dBFS of speech samples relative to a booth calibration level | own code | < 1 ms |
| Robot voice | Piper TTS, en_US-amy (offline) | see model card | 1.4 s per sentence |
| Robot's imagination | LCM-Dreamshaper v7 int8 (OpenVINO) + TAESD, img2img from the robot's own avatar drawing, strength 0.7, 4 steps (`experiments/build_imagination.py`); first variant: SD-Turbo text-to-image on CPU (replaced) | MIT / Stability Community Licence | 2.6 s per image on the integrated GPU (OpenVINO; 40 s one-time compile); 22–35 s for SD-Turbo on CPU |

Choices made after measurement:

- **CLIP ViT-B/32 over SigLIP2 B/16.** Glasses AUROC was 0.914 vs 0.920, but CLIP's calibration error was much lower (ECE 0.084 vs 0.150) and it is 3–4× faster on CPU.
- **The hat detector was removed.** Its AUROC was 0.75, or 0.83 with a linear probe, but it was dropped after the ethics review: headwear can reveal religion.
- **Glasses evidence is weighted by face size.** A face 40 px wide gave a false "glasses" in an early run; evidence quality now falls linearly below 80 px face width.
- **Loudness is calibrated per recording setup.** Speech levels in the dataset differ by 33 dB between recording vendors, so absolute dBFS measures the microphone, not the person. At the booth this is a one-time calibration with the fixed close-talk microphone.

Never computed anywhere: face recognition, face or voice embeddings, age, gender, emotion, skin tone, hair, height, body shape, accent or language of origin, headwear, speaking speed as a label.

## 4. Representation: what "the robot's picture of you" is

We compared five candidates:

| Candidate | Verdict |
|---|---|
| Generated portrait of the visitor | Rejected. It invents a face, skin tone, gender and age that no sensor inferred, which is unfaithful and leaks sensitive attributes. A realistic generated image of a child could also count as a deep fake (AI Act Art. 50) |
| Raw multimodal embedding (e.g. CLIP space) shown as a map | Rejected for children. It is not interpretable, and modalities are hard to separate |
| Semantic profile as text | Used for the explanations, but too abstract on its own for 7-year-olds |
| **Belief state over a closed set of concept slots + procedural avatar** | **Chosen.** Every element maps to one slot. Uncertainty is visible (faded, dashed, "?"). The provenance badge shows which sense found it. It is deterministic, renders in < 50 ms and cannot make things up |
| + optional generated "imagination" | Kept as an add-on. A generated restyle of the avatar, built only from closed-vocabulary words, labelled and machine-marked as AI-generated |

Slots (`robotsees/config.py`): favourite animal, favourite colour, clothes colour, glasses, "how much is happening right now", "the voice I hear right now". Each slot has a closed value set and a **relevance** per sensor. For example, clothes colour is only a weak hint about a favourite colour (relevance 0.35).

## 5. Memory and fusion

**Memory.** Each visitor has an in-RAM evidence ledger, which is a list of observations: time, sensor, slot, likelihood over the slot's values, quality in [0, 1], weight in independent-evidence units, and a child-readable evidence text. This is the robot's entire memory. It holds no images, audio, transcripts or embeddings, and it is wiped when the visitor leaves ("forget me"). It is neither a vector store nor a conversation memory: its only job is to accumulate evidence during one short interaction.

**Fusion** (`robotsees/fusion.py`), per slot with value set V:

- score(v) = log prior(v) + Σ over enabled sensors m of E_m(v), and P(v) = softmax(score). The prior is uniform, so before it sees you the robot has no idea.
- E_m(v) = κ_m · quality-weighted mean over observations of [ log( r·L(v) + (1−r)/|V| ) − log(1/|V|) ].
- κ_m = 1 − exp(−Σ q·w / τ), with τ = 1.5.
- r is the sensor's relevance for the slot: a mixture with "uninformative", so red clothes make "favourite colour = red" a bit more likely without ruling out blue.
- w is the independent-evidence weight: 0.2–0.3 for one video frame (frames are correlated), 2.0 for one spoken keyword.
- κ saturates, so 100 frames are not 100 proofs. A small likelihood floor (0.05) means no single observation is ever certain.

**Missing sensors.** A switched-off sensor simply contributes no term. This is exact marginalisation under the naive-Bayes assumption, and it is what the physical switch does. We never feed a black frame or silence, because that would be fabricated evidence.

**Certainty words.** The maximum probability is rescaled between "uniform" (0) and "one-hot" (1), then mapped to words: sure ≥ 0.75, think ≥ 0.5, guessing ≥ 0.25, otherwise "I don't know yet".

## 6. Explanations (XAI)

All explanations are computed from the same ledger and fusion the robot uses.

| Shown to visitors | How it is computed | Why it is faithful |
|---|---|---|
| **Clue balance** per slot and sensor | clue_m = E_m(v*) − mean_v E_m(v): the sensor's log-odds clues for the chosen answer v* | In log-odds space the fusion is additive, so clue_m equals the exact Shapley value of sensor m, the leave-one-sensor-out change, and the sum of that sensor's evidence cards (unit test `test_clues_are_exact_shapley_and_lomo_and_sum_of_cards`) |
| **Evidence cards** ("my ears heard you say 'horse' at 0:05") | Observations ranked by their push towards v*, merged when identical | Each card is a ledger row that the fusion actually summed |
| **What if?** strip (4 small avatars) | The fusion re-run for all 2^n sensor configurations at the same moment | It is literally what the switch would do |
| **Senses disagree** | Each sensor's own best answer (fusion with only that sensor) differs | Same fusion |
| **Certainty words, faded or dashed drawing** | Rescaled max probability | Same fusion |
| **Sentences** | Templates filled only from ledger fields (no LLM) | Cannot say anything the numbers don't |

We considered these methods and did not use them live (full six-question assessment in `research/07-xai.md`):

- attention maps or rollout: unfaithful;
- LIME, and KernelSHAP or RISE on pixels: minutes per explanation on CPU, unstable;
- MM-SHAP and the perceptual score: they answer other questions;
- MC dropout: CLIP has no dropout layers;
- evidential deep learning: documented critiques;
- LLM-written explanations: fluent but unfaithful.

A coarse occlusion "spotlight" on a stylised frame remains an option for later, but only after saliency sanity checks.

## 7. Generative model

The image generator receives **only words** from a closed phrase list, plus the robot's own avatar drawing as the starting image (img2img, strength 0.7). It never receives a camera frame. Only slots the robot believes at least at "guessing" level are put into words. The subject is always "a cute friendly robot mascot", never a person.

Each image carries IPTC `DigitalSourceType = trainedAlgorithmicMedia` in XMP plus an EXIF description, to meet the AI Act Art. 50(2) machine-readable marking duty. On screen it is labelled "AI-generated picture: the generator only got these words".

- **Exhibition GPU** (RTX 4060/4070 laptop): about 1 s per stage (research/06 estimate).
- **This laptop's integrated GPU** (OpenVINO): 2.6 s measured.

The exhibit must work with the generator switched off: it is the "imagination", not the representation.

## 8. Evaluation procedure

1. **Unit tests** (`prototype/tests`): flat prior with no sensors; voice beats clothes for favourite colour; conflict lowers confidence; Shapley efficiency; monotone accumulation; faithfulness (clues = Shapley = leave-one-out = sum of cards); JSON-ready snapshots.
2. **Vision calibration** (`experiments/calibrate_vision.py`): 5-fold cross-validated Platt scaling on Open Images head crops; AUROC, accuracy, ECE, Brier score, and precision of "sure" claims.
3. **Audio** (`experiments/eval_audio_grid.py`): colour-word recognition and plain-vs-Lombard loudness on GRID, clean and with crowd babble at 10/5/0 dB SNR, plus automatic language ID.
4. **End-to-end ablation** (`experiments/build_sessions.py`, `analyze_ablation.py`). We ran 6 visitors × {clean, noisy room, foggy lens} × {eyes + ears, eyes only, ears only}. For each run we record the number of slots the robot claims to know, mean certainty, correctness of checkable claims (animal, clothes colour, glasses, and any favourite-colour claim, which counts as unsupported because nobody stated one) and the time to the first confident animal claim.
5. **Demo video** (`video/render_video.py`): the real UI is driven by a shot list and captured frame by frame.

## 9. Results

### 9.1 Components

| Test | Result |
|---|---|
| Glasses, CLIP B/32, calibrated (Open Images, 219 adult faces, 5-fold CV) | AUROC 0.914, accuracy 0.858, ECE 0.084, Brier 0.117; "I'm sure" on 51% of faces with 92.8% correct |
| Glasses, SigLIP2 B/16 | AUROC 0.920, ECE 0.150 (worse calibration), 3–4× slower |
| Hat (removed later for ethics reasons) | AUROC 0.70 → 0.75 with simpler prompts → 0.83 with a linear probe |
| Colour words in speech (GRID, 192, clean) | 79.7% heard correctly, **0.0% wrong colour**, 20.3% missed |
| … with crowd babble 10 / 5 / 0 dB SNR | 71.4% / 64.1% / 26.6% correct; wrong 0 / 0 / 0.5% |
| Loud (Lombard) vs plain speech from absolute level | AUROC 0.81; +7.0 dB within talker |
| Automatic language ID on short GRID sentences | 85% English (hence a language button at the booth) |
| Hard far-field recording (Visitor C) | Whisper small **and** large-v3-turbo both miss "my dog" |

### 9.2 Sensor-configuration ablation on the 6 visitors

| Condition | Sensors | Visitors | Things known (of 6) | Mean certainty | Checkable claims correct | Confident claims correct | Animal right | Clothes colour right | Glasses right | Unsupported fav.-colour claims |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Clean | Eyes + ears | 6 | 4.5 | 0.46 | 94% (17) | 91% (11) | 5/6 | 6/6 | 5/6 | 1 |
| Clean | Eyes only | 6 | 2.33 | 0.24 | 100% (11) | 100% (5) | 0/6 | 6/6 | 5/6 | 0 |
| Clean | Ears only | 6 | 1.83 | 0.24 | 83% (6) | 83% (6) | 5/6 | 0/6 | 0/6 | 1 |
| Noisy room (ears) | Eyes + ears | 6 | 4.17 | 0.40 | 93% (15) | 89% (9) | 3/6 | 6/6 | 5/6 | 1 |
| Noisy room (ears) | Eyes only | 6 | 2.33 | 0.24 | 100% (11) | 100% (5) | 0/6 | 6/6 | 5/6 | 0 |
| Noisy room (ears) | Ears only | 6 | 1.67 | 0.19 | 75% (4) | 75% (4) | 3/6 | 0/6 | 0/6 | 1 |
| Foggy lens (eyes) | Eyes + ears | 6 | 2.67 | 0.30 | 60% (10) | 75% (8) | 5/6 | 0/6 | 1/6 | 1 |
| Foggy lens (eyes) | Eyes only | 6 | 0.67 | 0.06 | 25% (4) | 50% (2) | 0/6 | 0/6 | 1/6 | 0 |
| Foggy lens (eyes) | Ears only | 6 | 1.83 | 0.24 | 83% (6) | 83% (6) | 5/6 | 0/6 | 0/6 | 1 |

*Checkable claims are the ones we can verify: favourite animal, clothes colour, glasses, plus any favourite-colour claim. Nobody stated a favourite colour, so every such claim is counted as unsupported. "Confident" means think or sure. The number of claims is in brackets.*

Figures: `prototype/experiments/results/fig_ablation_matrix.png` (what each configuration concluded about each visitor), `fig_conditions.png` (noisy room and foggy lens), `fig_progressive_v02.png` (certainty over time), `fig_reliability.png` (glasses calibration), `fig_audio_grid.png` (colour words under noise).

### 9.3 What the results show (the exhibit's message, on real data)

1. **Each sense brings different evidence, and fusion knows the most.** With clean input, eyes and ears together know 4.5 of the 6 things about a visitor. Eyes alone know 2.3 and ears alone 1.8.
   - The favourite animal comes only from the ears: 5/6 correct, while the eyes get 0/6.
   - The clothes colour comes only from the eyes: 6/6 with eyes, 0/6 with ears alone.
   - Glasses come only from the eyes: 5/6. For Visitor E the robot says "I don't know", which is honest because her face is small in the frame.
2. **Missing information changes conclusions, and the robot says so.** Switching a sense off removes exactly that sense's clues (marginalisation). The answers that sense supported turn into "I don't know yet" instead of being guessed.
3. **Noise makes the robot unsure more often than wrong.**
   - In the noisy room, the ears still find the animal for 3 of 6 visitors, down from 5. The checkable claims that remain are still 93% correct with both senses on.
   - On GRID, crowd babble at 0 dB cuts correct colour words from 80% to 27%, but wrong colours stay at 0.5%.
4. **Other people's voices can inject false evidence.** In Visitor E's noisy-room variant the robot became *sure* her favourite colour is white. It heard "white" four times, but from the crowd-babble talkers: GRID sentences contain colour words. In a hall the microphone also hears other people. This is a further argument for the close-talk microphone and for counting words only as answers to the robot's question.
5. **But a degraded sense can also mislead.** Through the foggy lens, eyes-only claims are only 25% correct. A darkened, blurred image makes clothes look grey or black. The image-quality estimate (brightness and sharpness) lowers the evidence weight but does not remove it. This is a useful lesson for visitors and a to-do for the exhibit: a stronger quality gate.
6. **AI can be sure and wrong.** Visitor B said "Snow White" and "ginger brown" (about her rabbit), and the robot became *sure* that her favourite colour is brown. Keyword spotting has no understanding. In the booth, words count only as answers to the robot's own question.
7. **Evidence builds up over time** (`fig_progressive_v02.png`).
   - For Visitor B, the animal goes from "don't know" to "guessing" with the first "bunny rabbit" at about 4 s, and to "sure" by about 9 s.
   - It dips when she says "not a cat or a dog" at about 20 s, then recovers.
   - The time to the first confident animal claim is in `results/ablation.json`.
8. **The robot was right and the annotator wrong once.** Visitor C wears thin transparent glasses. The first hand annotation (made from a small thumbnail) said "no glasses" and the robot said "glasses (think)"; a full-resolution check proved the robot right. All glasses labels were then re-verified at full resolution. Ground truth needs care too.

## 10. Limitations

- The 6 visitors are adults from a dataset, talking freely rather than answering our robot's questions; the camera is not at robot height. The exhibit's numbers will differ, and we will measure them on our own consented adult recordings at the booth before the fair.
- Ground truth was annotated by one person. Clothes colour is genuinely ambiguous for patterned or teal clothes, which is why two accepted values are listed.
- Keyword spotting has no understanding of meaning ("Snow White", "not a cat or a dog"). At the booth, words count only as answers to the robot's own question, which removes most such errors.
- The fusion assumes the sensors are conditionally independent; correlated evidence is damped by the weights and saturation, not modelled.
- CPU latencies were measured with other jobs running and are upper bounds.
