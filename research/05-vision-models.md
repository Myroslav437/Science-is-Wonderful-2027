# 05 — Vision models for "How does a robot see you?" (local / offline pipeline)

Research track 05 · prepared 2026-10-01/02 for DC5 and DC7 (TUAI, Silesian University of Technology) · Science is Wonderful! 2027 demonstrator
Priorities used for every judgement: **feasibility > robustness > educational clarity > scientific value > visual appeal**.
Source numbers in square brackets refer to the Sources list at the end. "UNVERIFIED" means I could not confirm it from a primary source. "MEASURED" means our own micro-benchmark on the dev laptop (method in §1). This is not legal advice. Licence and AI-Act points should be confirmed by the legal/ethics track.
Revision 2 (2026-10-02): verifier corrections merged into the body; gap-fill added for RF-DETR CPU latency [73], Hailo-8L model-zoo throughput [74], small-VLM GPU figures [75][76], Florence-2 native `transformers` support [77], Gemma 4 release date [78], and the AI Act amendment Regulation (EU) 2026/1744 [79].

---

## 0. Decision summary

| # | Decision | Why (short) |
|---|---|---|
| 1 | **Build the core only on Apache-2.0/MIT components**: MediaPipe Tasks 1.0.x (pose, hands/gestures, face landmarks), **rtmlib** (YOLOX + RTMPose, multi-person), **YuNet** (faces at distance), **SigLIP 2 B/16** (zero-shot accessory checks on body-part crops), k-means + colour naming for clothing colour, ByteTrack (`supervision`, MIT) for tracking. | All permissive. Python-installable. Run offline on CPU, iGPU or NPU [15][26][29][41][72]. |
| 2 | **Keep Ultralytics YOLO11/YOLO26 out of the core.** Use it only as a benchmark baseline, or accept AGPL-3.0 for the *whole* demonstrator. | Ultralytics says code **and trained weights** are AGPL-3.0. Its own reading: the "entire project" must be open-sourced, or you buy an Enterprise licence (price on request) [2]. |
| 3 | **Use OpenVINO on the dev laptop's iGPU/NPU, not only the CPU.** | MEASURED on the Core Ultra 7 255U: YOLO26n detect/pose at 640 px takes **15–19 ms** on the NPU/iGPU vs 59–107 ms on the CPU. SigLIP2-B/16 image encoder takes **20 ms on the NPU** vs 190–500 ms in PyTorch on the CPU. NPU output cosine vs fp32 is ≥ 0.9999 (§1). For the vision stack, a "CPU-only" laptop of this class is enough. |
| 4 | **Never infer** age, sex/gender, ethnicity, emotion, identity, hair/eye colour, body size, or personality traits. No face embeddings, and no re-identification across visits. | AI Act definitions and prohibitions, Art. 3(39)/(40), recitals 16 and 18, Art. 5(1)(f)(g) and Art. 50(3) [63][64]. Even commercial age estimators have a mean absolute error of **1.42–5.34 years** at ages 8–14 on high-quality visa-application photos (NIST IR 8525, Table 19, six algorithms) [62]. Art. 50(3) information duties for biometric categorisation / emotion recognition apply from 2 Aug 2026 and were **not** deferred by the 2026 amendment (Reg. (EU) 2026/1744) [79], so they apply during the 2027 exhibition. |
| 5 | **Only describe things that are observable, non-bodily and changeable**: clothing colours, accessories (glasses, hat, backpack…), held objects, gestures and actions (waving, hands up, jumping), facing direction, distance zone, dwell time, number of people. | These are visible, non-sensitive and easy to explain. A "readily apparent" gesture or smile is not emotion recognition [63 recital 18][64]. |
| 6 | **No VLM in the live loop for v1.** At most an *optional* "robot diary" sentence built from the vetted evidence, or a VLM used as a yes/no *verifier* on crops on the GPU laptop. Never show raw VLM text to children. | MEASURED: SmolVLM2-256M/500M takes 24–38 s per sentence on the laptop CPU (under load), and both described the visitors with gendered words ("man") without being asked. VLMs hallucinate objects [59]. |
| 7 | **Make explanations faithful by construction.** Every inference is computed *only* from a named region (keypoint-defined crop or mask), by a named model, from a named sensor. The UI shows exactly that region plus a calibrated confidence. Post-hoc saliency is at most a secondary visual. | Saliency maps can fail sanity checks [70]. Crop-based evidence is cheap, robust and honest. |
| 8 | **Raspberry Pi on the dog = capture + streaming + local safety.** Person-related inference runs on the stand laptop over a closed local network. | Pi 5 CPU: YOLO26n NCNN 67 ms per frame [5], workable but no headroom. A Hailo AI HAT+ (from US$70) or AI HAT+ 2 (US$200, listed price Oct 2026) adds acceleration [71]. |

---

## 1. Method and measured numbers (dev laptop)

**Hardware and software (MEASURED setup).** Intel Core Ultra 7 255U (12 cores / 14 threads, integrated "Intel Graphics", "Intel AI Boost" NPU, all reported by OpenVINO), 32 GB, Windows 11, Python 3.12. Project `.venv` versions: torch 2.14.1+cpu, onnxruntime 1.30.0, mediapipe 1.0.1, opencv 5.0.0.93, ultralytics 8.4.171, open_clip 3.3.0, transformers 5.18. OpenVINO 2026.4.1, onnx 1.23 and rtmlib 0.0.16 were installed into a separate folder (the project venv was not modified).
- Test images: Ultralytics `zidane.jpg` (1280×720, 2 people, plus a blurred crowd) and `bus.jpg` (810×1080, 4 pedestrians).
- Method: batch 1, warm-up, then median of 15–40 runs.
- **Caveat:** other heavy jobs ran on the same machine at the same time (CPU load 5–100 %). CPU numbers are therefore noisy, and I give ranges across repeated runs. iGPU and NPU numbers were stable.
- Scripts: `research/05-vision-bench/` (re-run them on the real exhibition machine).

### Table 1 — Latency (MEASURED, single frame)

| Component | Runtime → device | Input | Median latency |
|---|---|---|---|
| YuNet face detector (2023mar, 232 KB ONNX) | OpenCV 5.0 DNN → CPU | 640×360 | **10.6–13.1 ms** |
| MediaPipe Face Detector (BlazeFace short-range) | MediaPipe 1.0.1 → CPU | 640×360 | **4.0 ms** |
| MediaPipe Face Landmarker (478 lm + blendshapes + matrix) | → CPU | 640×360 | 14.7 ms (no face accepted in frame, so this is a lower bound) |
| MediaPipe Gesture Recognizer (2 hands) | → CPU | 640×360 | 18.2 ms (no hand found, so a lower bound) |
| MediaPipe Pose Landmarker lite / full | → CPU | 640×360 | **40–47 ms / 50–51 ms** |
| MediaPipe Object Detector EfficientDet-Lite0 int8 | → CPU | 640×360 | 45 ms |
| MediaPipe multiclass selfie segmenter (6 classes incl. *clothes*) | → CPU | 256×256 | **216 ms** (Google-published CPU benchmark: 217.8 ms [24]). Too slow to run every frame |
| rtmlib "lightweight" (YOLOX-tiny + RTMPose-s), 2 people | ONNX Runtime → CPU | 1280×720 | 282–335 ms (min 131) |
| same | OpenVINO → CPU / **iGPU** | 1280×720 | 224–269 ms / **52 ms** |
| YOLO26n detect (AGPL) | PyTorch → CPU | 640 / 320 | 88 ms / 27 ms |
| YOLO26n detect | OpenVINO → CPU / **iGPU / NPU** | 640 | 59 / **19 / 16 ms** |
| YOLO26n-pose | OpenVINO → CPU / **iGPU / NPU** | 640 | 107 / **18.5 / 15 ms** |
| YOLO11n detect / YOLO11n-pose | PyTorch → CPU | 640 | 70 ms / 83 ms |
| CLIP ViT-B/32 (LAION-2B) image encoder | PyTorch fp32 → CPU (8 threads best) | 224 | 69–134 ms |
| same | OpenVINO → iGPU / **NPU** | 224 | 83 ms / **12.9 ms** |
| SigLIP 2 ViT-B/16 image encoder | PyTorch fp32 → CPU | 224 | 190–500 ms (thread count matters: 8 threads best on this hybrid CPU) |
| same | ONNX Runtime → CPU | 224 | 131–179 ms |
| same | OpenVINO → **iGPU / NPU** | 224 | **45 ms / 20 ms**. Output cosine vs fp32: iGPU 0.99990, NPU 0.99998 |
| Text encoder, 20 prompts (one-off at start-up) | PyTorch → CPU | — | 1.1–1.9 s, so precompute and cache |
| SmolVLM2-256M / 500M (one 22-token sentence, 880 input tokens) | transformers fp32 → CPU | 1280×720 | **24–33 s / 31–38 s** |

### Table 2 — Robustness spot-check (MEASURED; 2 images only, so these are anecdotes, not an evaluation)

| Model | zidane.jpg (2 large people, 1 blurred background face) | bus.jpg (4 smaller pedestrians) |
|---|---|---|
| MediaPipe Pose (full, `num_poses=5`) | 0 at full res (1 at 640×360) | 1 |
| rtmlib YOLOX-tiny + RTMPose-s | **2** | 3 |
| EfficientDet-Lite0 (person) | 2 | 3 |
| BlazeFace short-range | 1 | 0 |
| MediaPipe Face Landmarker | 0 | 0 |
| YuNet | 2 true + 1 low-score (0.61) detection in the blurred crowd | 2 (faces only ~40 px wide) |

**Takeaways.**
- MediaPipe Pose is a single-person model. Its model card lists "Multiple people in an image" and "further than 14 feet/4 meters" as out-of-scope [19].
- Short-range face models miss faces at stand distances.
- YuNet finds small faces, and will also find **bystanders' faces**. You therefore need a "primary visitor" selection rule (§4).

### Table 3 — Zero-shot sanity check (MEASURED; 2 crops, anecdotal)
The crops show two men in suits, both **wearing ties**, with no hats, glasses or backpacks. Each score is a binary prompt pair ("wearing X" vs "without X"):

| Attribute (truth) | CLIP B/32 pair-softmax (L / R) | SigLIP2 B/16 pair-softmax (L / R) | SigLIP2 raw sigmoid P |
|---|---|---|---|
| tie (**yes**) | 0.44 / 0.49 | 0.34 / 0.40 | 0.001 |
| backpack (no) | **0.68 / 0.68** | 0.03 / 0.03 | 0.000 |
| hat (no) | 0.05 / **0.55** | 0.00 / 0.01 | 0.000 |
| glasses (no) | 0.08 / 0.10 | 0.01 / 0.02 | 0.000 |
| pointing (L yes; R no) | 0.58 / **0.95** | 0.31 / **0.83** | ≤0.004 |

**Lessons.**
1. Uncalibrated zero-shot scores are unusable as shown. CLIP B/32 "sees" backpacks that are not there and misses visible ties. SigLIP2's raw sigmoid output sits near 0 for both true and false attributes.
2. SigLIP2 B/16 gives much better *rankings* than CLIP B/32, so it is calibratable.
3. The right crop's high "pointing" score is very likely caused by the *left* person's pointing hand reaching into that crop (my interpretation). Crops must be keypoint-tight, and group scenes leak evidence between people.

---

## 2. Licence triage (decide this first)

| Component | Code licence | Weights / model licence | Exhibition verdict |
|---|---|---|---|
| **Ultralytics** YOLOv8/YOLO11/YOLO26 (det, pose, seg) | AGPL-3.0 | AGPL-3.0 ("All Ultralytics YOLO trained models fall under the AGPL-3.0") [2] | ⚠ Only if the whole demonstrator is AGPL, or with an Enterprise licence. Not in the core |
| RT-DETR / RT-DETRv2 (also in HF transformers) | Apache-2.0 | Apache-2.0 [10][11] | ✅ |
| RF-DETR Nano–Large (`pip install rfdetr`) | Apache-2.0 | Apache-2.0. **XL/2XL are PML 1.0** [8] | ✅ (avoid XL/2XL) |
| D-FINE, DEIM | Apache-2.0 | Apache-2.0 [12] | ✅ |
| DEIMv2 (Sep 2025; Atto 0.5 M / 23.8 AP … X 50.3 M / 57.8 AP) [added by verifier] | **custom "DEIMv2 License"** | "Commercial Use … is **not permitted**"; non-commercial research/education only; PRC law (https://github.com/Intellindust-AI-Lab/DEIMv2/blob/main/LICENSE.md) | ❌ do not confuse with Apache-licensed DEIM v1 |
| YOLOX (used inside rtmlib) | Apache-2.0 | Apache-2.0 [14] | ✅ |
| NanoDet-Plus | Apache-2.0 | Apache-2.0 [13] | ✅ but unmaintained since Jan 2023 |
| MediaPipe Tasks (`mediapipe`) | Apache-2.0 [15] | Google model cards define intended use [19][23][25] | ✅ |
| rtmlib / RTMPose / RTMO / RTMW | Apache-2.0 [26][27] | Apache-2.0 (OpenMMLab) | ✅ |
| MoveNet | Apache-2.0 (TF Hub/Kaggle listing) [28] | UNVERIFIED for the Kaggle-hosted weights | ✅ but legacy (TensorFlow) |
| YuNet (OpenCV Zoo) | MIT [29] | MIT | ✅ |
| SCRFD / InsightFace models | MIT code | **Non-commercial research only** [30] | ❌ avoid |
| SAM 2.1 | Apache-2.0 | Apache-2.0 [31] | ✅ (GPU) |
| SAM 3 / SAM 3.1 | SAM License | Custom SAM License, gated on HF, CUDA ≥ 12.6 [32] | ❌ overkill and restrictive |
| EfficientSAM, MobileSAM | Apache-2.0 | Apache-2.0 [33] | ✅ |
| EdgeSAM | S-Lab License 1.0 [33] | same | ❌ |
| SegFormer-B2 "clothes" (mattmdjaga) | NVIDIA Source Code License | Model card `license: other`, pointing to NVIDIA's licence: **"non-commercially… research or evaluation purposes only"** [34] | ⚠ grey zone for a public exhibit, so ask legal |
| SCHP human parsing | MIT code [35] | Weights trained on LIP/ATR (dataset terms UNVERIFIED) | ⚠ |
| OpenAI CLIP | MIT | Model card: **"Any deployed use case… is currently out of scope"** [38] | ⚠ only with in-domain testing and a fixed taxonomy (§3f) |
| OpenCLIP (LAION) | MIT | Same out-of-scope language in the model card [40] | ⚠ same |
| **SigLIP 2** | Apache-2.0 | Apache-2.0 [41] | ✅ preferred |
| MobileCLIP / MobileCLIP2 | MIT code | **Apple AMLR licence: "non-commercial scientific research"** only [43] | ⚠ an exhibit is not research, so avoid |
| EVA-CLIP | MIT [44] | MIT (weights hosted on HF, terms not re-checked) | ✅ |
| VLMs | see §3g | Apache: SmolVLM2, Moondream 2, Qwen3-VL, InternVL3.5, Gemma 4. Restrictive: Qwen2.5-VL-3B (research-only), Gemma 3/PaliGemma 2 (Gemma ToU), Moondream 3 (BSL 1.1), LFM2-VL (LFM 1.0) | — |
| ImageBind | CC-BY-NC-4.0 | CC-BY-NC-4.0 [65] | ❌ |
| LanguageBind | MIT code | Data CC-BY-NC [66] | ⚠ |
| ONE-PEACE | Apache-2.0 | 4B params, CUDA, last update July 2023 [67] | ✅ legally, ❌ practically |
| LAION-CLAP / MS-CLAP | CC0-1.0 / MIT [68] | same | ✅ (MS-CLAP repo archived 2026-09-15) |
| MiVOLO (age/gender) | Apache-2.0 | Demo uses a YOLOv8 person+face detector (AGPL) [60] | ❌ (ethics, see §3h) |
| ByteTrack / `supervision` | MIT [72] | — | ✅ |

**AGPL in practice.**
- The AGPL §13 "Remote Network Interaction" clause obliges you to offer source to users interacting with a *modified* program over a network [6]. Ordinary GPL obligations trigger when copies are *conveyed*.
- A kiosk that the team never distributes might not trigger either. But Ultralytics' own reading is broader: the "entire project" must be open-sourced, including trained weights [2].
- Apache-2.0 code *can* be combined into an AGPL/GPLv3 project (the FSF lists Apache-2.0 as GPLv3-compatible [7]).
- The real risks are elsewhere:
  - the **robot vendor's SDK** may be proprietary;
  - other MSCA sites may later want a copy (that is conveying);
  - a later spin-off would be blocked.
- **Recommendation:** treat Ultralytics as an optional, separately-processed baseline. All of its capabilities (detect, pose, segment) have Apache equivalents above.

---

## 3. Component analysis

### (a) Person detection

| Model | Size | COCO AP (50:95) | Official latency | Our measurement | Packaging | Verdict |
|---|---|---|---|---|---|---|
| YOLO26n (Jan 2026, NMS-free) | 2.4 M | 40.9 | 38.9 ms CPU-ONNX; 1.7 ms T4-TRT [1] | 15–19 ms NPU/iGPU, 59 ms OV-CPU | `ultralytics` | AGPL. Baseline only |
| YOLO11n | 2.6 M | 39.5 | 56.1 ms CPU-ONNX; 1.5 ms T4 [4] | 70 ms PyTorch CPU | `ultralytics` | AGPL |
| **YOLOX-tiny / -m** (via rtmlib) | 5.05 M (YOLOX-tiny, per Hailo Model Zoo table) [corrected by verifier: was "~5 M UNVERIFIED"; https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst] / ~25 M (YOLOX-m, UNVERIFIED) | — | — | det+pose pipeline 52 ms on iGPU (2 people) | `rtmlib` (onnxruntime / OpenVINO / TensorRT) | ✅ **CPU/iGPU default** |
| RTMDet-nano | 0.99 M | 40.3 (as listed by MMPose) | 12.4 ms CPU i7-11700 (ORT); 2.5 ms GTX 1660Ti [27] | — | ONNX via rtmlib/MMDeploy | ✅ |
| **RF-DETR-N / -S** | 30.5 M / 32.1 M | 48.4 / 53.0 | 2.3 / 3.5 ms T4-TRT-FP16 [8]. Official CPU cookbook, RF-DETR-S on a 4-core Colab CPU: **312 ms (OpenVINO fp32), 368 ms (ONNX Runtime), 346 ms (PyTorch)**; "No format wins decisively"; fp16 did not help on CPU [73] | not measured | `pip install rfdetr`, ONNX/OpenVINO export [9][73] | ✅ **GPU default**; ❌ CPU (≈ 3 fps) |
| RT-DETRv2-R18 | 20 M | 46.5 (v1 R18) | 217 FPS T4 [10] | — | HF `transformers` [11] | ✅ |
| D-FINE-N / DEIM | — | — | — | — | GitHub, HF | ✅ (Apache) |
| MediaPipe EfficientDet-Lite0 int8 | 4.6 MB file | (COCO, 80 classes) | 29 ms Pixel 6 CPU [17] | 45 ms | `mediapipe` | ✅ simple fallback |
| NanoDet-Plus-m 320 | 1.17 M | 27.0 | 12 ms on 4×Cortex-A76 [13] | — | NCNN/ONNX | ✅ Pi-class only |
| OpenCV DNN | runtime, not a model | — | — | YuNet fine. OpenCV 5.0 warns "Targets are not supported by the new graph engine for now" (MEASURED log) | `opencv-python` | Use for YuNet. ONNX Runtime/OpenVINO for the rest |

**Evidence for explanations:**
- *Per-modality:* camera only.
- *Per-region:* the box and its score. Show "I found a person here (92 % sure)".
- Use the detector's COCO classes **backpack, handbag, umbrella, tie, sports ball, teddy bear, cell phone, book, bottle, cup** as an "objects with you" channel. These are more reliable than zero-shot CLIP for those categories (Table 3).

### (b) Pose: gestures, proxemics, engagement

| Model | Keypoints | Multi-person | Latency | Licence | Notes |
|---|---|---|---|---|---|
| **MediaPipe Pose Landmarker** lite/full/heavy | 33 (+3D world coords, optional segmentation mask) [18] | Officially out-of-scope; "tracks only one person" [19] | MEASURED 40–51 ms CPU | Apache | Fairness eval across 14 regions: PDJ full 91.8 % ± 1.4, heavy 94.2 % ± 1.3 [19]. Single person, < 4 m, head visible |
| **RTMPose-t/s/m** (top-down, via rtmlib) | 17 body. RTMW: 133 whole-body incl. hands and face | ✅ via detector | RTMPose-m 11.1 ms CPU / 2.3 ms GTX 1660Ti per person; AP 75.8 [27]. MEASURED pipeline 52 ms iGPU | Apache | Best permissive multi-person option. `rtmlib` needs only numpy/opencv/onnxruntime [26] |
| RTMO (one-stage) | 17 | ✅ | — | Apache | Constant time regardless of person count |
| MoveNet Lightning/Thunder/MultiPose | 17 | MultiPose ≤ 6 people | ~60 / 155 ms CPU FP16, as quoted from TensorFlow's MoveNet benchmarks (device not re-checked, UNVERIFIED) [28] | Apache (UNVERIFIED for current weights) | TensorFlow dependency, 2021 vintage. Not recommended |
| YOLO26n-pose | 17 | ✅ | 40.3 ms CPU-ONNX, 1.8 ms T4 [3]. MEASURED 15–18 ms NPU/iGPU | AGPL | Baseline only |

**Recipes (all rule-based, so they are explainable and need no training data):**

| Behaviour | Signal | Rule sketch | Uncertainty shown to visitor |
|---|---|---|---|
| Waving | wrist relative to elbow and shoulder | wrist above elbow, plus ≥ 2 direction changes of wrist-x (normalised by shoulder width) within 1.5 s | rule margin (amplitude, frequency) and keypoint confidences |
| Hands up | wrists vs nose/shoulders | both wrists above nose for ≥ 0.5 s | — |
| Jump | hip/ankle vertical velocity | both ankles and hips rise > 0.15 × torso length then return, within 0.8 s. Needs ≥ 15 fps, so pose must run at 15+ Hz (iGPU/NPU) | frame-rate warning |
| Crouch / sit | hip–knee–ankle angles | knee angle < 100° | — |
| Facing the robot | nose + both eyes visible; shoulder-width / torso-height ratio; head yaw | yaw within ±30° | yaw ± jitter |
| Distance zone (proxemics) | box height, shoulder width, face width (pinhole: d ≈ f·W/w) | report **zones** (close / talking distance / far) and *changes* ("you came closer"), not metres | **Show the ambiguity explicitly.** Small in the image can mean far *or* small. A child and an adult at different distances can look identical. This is a great XAI lesson. Use the dog's depth sensor if it has one (other track) |
| Engagement | facing × proximity × dwell time | weighted score shown as a meter, with each component visible | components visible |

**Evidence for explanations:**
- *Per-region:* the skeleton overlay. Highlight the keypoints the rule used (e.g. the wrist trajectory trace for "waving").
- *Per-modality:* camera only.
- *Uncertainty:* per-keypoint visibility/presence scores, which MediaPipe provides as `visibility`/`presence` [18] and RTMPose as keypoint scores.

### (c) Face detection only (no recognition)

| Model | Size | Range | Latency | Licence | Verdict |
|---|---|---|---|---|---|
| **YuNet 2023mar** (`cv2.FaceDetectorYN`) | 232 KB | faces ~10–300 px. WIDER Face AP 0.834/0.824/0.708 (easy/medium/hard) [29] | MEASURED 10–13 ms CPU @640×360 | MIT | ✅ **primary** (works at stand distances; returns 5 landmarks). OpenCV Zoo's default file is now `face_detection_yunet_2026may.onnx`: the same weights re-exported with dynamic H/W for the OpenCV 5.x ONNX Runtime engine (`OPENCV_FORCE_DNN_ENGINE=4`) [29]. Use it with OpenCV 5.0; it may also remove the "new graph engine" warning in §3(a). (The README's eval table gives AP 0.8844/0.8656/0.7503; 0.834/0.824/0.708 is from its header text.) |
| MediaPipe Face Detector, BlazeFace short-range | 230 KB, 128×128 input | "selfie-like" range [20] | MEASURED 4 ms | Apache | ✅ for close-up only. Missed faces in Table 2. Full-range variants are listed in the docs [20] |
| MediaPipe Face Landmarker | 3.8 MB bundle | needs a reasonably large face | MEASURED ≥ 15 ms | Apache | ✅ **for head pose only** (facial transformation matrix) [21]. Run on the primary visitor's face crop |
| SCRFD (InsightFace) | — | strong | — | ❌ models non-commercial [30] | avoid |

- **Head pose / attention.** Use either the Face Landmarker transformation matrix (yaw/pitch/roll) [21], or `cv2.solvePnP` on YuNet's 5 landmarks with a generic 3D face template (cheap, no extra model).
- **Blendshapes.** These are 52 expression coefficients meant for avatar rendering [21].
  - The AI Act says detecting "a frown or a smile" is *not* emotion recognition **unless used to infer emotions** [63 recital 18].
  - The Commission guidelines give the examples: "The observation that a person is smiling is not emotion recognition", but "Concluding that a person is happy is emotion recognition" [64].
  - The emotion-recognition prohibition (Art. 5(1)(f)) covers workplaces and *education institutions*. The guidelines describe these as institutions that are normally accredited, but also say the reference "is broad", covers public and private institutions, and has "no limitation as regards the types or ages of pupils… or of a specific environment" [64 §255]. A stand visited by *organised school groups* is therefore not clearly outside the scope. **Treat "no emotion inference" as a hard legal constraint**, not just good practice.
  - If you show anything, show "smile shape detected (mouth corners up)". Then make the limitation the lesson: *"I can see the shape of your mouth. I cannot know how you feel."*
- **Never** compute face embeddings (no ArcFace etc.). Tracking uses boxes only (ByteTrack).

### (d) Hand gestures

**MediaPipe Gesture Recognizer** [22][23]:
- Classes: `None, Closed_Fist, Open_Palm, Pointing_Up, Thumb_Down, Thumb_Up, Victory, ILoveYou`. Uses 21 hand landmarks.
- Latency: 16.8 ms CPU on Pixel 6. MEASURED ≥ 18 ms. `num_hands` defaults to 1.
- Customisable with Model Maker.
- The model card says it is "not tested in in-the-wild … low light, motion blur" conditions, and reports a fairness evaluation across Monk skin-tone groups [23].

**Practical trick for 1.5–3 m distance.** Hands are tiny in a 640 px frame, so:
1. take wrist keypoints from the body pose;
2. crop an upscaled square around each wrist (≈ 1.2 × forearm length);
3. run the Gesture Recognizer on the crop.

**Evidence for explanations:** a hand-landmark overlay on the crop, the class probability bar, and "I looked at your right hand".

### (e) Clothing colour and appearance

**Recommended pipeline (v1, CPU-friendly):**
1. Build torso and leg polygons from pose keypoints (shoulders→hips, hips→knees→ankles), shrunk by 15 % to avoid edges.
2. Intersect them with the person mask. The Pose Landmarker can output a segmentation mask itself (`output_segmentation_masks`) [18]. Otherwise use the binary selfie segmenter (≈33 ms CPU in Google's published benchmark [24]).
3. Remove skin-like pixels (or use the multiclass model's *clothes* class, but only at ≤ 1 Hz, since it costs 216 ms).
4. Colour-correct with a **grey card on the stand wall**, imaged at start-up (or gray-world as a fallback).
5. Convert to CIELAB and run k-means with k = 3 on ≤ 2,000 sampled pixels. Report the dominant cluster and its share.
6. Name the colour in two layers:
   - **11 basic colour terms** with probabilities, using the van de Weijer et al. learned colour-name model [37]. It gives *P(name | colour)*, which is exactly the uncertainty you want to display ("70 % blue, 25 % purple").
   - Optional fun names from the **XKCD survey** (954 names, CC0) [36], by nearest neighbour in Lab ("dusty teal").
7. Aggregate over 1–2 s of frames. Abstain when lighting is poor (low L*, a strong colour cast, or motion blur measured by variance of the Laplacian).

**Segmentation and parsing options:**

| Option | Licence | Cost | Use |
|---|---|---|---|
| MediaPipe selfie (binary) / multiclass (bg, hair, body-skin, face-skin, **clothes**, others) | Apache | 33 ms / 218 ms CPU (Google benchmark) [24]; MEASURED 216 ms | v1 (multiclass at ≤ 1 Hz). Model card warns of degradation with backlight, occluders and fast motion [25] |
| SAM 2.1 tiny/small (38.9 M / 46 M) | Apache-2.0 | 91 / 85 FPS on A100 [31] | GPU laptop: keypoint-prompted crisp masks |
| EfficientSAM / MobileSAM | Apache-2.0 | MobileSAM ≈ 424 ms CPU vs EdgeSAM 259 ms (figures quoted from EdgeSAM comparisons, UNVERIFIED) [33] | not needed |
| SAM 3 / 3.1 (text-prompted "red shirt") | SAM License, 848 M, CUDA | [32] | ❌ |
| SegFormer-B2 clothes (18 ATR labels: hat, sunglasses, upper-clothes, skirt, pants, dress, belt, shoes, bag, scarf…) | NVIDIA non-commercial | 27.4 M params, mIoU 0.69 [34] | ⚠ only if legal OKs it |
| SCHP (LIP 20 / ATR 18 / Pascal 7 classes) | MIT code, data terms UNVERIFIED | needs InPlaceABN CUDA extension [35] | ❌ for v1 |

**Do not use gender-coded garment classes** (dress, skirt) as visitor attributes. They act as a gender proxy. Upper / lower / shoes / headwear is enough.

**Evidence for explanations:**
- *Per-region:* the polygon or mask actually sampled, plus the colour swatch.
- *Uncertainty:* the colour-name distribution, plus a "lighting quality" indicator.
- *Per-modality:* camera.

### (f) Zero-shot attribute scoring (CLIP family)

**What the evidence says:**
- **Deployment caveat.** OpenAI's model card puts *any* deployed use out of scope unless there is "thorough in-domain testing … with a specific, fixed class taxonomy". It states that "surveillance and facial recognition are always out-of-scope" [38]. LAION's cards repeat this [40].
- **Class design drives harms, especially for children.** In OpenAI's FairFace probe, people aged 0–20 were the most likely to be put into crime-related (~18 %) and non-human (~14 %) classes. Adding a `child` class "drastically reduced" this [39], but unevenly: in the paper's Table 7 the share in crime-related or non-human classes fell from 35.0 % to 4.3 % for ages 3–9, yet only from 29.5 % to **14.7 %** for ages 10–19, which is exactly our 8–14 audience. Class design alone does not make person-level labels safe for older children. Never run an open or uncurated label set over people.
- **Composition and attribute binding are weak.** CLIP-style models behave like bags of words, which hurts colour↔garment binding [45]. "CLIP-blind" pairs fail on orientation, presence, colour and counting [46]. So *never* ask CLIP "red shirt and blue trousers?". Get colour from pixels (§e), and use CLIP only for *presence* questions on tight crops.
- **Calibration.** Zero-shot CLIP is miscalibrated across prompts, datasets and architectures. A single learned temperature per model generalises well [47].
- **Prompt ensembling** (80 templates) adds +3.5 % on ImageNet. Prompt engineering and ensembling together add almost 5 % [39].
- **Specialist literature.** Pedestrian-attribute work shows that *plain* zero-shot CLIP is only moderate. Prompt-tuned or fine-tuned CLIP is needed for strong results (e.g. PromptPAR [49]). No paper I found gives clean zero-shot numbers for hats, glasses or backpacks on children: **UNVERIFIED, so we must measure it.**

**Models:**

| Model | Licence | Notes | MEASURED (this laptop) |
|---|---|---|---|
| **SigLIP 2 ViT-B/16 (86 M vision)** | Apache-2.0 [41] | **Sigmoid loss gives independent per-label scores** [42], which suits multi-label attributes. Multilingual (Polish prompts possible). Training mix includes de-biasing [41] | 20 ms NPU / 45 ms iGPU / 131–500 ms CPU |
| OpenAI CLIP / OpenCLIP ViT-B/32 | MIT, but model-card restrictions [38][40] | weakest of the set in Table 3 | 13 ms NPU / 69–134 ms CPU |
| EVA02-CLIP-B/16 (149 M, 74.7 % IN zero-shot) | MIT [44] | alternative | — |
| MobileCLIP2-S0 (71.5 % IN, 1.5 + 3.3 ms iPhone) | weights research-only [43] | ❌ for the exhibit | — |

**Recommended procedure:**
1. **Vetted attribute list** (non-bodily, changeable): glasses, sunglasses, hat/cap, hood up, backpack, scarf, striped or patterned top, graphic/print on top, holding a ball / toy / book / phone / bottle.
2. **Region-specific crops from keypoints**: head crop for hat/glasses, torso for stripes/print/backpack straps, wrist crops for held objects.
3. **Binary prompt pairs with ensembles** (5–10 templates each side, English or Polish). Precompute the text embeddings at start-up.
4. **Calibrate per attribute** with Platt or temperature scaling on 150–300 locally recorded, *consented* stand images (team members, colleagues, adult volunteers, props). Pick thresholds for ≥ 90 % precision, and keep an explicit **"not sure"** band.
5. **Temporal aggregation**: mean logit over 1–2 s, with hysteresis.
6. **Report only above threshold.** Below it, say "I can't tell".

**Evidence for explanations:**
- *Per-region:* the exact crop. Optionally also a 4×4 **occlusion map** on the same model (16 forward passes ≈ 0.3 s on the NPU, fine at 1 Hz). This is more faithful than Grad-CAM-style saliency [70].
- *Uncertainty:* the calibrated probability with a "not sure" band.
- *Counterfactual:* "If I couldn't see your head, I couldn't tell about the hat."

### (g) Small VLMs for grounded descriptions

| Model | Params | Licence | Grounding | CPU (laptop) | 8 GB NVIDIA (RTX 4060 class) |
|---|---|---|---|---|---|
| SmolVLM2-256M / 500M / 2.2B | 0.26 / 0.5 / 2.2 B | Apache-2.0 [50] | no boxes | **MEASURED 24–38 s/sentence** (fp32, under load) | Paper (SmolVLM v1): GPU RAM at batch 1 = 0.8 / 1.2 / 4.9 GB; A100 batch-1 throughput 0.8 / 0.7 / 0.6 examples/s; L4 peak 2.7 / 1.4 / 0.25 examples/s [75]. RTX 4060 not published |
| Florence-2 base / large | 0.23 / 0.77 B | MIT [52] | ✅ OD, phrase grounding, dense region captions | not measured | fits easily (latency UNVERIFIED). Now **native in `transformers`** (`Florence2ForConditionalGeneration`, checkpoints `florence-community/Florence-2-base`), so `trust_remote_code` is no longer needed [77] |
| Moondream 2 | 1.93 B | Apache-2.0 [51] | ✅ detect / point / caption / query | not measured | 4-bit build: **2,450 MB VRAM, 184 tokens/s on an RTX 3090** (vendor figure) [76] |
| Moondream 3 (preview) | 9 B total / 2 B active MoE | BSL 1.1 + use grant [51] | ✅ | CUDA required | ❌ (size and licence) |
| Moondream 3.1 9B-A2B (final, released 7 Jul 2026) [added by verifier] | 9 B total / 2 B active | proprietary **"Moondream License"** (not Apache) | ✅ | GGUF CPU builds exist; NVIDIA needs ≥ 10 GB VRAM per vendor | ❌ for 8 GB GPU; licence needs legal review (https://moondream.ai/models/moondream_3-1_9B_A2B) |
| Qwen2.5-VL-3B | 3 B | **Qwen RESEARCH licence: non-commercial "research or evaluation" only** [53] | ✅ | — | ❌ licence |
| **Qwen3-VL-2B / 4B** | 2.13 / 4.44 B | Apache-2.0 [54] | ✅ 2D grounding, GGUF available | slow | 2B fits in bf16. 4B needs a 4-bit quant (UNVERIFIED latency) |
| PaliGemma 2 3B, Gemma 3 4B | 3.0 / 4.3 B | Gemma Terms of Use, gated [55] | PaliGemma: detect/segment | — | ⚠ licence |
| **Gemma 4 E2B / E4B** (released 2 Apr 2026 [78]) | 2.3 B effective (5.1 B with embeddings) / 4.5 B effective (8 B with embeddings) | **Apache-2.0** (first Gemma generation without the Gemma ToU) [56] | object detection, pointing; also audio input | — | E2B plausible in 8 GB (UNVERIFIED). Google says E2B is "3x faster than the E4B" on-device [78] |
| InternVL3-1B / InternVL3.5-1B | 0.94 / 1.06 B | Apache-2.0 (HF tag; v3 card also mentions MIT + Qwen2.5 component) [57] | ✅ | — | fits |
| LFM2-VL-450M / 1.6B | 0.45 / 1.6 B | LFM Open License 1.0: commercial use only below US$10 M annual revenue [58] | — | edge-oriented | ⚠ (non-commercial use OK) |
| **Qwen3.5-2B** (Feb 2026, natively multimodal: image + video + text) | 2 B | Apache-2.0 [80] | not mentioned on the card (UNVERIFIED) | not measured | newer successor to Qwen3-VL-2B. Card recommends it for "prototyping, task-specific fine-tuning"; thinking mode "more prone to entering thinking loops", so use non-thinking mode [80]. Evaluate alongside Qwen3-VL-2B |
| LFM2.5-VL-450M (released 8 Apr 2026 [corrected by verifier: not 2025-11-28, which is the date of the LFM2 technical report cited on the card; Liquid AI blog https://www.liquid.ai/blog/lfm2-5-vl-450m. Vendor latency at 512×512: 242 ms Jetson Orin, 944 ms Ryzen AI Max+ 395]) | 0.45 B | LFM 1.0 (same US$10 M threshold) | bounding-box prediction per card | GGUF/ONNX builds for CPU | successor to LFM2-VL. Same licence caveat [81] |

**Risks:**
- **Hallucination.** VLMs invent objects that frequently appear or co-occur in training data (POPE [59]). CLIP-based encoders share CLIP's blind spots [46].
- **Unprompted sensitive attributes.** Our SmolVLM2 test immediately said "the man on the left…", a gender inference nobody asked for.
- **Latency.** Tens of seconds on this CPU (MEASURED). On a GPU, the SmolVLM paper reports only 0.6–0.8 examples/s at batch 1 even on an A100 [75], i.e. ≈ 1.2–1.7 s per answer. Expect ~1–2 s per sentence on an RTX 4060 class GPU (extrapolation, UNVERIFIED). Fine for a "diary", not for the live loop.

**If a VLM is used** (GPU laptop only):
- (i) **Verifier mode.** Ask yes/no questions about a single crop ("Is the person in this crop holding a ball? Answer yes or no."), and treat the answer as one more piece of evidence with its own calibrated reliability.
- (ii) **Constrained generation.** Return JSON from a fixed whitelist vocabulary, and post-filter it against a deny-list (gender words, age words, body words, ethnicity, emotion words).
- (iii) **Grounded outputs** (Florence-2 / Moondream 2 / Qwen3-VL boxes), so the UI can show where the claim came from.
- Prefer **Qwen3-VL-2B or Gemma 4 E2B** (Apache, grounding) or **Florence-2-base** (MIT, tiny, grounded captions).

### (h) Apparent age estimation: **do not use**

- **Accuracy is insufficient for 8–14-year-olds, even in the best case.** NIST FATE AEV (NIST IR 8525, May 2024) tested six commercial algorithms on *high-quality frontal visa photos* of Mexican children [62]. Mean absolute error at ages 8–14 was **1.42–5.34 years** depending on algorithm and age (Table 19: lowest 1.42 at age 8, highest 5.34 at age 14). At age 12 it ranged from 1.97 (best) to 4.68 years. The share of estimates within ±1 year at age 12 was only 0.12–0.40.
- NIST notes that accuracy is "strongly influenced by algorithm, sex, image quality, region-of-birth, age itself", and that webcam-type "border" images are harder [62].
- A low, moving robot-dog camera in exhibition lighting is far worse than visa photos. Open models such as MiVOLO publish only adult-dominated aggregate MAE (≈ 3.7–4.2 years) and no child-specific results. Its demo pipeline also predicts gender and depends on an AGPL YOLOv8 detector [60]. FairFace models predict race and gender [61].
- **Legal and ethical.** Age is explicitly listed as a biometric-categorisation category (recital 16: "sex, age, hair colour, eye colour, tattoos, behavioural or personality traits…") [63]. Deployers of biometric categorisation systems must inform the people exposed (Art. 50(3)) [63]. Categorising by *sensitive* attributes is prohibited or high-risk (Art. 5(1)(g); Annex III 1(b)) [63]. Telling a child "you look 7" when they are 11 is also a harm in itself.
- **Safer alternative:** none. Turn the absence into content. Show a card saying **"Things I will NOT guess about you: your age, whether you are a boy or a girl, where you come from, how you feel, who you are."** Then demonstrate *why*: show the size–distance ambiguity live ("big in my camera = close OR tall?").
- **Do not** use "height in frame" as an age proxy. It is age-correlated (so still a proxy), unreliable from a low, moving camera, and confounded by distance.

### (i) Cross-modal shared embeddings

| Approach | Status | Verdict |
|---|---|---|
| ImageBind (6 modalities, `imagebind_huge`) | CC-BY-NC-4.0 code and weights [65] | ❌ licence and size |
| LanguageBind (video/audio/depth/thermal) | MIT code. Training data CC-BY-NC [66] | ⚠ heavy, GPU |
| ONE-PEACE (vision-audio-language, 4B) | Apache-2.0. CUDA, stale since 2023 [67] | ❌ practicality |
| **Concept bottleneck in a shared TEXT concept space** (recommended) | each modality → its own zero-shot encoder → calibrated probabilities for named concepts → interpretable fusion | ✅ **feasible on the laptop** |

**How the concept bottleneck works:**
- **Image concepts:** SigLIP 2 on crops, plus rule-based pose concepts (waving, jumping…).
- **Audio concepts:** LAION-CLAP (CC0, `laion-clap`. Checkpoint `music_speech_audioset_epoch_15_esc_89.98.pt` encodes ≈ 90 % ESC-50 zero-shot [68]) or MS-CLAP (MIT, `msclap`, 93.9 % ESC-50 [68], repo archived Sept 2026). Examples: "clapping", "laughing", "whistling", "speech present".
- **Speech:** keywords from ASR (other track).
- **Fusion:** each concept is a calibrated probability, *not* a raw cosine, because scores from different encoders are not comparable.
  - Fuse with a transparent rule (noisy-OR / naive-Bayes log-odds sum / small logistic layer), in the spirit of concept bottleneck models [69].
  - Each final inference ("you are excited to play" → **no**, that's emotion; use e.g. "you are trying to get my attention") then decomposes into per-concept, per-modality log-odds contributions.
- **Sensor toggles** simply remove that modality's concept inputs. The UI animates how the belief and its uncertainty change. This is the clearest possible demonstration of per-modality evidence.

### (j) Scene, context and groups

- **People count:** detector count after a minimum box size and a "within the stand area" mask (ignore people walking behind).
- **Primary visitor:** the tracked person who is closest (largest box), central, and facing the robot for ≥ 1 s. Only the primary visitor gets an individual "profile".
- **Group mode:** others are reported only as counts or group-level actions ("I see 3 people; 2 are waving").
- **Bystanders:** never build a profile for them. YuNet and the detector *will* pick them up (Table 2).
- **Lighting and quality** (cheap, and they double as explanations of low confidence):
  - mean L*, plus a colour-cast check from mean a*/b* → "too dark to judge colours";
  - variance of the Laplacian → "you moved too fast, I saw a blur";
  - backlight check (bright background vs dark person mask) → MediaPipe's segmenter card warns about backlit subjects [25].
- **Background:** do **not** describe it (it could reveal other people or the location). Optionally show a "background removed" view to make privacy-by-design visible.

---

## 4. Explainability hooks: what each component can honestly show

| Component | Per-modality evidence | Per-region evidence ("where I looked") | Uncertainty |
|---|---|---|---|
| Person detector | camera | box | detector score; stability over frames |
| Tracker (ByteTrack) | camera | track ID colour (no identity) | track age |
| Pose (MediaPipe / RTMPose) | camera | skeleton; highlighted keypoints per rule | keypoint visibility/presence; rule margin |
| Gesture rules | camera (pose time series) | wrist/hip trajectory trace | amplitude/frequency vs threshold; fps warning |
| Hand gesture | camera | hand crop + 21 landmarks | class probabilities |
| Face box / head pose | camera | face box + yaw arrow | detector score; yaw jitter |
| Clothing colour | camera | sampled polygon or mask + swatch | colour-name distribution; lighting index |
| Zero-shot attribute | camera | exact crop (+ optional occlusion map) | calibrated P with a "not sure" band; number of frames |
| Audio concepts (CLAP) | microphone | time segment of the waveform | calibrated P |
| Fusion (concept bottleneck) | all enabled sensors | links back to the above | per-concept log-odds bars; what changes when a sensor is toggled off |

**Implementation note.** Every module should emit the same *evidence record*:

```
{sensor, model+version, region (box/polygon/mask/time-span), concept, value, calibrated_p, n_frames, timestamp}
```

Inferences then cite record IDs. The visualisation renders from records only, so the UI cannot show anything the pipeline did not actually compute. Keep records in RAM only and drop them when the visit ends.

---

## 5. Recommended stacks

### (1) CPU-only prototype: dev laptop (Core Ultra 7 255U), using OpenVINO on iGPU/NPU

| Stage | Choice | Rate | Expected cost (from Table 1) |
|---|---|---|---|
| Capture | USB webcam or the dog's stream at 640×360–640×480 | 15–30 fps | — |
| Person detection + pose | `rtmlib` lightweight (YOLOX-tiny + RTMPose-s), OpenVINO **GPU** | 10–15 Hz | ~52 ms for 2 people (MEASURED) |
| Primary-visitor detail pose | MediaPipe Pose Landmarker *full* on the primary visitor crop, with segmentation mask | 10 Hz | ~50 ms CPU |
| Tracking | `supervision` ByteTrack (MIT) | per frame | < 1 ms (UNVERIFIED, trivial) |
| Faces + head pose | YuNet + solvePnP | 10 Hz | ~11 ms CPU |
| Hand gestures | MediaPipe Gesture Recognizer on wrist crops (primary visitor) | 5 Hz | ≥ 18 ms |
| Clothing colour | keypoint polygons ∩ pose mask → Lab k-means → colour names | 2 Hz | a few ms (UNVERIFIED) |
| Accessories | SigLIP 2 B/16 on 3–4 crops, OpenVINO **NPU** | 1 Hz | 4 × 20 ms |
| VLM | none | — | — |

This fits comfortably and leaves the CPU for audio/ASR. **Fallback** if OpenVINO GPU/NPU fails: run everything on CPU at reduced rates (pose 5 Hz, attributes 0.5 Hz). Note: the NPU first compile takes 24–36 s, so cache compiled blobs (OpenVINO `CACHE_DIR`).

### (2) Exhibition laptop with a mid-range NVIDIA GPU (RTX 4060-class, 8 GB)

- **Same architecture.** Switch runtimes to ONNX Runtime CUDA/TensorRT EP (rtmlib supports TensorRT/CUDA [26]).
- **Detection:** **RF-DETR-S** (Apache, 53.0 AP, 3.5 ms T4 [8]) or D-FINE-S.
- **Pose:** RTMPose-m (11 ms CPU / 2.3 ms GTX 1660Ti [27]) or **RTMW-m whole-body** (133 kps incl. hands and face, which can replace separate hand and face models).
- **Attributes:** SigLIP 2 B/16 at 384 px, or So400m on crops at 2–5 Hz.
- **Optional:**
  - SAM 2.1-tiny (Apache) with keypoint prompts for crisp clothing masks.
  - A VLM *verifier*: Qwen3-VL-2B / Qwen3.5-2B or Gemma 4 E2B (all Apache) or Florence-2-base (MIT, native in `transformers` [77]). At most one call every 3–5 s, with constrained output. Budget VRAM: SmolVLM-2.2B needs 4.9 GB at batch 1 [75]; Moondream 2 4-bit 2.45 GB [76]; this must coexist with ASR/LLM/TTS from other tracks on 8 GB.
- **RTX 4060 latencies are UNVERIFIED** (no hardware available). The T4 TensorRT figures above are the best published proxy.
- Keep the CPU/OpenVINO path as a hot fallback so the exhibit survives a driver crash.
- **Pragmatic note:** Table 1 suggests a Core Ultra-class laptop with an NPU covers the *vision* stack. A discrete GPU is mainly justified by VLM/LLM/TTS needs from other tracks.

### (3) Raspberry Pi 4/5 onboard the robot dog

| Option | What runs | Evidence |
|---|---|---|
| Pi 4 | Camera capture, H.264/MJPEG streaming, maybe YuNet "face present" | Pi 4 latencies for these models UNVERIFIED. Treat it as a streamer only |
| Pi 5 (CPU) | Person detection at ~5–15 fps: NanoDet-Plus / YOLOX-nano via NCNN or ONNX Runtime; MediaPipe also ships Linux ARM64 wheels [15] | YOLO26n: NCNN 67 ms, ONNX 126 ms, PyTorch 299 ms per frame at 640 (official Ultralytics Pi 5 table [5], AGPL model). NanoDet-Plus-m-320: 12 ms on 4×A76 (Pi 5 uses A76 cores; the published device differs) [13] |
| Pi 5 + **AI HAT+** (Hailo-8L 13 TOPS / Hailo-8 26 TOPS, from US$70) | detection / pose / segmentation offload | [71]. Hailo Model Zoo, Hailo-8L, batch 1 (chip throughput, not end-to-end on the Pi): **YOLOX-tiny 214 fps** (416², 32.6 float mAP / 31.4 on-chip mAP, Apache), NanoDet-RepVGG 620 fps (416², 29.3 float / 28.6 on-chip mAP) [corrected by verifier: the quoted mAPs are the float-model values; Hailo's quantised "Hardware mAP" is lower; figures measured with an i5-9400 host over PCIe Gen3 x4, not a Pi], YOLOv8n 202 fps (AGPL weights); pose: **CenterPose-RegNetX-800MF 85 fps** (512², 43.0 AP; weight licence UNVERIFIED), YOLOv8s-pose 107 fps (55.7 AP, AGPL weights) [74]. Hailo's ready-made Pi pose demo uses `yolov8s_pose` on Hailo-8L and `yolov8m_pose` on Hailo-8 [74], so it inherits the Ultralytics AGPL question |
| Pi 5 + **AI HAT+ 2** (Hailo-10H, 40 TOPS INT4, 8 GB, **US$200 listed Oct 2026**) | the above plus small LLM/VLM | [71] |
| **Raspberry Pi AI Camera** (Sony IMX500, US$70, all Pi models) | on-sensor detection, so only metadata leaves the sensor (a privacy plus) | [71] |

**Recommendation.** The Pi does capture, streaming and **local safety**: a "person too close, stop walking" detector, which must not depend on Wi-Fi. If that detector needs a neural net, the licence-clean option is **YOLOX-tiny / NanoDet on the Pi 5 CPU (NCNN/ONNX), or on an AI HAT+ (Hailo-8L: YOLOX-tiny 214 fps chip throughput [74])**, not the Ultralytics models that Hailo's demos ship by default. Everything that builds a person profile runs on the stand laptop, on a closed local network with no cloud, which keeps one controlled place for data deletion. The dog's camera height (low, looking up at children) is a **feasibility risk**: pose and attribute models are trained mostly on eye-level photos, and children at 0.5–1 m from a dog-height camera will be cut off at the torso. Plan a **stand-mounted "robot eye" camera** (~1.0–1.2 m) as the primary vision source, or put the dog on a podium. Test this in week 1.

---

## 6. Recommendations for our demonstrator

1. **Lock the licence policy now:** Apache/MIT/CC0 only in the shipped core. Keep a `THIRD_PARTY_LICENSES` file listing every model with its URL, version and hash. Ultralytics only in a separate benchmark folder.
2. **Adopt the evidence-record architecture** (§4) before adding models. It is what makes the XAI honest, and it makes the sensor toggles trivial: a disabled sensor means its modules are not executed, not merely hidden.
3. **Vision v1 =** rtmlib (YOLOX + RTMPose) + MediaPipe Pose/Gestures + YuNet + Lab k-means colours + SigLIP 2 accessory checks, on OpenVINO GPU/NPU. Target rates are those in §5(1).
4. **Fixed concept whitelist** (≈ 25 concepts):
   - presence/count, distance zone, approaching/leaving, facing, dwell;
   - wave, hands up, jump, crouch, point, clap (audio + pose);
   - thumbs up, open palm, victory, fist;
   - upper/lower clothing colour;
   - glasses, sunglasses, hat/cap, hood, backpack, scarf, pattern/stripes;
   - holding ball/toy/book/phone/bottle.

   Everything else is out of scope by design.
5. **Calibration sprint (2 weeks).**
   - Record ~300 consented clips from team members and adult volunteers in the actual exhibition lighting, with props (hats, backpacks, balls).
   - Fit per-concept temperature/Platt scaling and thresholds at ≥ 90 % precision.
   - Measure and publish false-positive rates per concept. That table is itself a nice exhibit item.
6. **Grey card + lighting index** on the stand. It improves colour naming and gives a tangible "why I'm unsure" explanation.
7. **Group policy:** a primary visitor gets a profile. Everyone else is counts only. Show a visible "I'm only looking at you, the person in the green box" frame.
8. **Make "what I won't guess" a feature:** age, gender, origin, feelings, identity, plus the size–distance ambiguity demo.
9. **Offline packaging:**
   - vendor all weights;
   - set `HF_HUB_OFFLINE=1` and `YOLO_AUTOINSTALL=false`;
   - pin `mediapipe==1.0.1` and use the **Tasks API**: the legacy `mp.solutions` API is absent from recent releases (absent in 0.10.33 per Google issue #6261; a third-party issue dates the removal to 0.10.31; no maintainer statement found) [16];
   - cache OpenVINO compiled models;
   - include a start-up self-test that runs one frame through every module.

   In our tests, model downloads from storage.googleapis.com and download.openmmlab.com timed out repeatedly. Don't depend on them at the venue.
10. **Benchmark on the real exhibition machine** with everything running at once (camera + audio + ASR + UI), on mains power with the "best performance" power plan. Hybrid-core CPUs vary a lot with thread count (Table 1).

---

## 7. Pitfalls / what not to do

- ❌ **Pulling in `ultralytics` casually.** The AGPL then reaches code and weights, and possibly the robot SDK integration [2][6]. It also tries to pip-install packages at runtime (observed when exporting).
- ❌ **Using MediaPipe Pose for groups.** It is single-person by design [19]. When a second child walks in, the skeleton will jump between people. Use a detector plus top-down pose (RTMPose).
- ❌ **Short-range face models for a stand.** BlazeFace short-range found 1 of 2 large faces and 0 of 4 small ones in our spot-check.
- ❌ **Running the multiclass selfie segmenter every frame** (216 ms CPU).
- ❌ **Showing raw CLIP/VLM outputs or open-vocabulary person labels.** Children are the group most often mislabelled into denigrating classes under some label sets [39]. VLMs volunteer gender (observed) and hallucinate objects [59].
- ❌ **Treating cosine similarities or softmax over unrelated labels as probabilities.** Use binary prompt pairs or sigmoid scores, calibrated, with an abstain band [42][47].
- ❌ **Turning blendshapes or smiles into "happy/sad/bored".** That is emotion recognition [63 Art. 3(39), recital 18][64].
- ❌ **Age, gender, ethnicity, hair/eye colour, height-as-age, body size, "personality" labels** ("you're shy", "energetic"). Recital 16 names exactly these as biometric-categorisation categories [63].
- ❌ **Gender-coded garments** (dress/skirt) as attributes. Same for reading text on clothing (it may reveal school, club or name).
- ❌ **Face embeddings or re-identification** to "remember" returning visitors.
- ❌ **Post-hoc saliency as the main explanation.** Saliency can be unfaithful [70]. Prefer evidence that is faithful by construction (crop used = crop shown).
- ❌ **Asking CLIP about attribute–object bindings** ("red shirt"). Get colour from pixels [45][46].
- ❌ **Using research-only weights in the public exhibit** (MobileCLIP2 AMLR, Qwen2.5-VL-3B, InsightFace/SCRFD, SegFormer-clothes without legal OK, ImageBind).
- ❌ **Assuming the dog's camera will "just work".** Check the low viewpoint, wide-angle distortion and motion blur while it walks. Do the perception while the dog is stationary.
- ❌ **Relying on internet at the venue** (model auto-downloads, HF Hub).
- ❌ **Copying vendor demo pipelines without checking the weights.** Hailo's Raspberry Pi pose/detection demos default to Ultralytics YOLOv8 models [74], which brings back the AGPL question. Pick YOLOX/NanoDet/CenterPose builds from the same model zoo instead.
- ❌ **Running DETR-family detectors (RF-DETR, RT-DETR) on CPU.** RF-DETR-S needs ≈ 310–370 ms per frame on a 4-core CPU [73]. Use them only on the NVIDIA laptop.

---

## 8. Unverified / to be measured

- RTX 4060 (laptop/desktop) latencies for every model. Only T4/GTX 1660Ti figures are published [1][8][27].
- D-FINE CPU/OpenVINO latency; NPU/iGPU compatibility of DETR-style models (RF-DETR-S CPU is now known: ≈ 310–370 ms on a 4-core cloud CPU [73]).
- Raspberry Pi 4 and Pi 5 latency for MediaPipe, rtmlib and YuNet. End-to-end Pi 5 + Hailo-8L fps (the model-zoo figures [74] are chip throughput; PCIe, pre/post-processing and the camera pipeline reduce them). Licence of Hailo-trained CenterPose weights.
- Zero-shot accuracy of SigLIP 2 for our concept list on *children* in exhibition lighting. Must be measured in the calibration sprint (§6.5).
- Gemma 4 / Qwen3.5-2B / Florence-2 latency on an RTX 4060 (only RTX 3090 / A100 / L4 proxies are published [75][76]). (Gemma 4 release date now confirmed: 2 Apr 2026 [78].)
- MoveNet weight licence as currently hosted on Kaggle.
- Licence terms of the LIP/ATR datasets behind SCHP and SegFormer-clothes.
- MobileSAM/EdgeSAM CPU figures (secondary source).
- Whether a public science-fair exhibit falls under "research or evaluation" for NVIDIA/Qwen research licences (assume **no**).
- Legal status of pose/gesture processing. The Commission guidelines treat "movements, gestures… body postures" as **behavioural biometrics** and call the AI-Act definition of biometric data "broad" [64 §§251–252]. So **assume our pose and gesture pipeline processes biometric data** in the AI-Act sense, and that any *categorisation* of visitors triggers the Art. 50(3) information duty [63]. Its GDPR Art. 9 status (which turns on unique identification) is for the legal track. Design so that it does not matter: no storage, no sensitive categories, and visible signage plus an on-screen explanation (which the exhibit provides anyway). [added by verifier: the Commission adopted **Guidelines on the transparency obligations under Art. 50** on 20 Jul 2026 (https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems). The legal track should check them for when a pose/clothing-attribute pipeline counts as "biometric categorisation". Under Art. 50(5), the notice must be "clear and distinguishable" and given "at the latest at the time of the first interaction or exposure" (https://artificialintelligenceact.eu/article/50/), so put signage at the stand entrance, not only on screen.]

---

## Sources (accessed 2026-10-01/02)

1. Ultralytics YOLO26 docs (sizes, CPU-ONNX/T4 latency, Jan 2026): https://docs.ultralytics.com/models/yolo26
2. Ultralytics licensing (AGPL-3.0 / Enterprise; trained models AGPL): https://www.ultralytics.com/license
3. Ultralytics pose task (YOLO26-pose table): https://docs.ultralytics.com/tasks/pose/
4. Ultralytics YOLO11 docs: https://docs.ultralytics.com/models/yolo11/
5. Ultralytics Raspberry Pi guide (Pi 5 YOLO26n per-format latency): https://docs.ultralytics.com/guides/raspberry-pi/
6. GNU AGPL-3.0 text, §13: https://www.gnu.org/licenses/agpl-3.0.txt
7. FSF licence list, Apache-2.0 compatible with GPLv3: https://www.gnu.org/licenses/license-list.html#apache2
8. RF-DETR repository (sizes, AP, T4 latency, Apache vs PML 1.0): https://github.com/roboflow/rf-detr
9. RF-DETR docs (export formats): https://rfdetr.roboflow.com/latest/learn/run/detection/
10. RT-DETR repository (Apache-2.0, v2/v4): https://github.com/lyuwenyu/RT-DETR
11. RT-DETRv2 on HF: https://huggingface.co/PekingU/rtdetr_v2_r18vd · https://huggingface.co/docs/transformers/main/en/model_doc/rt_detr_v2
12. D-FINE licence: https://github.com/Peterande/D-FINE · DEIM licence: https://github.com/ShihuaHuang95/DEIM
13. NanoDet: https://github.com/RangiLyu/nanodet
14. YOLOX licence: https://github.com/Megvii-BaseDetection/YOLOX
15. MediaPipe on PyPI (1.0.1, 2026-08-14; Py 3.9–3.12; Win/Linux x86-64 + ARM64): https://pypi.org/project/mediapipe/
16. Legacy `mp.solutions` removed: https://github.com/google-ai-edge/mediapipe/issues/6261 · https://github.com/djbielejeski/a-person-mask-generator/issues/89
17. MediaPipe Object Detector: https://developers.google.com/edge/mediapipe/solutions/vision/object_detector
18. MediaPipe Pose Landmarker: https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker
19. BlazePose GHUM 3D model card: https://storage.googleapis.com/mediapipe-assets/Model%20Card%20BlazePose%20GHUM%203D.pdf
20. MediaPipe Face Detector: https://developers.google.com/edge/mediapipe/solutions/vision/face_detector
21. MediaPipe Face Landmarker: https://developers.google.com/edge/mediapipe/solutions/vision/face_landmarker
22. MediaPipe Gesture Recognizer: https://developers.google.com/edge/mediapipe/solutions/vision/gesture_recognizer
23. Gesture classification model card (fairness): https://storage.googleapis.com/mediapipe-assets/gesture_recognizer/model_card_hand_gesture_classification_with_faireness_2022.pdf
24. MediaPipe Image Segmenter (models, latency): https://developers.google.com/edge/mediapipe/solutions/vision/image_segmenter
25. Multiclass segmentation model card: https://storage.googleapis.com/mediapipe-assets/Model%20Card%20Multiclass%20Segmentation.pdf
26. rtmlib: https://github.com/Tau-J/rtmlib
27. MMPose RTMPose project (CPU/GPU latency, AP): https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose
28. MoveNet: https://www.tensorflow.org/hub/tutorials/movenet · https://blog.tensorflow.org/2021/08/pose-estimation-and-classification-on-edge-devices-with-MoveNet-and-TensorFlow-Lite.html
29. YuNet in OpenCV Zoo (MIT, WIDER Face AP): https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet · https://github.com/opencv/opencv_zoo
30. InsightFace licence (models non-commercial): https://github.com/deepinsight/insightface
31. SAM 2 / 2.1: https://github.com/facebookresearch/sam2
32. SAM 3 / 3.1 (SAM License, 848 M, gated, CUDA ≥ 12.6): https://github.com/facebookresearch/sam3
33. EfficientSAM: https://github.com/yformer/EfficientSAM · MobileSAM: https://github.com/ChaoningZhang/MobileSAM · EdgeSAM (S-Lab licence): https://github.com/chongzhou96/EdgeSAM
34. SegFormer-B2 clothes: https://huggingface.co/mattmdjaga/segformer_b2_clothes · NVIDIA SegFormer licence: https://github.com/NVlabs/SegFormer/blob/master/LICENSE
35. SCHP: https://github.com/GoGoDuck912/Self-Correction-Human-Parsing
36. XKCD colour survey names (CC0): https://xkcd.com/color/rgb.txt
37. van de Weijer, Schmid, Verbeek, Larlus, "Learning Color Names for Real-World Applications", IEEE TIP 18(7):1512–1523, 2009, doi:10.1109/TIP.2009.2019809
38. OpenAI CLIP model card: https://github.com/openai/CLIP/blob/main/model-card.md
39. Radford et al., CLIP paper (prompt ensembling; FairFace probes incl. 'child' class): https://arxiv.org/abs/2103.00020
40. OpenCLIP LAION ViT-B/32 model card: https://huggingface.co/laion/CLIP-ViT-B-32-laion2B-s34B-b79K
41. SigLIP 2 B/16 model card: https://huggingface.co/google/siglip2-base-patch16-224 · paper: https://arxiv.org/abs/2502.14786
42. Zhai et al., SigLIP (sigmoid loss): https://arxiv.org/abs/2303.15343
43. MobileCLIP / MobileCLIP2: https://github.com/apple/ml-mobileclip · AMLR licence: https://huggingface.co/apple/MobileCLIP2-S0
44. EVA-CLIP: https://github.com/baaivision/EVA/tree/master/EVA-CLIP
45. Yuksekgonul et al., VLMs as bags-of-words (ICLR 2023): https://arxiv.org/abs/2210.01936
46. Tong et al., Eyes Wide Shut / MMVP: https://arxiv.org/abs/2401.06209
47. LeVine et al., calibration of zero-shot VLMs: https://arxiv.org/abs/2303.12748
48. Agarwal et al., Evaluating CLIP: https://arxiv.org/abs/2108.02818
49. PromptPAR, CLIP-based pedestrian attribute recognition: https://arxiv.org/abs/2312.10692
50. SmolVLM2-2.2B card: https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct · SmolVLM paper: https://arxiv.org/abs/2504.05299 · blog: https://huggingface.co/blog/smolervlm
51. Moondream 2: https://huggingface.co/vikhyatk/moondream2 · Moondream 3 preview: https://huggingface.co/moondream/moondream3-preview
52. Florence-2: https://huggingface.co/microsoft/Florence-2-base
53. Qwen2.5-VL-3B licence (Qwen RESEARCH): https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct/blob/main/LICENSE
54. Qwen3-VL-2B / 4B: https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct · https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct
55. PaliGemma 2: https://huggingface.co/google/paligemma2-3b-pt-224 · Gemma 3 4B: https://huggingface.co/google/gemma-3-4b-it
56. Gemma 4 model card: https://ai.google.dev/gemma/docs/core/model_card_4 · https://huggingface.co/google/gemma-4-E2B-it
57. InternVL3-1B: https://huggingface.co/OpenGVLab/InternVL3-1B · InternVL3.5-1B: https://huggingface.co/OpenGVLab/InternVL3_5-1B
58. LFM2-VL-450M and LFM Open License 1.0: https://huggingface.co/LiquidAI/LFM2-VL-450M
59. Li et al., POPE object hallucination (EMNLP 2023): https://arxiv.org/abs/2305.10355
60. MiVOLO: https://github.com/WildChlamydia/MiVOLO
61. FairFace: https://github.com/joojs/fairface
62. NIST IR 8525, Face Analysis Technology Evaluation: Age Estimation and Verification (May 2024), Table 19: https://doi.org/10.6028/NIST.IR.8525
63. Regulation (EU) 2024/1689 (AI Act), Art. 3(34),(39),(40); Art. 5(1)(f),(g); Art. 50(3); Annex III 1(b),(c); recitals 16, 18: https://eur-lex.europa.eu/eli/reg/2024/1689/oj
64. European Commission, Guidelines on prohibited AI practices, C(2025) 5052 final (29.7.2025): §249 (smiles are not emotion recognition), §§251–252 (behavioural biometrics incl. gestures and postures), §255 (education institutions): https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-prohibited-artificial-intelligence-ai-practices-defined-ai-act
65. ImageBind (CC-BY-NC-4.0): https://github.com/facebookresearch/ImageBind
66. LanguageBind: https://github.com/PKU-YuanGroup/LanguageBind
67. ONE-PEACE: https://github.com/OFA-Sys/ONE-PEACE
68. LAION-CLAP (CC0): https://github.com/LAION-AI/CLAP · MS-CLAP (MIT, archived): https://github.com/microsoft/CLAP
69. Koh et al., Concept Bottleneck Models: https://arxiv.org/abs/2007.04612 · Oikarinen et al., Label-free CBM: https://arxiv.org/abs/2304.06129
70. Adebayo et al., Sanity Checks for Saliency Maps: https://arxiv.org/abs/1810.03292
71. Raspberry Pi AI HAT+: https://www.raspberrypi.com/products/ai-hat/ · AI HAT+ 2: https://www.raspberrypi.com/products/ai-hat-plus-2/ · AI Camera: https://www.raspberrypi.com/products/ai-camera/
72. Roboflow `supervision` (MIT): https://github.com/roboflow/supervision · ByteTrack (MIT): https://github.com/ifzhang/ByteTrack
73. RF-DETR docs, "RF-DETR on CPU — Export, Inference & Latency" (RF-DETR-S, Colab 4-core x86 CPU, PyTorch/ONNX/OpenVINO): https://rfdetr.roboflow.com/latest/cookbooks/export-cpu/
74. Hailo Model Zoo, Hailo-8L public models: object detection https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst · pose estimation https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_pose_estimation.rst · Hailo Pi pose demo (yolov8s_pose / yolov8m_pose): https://github.com/hailo-ai/hailo-apps/blob/main/hailo_apps/python/pipeline_apps/pose_estimation/README.md
75. Marafioti et al., SmolVLM paper (GPU RAM, A100/L4 throughput): https://arxiv.org/html/2504.05299v1
76. Moondream 2 4-bit model card (2,450 MB VRAM, 184 tok/s on RTX 3090, Apache-2.0): https://huggingface.co/moondream/moondream-2b-2025-04-14-4bit
77. Hugging Face `transformers` Florence-2 docs (native `Florence2ForConditionalGeneration`, `florence-community/Florence-2-base`): https://huggingface.co/docs/transformers/model_doc/florence2
78. Android Developers Blog, "Announcing Gemma 4 in the AICore Developer Preview" (2 Apr 2026): https://android-developers.googleblog.com/2026/04/AI-Core-Developer-Preview.html
79. Digital Omnibus on AI, Regulation (EU) 2026/1744: Lewis Silkin (27 Jul 2026) https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo · K&L Gates / Cyber Law Watch (31 Jul 2026) https://www.cyberlawwatch.com/2026/07/31/eu-digital-omnibus-on-ai-enters-into-force/
80. Qwen3.5-2B model card (Apache-2.0, Feb 2026): https://huggingface.co/Qwen/Qwen3.5-2B
81. LFM2.5-VL-450M model card: https://huggingface.co/LiquidAI/LFM2.5-VL-450M

---

## Verification log

The independent verifier re-checked these claims on 2026-10-02 using fresh fetches of primary sources. Two exceptions: the AI Act article texts came from the artificialintelligenceact.eu mirror because EUR-Lex returned an empty page, and the NIST, guidelines and CLIP figures were read from the downloaded PDFs.

| # | Claim in report | Verdict | Source / note |
|---|---|---|---|
| 1 | Ultralytics: "All Ultralytics YOLO trained models fall under the AGPL-3.0"; the entire derivative work, incl. weights, must be open-sourced; Enterprise price on request | **Confirmed** | https://www.ultralytics.com/license ("complete corresponding source code for the entire derivative work… where applicable, model weights"; "tailored quote") |
| 2 | YOLO26 released Jan 2026; YOLO26n 2.4 M, 40.9 AP, 38.9 ms CPU-ONNX, 1.7 ms T4 | **Confirmed** | https://docs.ultralytics.com/models/yolo26 |
| 3 | YOLO26n-pose 40.3 ms CPU-ONNX, 1.8 ms T4; YOLO11n 2.6 M / 39.5 AP / 56.1 ms / 1.5 ms | **Confirmed** (YOLO26n-pose: 2.9 M params, 57.2 pose mAP) | https://docs.ultralytics.com/tasks/pose/ · https://docs.ultralytics.com/models/yolo11/ |
| 4 | RF-DETR N–L Apache-2.0, XL/2XL PML 1.0; N 30.5 M / 48.4 AP / 2.3 ms; S 32.1 M / 53.0 / 3.5 ms | **Confirmed** | https://github.com/roboflow/rf-detr |
| 5 | mediapipe 1.0.1 released 2026-08-14, Py 3.9–3.12, Win/Linux x86-64 + ARM64, Apache-2.0 | **Confirmed** (macOS 11+ ARM64 wheels also exist) | https://pypi.org/project/mediapipe/ |
| 6 | `mp.solutions` removed from 0.10.31 onward | **Partly confirmed** (secondary source only; Google issue shows it absent in 0.10.33) | https://github.com/djbielejeski/a-person-mask-generator/issues/89 · https://github.com/google-ai-edge/mediapipe/issues/6261 |
| 7 | BlazePose card out of scope: "Multiple people in an image", "further than 14 feet/4 meters"; fairness PDJ full 91.8 % ± 1.4, heavy 94.2 % ± 1.3 | **Confirmed** (text extracted from PDF) | https://storage.googleapis.com/mediapipe-assets/Model%20Card%20BlazePose%20GHUM%203D.pdf |
| 8 | YuNet MIT, 232 KB, faces ~10–300 px, WIDER AP 0.834/0.824/0.708 | **Confirmed** (file is 232,589 bytes; the README's eval table also gives 0.8844/0.8656/0.7503; a new 2026may dynamic-shape export exists) | https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet |
| 9 | InsightFace/SCRFD models non-commercial research only | **Confirmed** ("available for non-commercial research purposes only") | https://github.com/deepinsight/insightface |
| 10 | SegFormer-B2-clothes: `license: other`, NVIDIA licence "non-commercially… research or evaluation purposes only"; 18 labels, 27.4 M, mIoU 0.69 | **Confirmed** | https://huggingface.co/mattmdjaga/segformer_b2_clothes · https://github.com/NVlabs/SegFormer/blob/master/LICENSE (§3.3) |
| 11 | MobileCLIP2 weights: Apple AMLR, non-commercial research only; S0 71.5 % IN, 1.5 + 3.3 ms | **Confirmed** | https://huggingface.co/apple/MobileCLIP2-S0 (+ LICENSE: "non-commercial scientific research and academic development") |
| 12 | Qwen2.5-VL-3B under the Qwen RESEARCH licence (non-commercial) | **Confirmed** | https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct/blob/main/LICENSE |
| 13 | Gemma 4 E2B/E4B Apache-2.0, 2.3 B eff. (5.1 B w/ emb.) / 4.5 B eff.; detection, pointing, audio | **Confirmed** (E4B is 8 B with embeddings; the family also has 26B-A4B and 31B [corrected by verifier pass 2: launch coverage lists four sizes, E2B, E4B, 26B MoE and 31B dense, with no 12B; https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html]). Release date still **UNVERIFIED** (card "last updated" 2026-07-30) | https://huggingface.co/google/gemma-4-E2B-it · https://ai.google.dev/gemma/docs/core/model_card_4 |
| 14 | Moondream 3 BSL 1.1, 9.3 B / 2 B active, CUDA | **Corrected** (card says 9 B total, 2 B active; the BSL use grant allows in-product use that does not compete with M87's paid offerings) | https://huggingface.co/moondream/moondream3-preview |
| 15 | LFM2-VL: LFM Open License 1.0, commercial use only below US$10 M revenue | **Confirmed** (Threshold = "annual revenue of … $10,000,000 or more") | https://huggingface.co/LiquidAI/LFM2-VL-450M/blob/main/LICENSE |
| 16 | SmolVLM2 Apache-2.0; Qwen3-VL-2B Apache-2.0 with 2D grounding; InternVL3.5-1B Apache-2.0 (1.1 B); Moondream 2 Apache-2.0 (detect/point); Florence-2 MIT (needs `trust_remote_code`) | **Confirmed** | HF cards: SmolVLM2-256M-Video-Instruct, Qwen3-VL-2B-Instruct, InternVL3_5-1B, vikhyatk/moondream2 (rev. 2025-06-21), microsoft/Florence-2-base |
| 17 | SAM 3: SAM License, 848 M, gated, CUDA ≥ 12.6; SAM 3.1 exists | **Confirmed** (SAM 3.1 Object Multiplex released 2026-03-27; Python ≥ 3.12, PyTorch ≥ 2.7) | https://github.com/facebookresearch/sam3 |
| 18 | ImageBind CC-BY-NC-4.0; EdgeSAM S-Lab 1.0; LAION-CLAP CC0 (89.98 % ESC-50 ckpt); MS-CLAP MIT, archived 2026-09-15, 93.9 % ESC-50 | **Confirmed** | https://github.com/facebookresearch/ImageBind · https://github.com/chongzhou96/EdgeSAM · https://github.com/LAION-AI/CLAP · https://github.com/microsoft/CLAP |
| 19 | RTMPose-m 75.8 AP, 11.06 ms CPU (i7-11700, ORT), 2.29 ms GTX 1660Ti; RTMDet-nano 0.99 M / 40.3 / 12.4 ms / 2.5 ms | **Confirmed** | https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose |
| 20 | CLIP model card: "Any deployed use case… is currently out of scope"; surveillance and facial recognition "always out-of-scope" | **Confirmed** | https://github.com/openai/CLIP/blob/main/model-card.md |
| 21 | CLIP paper: ages 0–20 ~18 % crime-related, 14 % non-human; 'child' class "drastically reduced" it; ensembling +3.5 %, ~5 % total | **Confirmed, with nuance added** (ages 10–19 still 14.7 % with 'child' class, Table 7) | https://arxiv.org/abs/2103.00020 |
| 22 | SigLIP 2 Apache-2.0; training mix includes de-biasing | **Confirmed** (the de-biasing claim is in the paper abstract, not the HF card) | https://huggingface.co/google/siglip2-base-patch16-224 · https://arxiv.org/abs/2502.14786 |
| 23 | NIST IR 8525 (May 2024): six commercial algorithms; MAE 1.3–5.3 y at ages 8–14; age 12: 1.97–4.68 y; Acc(±1) 0.12–0.40 | **Corrected** (range is 1.42–5.34 y; age-12 figures and Acc(1) 0.122–0.399 confirmed; images are Mexican visa photos) | https://doi.org/10.6028/NIST.IR.8525 (Table 19, p. 36) |
| 24 | AI Act recital 16 lists sex, age, hair colour, eye colour, tattoos, behavioural or personality traits; recital 18 frown/smile; Art. 50(3) duty to inform people exposed to biometric categorisation / emotion recognition | **Confirmed** | https://artificialintelligenceact.eu/recital/16/ · /recital/18/ · /article/50/ (mirror of Reg. (EU) 2024/1689; EUR-Lex HTML returned empty in this session) |
| 25 | Commission guidelines C(2025) 5052 final (29.7.2025): §249 "observation that a person is smiling is not emotion recognition" / "Concluding that a person is happy is"; §§251–252 behavioural biometrics incl. gestures/postures, "broad"; §255 education institutions "normally accredited" | **Confirmed, with nuance** (§255 also says the term "is broad", with no limitation on pupils' age or setting) | https://ec.europa.eu/newsroom/dae/redirection/document/112367 (PDF, pp. 79–81) |
| 26 | Pi 5 YOLO26n: NCNN 67 ms, ONNX 126 ms, PyTorch 299 ms | **Confirmed** (67.03 / 125.99 / 299.09 ms; excludes pre/post-processing; OpenVINO 104.55, MNN 91.87) | https://docs.ultralytics.com/guides/raspberry-pi/ |
| 27 | AI HAT+ Hailo-8L 13 TOPS / Hailo-8 26 TOPS from US$70; AI HAT+ 2 Hailo-10H 40 TOPS INT4, 8 GB, US$200; AI Camera IMX500 US$70, all Pi models | **Confirmed** (official product pages, accessed 2026-10-02; "Available now") | https://www.raspberrypi.com/products/ai-hat/ · https://www.raspberrypi.com/products/ai-hat-plus-2/ · https://www.raspberrypi.com/products/ai-camera/ |
| 28 | MediaPipe multiclass selfie segmenter 217.8 ms CPU; selfie binary ≈33 ms (Pixel 6) | **Confirmed** (217.76 ms CPU / 71.24 ms GPU; 33.46 ms) | https://developers.google.com/edge/mediapipe/solutions/vision/image_segmenter |

The verifier did **not** re-run the MEASURED laptop numbers in Tables 1–3. They are first-party measurements, and the scripts exist in `research/05-vision-bench/`.

## Omissions added by verifier

1. **The AI Act has been amended (2026) and the timeline has shifted.** The current consolidated Art. 113 (artificialintelligenceact.eu mirror) shows new prohibitions in Art. 5(1)(ba)/(bb) and Art. 5(1a)/(1b), applying from **2 Dec 2026**. Annex III high-risk obligations now apply from **2 Dec 2027**, and Annex I-linked ones from 2 Aug 2028. The general application date stays **2 Aug 2026**, so **Art. 50(3) transparency duties apply during the 2027 exhibition**. The legal track must cite the *consolidated* text, not the 2024 OJ version alone. https://artificialintelligenceact.eu/article/113/
   **Resolved in revision 2:** the amending act is the **Digital Omnibus on AI, Regulation (EU) 2026/1744**, published in the OJ on 24 July 2026, in force 27 July 2026. The two new prohibitions target AI systems generating non-consensual intimate imagery ("nudifiers") and CSAM; they do not touch this demonstrator. The "notification obligations for emotion recognition and biometric categorisation systems" were **not** delayed and apply from 2 Aug 2026 [79]. (Number taken from law-firm summaries; the OJ text itself was not opened in this session.) [verifier pass 2: the EUR-Lex text was opened and confirms Regulation (EU) 2026/1744 of 8 July 2026, OJ 24 Jul 2026, in force on the third day after publication, Annex III high-risk from 2 Dec 2027, and the two new Art. 5 prohibitions. The only Art. 50 concession is a 4-month transition, to 2 Dec 2026, for **Art. 50(2) machine-readable marking** by generative-AI providers already on the market before 2 Aug 2026. Art. 50(3) is unchanged. https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng]
2. **CLIP's 'child'-class fix does not protect 10–19-year-olds well.** Table 7 of the CLIP paper shows 14.7 % of that group were still in crime-related or non-human classes. This strengthens the "no open person labels" rule for an 8–14 audience. https://arxiv.org/abs/2103.00020
3. **YuNet 2026may export** (dynamic input shape, for the OpenCV 5.x ONNX Runtime engine) is now OpenCV Zoo's default. Use it with OpenCV 5.0. https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet
4. **Qwen3.5 small models** (e.g. Qwen3.5-2B, Feb 2026, Apache-2.0, natively multimodal) supersede Qwen3-VL-2B as the Apache VLM candidate. Grounding quality and CPU latency are UNVERIFIED. https://huggingface.co/Qwen/Qwen3.5-2B
5. **LFM2.5-VL-450M** (released 8 Apr 2026 [corrected by verifier pass 2], LFM 1.0, bounding-box output, GGUF/ONNX CPU builds) is the newer Liquid edge VLM. It has the same revenue-threshold licence. https://huggingface.co/LiquidAI/LFM2.5-VL-450M
6. **Education-institution scope (guidelines §255) is "broad".** Organised school-group visits make the Art. 5(1)(f) emotion-recognition prohibition more plausibly relevant than the report suggests. Treat "no emotion inference" as a hard legal constraint, not just good practice. https://ec.europa.eu/newsroom/dae/redirection/document/112367
7. **Pi 5 Ultralytics timings exclude pre/post-processing.** Real end-to-end frame time is higher than 67 ms. https://docs.ultralytics.com/guides/raspberry-pi/

## Verification log (pass 2, 2026-10-02)

A second independent pass covered the claims added in revision 2 plus a re-check of the most decision-critical ones. Each was checked with fresh fetches of primary sources (EUR-Lex, vendor pages, GitHub, HF cards). The NIST and CLIP figures were re-extracted from the original PDFs with `pdftotext`.

| # | Claim | Verdict | Source |
|---|---|---|---|
| P1 | RF-DETR-S on a 4-core CPU: 312 ms OpenVINO fp32, 368 ms ORT, 346 ms PyTorch; "No format wins decisively"; fp16 not faster | **Confirmed** (311.92 / 368.33 / 345.76 ms; JIT 327.30; OV fp16 354.55; Colab x86, 4 physical / 8 logical cores @ 2.2 GHz) | https://rfdetr.roboflow.com/latest/cookbooks/export-cpu/ |
| P2 | RF-DETR N–L Apache-2.0, XL/2XL PML 1.0; N 30.5 M / 48.4 AP / 2.3 ms; S 32.1 M / 53.0 / 3.5 ms (T4) | **Confirmed** | https://github.com/roboflow/rf-detr |
| P3 | Hailo-8L: YOLOX-tiny 214 fps, NanoDet-RepVGG 620 fps, YOLOv8n 202 fps; CenterPose-800MF 85 fps / 43.0 AP; YOLOv8s-pose 107 fps / 55.7 AP | **Confirmed, with nuance** (the mAPs quoted are float; hardware mAPs are 31.4 / 28.6; zoo v2.19.0, host i5-9400, PCIe Gen3 x4). Corrected inline | https://github.com/hailo-ai/hailo_model_zoo/blob/master/docs/public_models/HAILO8L/HAILO8L_object_detection.rst · …/HAILO8L_pose_estimation.rst |
| P4 | SmolVLM GPU RAM 0.8 / 1.2 / 4.9 GB; A100 batch 1: 0.8 / 0.7 / 0.6 ex/s; L4 peak 2.7 / 1.4 / 0.25 | **Confirmed** | https://arxiv.org/html/2504.05299v1 |
| P5 | Moondream 2 4-bit: 2,450 MB VRAM, 184 tok/s on an RTX 3090, Apache-2.0 | **Confirmed** (also needs `torch.compile` and `torchao`) | https://huggingface.co/moondream/moondream-2b-2025-04-14-4bit |
| P6 | Florence-2 native in `transformers` (`Florence2ForConditionalGeneration`, `florence-community/Florence-2-base`) | **Confirmed** (docs v5.17) | https://huggingface.co/docs/transformers/model_doc/florence2 |
| P7 | Gemma 4 released 2 Apr 2026; E2B "3x faster than the E4B"; Apache-2.0; E2B 2.3 B eff. / 5.1 B with embeddings | **Confirmed** | https://android-developers.googleblog.com/2026/04/AI-Core-Developer-Preview.html · https://huggingface.co/google/gemma-4-E2B-it |
| P8 | Reg. (EU) 2026/1744 (Digital Omnibus on AI): OJ 24 Jul 2026, in force 27 Jul 2026; Annex III deferred to 2 Dec 2027; Art. 50(3) still applies from 2 Aug 2026 | **Confirmed from EUR-Lex** (adopted 8 Jul 2026; the only Art. 50 transition is for 50(2) marking, to 2 Dec 2026) | https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng · https://www.bakerbotts.com/thought-leadership/publications/2026/september/eu-ai-act-article-50-transparency-obligations-go-live |
| P9 | Art. 50(3): deployers of emotion-recognition / biometric-categorisation systems must inform exposed persons | **Confirmed** (plus Art. 50(5): at the latest at first exposure, "clear and distinguishable") | https://artificialintelligenceact.eu/article/50/ |
| P10 | Guidelines C(2025) 5052 final (29.7.2025): "The observation that a person is smiling is not emotion recognition"; "Concluding that a person is happy is emotion recognition"; §255 education "is broad", "no limitation as regards the types or ages of pupils" | **Confirmed** (verbatim from the PDF; §255 also says such institutions are "normally accredited" and may issue certificates, so a science-fair stand is probably *outside* Art. 5(1)(f). Keeping the conservative hard constraint is still right) | https://ec.europa.eu/newsroom/dae/redirection/document/112367 |
| P11 | NIST IR 8525 Table 19: MAE 1.42–5.34 y at ages 8–14; age 12: 1.97–4.68 y; Acc(1) 0.12–0.40; Mexican visa photos | **Confirmed** (min 1.42 incode/yoti at age 8; max 5.34 neuro at age 14; age 12 Acc(1) 0.122–0.399) | https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8525.pdf (p. 36) |
| P12 | CLIP Table 7: ages 3–9 35.0 % → 4.3 %; ages 10–19 29.5 % → 14.7 % with a 'child' class; ages 0–20 ≈ 18 % crime-related, 14 % non-human; ensembling +3.5 % | **Confirmed** (verbatim from PDF) | https://arxiv.org/abs/2103.00020 |
| P13 | CLIP model card: "Any deployed use case… is currently out of scope"; surveillance / facial recognition "always out-of-scope" | **Confirmed** | https://github.com/openai/CLIP/blob/main/model-card.md |
| P14 | Ultralytics: "All Ultralytics YOLO trained models fall under the AGPL-3.0"; Enterprise priced per request | **Confirmed** | https://www.ultralytics.com/license |
| P15 | mediapipe 1.0.1, 2026-08-14, Py 3.9–3.12, Win/Linux x86-64 + ARM64, Apache-2.0 | **Confirmed** (macOS 11+ ARM64 wheels also exist) | https://pypi.org/project/mediapipe/ |
| P16 | YuNet MIT; `face_detection_yunet_2026may.onnx` = dynamic H/W export for the OpenCV 5.x ORT engine; 10–300 px faces | **Confirmed** | https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet |
| P17 | Pi 5 YOLO26n NCNN 67 ms (excl. pre/post-processing) | **Confirmed** (67.03 ms; MNN 91.87, OpenVINO 104.55, ONNX 125.99, PyTorch 299.09) | https://docs.ultralytics.com/guides/raspberry-pi/ |
| P18 | AI HAT+ from US$70 (Hailo-8L 13 TOPS / Hailo-8 26 TOPS); AI HAT+ 2 US$200 (Hailo-10H, 40 TOPS INT4, 8 GB); AI Camera US$70 (IMX500, all Pi models) | **Confirmed** (official product pages accessed 2026-10-02; AI HAT+ 2 production to Jan 2036; AI Camera to Jan 2028) | https://www.raspberrypi.com/products/ai-hat/ · https://www.raspberrypi.com/products/ai-hat-plus-2/ · https://www.raspberrypi.com/products/ai-camera/ |
| P19 | MobileCLIP2 weights Apple AMLR, research only | **Confirmed** ("exclusively for Research Purposes"; excludes "use in any commercial product or service") | https://huggingface.co/apple/MobileCLIP2-S0/blob/main/LICENSE |
| P20 | SigLIP 2 B/16 Apache-2.0; Qwen3-VL-2B Apache-2.0 with 2D grounding; Qwen3.5-2B Apache-2.0, Feb 2026, image + video, use non-thinking mode | **Confirmed** (Qwen3.5-2B grounding still not stated on the card) | https://huggingface.co/google/siglip2-base-patch16-224 · https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct · https://huggingface.co/Qwen/Qwen3.5-2B |
| P21 | LAION-CLAP CC0, ckpt 89.98 % ESC-50; MS-CLAP MIT, 93.9 % ESC-50, archived 2026-09-15 | **Confirmed** | https://github.com/LAION-AI/CLAP · https://github.com/microsoft/CLAP |
| P22 | rtmlib Apache-2.0, backends onnxruntime/opencv/openvino/tensorrt | **Confirmed** (dependencies also include `opencv-contrib-python`) | https://github.com/Tau-J/rtmlib |
| P23 | LFM2.5-VL-450M dated 2025-11-28 | **Corrected** to 8 Apr 2026 (2025-11-28 is the LFM2 tech report). Fixed inline | https://www.liquid.ai/blog/lfm2-5-vl-450m · https://huggingface.co/LiquidAI/LFM2.5-VL-450M |
| P24 | Pass-1 log: Gemma 4 family includes a 12B | **Corrected** (four sizes: E2B, E4B, 26B MoE, 31B). Fixed inline | https://opensource.googleblog.com/2026/03/gemma-4-expanding-the-gemmaverse-with-apache-20.html |

## Omissions added by verifier (pass 2)

1. **DEIMv2 (Sep 2025) is NOT Apache.** Its custom licence prohibits commercial use. It is easy to confuse with DEIM v1 (Apache-2.0), which the report recommends. Pin DEIM v1 / D-FINE if you use that family. https://github.com/Intellindust-AI-Lab/DEIMv2/blob/main/LICENSE.md
2. **Moondream 3.1 (final, 7 Jul 2026)** replaced the preview. It uses a proprietary "Moondream License", not BSL→Apache, and needs ≥ 10 GB VRAM. Moondream **2** stays the only Apache Moondream. https://moondream.ai/models/moondream_3-1_9B_A2B
3. **Commission Art. 50 transparency guidelines (20 Jul 2026)** exist and should be the legal track's primary reference for the stand notice (Art. 50(3)/(5)). https://digital-strategy.ec.europa.eu/en/library/guidelines-transparency-obligations-providers-and-deployers-ai-systems
4. **The Omnibus also rewrote Art. 4 (AI literacy)** into an obligation to "take measures", with no guaranteed level, still applicable to deployers (secondary sources only, **UNVERIFIED** against the OJ text). The XAI exhibit itself plus staff briefing would plausibly satisfy it. https://www.nicfab.eu/en/posts/digital-omnibus-ai-official-journal/
5. **Hailo zoo numbers are chip throughput on an x86 host** (i5-9400, PCIe Gen3 x4). The Pi 5 exposes a single PCIe lane (Gen 2 by default, Gen 3 optional; UNVERIFIED for the HAT configuration), so expect lower end-to-end fps on the dog.
