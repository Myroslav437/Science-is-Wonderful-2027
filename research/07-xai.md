# 07 — Explainable AI and uncertainty for the "How does a robot see you?" exhibit

*Research track 07 (XAI for a multimodal sensor-fusion exhibit). First version 2026-10-01; **revision 2, 2026-10-02**. Method: desk research (papers, official repos and docs, PyPI, EUR-Lex / AI Act text), a latency benchmark on the dev laptop (Intel Core Ultra 7 255U, 32 GB, CPU only), and an audit of the team's prototype (`prototype/robotsees`). Numbers in square brackets [n] point to the **Sources** list. Anything I could not check is marked **UNVERIFIED**.*

**What changed in revision 2.**
- The round-1 verifier's corrections (gScoreCAM scope, repo licences, AI Act Art. 5(1)(g) scope, latency under load) are now folded into the text. The verification log is kept at the end.
- Concept examples now follow the attribute register in `09-ethics-law.md` [103]. **Hats/headwear and hair colour are out**, pitch is not a personal label, and speaking speed is framed from the robot's side.
- New §2.2 with the team's own calibration numbers [102].
- New §8.7 auditing the prototype's XAI code against this design. It found 4 concrete faithfulness or calibration gaps.
- Added and verified for 2025–2026:
  - LeGrad (ICCV 2025). Its pip package pins an old open_clip.
  - shapiq 1.7.0, for cross-modal interactions.
  - Counterfactual Modality Attribution (2026).
  - Long & Magerko's full 17/15 lists.
  - Children's Bayesian reasoning with natural frequencies, and a failed replication.
  - Children's scepticism towards inaccurate robots (2024).
  - The VHX museum case study.
  - The AI Act Art. 50 timeline after the Digital Omnibus.

---

## 0. Bottom line

1. **Make the fusion itself the explanation.** Each sensor gives calibrated per-concept **log-likelihood ratios** (log-evidence). The fusion **adds** them in log space: a tempered logarithmic opinion pool, or weighted naive Bayes. Each sensor's weight depends only on that sensor's own signal quality.
   - Because the combination is additive, three quantities are the same number: the per-sensor evidence sum, the leave-one-modality-out (LOMO) change, and the **exact Shapley value** of each sensor.
   - Nothing has to be estimated, the three explanations cannot disagree, and the cost is close to zero: **75 µs per attribute** for exact 4-player Shapley in plain Python (§2).
   - The prototype already implements this and unit-tests it. 7/7 tests pass, 2026-10-02 [102].
2. **The sensor toggle is a real interventional counterfactual.** Under the fusion's conditional-independence assumption, switching a sensor off means dropping its term. That is exact marginalisation over the missing sensor. **Never implement "off" by feeding a black frame or silence into the model.** That is a *baseline input*, not an absence, and it creates spurious evidence (§3.1; [4][6][13]).
3. **What visitors see, all computed from one evidence ledger:**
   - (a) a **balance scale per attribute**, with weights coloured by sensor;
   - (b) a **"what would change the robot's mind?"** preview: ghost bars before a toggle, plus the evidence gap still needed;
   - (c) **clue cards** from each sensor, *including counter-clues*: matched words, sound tags, visible-concept tags, and optionally a coarse occlusion "spotlight";
   - (d) **calibrated 3–4-level verbal confidence**, uncertain attributes drawn fuzzy on the avatar, and "it's one of these" sets;
   - (e) **template sentences** generated only from ledger fields. No LLM writes text at runtime.
4. **Do not use in front of visitors:**
   - raw attention or attention rollout;
   - Guided Backprop or Guided Grad-CAM;
   - LIME;
   - KernelSHAP, RISE or IG on pixels (seconds to minutes per explanation on this CPU);
   - MM-SHAP and the perceptual score (they answer a different question, and the perceptual score needs other visitors' data);
   - TCAV, ProtoPNet, or LLM-written explanations;
   - MC dropout (the CLIP model has **0 dropout layers**, checked locally) or evidential deep learning.
5. **Handle uncertainty with cheap, checkable tools:**
   - per-concept Platt/temperature calibration on a small labelled set [45][46];
   - a discount for correlated frames (the prototype's saturating κ);
   - "I'm sure" thresholds set by **selective classification on held-out sessions** [47];
   - split-conformal "one of these" sets for categorical attributes, with about 1,000 calibration points [47], recalibrated on site.

   Our own data (§2.2): after Platt scaling, CLIP B/32 per-frame "glasses" claims at calibrated p ≥ 0.8 or ≤ 0.2 were 92.8% correct and covered 50.7% of images. "Hat" almost never reached "sure" (1.5%), which is the correct behaviour for a weak concept.
6. **Compute is feasible on CPU, but sensitive to load.**
   - On an idle machine, CLIP ViT-B/32 takes **128 ms** per frame and SigLIP2 B/16 **236 ms**.
   - With the CPU at 100% from other processes, the verifier measured a median of 1,669 ms (12 threads) and 417 ms (4 threads, best run 142 ms).
   - So the exhibition PC must run nothing else heavy, and the thread count must be pinned.
   - An optional per-keyframe saliency map costs about 0.3–1.2 s. Explanations at the fusion level are effectively free.
7. **Evaluate on four levels:**
   - faithfulness unit tests: completeness, LOMO consistency, and **displayed clue cards summing to the displayed scale**;
   - calibration of the **fused session belief**, not only per frame (ECE, empirical coverage);
   - saliency sanity checks [57] and deletion/insertion/ROAD [24][62], if saliency is used at all;
   - a children's *simulatability* test: "predict what the robot will think if we switch the mic off" [67].

---

## 1. Proposed glass-box pipeline (and why it makes faithful XAI cheap)

```
camera ──► CLIP/SigLIP (frozen) ──► concept scores s(c) ─► per-concept calibration ─► log-evidence_cam(a,t) ┐
mic ─┬──► faster-whisper ASR ─────► closed-vocabulary keyword match ─► calibration ─► log-evidence_asr(a,t) ├─► EVIDENCE LEDGER ─► log-space fusion ─► P(a), evidence volume ─► avatar + explanations
     ├──► loudness / activity (RMS, VAD) ─► tiny rule/logistic model ─────────────► log-evidence_snd(a,t) │      (one row per clue:
     └──► CLAP (optional) ─────────► sound-tag scores ─► calibration ─────────────► log-evidence_clap(a,t)┘       t, sensor, concept, raw score,
(optional low-privacy sensors: PIR / IR distance / touch / IMU on the dog [see 02/03 tracks] = extra players)    calibrated p, log-ev, weight, contribution)
```

The prototype currently has **2 toggle groups**, `camera` ("Eyes") and `microphone` ("Ears") [102]. ASR, loudness and CLAP are sub-streams of "Ears". Explanations should be shown at the level of the **toggle group**, because that is what the visitor can intervene on.

**Fusion rule (general form).** For a binary attribute *a* (e.g. "wearing glasses") and sensor *m*:

- Per-window evidence: ℓ<sub>m,a,k</sub> = logit(p̂<sub>m,a,k</sub>) − logit(π<sub>a</sub><sup>calib</sup>). This is a calibrated LLR: the calibrated probability minus the base rate of the calibration set.
- Fused log-odds: L<sub>a</sub> = ℓ<sup>0</sup><sub>a</sub> + Σ<sub>m</sub> φ<sub>m,a</sub>, where φ<sub>m,a</sub> = w<sub>m</sub>(q<sub>m</sub>) · g(ℓ<sub>m,a,1..K</sub>). Here g is a correlation-discounted aggregate: either a discounted sum with per-window clipping ±c, or the prototype's quality-weighted mean × saturating κ<sub>m</sub> = 1 − exp(−Σq·w/τ) [102].
- P(a) = σ(L<sub>a</sub>). Also track the evidence volume: E<sup>+</sup><sub>a</sub> = Σ positive contributions and E<sup>−</sup><sub>a</sub> = Σ |negative contributions|.
- Categorical attributes (clothes colour, favourite animal) use one log-score per value and a softmax (log-linear pooling). The prototype also mixes each likelihood with "uninformative" using a per-slot *relevance* r<sub>m</sub>. For example, clothes colour is a weak hint about favourite colour (r = 0.35) [102].

**Properties that make the explanations faithful by construction:**

| Property | Statement | Consequence for XAI |
|---|---|---|
| Completeness | L<sub>a</sub> = ℓ<sup>0</sup><sub>a</sub> + Σ<sub>m</sub> φ<sub>m,a</sub> | The bars always add up to the displayed belief, like IG's completeness axiom [12] |
| LOMO = contribution | L<sub>a</sub> − L<sub>a</sub><sup>(−m)</sup> = φ<sub>m,a</sub> | The toggle preview shows exactly what the toggle will do |
| Exact Shapley = contribution | v(S) = ℓ<sup>0</sup> + Σ<sub>m∈S</sub> φ<sub>m</sub> is additive, so the Shapley value of *m* is φ<sub>m</sub> | No sampling and no estimation error (verified numerically, §2) |
| Toggle-off = marginalisation | Under conditional independence of sensors given *a*, an unobserved sensor's likelihood integrates to 1, so its term disappears | "Camera off" means the robot *has no camera clues*, not "the camera saw darkness" |
| No interactions | w<sub>m</sub> depends only on sensor *m*'s own quality q<sub>m</sub>: person visible, blur, ASR `no_speech_prob`/`avg_logprob` (exposed by faster-whisper 1.2.1 [88]), SNR | If weights depended on *other* sensors, interactions would appear and one bar per sensor would no longer be the whole story (then see shapiq, §3.1) |
| Ignorance ≠ conflict | Empty pans (E<sup>+</sup> ≈ E<sup>−</sup> ≈ 0) vs heavy pans on both sides | The display separates "not enough clues" from "clues disagree"; entropy alone cannot (§4) |

**Units.** In the prototype, the per-sensor "clue" for value v is E<sub>m</sub>(v) − mean<sub>v'</sub>E<sub>m</sub>(v'), a *centred log-score*. It is additive across sensors, so all the properties above hold. For a **binary** slot it equals **half** the log-odds: measured ratio 2.00 on a glasses example, §8.7. That is harmless, provided the UI calls the unit "clue points" and never "log-odds" or "%".

**Neutral prior.** Use ℓ<sup>0</sup> = 0 (50/50) for visible binary attributes and uniform priors for categorical ones; the prototype does this [102]. Population base rates would bake stereotypes into the robot's "first guess". "Before it sees you, the robot has no idea" is also the clearest story for children.

This is effectively a **training-free concept-bottleneck model**: a human-curated vocabulary, frozen encoders, and a transparent additive head. It gives the intervention benefits Koh et al. argue for [29], without a learned final layer that could leak information [32][33][34].

---

## 2. Measured compute and calibration

### 2.1 Latency on the dev laptop (2026-10-01)

Setup: Intel Core Ultra 7 255U, PyTorch 2.14.1+cpu with 12 threads, fp32, open_clip 3.3.0 (local install [89]). Input was a synthetic 224×224 image. Each figure is the median of 5 runs after warm-up on an **idle** machine. Under full background CPU load the verifier measured B/32 at a median of 1,669 ms (12 threads) and 417 ms (4 threads). **The figures are indicative only.** OpenVINO, the iGPU/NPU and the final exhibition PC were not tested (UNVERIFIED for deployment).

| Operation | CLIP ViT-B/32 (laion2b_s34b_b79k) | SigLIP2 ViT-B/16 @224 |
|---|---|---|
| 1 image forward (concept scores) | **128 ms** | **236 ms** |
| 1 forward + backward (gradient / Grad-CAM / LeGrad-type saliency) | **322 ms** | **761 ms** |
| Batch of 49 masked images (7×7 occlusion) | 2.6 s (≈53 ms/img) | — |
| Batch of 64 / 16 images | 4.7 s (≈73 ms/img) | 3.1 s for 16 (≈195 ms/img) |
| *Derived:* 4×4 coarse occlusion (16 passes) | ≈0.9–1.2 s | ≈3 s |
| *Derived:* IG with 32 steps (paper recommends 20–300 steps [12]) | ≈10 s | ≈24 s |
| *Derived:* RISE with 4,000–8,000 masks (paper's settings [24]) | ≈5–10 min | ≈13–26 min |
| *Derived:* KernelSHAP, default nsamples = 2M+2048 [8]; M = 49 superpixels gives 2,146 evals | ≈2.6 min | ≈7 min |
| *Derived:* LIME image, default `num_samples=1000` [25] | ≈73 s | ≈3 min |
| Exact 4-modality Shapley on cached ledger (Python, unoptimised) | **75 µs per attribute** (verifier: 59 µs; round-2 verifier, system Python 3.14: 158 µs) | same |

**Worked check of the Shapley property.** Take per-modality LLRs of camera +1.2, ASR +0.8, loudness −0.3, CLAP +0.1, with a prior of −1.
- Exact Shapley in **log-odds** space returns exactly (1.2, 0.8, −0.3, 0.1).
- In **probability** space it returns (0.281, 0.182, −0.063, 0.022). These values depend on the prior and on the order-averaged sigmoid curvature, which is harder to explain.
- **So display in log-space units ("clues"), not as percentage-point attributions.** The prototype computes the probability-space version (`shapley_prob`) only for comparison and displays the log-space clues. That is correct.

The local open_clip ViT-B/32 model has **zero `nn.Dropout` modules and MultiheadAttention dropout = 0.0** (re-confirmed by the verifier). MC dropout therefore cannot be applied to it as trained (§4).

### 2.2 The team's own per-frame calibration (prototype experiment, 2026-10-01) [102]

Protocol:
- **Data:** Open Images V7 validation, human-verified labels, adults only (Boy/Girl images excluded).
- **Score:** contrast-prompt score on the head crop.
- **Calibration:** per-concept Platt scaling, evaluated with 5-fold stratified CV.
- **"Sure":** calibrated p ≥ 0.8 or ≤ 0.2.

| Backbone | Concept | n+ / n− | AUROC (prompt) | ECE (CV) | Brier | "Sure" coverage → precision | Linear-probe AUROC |
|---|---|---|---|---|---|---|---|
| CLIP ViT-B/32 | glasses | 120 / 99 | 0.914 | **0.084** | 0.117 | 50.7% → **92.8%** | 0.915 |
| CLIP ViT-B/32 | hat (technical test only) | 79 / 52 | 0.751 | 0.103 | 0.207 | 1.5% → 50% | **0.826** |
| SigLIP2 B/16 | glasses | 120 / 99 | 0.920 | 0.150 | 0.110 | 37.0% → 91.4% | 0.921 |
| SigLIP2 B/16 | hat (technical test only) | 79 / 52 | 0.774 | 0.179 | 0.210 | 0% → — | **0.852** |

What these numbers mean for XAI:
1. **Calibration plus selective claims work for a strong concept.** For glasses, B/32 gives about 93%-correct "sure" claims on about half of the images.
2. **For weak concepts the system correctly stays unsure.** Hat almost never became "sure". Linear probes beat prompts on weak concepts (0.83–0.85 vs 0.75–0.77 AUROC), which supports the post-hoc-CBM fallback (§3.12). Hat is excluded from the exhibit anyway (headwear can reveal religion [103]).
3. **SigLIP2's independent sigmoid scores did not calibrate better here.** Round 1 hypothesised that they might. On this small set, SigLIP2's ECE was higher (0.15–0.18 vs 0.08–0.10) at similar AUROC. The hypothesis is **not supported** (small n; adults only; one split protocol).
4. These are **per-frame** numbers. The exhibit shows a **fused, multi-frame** belief whose "sure" threshold is a fixed constant (§8.7). Calibration of the fused belief is **not yet measured**.

---

## 3. Method-by-method assessment (the six questions)

**Summary table.** "Live" means usable in front of visitors within a 3–5 min interaction. "Offline" means usable for development, validation or research.

| Method | Explains | Fits frozen + late fusion + real-time | Child-understandable (8–14) | Separates modalities | Cost | Verdict |
|---|---|---|---|---|---|---|
| Exact Shapley over modality coalitions | Any model evaluable on modality subsets | **Yes** (2ⁿ ≤ 16 coalitions on cached evidence) | Yes, as "who found the clues" | **Yes** | ~0 | **USE (core, log-space)** |
| Leave-one-modality-out / ablation | Any | **Yes** (it *is* the toggle) | **Very** | **Yes** | n extra fusion evals ≈ 0 | **USE (toggle + preview)** |
| Counterfactual ("what would change its mind") | Any; computed on the fusion | **Yes** | **Very** (contrastive, "what if") [28] | Yes | ~0 | **USE** |
| Concept bottleneck (curated vocabulary) | Concept layer → output | **Yes** (the pipeline *is* one) | Yes (named concepts) | Yes (per-sensor concept heads) | ~0 | **USE (architecture)** |
| Post-hoc CBM / linear probes [31] | Pretrained embedding → concepts | Yes (per-concept probes on CLIP embedding) | Yes | Per sensor | Training minutes | **USE where prompts fail** (§2.2) |
| Occlusion (coarse grid) | Any black box | Per keyframe only (≈1 s) | Yes ("cover part of the picture") | Within camera only | 9–16 passes | **OPTIONAL (Phase 2)** |
| LeGrad / Grad-CAM / CLIP saliency (Chefer, Grad-ECLIP, CLIP Surgery, gScoreCAM) | ViT / CLIP image encoders | Per keyframe (0.3–0.8 s); gScoreCAM's speed-up is for ResNet CLIP | Partly (risk of over-reading) | No | 1 fwd+bwd; gScoreCAM ≈300 fwd | **OPTIONAL, only after sanity checks** |
| Template NL explanations | The ledger | **Yes** | **Yes** | Yes | ~0 | **USE** |
| Shapley interactions (shapiq) | Non-additive fusion heads | Yes (exact for ≤4 players) | Low | Yes, plus pairs | ~0 | Only if fusion becomes non-additive |
| Integrated Gradients | Differentiable nets | Too slow on pixels; at the fusion it equals our bars | Poor (noisy pixels) | No | 20–300 fwd+bwd | AVOID live |
| KernelSHAP / PartitionSHAP (features/pixels) | Any | Too slow on pixels; trivial and redundant at the fusion | Medium | Only if modalities are players | 10²–10³ evals | AVOID live |
| RISE | Any black box | Offline only | Medium | No | 4,000–8,000 masks | Offline evaluation only |
| LIME | Any black box | Slow, unstable | Medium | No | ≥1,000 evals | **AVOID** |
| Attention maps / rollout | Transformers | Cheap, but unfaithful and class-agnostic | Looks easy, misleads | No | 1 fwd | **AVOID** |
| MM-SHAP | VL transformers on image–text pairs | Wrong question for us | Low | 2 modalities inside one model | 2p+1 sampled evals per sample | **AVOID live**; research only |
| Perceptual score / SHAPE | Multimodal classifiers, dataset level | Needs labels and other samples | No | Yes (global) | K permutations × dataset | Offline validation only |
| Counterfactual Modality Attribution (CMA, 2026) | Multimodal LLMs | Needs diffusion-generated counterfactuals | No | Yes | Many generative passes | **AVOID** (wrong scale) |
| Label-free CBM | Backbone + LLM-generated concepts | Needs training data; uncontrolled vocabulary | Too many concepts | No | Hours of training | **AVOID** (borrow ideas) |
| TCAV | Internal layer of a classifier, globally | Not per visitor | No | No | Concept sets + gradients | **AVOID** |
| Prototypes (ProtoPNet) | Purpose-built networks | Needs training; prototypes = other people's images | Very | Possible | Training | **AVOID** (curated "concept cards" OK) |
| LLM-generated explanations | Nothing (post-hoc story) | Possible, but unfaithful | Fluent | Pretends to | LLM inference | **AVOID live** |

### 3.1 Exact Shapley values over modality coalitions
- **Q1 What it explains.** Any model whose output can be evaluated for every subset S of modalities. Shapley values split v(all) − v(∅) fairly across players [7].
- **Q2 Fit.** Ideal. With 2–4 sensors there are only 4–16 coalitions. If v(S) is computed from the cached ledger, no extra forward passes are needed (75 µs measured, §2). A non-additive fusion head (e.g. an MLP over concatenated features) would need 2ⁿ evaluations of *the head only*, which is still cheap. But then "absent" must be defined for that head.
- **Q3 Children.** Yes, shown as "who found the clues" (sensor-coloured weights on a balance) rather than as numbers.
- **Q4 Modalities.** Yes, by definition.
- **Q5 Cost.** Negligible.
- **Q6 Limitations.** Everything hinges on **the value of a missing modality**. The options are:
  - (i) a fixed baseline input (zeros, black frame, silence), the "Baseline Shapley/BShap" family;
  - (ii) the marginal/interventional expectation over a background set;
  - (iii) the conditional/observational expectation;
  - (iv) a retrained or marginalised model without the modality.

  These give different attributions, and some can credit features the model does not use [4][5][6]. Janzing et al. argue that *interventional* (unconditional) expectations are the right notion of "dropping" a feature [6]. SHAPE [3] uses zeros for one missing modality and a majority-class predictor when all are missing. For our product-of-experts fusion, **marginalisation (omit the term)** is principled and matches what the toggle does, so the explanation and the intervention coincide.

  The output space must also be chosen. Shapley in probability space mixes in interaction and prior effects (§2). If the fusion ever becomes non-additive (cross-modal gating), per-sensor bars stop being complete. In that case compute pairwise **Shapley interactions** with shapiq 1.7.0 (MIT, released 2026-08-27, Python ≥ 3.12; NeurIPS 2024 D&B) [93] and show the interaction explicitly, or better, keep the fusion additive. **Verdict: USE, in log space.**

### 3.2 KernelSHAP / PartitionSHAP on features
- **Q1.** Model-agnostic Shapley estimation [7]. KernelSHAP is a weighted linear regression over sampled coalitions, with absent features filled from a background dataset [8]. PartitionSHAP computes Owen-type values over a feature hierarchy, with "quadratic exact runtime" for a balanced tree [9]. For linear models it equals standard Shapley values [9].
- **Q2.** On pixels/superpixels: default `nsamples = 2·M + 2048` [8], about 2.6 min per explanation for CLIP B/32 on this CPU (§2), so not live. On our fusion features it is redundant, because exact Shapley is trivial (§3.1).
- **Q3.** Superpixel heatmaps are moderately understandable.
- **Q4.** Only if modalities or concepts are made the players.
- **Q5.** Hundreds to thousands of forward passes.
- **Q6.** Background/baseline dependence [4][5][6]. Off-manifold masked inputs, which an adversarial model can even exploit to hide biases [11]. Sampling variance. **Verdict: AVOID live.** shap 0.52.0 (MIT, released 2026-05-28) [10] is fine for offline comparison.

### 3.3 MM-SHAP (Parcalabescu & Frank, ACL 2023)
- **Q1.** Pretrained VL transformers (CLIP, LXMERT, ALBEF) on *image–text pairs*. Text tokens and image patches are the Shapley players. **T-SHAP = Σ|φ<sub>text</sub>| / (Σ|φ<sub>text</sub>| + Σ|φ<sub>image</sub>|)**, and V-SHAP = 1 − T-SHAP. Text is masked with `[MASK]` and image patches are zeroed (≈16 patches) [1].
- **Q2.** **Mismatch.** In our pipeline CLIP's text input is our *fixed concept prompt*, not a sensor. MM-SHAP would measure "prompt vs image" reliance, not "camera vs microphone". ASR text and camera are fused *late*, outside any VL model.
- **Q3.** A single percentage. Because it uses absolute values, the *direction* (for vs against) is lost.
- **Q4.** Yes, but only for two modalities inside one model.
- **Q5.** 2p+1 model evaluations with p ≈ 40 tokens. These coalitions are a *Monte Carlo sub-sample*, so scores are approximate per sample (paper §Limitations). About 3 s per pair for CLIP on an NVIDIA Titan X [1], which suggests several seconds on our CPU (UNVERIFIED).
- **Q6.** Zero-pixel masking is out-of-distribution [63]. It is performance-agnostic by design: it tells you a modality was *used*, not that it was used *correctly* [1]. **Verdict: AVOID live.** Relevant only if we later adopt an early-fusion VLM. Code: MIT [1].

### 3.4 Perceptual score (Gat et al., NeurIPS 2021) and SHAPE (IJCAI 2022)
- **Q1.** Any multimodal classifier. The perceptual score permutes one modality *across test samples* and measures the drop in accuracy. It is normalised by majority-vote or model accuracy, with **5 permutations per sample** in the paper [2]. SHAPE turns this into Shapley values over modalities, with accuracy as the utility, and adds a *cooperation* score [3].
- **Q2.** It needs labels and *other samples' modality data*. Doing it live would mean injecting another visitor's audio or video into someone's explanation, which is a privacy problem. It works offline on recorded, consented calibration data.
- **Q3.** No.
- **Q4.** Yes, but globally (dataset level), not per visitor.
- **Q5.** K permutations × dataset size.
- **Q6.** For more than 2 modalities it measures contribution *conditional on all other modalities* [3]. Being accuracy-based, it misses cases where a modality is used but the prediction is wrong [1]. **Verdict: offline system validation only** ("does our fusion actually use the audio?"). In our additive fusion, the *aggregate* |φ<sub>m</sub>| over many sessions gives a cheap SHAPE-like statistic with no permutation. It can feed an anonymous "today the robot's eyes found 61% of all clues" panel that stores counters only. The prototype's `sensor_share` is this statistic per session [102].

### 3.5 Modality ablation / dropout and leave-one-modality-out (LOMO)
- **Q1.** Any model.
- **Q2.** The visitor's toggle *is* LOMO. In our additive fusion, LOMO = Shapley = φ<sub>m</sub>, so the preview is exact with no extra inference. The prototype precomputes the belief for **every sensor configuration** (`counterfactuals`) and each sensor's opinion "alone" [102]. Modality *dropout during training* (for robustness to missing inputs) is unnecessary with frozen encoders plus Bayesian fusion.
- **Q3.** Very understandable. It is embodied and hands-on, matching Long & Magerko's design considerations *Embodied Interactions* and *Promote Transparency* [70][95].
- **Q4.** Yes.
- **Q5.** n extra fusion evaluations, which is free.
- **Q6.** In *non-additive* models, LOMO under-credits redundant modalities: if camera and ASR both say "likes dogs", removing either changes little. It also cannot show synergy (cf. the redundancy/uniqueness/synergy decomposition in [87]). In our design this matters only through correlated evidence (§4). **Verdict: USE.**

### 3.6 Integrated Gradients (IG)
- **Q1.** Differentiable models. IG integrates gradients along a straight path from a baseline to the input and satisfies completeness [12].
- **Q2.** On our log-linear fusion, IG with a zero-evidence baseline reproduces φ<sub>m</sub> exactly, so it is redundant there. On pixels it needs 20–300 steps [12]: about 10 s (B/32) or 24 s (SigLIP2) for 32 steps on this CPU (§2).
- **Q3.** Pixel-level IG maps are noisy and hard for children to read.
- **Q4.** No, unless applied at the fusion.
- **Q5.** 20–300 forward+backward passes.
- **Q6.** **Baseline choice.** With a black baseline, black pixels get zero attribution even when they are the object [13]. Blurred, uniform, Gaussian or "expected gradients" baselines encode different notions of missingness [13]. Saliency methods can be input-shift-sensitive [59] and fragile [60]. **Verdict: AVOID live.**

### 3.7 Grad-CAM and CLIP-specific saliency (LeGrad, gScoreCAM, CLIP Surgery, Chefer et al., Grad-ECLIP)
- **Q1.**
  - *Grad-CAM*: gradient-weighted class activation maps for CNNs [14]. ViT use requires reshaping tokens. `pytorch-grad-cam` (grad-cam 1.5.7, 2026-08-21, MIT) supports ViTs, has CLIP examples, and implements ROAD metrics [65].
  - *LeGrad* (Bousselham et al., **ICCV 2025**): uses gradients w.r.t. the attention maps of all ViT layers as the signal. It is built as a wrapper around **open_clip** and reports 48.4 p-mIoU on OpenImagesV7 with OpenCLIP ViT-B/16 [91]. Repo MIT [91]. **But** `legrad_torch` 1.1 (PyPI, 2024-10-14) declares `open-clip-torch<=2.23.0` and has an empty licence field [92], while the project uses open_clip 3.3.0. Vendor the method (about one file) rather than pip-installing it into the exhibit environment.
  - *gScoreCAM* (ACCV 2022, MIT): ScoreCAM over the top-300 of 3,072 channels, about 8–10× faster than ScoreCAM [15]. The 3,072 channels are layer 4 of the **ResNet** CLIP RN50x16, where its gains were shown. On CLIP ViT-B/32 the paper's Table 4 has it only *on par with* Chefer et al. So it is not the right choice for our ViT encoders.
  - *CLIP Surgery* (Pattern Recognition 2025): training-free changes to the inference architecture. It identifies CLIP's **"opposite visualization"** (raw maps highlight background over foreground) and **noisy activations** [16].
  - *Chefer et al. ICCV 2021*: relevancy propagation for bi-modal and encoder-decoder transformers, with a CLIP notebook (MIT) [17]. Its predecessor goes "beyond attention visualization" [18].
  - *Grad-ECLIP* (IEEE TPAMI 2026): channel and spatial weights on token features, giving image *and* word heatmaps for CLIP matching [19].
- **Q2.** These run on the frozen image encoder for a given concept prompt. Gradient methods (LeGrad, Grad-CAM, Grad-ECLIP, Chefer) need one forward+backward: 322 ms for B/32, 761 ms for SigLIP2 (measured). gScoreCAM needs about 300 forwards, roughly 20 s on CPU (UNVERIFIED extrapolation). **The target must be the same quantity the fusion uses**: the calibrated contrast score (prompt minus contrast prompt), on the **same head/torso crop** the live pipeline scores [102]. It must not be raw similarity to one prompt on the full frame.
- **Q3.** Melsión et al. showed Grad-CAM to **78 children aged 10–14**, and their understanding of gender bias improved significantly [75]. So heatmaps *can* work at this age with scaffolding. With adults, saliency maps gave "very limited help" in anticipating a CNN's output [68].
- **Q4.** No. These are within-image only.
- **Q5.** See Q2.
- **Q6.**
  - Guided Backprop and Guided Grad-CAM **fail** the model-randomisation sanity test; gradients and Grad-CAM pass (on CNNs) [57][58].
  - Saliency maps are fragile [60].
  - CLIP-specific failure modes exist (opposite visualisation [16]).
  - **Licences:** Grad-ECLIP and CLIP Surgery have no LICENSE file and no licence mention in their READMEs. Default copyright therefore applies (all rights reserved), so re-implement from the paper or use MIT-licensed LeGrad, Chefer or pytorch-grad-cam.
  - A heatmap on a child's face invites a "face analysis" reading. Prefer body-, object- or scene-level concepts and stylised frames. Glasses are the one face-region concept, so for glasses show the icon, not a heatmap.

  **Verdict: optional Phase-2 keyframe "spotlight"**, deployed only after offline sanity and deletion/insertion/ROAD checks (§5). Prefer occlusion (§3.9) for conceptual coherence with the toggle. LeGrad is the best gradient option for open_clip ViTs.

### 3.8 Attention maps and attention rollout
- **Q1.** Transformers.
- **Q2.** Attention can be read from the CLIP ViT in one forward pass, but it is *class-agnostic*, so it cannot explain *a specific concept*.
- **Q3.** It looks intuitive ("where the robot looks"), and that is exactly why it misleads.
- **Q4.** No.
- **Q5.** One forward pass.
- **Q6.**
  - Jain & Wallace found attention weights often uncorrelated with gradient and leave-one-out importance, and very different attention distributions can give the same prediction [21].
  - Wiegreffe & Pinter rebut the strong claim but do not establish attention as a faithful explanation [22].
  - Information mixes across layers. Rollout and flow are approximations proposed to cope with that [20].
  - Later work moved to relevancy propagation and gradient-weighted attention because rollout-style heuristics are limited [18][91].
  - For CLIP specifically, raw self-attention links inconsistent semantic regions [16].

  **Verdict: AVOID visitor-facing.**

### 3.9 Occlusion and RISE
- **Q1.** Any black box. Occlusion slides a mask over the input [23]. RISE averages random masks weighted by output [24].
- **Q2.** Coarse occlusion on *one keyframe* when an attribute "locks in" is feasible: a 3×3 or 4×4 grid is 9–16 passes, about 0.5–1.2 s on CPU for B/32. RISE used 4,000 (VGG16) and 8,000 (ResNet50) masks [24], which takes minutes on CPU, so it is offline only.
- **Q3.** Good: "If the robot couldn't see this part of the picture, it would be less sure you're holding a ball." That is the *same counterfactual logic as the sensor toggle* at finer grain, which is pedagogically coherent.
- **Q4.** Within one modality. The same idea gives leave-one-word-out for ASR and leave-one-segment-out for audio.
- **Q5.** See Q2.
- **Q6.**
  - **Missingness bias**: grey or black patches are out-of-distribution; ViTs allow token dropping instead [63].
  - The fill (grey, blur, crop) changes results [24].
  - Single-patch occlusion ignores interactions.
  - Grid size is arbitrary.

  **Verdict: optional live, coarse grid, blur or token-drop fill. RISE offline only.**

### 3.10 LIME
- **Q1.** Any black box, via a local sparse linear surrogate on superpixels [25].
- **Q2.** The image default is `num_samples=1000` [25], about 73 s on this CPU. The last package release was 0.2.0.1 in **June 2020** [25].
- **Q3.** Moderate.
- **Q4.** Only if modalities are made features, where exact Shapley is cheaper and exact.
- **Q5.** 1,000+ forward passes.
- **Q6.** Unstable for similar inputs [26]. Dependent on neighbourhood size [1]. Can be fooled adversarially [11]. **Verdict: AVOID.**

### 3.11 Counterfactual explanations (the toggle, and "what would change the robot's mind")
- **Q1.** Model-agnostic: the smallest change that would flip the outcome [27]. People's everyday explanations are contrastive ("why P rather than Q?") [28].
- **Q2.** Three kinds, all computed from the ledger with **no extra inference**:
  - (i) **interventional**: the physical sensor toggle, a true causal intervention on the system's inputs;
  - (ii) **preview**: ghost bars, e.g. "if you switch the eyes off, the glasses-scale goes back to the middle";
  - (iii) **evidence gap**: "the robot needs about 2 more clues to be sure", computed as (threshold − L<sub>a</sub>) divided by the typical per-clue contribution.

  Recent work generates image-only / text-only counterfactuals with coupled diffusion priors and turns them into Shapley modality scores for multimodal LLMs (CMA, arXiv July 2026) [94]. It is far too heavy for us, and unnecessary, because our toggle *is* an exact counterfactual. It does confirm the framing: "which modality decides?" is a question that accuracy alone cannot answer [94].
- **Q3.** Very understandable: "What if…" maps directly onto the hands-on toggle.
- **Q4.** Yes, at the modality level by construction.
- **Q5.** About zero.
- **Q6.** Input-space counterfactuals can suggest changing *who you are*. Restrict "mind-changers" to **actionable, playful, non-identity concepts**: hold up a card or toy, wave, say a word. Never "look older/different". Many counterfactuals exist, so choose one deliberately. **Verdict: USE (core).**

### 3.12 Concept bottleneck models: CBM, label-free CBM, post-hoc CBM
- **Q1.**
  - *CBM* (Koh et al. 2020): input → human-named concepts → label, trained with concept labels. It supports test-time **concept interventions** [29].
  - *Label-free CBM*: GPT-3-generated concept sets, a CLIP-Dissect projection and a sparse final layer, trained without concept labels [30].
  - *Post-hoc CBM*: projects any pretrained embedding onto concept vectors (from examples or CLIP text) plus a sparse linear head (MIT) [31].
- **Q2.** Our pipeline *is* a CBM whose "label" is the concept itself. **Per-concept linear probes on the CLIP image embedding** are the fallback where prompts are weak (our data: +0.07–0.08 AUROC for the weak concept, §2.2). They stay faithful because the probe output is what the fusion uses. Label-free CBM needs a downstream task and dataset, and its LLM-generated vocabulary is uncontrolled: it could introduce sensitive or emotion concepts.
- **Q3.** Concept names are child-readable. Keep the vocabulary small: concept explanations lose practical usefulness beyond about **32 concepts** even for adults [38].
- **Q4.** Yes, with separate concept heads per sensor.
- **Q5.** Negligible at inference; minutes of training for probes.
- **Q6.**
  - **Leakage**: concept activations encode more than the named concept [32][33][34]. This matters little for us, since no downstream head exploits leaked information.
  - **Entanglement of CLIP concept scores**: related concepts get entangled, so individual scores "do not reflect their intended meaning" [36] (preprint, 2026-09).
  - **Negation failure**: VLMs perform at about chance on negated queries [37], so never use "not wearing glasses" prompts; use contrast prompts or probes.
  - **Concept names may not mean what they say**: random-word descriptors match LLM descriptors in zero-shot accuracy [35].

  **Verdict: USE a curated CBM. AVOID label-free CBM.**

### 3.13 TCAV
- **Q1.** Global sensitivity of a *class* to a concept direction (a CAV learned from example sets) at an internal layer [39].
- **Q2.** Not per visitor. It needs concept example sets and gradients. Captum 0.9.0 (BSD-3) implements it [66].
- **Q3.** No.
- **Q4.** No.
- **Q5.** Concept sets, random sets and statistical tests.
- **Q6.** Different probe datasets can give very different explanations [38]. **Verdict: AVOID**, since we have no hidden class to explain.

### 3.14 Prototype-based explanations
- **Q1.** ProtoPNet: "this looks like that" part-prototypes inside a purpose-trained network [40].
- **Q2.** Needs training. The prototypes would be crops of *other people*, which is a privacy problem.
- **Q3.** Very intuitive.
- **Q4.** Possible.
- **Q5.** Training.
- **Q6.**
  - There is a semantic gap between latent and human similarity; even JPEG artefacts can give incomprehensible prototype matches [41].
  - Prototypes need extra explanation of *why* they are similar [42].
  - Example-based explanations helped in simulation tests [67], but only when the decision really is example-based.

  **Verdict: AVOID as a decision explanation.** Illustrated "concept cards" ("what the robot looks for when it checks for glasses") are fine if labelled as *concept examples*, not reasons. The VHX exhibit used laminated example photos the same way and visitors used them to probe the AI [99].

### 3.15 Natural-language explanations: templates vs LLMs
- **Q1.** Templates verbalise the ledger. LLM explanations are generated text that need not reflect the computation.
- **Q2.** Templates: yes, at zero cost and fully local; the prototype already does this [102]. LLMs: possible, but they add latency, safety and privacy risk.
- **Q3.** Both are child-friendly if the wording is designed. Templates can be tested and translated (EN/FR/NL/PL).
- **Q4.** Templates state only what the ledger says per sensor.
- **Q5.** Templates ≈ 0.
- **Q6.** Chain-of-thought explanations "systematically misrepresent the true reason". Biasing features dropped accuracy by **up to 36% on 13 BIG-Bench Hard tasks**, and the explanations did not mention them (GPT-3.5, Claude 1.0) [43]. Plausibility ≠ faithfulness [44]. **Verdict: templates live.** An LLM may only *draft template variants offline*, reviewed by humans. Every sentence slot must map to a ledger field (unit-tested).

---

## 4. Uncertainty quantification

| Method | Captures | Works with frozen models + late fusion? | Cost | Verdict |
|---|---|---|---|---|
| Bayesian evidence accumulation (log-odds / Beta / Dirichlet) | Belief **and** amount of evidence | **Yes** (it is the fusion) | ~0 | **USE** |
| Entropy of P(a) | Total uncertainty (conflates ignorance and conflict) | Yes | ~0 | Use only together with evidence volume |
| Temperature / Platt scaling | Per-model or per-concept miscalibration | **Yes** (post-hoc, needs a labelled set) | ~0 | **USE** (done per frame, §2.2) |
| Selective classification (calibrated "I'm sure" threshold) | Precision of displayed claims | **Yes** | ~0 | **USE** (on fused session beliefs) |
| Conformal prediction sets | Coverage-guaranteed "one of these" sets | **Yes** (any model) | ~0 at runtime | **USE** for categorical attributes |
| MC dropout | Approximate Bayesian epistemic uncertainty | **No** (CLIP has no dropout) | T forward passes | **AVOID** |
| Deep ensembles | Epistemic uncertainty via model disagreement | Not by retraining CLIP; a 2-model committee is possible | ×M compute | Optional (CLIP + SigLIP disagreement) |
| Evidential deep learning | Claimed epistemic uncertainty from one network | Needs training | — | **AVOID** |

- **Evidence accumulation.** Fused log-odds plus (E<sup>+</sup>, E<sup>−</sup>) is equivalent to a Beta "clue jar": the colour ratio is the belief and the fill level is the amount of evidence. Subjective logic (as used by EDL) formalises this as belief b<sub>k</sub> = e<sub>k</sub>/S and uncertainty u = K/S over a Dirichlet [52]. We get the interpretability of the evidence view without training an EDL network.
- **Calibration.** Modern nets are often over-confident. A single temperature fixes softmax calibration without changing accuracy [45]. CLIP *zero-shot* is poorly calibrated across prompts, datasets and architectures, and a single learned temperature per CLIP model generalises [46]. For *binary* concepts use per-concept Platt scaling (2 parameters) on the contrast score. This brought ECE to 0.08–0.10 for B/32 in our test (§2.2).
- **Selective classification.** "Only show a model's prediction when it is confident… otherwise say 'I don't know'" [47]. Set the threshold for the words **"I'm sure"** so that those claims are, say, ≥90% correct on held-out **whole sessions**. The verbal scale itself then becomes calibrated. The prototype currently uses fixed thresholds (0.75/0.50/0.25 on rescaled max-probability), which are not yet calibrated (§8.7).
- **Conformal prediction.** The guarantee is **marginal** 1−α coverage under **exchangeability** [47]. About **1,000 calibration points** gives coverage typically between **0.88 and 0.92** at α = 0.1 [47]. Conditional, per-group coverage is *not* guaranteed, so check stratified coverage (lighting, clothing colour) [47]. Booth lighting and crowd noise break exchangeability, so recalibrate on day 0 with staff. Adaptive conformal inference handles drift but needs ongoing true labels [48]. In an RCT, conformal sets improved human accuracy compared with fixed-size sets (adults) [49]. For binary attributes the set is {yes}, {no} or {yes, no}, which maps naturally onto "I'm sure / I'm sure it's not / I'm not sure". Libraries: MAPIE 1.5.0 (BSD-3, 2026-08-05), crepes 0.9.1 (2026-06-12, BSD-3; implements "standard and Mondrian conformal classifiers", including class-conditional ones [86]), TorchCP 1.2.1 [86].
- **MC dropout** treats test-time dropout as approximate Bayesian inference [50]. It needs trained dropout, and the local CLIP B/32 has none (§2). **Deep ensembles** train M independent networks [51], which is infeasible for CLIP. A CLIP+SigLIP committee costs about 128 + 236 ms per frame and gives a disagreement signal, not a posterior.
- **Evidential deep learning** [52]. Critiques:
  - no second-order loss incentivises faithful epistemic uncertainty [55];
  - EDL's epistemic uncertainty is not faithfully represented [54];
  - EDL's UQ "capabilities" are a mirage and are better read as an energy-based OOD detector [53].
- **Missing modalities: prior vs marginalisation.**
  - Omitting a sensor's term = marginalisation, which keeps the other sensors' evidence.
  - "Reset to prior" throws away *all* evidence.
  - Zero or black-frame imputation is a *fabricated observation*.

  Product-of-experts fusion (e.g. MVAE) similarly works with any subset of modalities [56]. The prototype's test `test_missing_modality_falls_back_to_flat_prior` covers the all-off case [102].
- **Correlated evidence (the main overconfidence risk).** Consecutive frames are not independent, and ASR text, loudness and CLAP all come from the *same* microphone. Naive summation double-counts. Mitigations:
  - a per-window discount, or the prototype's saturating κ = 1 − exp(−Σq·w/τ), τ = 1.5, with frame weight 0.2–0.5 vs spoken word 2.0 [102];
  - per-window clipping;
  - a likelihood floor (the prototype uses 0.05);
  - treating "Ears" as one toggle group.

  Fit τ, the weights and the floor by minimising ECE of the **fused** belief on recorded sessions. Current values are **design guesses (UNVERIFIED)**.

---

## 5. Evaluating the explanations

| Level | Test | Pass criterion | Tool |
|---|---|---|---|
| Fusion faithfulness (unit tests, CI) | Completeness (prior + Σ clues = displayed score); toggle-off score = score − clue<sub>m</sub>; **sum of displayed clue cards (incl. counter-clues) = scale**; every template slot ↔ a ledger field | Exact equality (float tolerance) | pytest. The prototype has 7 passing tests, including `test_clues_are_exact_shapley_and_lomo_and_sum_of_cards` [102] |
| Calibration | Reliability diagram / ECE per concept **and for fused session beliefs**; empirical coverage of conformal sets; precision of "I'm sure" claims | ECE small; coverage ≈ 1−α; precision ≥ target | MAPIE/crepes [86]; `calibrate_vision.py` [102] |
| Saliency (only if used) | Model- and data-randomisation sanity checks [57][58]; deletion/insertion AUC [24]; ROAD (MoRF/LeRF), which avoids retraining and saves up to 99% compute vs ROAR [62]; ROAR found many methods no better than random [61] | Map changes under randomisation; beats random and occlusion baselines | pytorch-grad-cam ROAD metrics [65]; Quantus (LGPL-3.0) [64]; Captum [66] |
| Modality usage (system level) | SHAPE / perceptual-score-style analysis on recorded team data [2][3]; aggregate \|φ<sub>m</sub>\| | Each sensor contributes for the concepts it should | own scripts |
| Human-centred (children) | **Forward simulation**: "If we switch the mic off, will the robot be more or less sure?" before vs after the explanation [67]; AI-literacy items mapped to Long & Magerko competencies *Sensors*, *Representations*, *AI Strengths & Weaknesses* [70][95] and AI4K12 Big Ideas 1–2 [72]; observation of family talk [71][99] | Improvement over a no-explanation condition. Subjective ratings alone do **not** predict helpfulness [67] | Ethics approval and parental consent required |

---

## 6. What research says about explaining AI to children and in museums

- **AI literacy frameworks.**
  - Long & Magerko define AI literacy as competencies to "critically evaluate AI technologies; communicate and collaborate effectively with AI…" [70].
  - The framework has **17 competencies and 15 design considerations**, now verified via the complete lists reproduced in Zhou, Van Brummelen & Lin (Figs 1–2) [95].
  - Competencies directly addressed by our exhibit: **#7 Representations, #15 Sensors, #14 Action & Reaction, #5 AI Strengths & Weaknesses, #13 Critically Interpreting Data, #16 Ethics** [95].
  - Design considerations we implement: **#1 Explainability, #2 Embodied Interactions, #4 Promote Transparency, #5 Unveil Gradually, #10 Support for Parents, #13 Acknowledging Preconceptions, #15 Low Barrier to Entry** [95].
  - AI4K12 Big Idea 1 is **Perception** and Big Idea 2 is **Representation & Reasoning** [72]. Our exhibit maps almost 1:1 onto these two.
- **Museum exhibits.**
  - Long, Blunt & Magerko co-designed low-fidelity AI exhibits with families, including a *Sensor Wall* and a *Magic Mirror* that compares sensors to body organs [71]. Families explored sensors physically (clapping, whistling, volumes) and pointed out sensor limitations. Parents and older children read cards aloud to younger ones, and privacy concerns surfaced spontaneously.
  - The **Virtually Human Experience (VHX)** at the Lawrence Hall of Science (ages 7–12 with families; NSF DRL 2116109) found three things in case studies [99]:
    - (i) interactions were typically collaborative. Parents used brief sign prompts that compare "how you would do it" with "how the AI does it";
    - (ii) **impromptu experimentation drove learning**. Twins came back to "trick" the AI, and children re-purposed a two-class trainer as glasses / no glasses;
    - (iii) visitors discovered **shortcut learning** on their own: the model learned *head position* instead of expression, because people looked at the side of the screen where their photo appeared. [corrected by verifier: the paper says the model "sometimes" learned head position "in addition to or instead of" the intended Silly/Serious classes. This *sometimes led to frustration* when visitors did not realise it, and "museum facilitators, and often parents, were instrumental" in turning confusion into discovery. So discovery was supported by facilitators and parents, and not reliably independent. Design implication: staff or the signage should point out shortcut clues. Source: full text, https://par.nsf.gov/servlets/purl/10528574]

    Design features that helped were redundancy, "show in addition to tell", and deliberate pauses [99]. Note: VHX includes facial-expression classification, which **cannot be copied in our EU setting** (Art. 5(1)(f); see [103]).
  - Implications: **embodied toggles, read-aloud-friendly text, parent prompts on signage, explicit room for "fool the robot" experiments, and an explicit privacy story.**
- **Children's perceptions and trust.**
  - Children aged 3–10 (N = 26) mostly saw agents as friendly and genuine [73].
  - After training and coding ML programs, children aged 7–12 (N = 52) became **more sceptical** and shifted agency from the device to the people who program it [74]. Letting children *see and steer* the evidence is the right lever.
  - In a word-guessing game with 168 children aged 4–7 and 168 adults, **older children were less trusting than younger children and adults, and even more sceptical after errors**. They kept trusting longer when a *robot* (but not a human) apologised for its mistake [98]. Implication: a robot that says "I was wrong, my camera was fooled" supports calibrated trust.
  - Children tend to over-trust robots, and a robot expressing uncertainty has been proposed to induce a critical attitude [77].
- **Explanations with this age group.**
  - Grad-CAM explanations improved 10–14-year-olds' understanding of gender bias in AI (N = 78) [75].
  - A K-12 spoofing + CAM game (ages 10–15) exists, without outcome data yet [76].
- **Children and probabilities.**
  - Given probabilities (%), 4th–6th graders' Bayesian answers were **zero**. Given **natural frequencies**, 19%, 39% and 53% answered correctly (grades 4, 5, 6), and sixth graders matched adults with probabilities [96]. [corrected by verifier: more precisely, sixth graders *using natural frequencies* performed as well as *adults given probabilities*. About one-third of sixth graders still solved none of the problems (abstract, via Europe PMC, DOI 10.1016/j.cognition.2004.12.003). The children were Chinese, and the replication [97] was in Italy.]
  - **But** an Italian replication found much lower success. Accuracy depended on the *question type*, not the format (natural frequency vs "number of chances") [97].
  - Implication: never show percentages, and do not expect children to *compute* with counts. Use counts only as an illustration ("7 out of 10 robots"), and carry the main message qualitatively (scale tilt, fuzziness, words).
- **Cautions from adult studies.**
  - Explanations can increase acceptance of AI advice *regardless of correctness* [69].
  - Saliency maps gave limited help in predicting model outputs [68].
  - Self-rated helpfulness does not track real helpfulness [67].
  - **Design for calibrated trust**: include a "fool the robot" moment and an "I'm not sure" state that actually occurs.
- **Gap.** I found no peer-reviewed study of *uncertainty visualisation specifically for 8–14-year-olds* (UNVERIFIED that none exists). Pilot testing at the stand is needed, and is itself a publishable contribution.

---

## 7. Visualising uncertainty for lay audiences, adapted for 8–14

| Technique | Evidence | Our use |
|---|---|---|
| **Fuzziness / blur** | Fuzziness, along with location, value, arrangement, size and transparency, rated highly intuitive for uncertainty [81] | Avatar features drawn sharper as P(a) moves away from 0.5; unknown features as a sketchy outline |
| **Frequency formats / icon arrays** | Icon arrays help people with low numeracy [82]; natural frequencies helped some 9–12-year-olds [96], with mixed replication [97] | "If 10 robots had these clues, 7 would say 'glasses'" (10-icon strip, never percentages), as an *illustration* only |
| **Quantile dotplots** | Reduced the variance of probability estimates by about 1.15× vs density plots [78] | For the "how many clues" meter, discrete dots instead of a continuous bar |
| **Hypothetical outcome plots (animated draws)** | Better than error bars and violin plots for multi-quantity judgements [79] | For a conformal set {red, orange}, the T-shirt colour *flickers* between members |
| **Verbal labels** | "I don't know" output via selective classification [47]; robot uncertainty to counter over-trust [77]; robot apology sustains older children's trust [98] | 3–4 levels: **"I'm sure" / "I think" / "I'm guessing" / "I don't know yet"** (prototype wording [102]) + "I can't tell: my eyes are switched off" |
| General guidance | Review of techniques and cognitive trade-offs [80] | Avoid bare percentages; pair every graphic with a sentence |

---

## 8. Recommendations for our demonstrator

### 8.1 The faithful XAI stack

| Layer | Shown to visitor | Computed how | Why it is faithful | Cost |
|---|---|---|---|---|
| L0 Sensor state | Physical toggles with an LED per sensor; lens shutter; on-screen eye/ear icons; "no data from camera since 12:03:15" | Toggle **gates data at the source**: the device handle is released, and frames/audio are never processed [103] | The "off" claim is literally true | 0 |
| L1 Clue cards (per sensor) | "[eye] saw: glasses-like shape (6×)" / "[eye] *but* 1 frame: no frame visible" / "[ear] heard you say: *dog*" / "[ear] sound level now: loud" | Ledger rows: concept, sensor, calibrated p. ASR shows **only matched vocabulary words**, never the transcript. **Counter-clues are shown too** | Each card is a row the fusion actually summed, and the cards sum to the scale | 0 |
| L2 Balance scale per attribute | Sensor-coloured weights on the pans; tilt = belief; empty vs heavy pans = ignorance vs conflict | Per-sensor clue, E<sup>+</sup>, E<sup>−</sup> from the log-space fusion | = exact Shapley = LOMO (additive game) | 0 |
| L3 Counterfactual preview | Hover or half-press a toggle shows a ghost scale "without eyes…"; "needs ~2 more clues to be sure" | Precomputed belief for every sensor configuration; evidence gap | Same function as the real intervention | 0 |
| L4 Uncertainty | Fuzzy or flickering avatar features; verbal levels; "one of these" swatches | Calibrated P(a); selective-classification thresholds; split-conformal sets | Calibrated on held-out sessions; coverage audited | 0 at runtime |
| L5 Sentences | "My eyes found 6 glasses-clues and 1 against. I think you're wearing glasses." | Templates over ledger fields (EN/FR/NL/PL) | Every slot is a ledger value (unit-tested) | 0 |
| L6 (optional, Phase 2) Spotlight | Soft spotlight on a *stylised* keyframe for one locked-in object/scene concept (not on faces) | 3×3 or 4×4 occlusion with blur/token-drop fill, or vendored LeGrad, targeting the *calibrated contrast score on the same crop* | An intervention on the actual scorer; passes sanity and ROAD tests offline | ≈0.3–1.2 s per keyframe |

### 8.2 Interaction script (3–5 min): "Unveil Gradually" + "Embodied Interactions" [70][95]
1. **All sensors off.** Empty scales and a blank silhouette: "I know nothing about you yet." This also serves as the AI Act Art. 50(1) disclosure moment: "I am an AI. Here is what my sensors can use" [100][103].
2. **Eyes on.** Visual clue cards appear, scales tilt, avatar features sharpen.
3. **Ears on.** Prompt: "Tell the robot your favourite animal." Word clue cards and a sound-level meter appear.
4. **Predict, then toggle.** "What will happen if we switch the eyes off?" The child guesses, then toggles, and the ghost-scale animation confirms or contradicts. This is a built-in simulatability probe [67].
5. **Fool the robot.** Hold up a picture of a cat while saying "dog", or put on prop glasses. The robot is confidently wrong, or sees conflicting clues: "Evidence isn't truth." Then the robot apologises: "My eyes were fooled" [98].
6. **Summary and forget.** A postcard of the procedural avatar with its evidence. A "Forget me" button visibly empties the ledger (session data is deleted anyway).

### 8.3 Concept vocabulary rules (XAI-relevant; legal detail in [103])
- **About 6–25 concepts in total, at most 5 on screen at once.** Usefulness drops beyond about 32 concepts even for adults [38]. The prototype has 6 slots [102].
- **Only visible or audible, non-sensitive, actionable concepts.** These are ACCEPTABLE per the attribute register [103]:
  - clothes colour (dominant colour only);
  - glasses (no eyesight conclusion);
  - holding a toy, book or ball;
  - waving or raising a hand;
  - clapping;
  - momentary movement ("lots of movement right now");
  - momentary sound level;
  - closed-vocabulary favourite-thing words;
  - distance to the robot;
  - number of people.
- **Out: hats/headwear** (can reveal religion), **hair colour** (Recital 16 categorisation category → Art. 50(3) notice; ethnicity proxy), **pitch as a personal label**, accent/language, height, age, gender, attractiveness, health, gaze/attention, and interaction style [103].
- **Never infer emotion.** A "smile" may be detected only as a mouth movement and must never be turned into "happy". Recital 18 excludes mere detection of readily apparent expressions *unless used to infer emotions* [83]. Art. 5(1)(f) prohibits emotion inference in workplaces and education institutions (since 2 Feb 2025). The ethics track treats it as prohibited for us [103].
- **Legal scope, stated precisely.** Art. 5(1)(g) bans biometric categorisation inferring race, political opinions, trade-union membership, religious or philosophical beliefs, sex life or sexual orientation [83]. It does **not** list age or gender. Avoiding those is a design, GDPR and child-safety choice, and any non-prohibited biometric categorisation would trigger an **Art. 50(3) notice duty** [100][103].
  - Art. 50 applies from **2 Aug 2026**, so it binds us at SiW (17–19 Mar 2027).
  - The Digital Omnibus on AI (Reg. (EU) 2026/1744, in force 27 Jul 2026) deferred Annex III high-risk obligations to 2 Dec 2027, but did not change Art. 5 or the rest of Art. 50 [101][103]. [corrected by verifier: the Omnibus *did* amend Art. 5. It inserted new prohibitions Art. 5(1)(ba) (non-consensual intimate imagery) and 5(1)(bb) (CSAM), which apply from 2 Dec 2026. Neither is relevant to this exhibit, and points (f) and (g) are unchanged. In Art. 50 it only gave generative systems already on the market before 2 Aug 2026 a grace period for 50(2) marking, until 2 Dec 2026. The 50(1) and 50(3) duties still apply from 2 Aug 2026. It also rewrote Art. 4 (AI literacy) from a duty of result into a duty to "take measures to support" literacy, and deferred Annex I high-risk obligations to 2 Aug 2028. Sources: https://artificialintelligenceact.eu/article/5/ ; https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ ; https://www.regulation-ai.eu/en/changes/]
- **Speaking speed** only from the robot's side ("I needed 3 s to understand"), never "slow/fast talker" [103].
- **No face-identity processing and no stored embeddings.** Biometric data under GDPR means data "which allow or confirm the unique identification" of a person [84].
- **Use contrast prompts or linear probes per concept, not negated prompts** [37].

### 8.4 Calibration protocol
1. Record labelled clips from **consenting adult staff and volunteers** under booth-like light and noise. Use licensed or public images per concept; the team already uses Open Images V7 for per-frame calibration [102]. Do **not** use visitor data. At most, keep anonymous counters such as "was the robot right? yes/no".
2. Per concept, fit Platt scaling on 50–200 positives and 50–200 negatives (UNVERIFIED sizing heuristic; our glasses set was 120/99). Then fit the fusion's τ, weights and floor on **whole simulated sessions** by minimising ECE of the fused belief.
3. Set the verbal thresholds by selective classification on those sessions (target ≥90% precision for "I'm sure") [47]. Build conformal sets for categorical attributes with about 1,000 calibration points [47]. Report stratified coverage (lighting, clothing colour, foggy/noisy degradations, as in the prototype's session variants [102]).
4. **Day-0 on-site recalibration** with staff; re-check the next day for drift [48].

### 8.5 Software (checked on PyPI/GitHub, 2026-10)

| Purpose | Package | Version (date) | Licence |
|---|---|---|---|
| Vision–language scoring | open_clip | 3.3.0 (installed; PyPI 2026-02-27) [89] | MIT |
| ASR with confidence fields | faster-whisper | 1.2.1 (2025-10-31); exposes `avg_logprob`, `no_speech_prob`, word `probability` [88] | MIT |
| Prosody / loudness features | openSMILE (or plain RMS/VAD) | — | audEERING *research* licence; non-commercial incl. "public demonstrations" [85] |
| Conformal sets | MAPIE / crepes / TorchCP | 1.5.0 (2026-08-05) / 0.9.1 (2026-06-12) / 1.2.1 (2025-10-14) [86] | BSD-3 / BSD-3 / — [corrected by verifier: TorchCP is **LGPL** (LICENSE + LICENSE.GPL per its PyPI description; no licence classifier set), https://pypi.org/project/torchcp/] |
| Offline saliency + ROAD | grad-cam (pytorch-grad-cam) | 1.5.7 (2026-08-21) [65] | MIT |
| ViT/CLIP saliency (optional L6) | LeGrad (vendor the code) | `legrad_torch` 1.1 (2024-10-14) pins `open-clip-torch<=2.23.0` [92] | MIT (repo) [91]; PyPI licence field empty |
| Offline attribution (IG, occlusion, Shapley sampling, TCAV) | captum | 0.9.0 (2026-04-17) [66] | BSD-3 |
| Offline SHAP comparisons | shap | 0.52.0 (2026-05-28) [10] | MIT |
| Shapley interactions (only if fusion is non-additive) | shapiq | 1.7.0 (2026-08-27), Python ≥ 3.12 [93] | MIT |
| Explanation metrics | Quantus | — [64] | LGPL-3.0 |
| CLIP relevancy (offline) | Transformer-MM-Explainability [17]; gScoreCAM [15]; Grad-ECLIP [19]; CLIP Surgery [16] | — | MIT / MIT / no licence (all rights reserved) / no licence (all rights reserved) |

### 8.6 Phased plan
- **Phase 1 (MVP, low risk; largely built in the prototype [102]):**
  - ledger + log-space fusion + L0–L5;
  - unit tests for completeness and LOMO;
  - per-concept calibration;
  - verbal confidence;
  - procedural avatar with fuzziness;
  - **plus the four fixes in §8.7**.
- **Phase 2:**
  - conformal sets for clothes colour and favourite animal;
  - the L6 occlusion/LeGrad spotlight, only if it passes the sanity and ROAD checks;
  - an anonymous aggregate "today's clues by sensor" panel;
  - optional low-privacy sensors (distance/touch) as extra players.
- **Phase 3 (research value):**
  - an ethics-approved study comparing explanation conditions (balance scale vs words only) on children's simulatability and AI-literacy items [67][70][95].

### 8.7 Audit of the prototype's XAI (`prototype/robotsees`, 2026-10-02) [102]

**What is already right:**
- The fusion is additive across sensors (a tempered log opinion pool).
- `sensor_clues` = exact Shapley = LOMO, and this is unit-tested.
- A disabled sensor contributes nothing, with no imputation.
- Neutral priors.
- Counterfactuals for all sensor configurations.
- Each sensor's opinion "alone" plus an explicit disagreement sentence.
- Templates only, no LLM.
- An evidence-volume field (ignorance vs conflict).
- A `NEVER_GUESS` list shown to visitors.
- Headwear removed from the vocabulary.
- 7/7 tests pass.

**Gaps found, with fixes:**

| # | Finding (reproduced locally) | Why it matters | Fix |
|---|---|---|---|
| A1 | `evidence_ranking` keeps only observations with positive push. In a glasses example (6 "glasses-like" frames + 1 contrary frame), the displayed card shows +0.361, but the scale is +0.301. The −0.060 counter-clue is hidden | The cards no longer sum to the scale, and children see one-sided "because" evidence (confirmation framing) | Show the strongest counter-clue per sensor ("but…"). Add a unit test: Σ(displayed cards) = clue<sub>m</sub>, or show an explicit "+ small clues" remainder |
| A2 | Per-card push is a proportional *allocation* of the saturating κ·mean. Removing that contrary frame changes the clue by +0.084, not by its allocated −0.060 | A card's size is not "what would happen without this clue". Only sensor-level numbers are exact counterfactuals | Present cards as "how much this clue counted", not "if you remove it". Keep counterfactual language for sensor toggles only |
| A3 | Verbal levels use fixed thresholds on rescaled max-probability (0.75/0.50/0.25). For binary slots "sure" ⇔ p ≥ 0.875; for 11 colours ⇔ p ≥ 0.77. The per-frame calibration (§2.2) does not cover the fused, multi-frame belief | "I'm sure" may not be ≥90% correct in practice. That is exactly the false precision we want to avoid teaching | Calibrate thresholds per slot by selective classification on recorded/simulated sessions (clean/foggy/noisy variants exist), and report the achieved precision on the info panel |
| A4 | The docstring calls clues "log-odds units", but they are centred log-scores (binary: exactly ½ log-odds, ratio 2.00 measured) | Harmless if unlabelled. Misleading if a technical overlay prints "log-odds" | Label the unit "clue points" in the UI and fix the docstring |

The relevance values r (e.g. camera → favourite colour 0.35) and the frame/word weights are **hand-set design choices** [102]. That is acceptable, and the prototype already explains it to visitors ("eyes can only guess your favourite colour from your clothes"). They should still be listed on the technical info panel as *assumptions*, not learned facts.

---

## 9. Pitfalls / what not to do

1. **Implementing "sensor off" as zeros, a black frame or silence.** A black frame is evidence for "dark room / black clothes". Off must mean *no term* [4][13].
2. **Explaining a different quantity than the one fused.** Examples: a saliency map on raw full-frame CLIP similarity when the fusion uses a calibrated contrast score on a crop, or probability-space Shapley while the bars are in log space.
3. **Showing raw attention or rollout as "where the robot looks"** [16][20][21]. **Guided Backprop / Guided Grad-CAM** fail sanity checks [57].
4. **Live LIME, KernelSHAP, RISE or IG on pixels.** They take seconds to minutes on CPU (§2), are unstable or foolable [11][26], and depend on the baseline [13].
5. **MM-SHAP or perceptual score as visitor explanations.** They answer "prompt vs image" or dataset-level questions [1][2], and the perceptual score swaps in other visitors' data.
6. **LLM-written explanations at runtime.** They are fluent but unfaithful [43][44], may hallucinate sensitive content, and are hard to safety-test for children.
7. **A diffusion-generated "portrait" as the representation.** It invents details with no evidence (faces, skin tone, gender cues, age), which is unfaithful *and* leaks sensitive attributes. Use a procedural avatar where every element maps 1:1 to an attribute (see 06-generative, Layer A). Any generative image is an "imagination" layer, never the explanation.
8. **Counting correlated frames or audio streams as independent.** Posteriors hit 99% within seconds and "I'm not sure" never appears (§4).
9. **Priors from population statistics.** They encode stereotypes into the robot's first guess. Use neutral priors.
10. **Cross-modal gating** (e.g. camera weight depending on what the mic heard). It creates interactions, and one bar per sensor would then mislead. If unavoidable, compute exact 2ⁿ-coalition Shapley and pairwise interactions (shapiq [93]) and show the interaction explicitly.
11. **Percentages, or fixed uncalibrated "sure" thresholds.** CLIP zero-shot is miscalibrated [46], and children do not reason with percentages [96]. Uncalibrated "87%" or "I'm sure" teaches false precision (§8.7 A3).
12. **Hiding counter-evidence.** One-sided "because" lists break completeness and model confirmation bias (§8.7 A1).
13. **MC dropout on CLIP/SigLIP** (no dropout layers) and **evidential deep learning** [53][54][55].
14. **Treating conformal sets as per-person guarantees.** Coverage is marginal under exchangeability, and booth conditions shift [47][48].
15. **Label-free, LLM-generated concept vocabularies.** They are uncontrolled, may include emotion or sensitive concepts, and concept names may not mean what they say [30][35][36].
16. **Showing the ASR transcript on the public screen.** It may contain names or school details. Show only matched vocabulary words.
17. **Prosody → emotion, or voice → age/gender; hats and hair colour as concepts.** These are legal and ethical red lines or AVOID items [83][103]. Sound stays at "momentary sound level".
18. **Explanations that only build trust.** They raise acceptance regardless of correctness [69], and children over-trust robots [77]. Include the "fool the robot" step, a genuine "not sure" state, and an apology when wrong [98].
19. **Heatmaps over children's faces.** They invite a face-analysis reading and create privacy optics.
20. **A toggle that only hides the UI while processing continues.** It makes the whole explanation a lie. Gate data at the source with a visible indicator [103].
21. **pip-installing `legrad_torch` into the exhibit environment.** It pins `open-clip-torch<=2.23.0` [92] and would downgrade or break open_clip 3.3.0. Vendor the method or use a separate offline environment.
22. **Copying US museum activities that classify facial expressions** (e.g. VHX "Mirror Mirror" [99]). That is emotion inference, which is out of bounds for us [83][103].

---

## 10. Open items / UNVERIFIED

- Latency on the actual exhibition PC; OpenVINO/iGPU/NPU acceleration; behaviour under sustained thermal load. Only the dev-laptop CPU was measured, with synthetic input.
- gScoreCAM and MM-SHAP CPU costs are extrapolations. LeGrad latency on our CPU is assumed to be about one forward+backward (≈0.3 s for B/32), not measured.
- Calibration of the **fused session belief** and of the verbal thresholds (§8.7 A3). This needs recorded or simulated sessions.
- Fusion hyperparameters (τ, frame/word weights, relevance r, likelihood floor) and per-concept calibration-set sizes are design starting points.
- Per-frame calibration (§2.2) used adults from Open Images. Behaviour on children, booth lighting and the robot's camera is untested. The SigLIP2-vs-CLIP calibration comparison is small-n.
- Whether 8–14-year-olds read the balance scale or clue jar as intended. No direct study found; needs a pilot.
- The VHX paper's venue/year (retrieved via NSF PAR, references up to 2024) [99]. [verifier round 2: the PDF's bibliography style line points to https://iated.org/citation_guide, so this is an IATED conference paper (EDULEARN/ICERI/INTED). The exact conference and year are still UNVERIFIED.]
- Licence of the Label-free-CBM repo (no root LICENSE found in round 1; not needed, since we do not use it).

---

## Sources

1. Parcalabescu & Frank, *MM-SHAP*, ACL 2023 — https://aclanthology.org/2023.acl-long.223/ ; PDF https://aclanthology.org/2023.acl-long.223.pdf ; code (MIT) https://github.com/Heidelberg-NLP/MM-SHAP
2. Gat, Schwartz & Schwing, *Perceptual Score*, NeurIPS 2021 — https://arxiv.org/abs/2110.14375 ; PDF https://proceedings.neurips.cc/paper_files/paper/2021/file/b51a15f382ac914391a58850ab343b00-Paper.pdf
3. Hu et al., *SHAPE: contribution and cooperation of individual modalities*, IJCAI 2022 — https://arxiv.org/abs/2205.00302
4. Sundararajan & Najmi, *The Many Shapley Values for Model Explanation*, ICML 2020 — https://proceedings.mlr.press/v119/sundararajan20b.html
5. Kumar et al., *Problems with Shapley-value-based explanations as feature importance measures*, ICML 2020 — https://proceedings.mlr.press/v119/kumar20e.html
6. Janzing, Minorics & Blöbaum, *Feature relevance quantification in XAI: a causal problem*, AISTATS 2020 — https://arxiv.org/abs/1910.13413
7. Lundberg & Lee, *A Unified Approach to Interpreting Model Predictions*, NeurIPS 2017 — https://arxiv.org/abs/1705.07874
8. SHAP docs, KernelExplainer (nsamples = 2·M+2048; background data) — https://shap.readthedocs.io/en/latest/generated/shap.KernelExplainer.html
9. SHAP docs, PartitionExplainer (Owen values; quadratic runtime) — https://shap.readthedocs.io/en/latest/generated/shap.PartitionExplainer.html
10. shap on PyPI (0.52.0, 2026-05-28, MIT) — https://pypi.org/project/shap/
11. Slack et al., *Fooling LIME and SHAP*, AIES 2020 — https://arxiv.org/abs/1911.02508
12. Sundararajan, Taly & Yan, *Axiomatic Attribution for Deep Networks* (IG; 20–300 steps; completeness), ICML 2017 — https://arxiv.org/abs/1703.01365
13. Sturmfels, Lundberg & Lee, *Visualizing the Impact of Feature Attribution Baselines*, Distill 2020 — https://distill.pub/2020/attribution-baselines/
14. Selvaraju et al., *Grad-CAM* — https://arxiv.org/abs/1610.02391
15. Chen et al., *gScoreCAM: What objects is CLIP looking at?*, ACCV 2022 — https://openaccess.thecvf.com/content/ACCV2022/html/Chen_gScoreCAM_What_objects_is_CLIP_looking_at_ACCV_2022_paper.html ; PDF (Table 4) https://openaccess.thecvf.com/content/ACCV2022/papers/Chen_gScoreCAM_What_objects_is_CLIP_looking_at_ACCV_2022_paper.pdf ; code (MIT) https://github.com/anguyen8/gScoreCAM
16. Li et al., *A closer look at the explainability of CLIP* ("CLIP Surgery"), Pattern Recognition 2025, DOI 10.1016/j.patcog.2025.111409 — https://arxiv.org/abs/2304.05653 ; code (no licence file) https://github.com/xmed-lab/CLIP_Surgery
17. Chefer, Gur & Wolf, *Generic Attention-model Explainability for Bi-Modal and Encoder-Decoder Transformers*, ICCV 2021 — https://openaccess.thecvf.com/content/ICCV2021/html/Chefer_Generic_Attention-Model_Explainability_for_Interpreting_Bi-Modal_and_Encoder-Decoder_Transformers_ICCV_2021_paper.html ; code (MIT, CLIP notebook) https://github.com/hila-chefer/Transformer-MM-Explainability
18. Chefer, Gur & Wolf, *Transformer Interpretability Beyond Attention Visualization*, CVPR 2021 — https://arxiv.org/abs/2012.09838
19. Zhao et al., *Grad-ECLIP*, IEEE TPAMI 2026 — https://arxiv.org/abs/2502.18816 ; code (no licence file) https://github.com/Cyang-Zhao/Grad-Eclip
20. Abnar & Zuidema, *Quantifying Attention Flow in Transformers*, ACL 2020 — https://aclanthology.org/2020.acl-main.385/
21. Jain & Wallace, *Attention is not Explanation*, NAACL 2019 — https://aclanthology.org/N19-1357/
22. Wiegreffe & Pinter, *Attention is not not Explanation*, EMNLP 2019 — https://aclanthology.org/D19-1002/
23. Zeiler & Fergus, *Visualizing and Understanding Convolutional Networks* (occlusion) — https://arxiv.org/abs/1311.2901
24. Petsiuk, Das & Saenko, *RISE* (4,000/8,000 masks; deletion/insertion metrics), BMVC 2018 — https://arxiv.org/abs/1806.07421
25. Ribeiro et al., *"Why Should I Trust You?"* (LIME) — https://arxiv.org/abs/1602.04938 ; `num_samples=1000` default https://github.com/marcotcr/lime/blob/master/lime/lime_image.py ; PyPI (0.2.0.1, 2020-06-26) https://pypi.org/project/lime/
26. Alvarez-Melis & Jaakkola, *On the Robustness of Interpretability Methods*, 2018 — https://arxiv.org/abs/1806.08049
27. Wachter, Mittelstadt & Russell, *Counterfactual Explanations without Opening the Black Box*, Harvard JOLT 2018 — https://arxiv.org/abs/1711.00399
28. Miller, *Explanation in AI: Insights from the Social Sciences*, Artificial Intelligence 267 (2019) — https://arxiv.org/abs/1706.07269 ; https://doi.org/10.1016/j.artint.2018.07.007
29. Koh et al., *Concept Bottleneck Models*, ICML 2020 — https://arxiv.org/abs/2007.04612
30. Oikarinen et al., *Label-free Concept Bottleneck Models*, ICLR 2023 — https://arxiv.org/abs/2304.06129 ; code https://github.com/Trustworthy-ML-Lab/Label-free-CBM
31. Yuksekgonul, Wang & Zou, *Post-hoc Concept Bottleneck Models*, ICLR 2023 — https://arxiv.org/abs/2205.15480 ; code (MIT) https://github.com/mertyg/post-hoc-cbm
32. Mahinpei et al., *Promises and Pitfalls of Black-Box Concept Learning Models*, 2021 — https://arxiv.org/abs/2106.13314
33. Margeloiu et al., *Do Concept Bottleneck Models Learn as Intended?*, 2021 — https://arxiv.org/abs/2105.04289
34. Almudévar, Hernández-Lobato & Ortega, *There Was Never a Bottleneck in Concept Bottleneck Models*, ICLR 2026 — https://arxiv.org/abs/2506.04877
35. Roth et al., *Waffling around for Performance* (WaffleCLIP), ICCV 2023 — https://arxiv.org/abs/2306.07282
36. *CHOQOLATE: Organizing Concept Bottleneck Latent Spaces with Choquet Integrals* (preprint, 2026-09-29) — https://arxiv.org/abs/2609.37786
37. Alhamoud et al., *Vision-Language Models Do Not Understand Negation* (NegBench), CVPR 2025 — https://arxiv.org/abs/2501.09425
38. Ramaswamy et al., *Overlooked factors in concept-based explanations* (~32 concepts), CVPR 2023 — https://arxiv.org/abs/2207.09615
39. Kim et al., *TCAV*, ICML 2018 — https://proceedings.mlr.press/v80/kim18d.html
40. Chen et al., *This Looks Like That* (ProtoPNet), NeurIPS 2019 — https://proceedings.neurips.cc/paper/2019/hash/adf7ee2dcf142b0e11888e72b43fcb75-Abstract.html
41. Hoffmann et al., *This Looks Like That… Does it?*, 2021 — https://arxiv.org/abs/2105.02968
42. Nauta et al., *This Looks Like That, Because…*, 2021 — https://arxiv.org/abs/2011.02863
43. Turpin et al., *Language Models Don't Always Say What They Think*, NeurIPS 2023 — https://arxiv.org/abs/2305.04388
44. Jacovi & Goldberg, *Towards Faithfully Interpretable NLP Systems*, ACL 2020 — https://arxiv.org/abs/2004.03685
45. Guo et al., *On Calibration of Modern Neural Networks*, ICML 2017 — https://arxiv.org/abs/1706.04599
46. LeVine et al., *Enabling Calibration in the Zero-Shot Inference of Large Vision-Language Models*, 2023 — https://arxiv.org/abs/2303.12748
47. Angelopoulos & Bates, *A Gentle Introduction to Conformal Prediction and Distribution-Free UQ* (n ≈ 1000; marginal vs conditional coverage; selective classification) — https://arxiv.org/abs/2107.07511
48. Gibbs & Candès, *Adaptive Conformal Inference Under Distribution Shift* — https://arxiv.org/abs/2106.00170
49. Cresswell et al., *Conformal Prediction Sets Improve Human Decision Making*, ICML 2024 — https://proceedings.mlr.press/v235/cresswell24a.html
50. Gal & Ghahramani, *Dropout as a Bayesian Approximation*, ICML 2016 — https://proceedings.mlr.press/v48/gal16.html
51. Lakshminarayanan et al., *Deep Ensembles*, NeurIPS 2017 — https://arxiv.org/abs/1612.01474
52. Sensoy, Kaplan & Kandemir, *Evidential Deep Learning*, NeurIPS 2018 — https://arxiv.org/abs/1806.01768
53. Shen et al., *Are UQ Capabilities of Evidential Deep Learning a Mirage?*, NeurIPS 2024 — https://arxiv.org/abs/2402.06160
54. Jürgens et al., *Is Epistemic Uncertainty Faithfully Represented by Evidential Deep Learning Methods?*, ICML 2024 — https://arxiv.org/abs/2402.09056
55. Bengs, Hüllermeier & Waegeman, *Pitfalls of Epistemic UQ through Loss Minimisation*, NeurIPS 2022 — https://www.semanticscholar.org/paper/4e70f6cb2bed6fb67d15d088df4399aee008a58d
56. Wu & Goodman, *Multimodal Generative Models for Scalable Weakly-Supervised Learning* (MVAE, PoE), NeurIPS 2018 — https://arxiv.org/abs/1802.05335
57. Adebayo et al., *Sanity Checks for Saliency Maps*, NeurIPS 2018 — https://arxiv.org/abs/1810.03292
58. Yona & Greenfeld, *Revisiting Sanity Checks for Saliency Maps*, 2021 — https://arxiv.org/abs/2110.14297
59. Kindermans et al., *The (Un)reliability of Saliency Methods* — https://arxiv.org/abs/1711.00867
60. Ghorbani, Abid & Zou, *Interpretation of Neural Networks is Fragile*, AAAI 2019 — https://arxiv.org/abs/1710.10547
61. Hooker et al., *A Benchmark for Interpretability Methods in Deep Neural Networks* (ROAR), NeurIPS 2019 — https://proceedings.neurips.cc/paper_files/paper/2019/file/fe4b8556000d0f0cae99daa5c5c5a410-Paper.pdf
62. Rong et al., *A Consistent and Efficient Evaluation Strategy for Attribution Methods* (ROAD), ICML 2022 — https://proceedings.mlr.press/v162/rong22a.html
63. Jain et al., *Missingness Bias in Model Debugging*, ICLR 2022 — https://arxiv.org/abs/2204.08945
64. Hedström et al., *Quantus*, JMLR — https://arxiv.org/abs/2202.06861 ; licence (LGPL-3.0) https://github.com/understandable-machine-intelligence-lab/Quantus
65. pytorch-grad-cam (MIT; ViT/CLIP; ROAD metrics) — https://github.com/jacobgil/pytorch-grad-cam ; PyPI grad-cam 1.5.7 (2026-08-21) https://pypi.org/project/grad-cam/
66. Captum (BSD-3) — https://github.com/pytorch/captum ; PyPI 0.9.0 (2026-04-17) https://pypi.org/project/captum/
67. Hase & Bansal, *Evaluating Explainable AI: Which Algorithmic Explanations Help Users Predict Model Behavior?*, ACL 2020 — https://arxiv.org/abs/2005.01831
68. Alqaraawi et al., *Evaluating Saliency Map Explanations for CNNs: A User Study*, IUI 2020 — https://arxiv.org/abs/2002.00772
69. Bansal et al., *Does the Whole Exceed its Parts?*, CHI 2021 — https://arxiv.org/abs/2006.14779
70. Long & Magerko, *What is AI Literacy? Competencies and Design Considerations*, CHI 2020 — https://dl.acm.org/doi/10.1145/3313831.3376727
71. Long, Blunt & Magerko, *Co-Designing AI Literacy Exhibits for Informal Learning Spaces*, PACM HCI (CSCW2) 2021 — https://www.durilong.com/s/CSCW-2021-Co-Designing-AI-Literacy-Exhibits-for-Informal-Learning-Spaces-Camera-Ready.pdf
72. AI4K12, Five Big Ideas in AI — https://ai4k12.org/
73. Druga & Williams, *"Hey Google is it OK if I eat you?"*, IDC 2017 — https://www.media.mit.edu/publications/hey-google-is-it-ok-if-i-eat-you-initial-explorations-in-child-agent-interaction/
74. Druga & Ko, *How do children's perceptions of machine intelligence change when training and coding smart programs?*, IDC 2021 — https://dl.acm.org/doi/pdf/10.1145/3459990.3460712
75. Melsión et al., *Using Explainability to Help Children Understand Gender Bias in AI*, IDC 2021 — https://dl.acm.org/doi/fullHtml/10.1145/3459990.3460719
76. *Breakable Machine: K–12 game for AI literacy through spoofing and XAI*, 2025 — https://arxiv.org/abs/2508.14201
77. *Does your robot know? … responsible robots* (children over-trust; robot adapts), IR4Children@SIGIR 2021 — https://arxiv.org/abs/2106.07931
78. Kay et al., *When (ish) is My Bus?* (quantile dotplots), CHI 2016 — https://users.eecs.northwestern.edu/~jhullman/busUncertaintyVis.pdf
79. Hullman, Resnick & Adar, *Hypothetical Outcome Plots Outperform Error Bars and Violin Plots*, PLOS ONE 2015 — https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0142444
80. Padilla, Kay & Hullman, *Uncertainty Visualization*, 2022 — http://space.ucmerced.edu/Downloads/publications/Uncertainty_Visualization_Padilla_Kay_Hullman_2022.pdf
81. MacEachren et al., *Visual Semiotics & Uncertainty Visualization: An Empirical Study*, IEEE TVCG 2012 — https://pubmed.ncbi.nlm.nih.gov/26357158/
82. Galesic, Garcia-Retamero & Gigerenzer, *Using icon arrays to communicate medical risks: overcoming low numeracy*, Health Psychology 2009 — https://pure.mpg.de/view/item_2099767
83. EU AI Act, Regulation (EU) 2024/1689 — https://eur-lex.europa.eu/eli/reg/2024/1689/oj ; Recital 18 https://artificialintelligenceact.eu/recital/18/ ; Article 5 https://artificialintelligenceact.eu/article/5/
84. GDPR Art. 4(14) "biometric data" — https://gdpr-info.eu/art-4-gdpr/ ; https://eur-lex.europa.eu/eli/reg/2016/679/oj
85. openSMILE licence (audEERING research licence) — https://github.com/audeering/opensmile/blob/master/LICENSE
86. MAPIE https://pypi.org/project/mapie/ (1.5.0, 2026-08-05, BSD-3); crepes https://pypi.org/project/crepes/ (0.9.1, 2026-06-12); TorchCP https://pypi.org/project/torchcp/ (1.2.1, 2025-10-14)
87. Liang et al., *Quantifying & Modeling Multimodal Interactions: An Information Decomposition Framework*, NeurIPS 2023 — https://arxiv.org/abs/2302.12247
88. faster-whisper `transcribe.py` (Segment.avg_logprob, no_speech_prob; Word.probability) — https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/transcribe.py
89. open_clip (MIT) — https://github.com/mlfoundations/open_clip
90. Local benchmark scripts (run 2026-10-01 on the dev laptop): `xai_bench.py`, `xai_bench2.py`, `verify_xai.py` in the session scratchpad. Results in §2.1.
91. Bousselham, Boggust, Chaybouti, Strobelt & Kuehne, *LeGrad: An Explainability Method for Vision Transformers via Feature Formation Sensitivity*, ICCV 2025 — https://openaccess.thecvf.com/content/ICCV2025/html/Bousselham_LeGrad_An_Explainability_Method_for_Vision_Transformers_via_Feature_Formation_ICCV_2025_paper.html ; https://arxiv.org/abs/2404.03214 ; code (MIT) https://github.com/WalBouss/LeGrad
92. `legrad_torch` on PyPI (1.1, uploaded 2024-10-14; requires `open-clip-torch<=2.23.0`; licence field empty), accessed 2026-10-02 — https://pypi.org/pypi/legrad_torch/json
93. Muschalik et al., *shapiq: Shapley Interactions for Machine Learning*, NeurIPS 2024 Datasets & Benchmarks — https://arxiv.org/abs/2410.01649 ; PyPI 1.7.0 (2026-08-27, MIT, Python ≥ 3.12), accessed 2026-10-02 — https://pypi.org/project/shapiq/
94. Hasic, Wang, Garcia-Peraza-Herrera, Watson & Krivic, *Which Modality Decides? Counterfactual Modality Attribution for Multimodal LLMs*, arXiv 2608.00076 (2026-07-29, rev. 2026-08-04; preprint) — https://arxiv.org/abs/2608.00076
95. Zhou, Van Brummelen & Lin, *Designing AI Learning Experiences for K-12: Emerging Works, Future Opportunities and a Design Framework*, arXiv 2020 (Figs 1–2 reproduce Long & Magerko's 17 competencies and 15 design considerations) — https://arxiv.org/abs/2009.10228
96. Zhu & Gigerenzer, *Children can solve Bayesian problems: the role of representation in mental computation*, Cognition 98(3), 287–308 (2006) — https://doi.org/10.1016/j.cognition.2004.12.003 ; author copy https://pure.mpg.de/rest/items/item_2100734_1/component/file_2100733/content
97. Pighin, Girotto & Tentori, *Children's quantitative Bayesian inferences from natural frequencies and number of chances*, Cognition 2017 — https://pubmed.ncbi.nlm.nih.gov/28692831/
98. Flanagan, Georgiou, Scassellati & Kushnir, *School-age children are more skeptical of inaccurate robots than adults*, Cognition 249 (2024) 105814 — https://doi.org/10.1016/j.cognition.2024.105814 ; abstract https://pubmed.ncbi.nlm.nih.gov/38763071/
99. Greenwald, Cavero, Grindstaff, Krakowski, Hurt & Wang, *Building Blocks for Understanding Artificial Intelligence: Designing Interactive AI Learning Experiences for Young Children and Their Families in a Museum Setting* (VHX; NSF DRL 2116109) — https://par.nsf.gov/servlets/purl/10528574 ; exhibit https://lawrencehallofscience.org/news/virtually-human-explores-what-it-means-for-ai-to-act-like-a-human/
100. AI Act Article 50 (transparency obligations) — https://artificialintelligenceact.eu/article/50/
101. Digital Omnibus on AI, Regulation (EU) 2026/1744 (OJ 24 Jul 2026; in force 27 Jul 2026) — https://www.nicfab.eu/en/posts/digital-omnibus-ai-official-journal/ ; https://lawandtechnology.eu/en/digital-omnibus-on-ai-official-journal-regulation-2026-1744/
102. Team prototype (local, read 2026-10-02): `prototype/robotsees/fusion.py`, `xai.py`, `config.py`; `prototype/tests/test_fusion.py` (7 passed); `prototype/experiments/calibrate_vision.py` and `results/vision_calibration.json`, `results/platt_all_backbones.json`
103. Project ethics/law track: `research/09-ethics-law.md` (§4.1 AI Act timeline; §4.5 Art. 50; §8 attribute register; §9 privacy-by-design controls)

---

## Verification log (round 1, 2026-10-01)

*Independent re-check by an adversarial verifier using fresh fetches of primary sources and a local re-run on the dev laptop. Verdicts: confirmed / corrected / refuted / unverifiable. All corrections are folded into the text above (revision 2).*

| # | Claim | Verdict | Source / note |
|---|---|---|---|
| 1 | Local open_clip ViT-B/32 (laion2b_s34b_b79k) has 0 `nn.Dropout` modules and MHA dropout 0.0 | **confirmed** | Verifier re-ran in project `.venv` (torch 2.14.1+cpu, open_clip 3.3.0) |
| 2 | Exact 4-player Shapley in log-odds returns (1.2, 0.8, −0.3, 0.1); in probability space (0.281, 0.182, −0.063, 0.022); ≈75 µs per attribute | **confirmed** | Verifier re-run: identical values, 59 µs per attribute |
| 3 | CLIP B/32 forward 128 ms | **corrected** (context) | Under 100% background CPU load: 1,669 ms median (12 threads); 417 ms median, best 142 ms (4 threads) |
| 4 | shap 0.52.0, MIT, 2026-05-28 | **confirmed** | https://pypi.org/project/shap/ |
| 5 | captum 0.9.0, BSD-3, 2026-04-17 | **confirmed** | https://pypi.org/project/captum/ |
| 6 | grad-cam 1.5.7, MIT, 2026-08-21 | **confirmed** | https://pypi.org/pypi/grad-cam/json |
| 7 | MAPIE 1.5.0 BSD-3 2026-08-05; crepes 0.9.1 2026-06-12; TorchCP 1.2.1 2025-10-14; lime 0.2.0.1 2020-06-26, `num_samples=1000` | **confirmed** | PyPI JSON; https://github.com/marcotcr/lime/blob/master/lime/lime_image.py |
| 8 | KernelSHAP default nsamples = 2M+2048 | **confirmed** | https://shap.readthedocs.io/en/latest/generated/shap.KernelExplainer.html |
| 9 | MM-SHAP: abs-value Shapley; 2p+1 evals, p ≈ 40; ≈3 s/pair on Titan X; [MASK]/zeroed patches; code MIT | **confirmed** (2p+1 is a Monte Carlo sub-sample) | https://arxiv.org/pdf/2212.08158 ; https://github.com/Heidelberg-NLP/MM-SHAP |
| 10 | Perceptual score: 5 permutations per sample | **confirmed** | https://arxiv.org/pdf/2110.14375 |
| 11 | gScoreCAM: top-300 of 3,072 channels, 8–10× faster | **corrected** | 3,072 = RN50x16 ResNet; on ViT-B/32 only on par with HilaCAM (Table 4) |
| 12 | Grad-ECLIP in IEEE TPAMI 2026 | **confirmed** | https://arxiv.org/abs/2502.18816 |
| 13 | Grad-ECLIP / CLIP Surgery licences | **corrected** | No LICENSE file and no licence mention → all rights reserved. Chefer repo MIT |
| 14 | CLIP Surgery findings; Pattern Recognition | **confirmed** (2025) | https://doi.org/10.1016/j.patcog.2025.111409 |
| 15 | Adebayo: Guided BP / Guided Grad-CAM fail; gradients and Grad-CAM pass | **confirmed** | https://arxiv.org/pdf/1810.03292 |
| 16 | Turpin et al.: up to 36% drop, 13 BBH tasks | **confirmed** | https://arxiv.org/abs/2305.04388 |
| 17 | NegBench: about chance on negation | **confirmed** | https://arxiv.org/abs/2501.09425 |
| 18 | Ramaswamy: ~32 concepts; probe dataset matters | **confirmed** | https://arxiv.org/abs/2207.09615 |
| 19 | CHOQOLATE: CLIP concept scores entangled | **confirmed** (preprint 2026-09-29) | https://arxiv.org/abs/2609.37786 |
| 20 | LeVine: CLIP zero-shot miscalibrated; one temperature per model generalises | **confirmed** | https://arxiv.org/abs/2303.12748 |
| 21 | n = 1000 → coverage typically 0.88–0.92 at α = 0.1 | **confirmed** | https://arxiv.org/abs/2107.07511 |
| 22 | Cresswell RCT: conformal sets improve human accuracy | **confirmed** | https://proceedings.mlr.press/v235/cresswell24a.html |
| 23 | Shen et al.: EDL UQ a "mirage" | **confirmed** | https://arxiv.org/abs/2402.06160 |
| 24 | Melsión: Grad-CAM, N = 78, ages 10–14 | **confirmed** | DOI 10.1145/3459990.3460719 |
| 25 | Druga & Ko: N = 52, ages 7–12, more sceptical | **confirmed** | DOI 10.1145/3459990.3460712 |
| 26 | Bansal CHI 2021 | **confirmed** | https://arxiv.org/abs/2006.14779 |
| 27 | Hase & Bansal: ratings not predictive | **confirmed** | https://arxiv.org/abs/2005.01831 |
| 28 | Kay: quantile dotplots ≈1.15× lower variance | **confirmed** | https://users.eecs.northwestern.edu/~jhullman/busUncertaintyVis.pdf |
| 29 | Art. 5(1)(f) since 2 Feb 2025; Recital 18 | **confirmed** | https://artificialintelligenceact.eu/article/5/ ; https://artificialintelligenceact.eu/recital/18/ |
| 30 | Art. 5(1)(g) as basis for "never infer age, sex/gender" | **corrected** | (g) lists race, political opinions, trade-union membership, religious/philosophical beliefs, sex life, sexual orientation, not age or gender |
| 31 | openSMILE licence allows "public demonstrations" (non-commercial) | **confirmed** | https://github.com/audeering/opensmile/blob/master/LICENSE |
| 32 | open_clip and faster-whisper licences | **confirmed: MIT** | Repo LICENSE files |
| 33 | AI4K12 Big Ideas 1–2 | **confirmed** (titles) | https://ai4k12.org/ |
| 34 | Long & Magerko: 17 competencies, 15 design considerations | round 1: unverifiable → **revision 2: confirmed** | Full lists in Zhou, Van Brummelen & Lin 2020, Figs 1–2 [95] |

**Revision-2 checks (2026-10-02):**
- LeGrad venue ICCV 2025 and repo MIT [91]. `legrad_torch` 1.1 pins `open-clip-torch<=2.23.0` and has an empty licence field [92].
- shapiq 1.7.0, MIT, 2026-08-27 [93]. CMA preprint dates [94].
- Zhu & Gigerenzer figures (0% with probabilities; 19/39/53% with natural frequencies), from the author PDF [96]. Pighin et al. abstract via PubMed E-utilities [97]. Flanagan et al. N = 168 + 168, from the abstract [98].
- VHX findings from the full text via NSF PAR [99].
- Regulation (EU) 2026/1744 dates [101].
- Prototype tests re-run (7 passed). The §8.7 A1/A2/A4 numbers were reproduced with a local script against `robotsees`.

---

## Verification log (round 2, 2026-10-02)

*Second independent adversarial pass on revision 2. Each claim below was re-checked with fresh fetches of primary sources and local re-runs. Inline fixes are marked "[corrected by verifier: ...]".*

| # | Claim | Verdict | Source / note |
|---|---|---|---|
| R2-1 | `legrad_torch` 1.1 (uploaded 2024-10-14) requires `open-clip-torch<=2.23.0`; licence field empty | **confirmed** | https://pypi.org/pypi/legrad_torch/json (only 1.0 of 2024-04-05 and 1.1 exist; requires_python >=3.7) |
| R2-2 | LeGrad is ICCV 2025; repo is MIT; 48.4 p-mIoU on OpenImagesV7 with OpenCLIP ViT-B/16 | **confirmed** | https://api.github.com/repos/WalBouss/LeGrad/license (MIT); repo tagline "[ICCV25]"; arXiv v2 Table: 48.38 (B/16), 47.69 (L/14), 46.51 (H/14), https://arxiv.org/html/2404.03214v2. Paper Table 3 also reports 96 fps on GPU for B/16, vs 108 for GradCAM, so it is about as cheap as Grad-CAM |
| R2-3 | shapiq 1.7.0, MIT, 2026-08-27, Python ≥ 3.12 | **confirmed** | https://pypi.org/pypi/shapiq/json |
| R2-4 | CMA, arXiv 2608.00076, v1 2026-07-29, v2 2026-08-04; uses coupled diffusion priors and Shapley over modalities | **confirmed** | https://arxiv.org/abs/2608.00076 |
| R2-5 | Flanagan et al. 2024: 168 children aged 4–7 + 168 adults; older children were more sceptical after errors; a robot's apology prolonged trust | **confirmed** | Europe PMC abstract, DOI 10.1016/j.cognition.2024.105814, Cognition 249 |
| R2-6 | Zhu & Gigerenzer 2006: 0% with probabilities; 19/39/53% with natural frequencies | **confirmed**, with a wording fix | Europe PMC abstract, DOI 10.1016/j.cognition.2004.12.003. "Sixth graders matched adults" refers to sixth graders *with natural frequencies* vs adults *with probabilities* (fixed inline) |
| R2-7 | Pighin et al. 2017 replication: much lower success; accuracy depended on question type, not format | **confirmed** | Europe PMC abstract (PMID 28692831): "only a tiny minority" of Italian children were correct |
| R2-8 | Long & Magerko numbering: competencies #5, #7, #13, #14, #15, #16; design considerations #1, #2, #4, #5, #10, #13, #15 | **confirmed** | Text of Figs 1–2 in https://arxiv.org/pdf/2009.10228 (extracted locally with pypdf) |
| R2-9 | VHX: ages 7–12, Lawrence Hall of Science, NSF DRL 2116109; collaborative parent prompts; "trick the AI" experimentation; glasses / no glasses re-purposing; head-position shortcut | **confirmed**, with a nuance fix | Full text https://par.nsf.gov/servlets/purl/10528574. Shortcut discovery was often facilitated and sometimes caused unnoticed frustration (fixed inline). The venue is an IATED conference |
| R2-10 | AI Act Art. 5(1)(g) list (race, political opinions, trade-union membership, religious/philosophical beliefs, sex life, sexual orientation); age and gender not listed | **confirmed** | https://artificialintelligenceact.eu/article/5/ |
| R2-11 | Art. 50 applies from 2 Aug 2026 (so it binds SiW, 17–19 Mar 2027); 50(1) disclosure; 50(3) notice for biometric categorisation | **confirmed** | https://artificialintelligenceact.eu/article/50/ ; EC FAQ: disclosure "from the start of the first interaction"; the "obvious" exception is interpreted restrictively, https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act |
| R2-12 | Reg. (EU) 2026/1744 published in the OJ on 24 Jul 2026, in force 27 Jul 2026; Annex III deferred to 2 Dec 2027 | **confirmed** | https://euaiactchecklist.com/eu-ai-act-digital-omnibus-2026-1744.html ; https://www.licentium.io/post/eu-ai-digital-omnibus-regulation-2026-1744-enters-into-force-july-2026 (secondary sources; EUR-Lex not fetched) |
| R2-13 | "The Omnibus did not change Art. 5 or the rest of Art. 50" | **corrected** | It inserted Art. 5(1)(ba) and (bb) (NCII and CSAM, applying from 2 Dec 2026). It gave a 50(2) marking grace period, until 2 Dec 2026, to generative systems already on the market. It also rewrote Art. 4. https://artificialintelligenceact.eu/article/5/ ; https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ |
| R2-14 | Grad-ECLIP and CLIP Surgery repos have no licence | **confirmed** | GitHub API `license: null` for both: https://api.github.com/repos/Cyang-Zhao/Grad-Eclip (pushed 2026-08-18) and https://api.github.com/repos/xmed-lab/CLIP_Surgery |
| R2-15 | MAPIE 1.5.0, BSD-3, 2026-08-05; crepes 0.9.1, BSD-3, 2026-06-12 | **confirmed** | https://pypi.org/pypi/mapie/json ; https://pypi.org/pypi/crepes/json |
| R2-16 | TorchCP licence "—" | **corrected** | LGPL (fixed inline), https://pypi.org/pypi/torchcp/json |
| R2-17 | faster-whisper 1.2.1 (2025-10-31, MIT); open_clip 3.3.0 (MIT); shap 0.52.0 (2026-05-28); grad-cam 1.5.7 (2026-08-21, MIT) | **confirmed** | PyPI JSON for each package. These are still the latest versions on 2026-10-02 |
| R2-18 | About 1,000 calibration points gives coverage typically 0.88–0.92 at α = 0.1 | **confirmed** | Angelopoulos & Bates v6, §3.2: "choosing n = 1000 calibration points leads to coverage that is typically between .88 and .92", https://arxiv.org/abs/2107.07511 |
| R2-19 | Shen et al., NeurIPS 2024: EDL UQ is a "mirage" and is better read as energy-based OOD detection | **confirmed** | https://arxiv.org/abs/2402.06160 |
| R2-20 | Prototype: 7/7 tests pass; per-frame calibration numbers in §2.2; fixed 0.75/0.25 thresholds on rescaled max-probability; `evidence_ranking` keeps only positive push; docstring says "log-odds units" | **confirmed** (local) | `pytest` re-run: 7 passed in 0.59 s (torch 2.14.1+cpu, open_clip 3.3.0). Every §2.2 value matches `experiments/results/vision_calibration.json`. `config.py` L78–89 (τ = 1.5, floor 0.05). `xai.py` L70 filter `push > 1e-4`. `fusion.py` L145, L175 |
| R2-21 | Exact Shapley worked example: (1.2, 0.8, −0.3, 0.1) in log-odds; (0.281, 0.182, −0.063, 0.022) in probability | **confirmed** | Local recomputation gave identical values. Timing was 158 µs per attribute with system Python 3.14, on the same order as 59–75 µs |

## Omissions added by verifier

1. **New Art. 5(1)(ba)/(bb) prohibitions and the Art. 4 rewrite from the Digital Omnibus** (see R2-13). They do not affect this exhibit's design, but any legal summary that says "Art. 5 unchanged" is now wrong. The Art. 4 AI-literacy duty for the team as provider/deployer is now a duty of means ("take measures to support"). The exhibit itself is a good example of such a measure. https://artificialintelligenceact.eu/article/5/
2. **Commission guidance on Art. 50 has been published.** It includes the Guidelines and the Code of Practice on Transparency of AI-generated content, which law-firm summaries date to 20 Jul 2026 (date UNVERIFIED on an EC primary page). The EC FAQ states that the 50(1) disclosure must come "from the start of the first interaction", and that the "obvious" exception is read restrictively against an "average person, reasonably well-informed" standard. So step 1 of the interaction script (§8.2) must disclose explicitly and must not rely on "it's obviously a robot". For an audience of children, wording and accessibility should be age-appropriate. https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act
3. **Art. 5(1)(b)** (exploiting vulnerabilities due to *age*) is the Art. 5 point most relevant to a child audience. It is not mentioned in this report. It is low risk for an explanatory exhibit that does not manipulate behaviour, but the ethics track should cite it explicitly. https://artificialintelligenceact.eu/article/5/
4. **LeGrad runtime evidence.** The paper's Table 3 (GPU) puts LeGrad at 96 fps vs Grad-CAM at 108 fps for ViT-B/16. That supports the report's assumption that LeGrad costs about one forward+backward pass, i.e. about 0.3 s on our CPU. The CPU figure is still unmeasured. https://arxiv.org/html/2404.03214v2
5. **TorchCP is LGPL.** That is acceptable for a non-distributed exhibit, but MAPIE or crepes (BSD-3) are simpler licence-wise.
