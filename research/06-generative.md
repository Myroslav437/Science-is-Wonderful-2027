# 06 — Local generative visualisation ("how the robot sees you")

Research track 06 for the TUAI DC5/DC7 demonstrator for *Science is Wonderful! 2027* (Brussels, 17–19 Mar 2027, see `research/01-call-and-tuai.md`).

Status: researched and measured on **2026-10-01** (round 1), extended on **2026-10-02** (round 2: second measurement round on the dev laptop, step-count mechanics, quality sweep, concurrency with the prototype's perception, FLUX.2-klein on the iGPU, 2026 model releases, tooling corrections, cloud/EU options). Benchmark scripts, raw results (`results.jsonl`, `results2.jsonl`) and contact sheets are in `research/assets-06/`.

Conventions: every factual claim has a URL in brackets or in **Sources**. Anything we could not verify is marked **UNVERIFIED**. Latency figures are labelled **[measured-here]** (we ran it on the dev laptop), **[reported]** (a primary or community source measured it) or **[estimate]** (we scaled from a reported number and say how). Prices carry their access date.

---

## 0. Decision summary (TL;DR)

1. **Two layers.**
   - **Layer A, the "robot's notebook"** (primary, non-negotiable): a deterministic procedural SVG/canvas avatar. Every visual element maps 1:1 to one inferred attribute, shows that attribute's confidence and names the sensor it came from. It renders in <50 ms on any hardware, cannot invent anything and carries all of the XAI. This matches the legal track's design choice ("draw any avatar procedurally", `09-ethics-law.md` §4.5).
   - **Layer B, the "robot's imagination"** (optional): a distilled diffusion model **restyles the Layer A render** (img2img from the coloured Layer A raster, style-only prompt; ControlNet on the NVIDIA laptop). It is labelled "AI-generated picture, may invent details" and the exhibit must work with Layer B switched off.
2. **The generator never sees the camera.** No img2img from webcam frames, no IP-Adapter / InstantID / PhotoMaker (§6). Inputs are only closed-vocabulary tokens and the procedural sketch.
3. **Draw a non-human mascot in the visitor's colours, not a portrait.** Plain text-to-image of "…red striped shirt and yellow hat" drew a *human child* with hair, skin tone and face, and put the colours on the wrong garments (§3.1). Carrying attributes in pixels (Layer A as init image) fixes the colour-binding problem.
4. **Dev laptop (Core Ultra 7 255U, no NVIDIA): run Layer B on the integrated GPU via OpenVINO GenAI, never on the CPU.**
   - Recommended: **LCM-Dreamshaper int8 + TAESD, img2img from Layer A, 3–4 steps × strength 0.6–0.7 → 2.0–2.6 s per stage** on the iGPU [measured-here, §3.1]. CPU: 26–53 s for the same kind of job.
   - **Step mechanics matter:** with LCM the cost is *fixed by `num_inference_steps`* whatever the strength; with SD-Turbo only `int(steps × strength)` steps run (4 × 0.7 = 2 steps, 1.1 s). 1–2 SD-Turbo steps barely restyle the sketch; 3 steps (4 × 0.9, 1.7 s) restyle but re-interpret the subject (hat dropped, robot head turned into a cat) (§3.1, [S60]).
   - SD-Turbo + TAESD text-to-image is 0.58 s on the iGPU, but plain text-to-image is the wrong mode for us (point 3).
   - FLUX.2-klein-4B int4 runs on the iGPU but is far from interactive (see §3.1 round 2, FLUX.2 row).
5. **Exhibition laptop (RTX 4060/4070 Laptop, 8 GB):** same hybrid in diffusers fp16, **SD1.5-LCM + ControlNet lineart/scribble img2img + TAESD, 4 steps → ≈0.4–1.2 s per stage** [estimate, §3.3]. Upgrade options: SDXL-Turbo/Lightning + ControlNet-Union or T2I-Adapter (≈0.6–1.5 s), SANA-Sprint 0.6B (Apache-2.0) or FLUX.2-klein-4B FP8 (Apache-2.0, ≈4 GB transformer) for 1024 px (≈1–5 s, **UNVERIFIED** on 8 GB).
   - If the laptop is bought in 2026–27: an **RTX 5070 Ti Laptop (12 GB GDDR7)** is the cheapest guaranteed-12 GB option; RTX 5070 Laptop exists with 8 *or* 12 GB; 4060/4070 Laptop are both 8 GB [S77]. A 4070 Laptop adds only ≈10–20% over a 4060 Laptop for SD workloads [S42].
6. **Licences OK for a public outreach exhibit:** SD-Turbo / SDXL-Turbo / SD 3.5 (Stability Community Licence: free for non-commercial use; "Powered by Stability AI" attribution is a distribution duty, not only a commercial one [S4]), SDXL-Lightning and Hyper-SD SD1.5/SDXL LoRAs (OpenRAIL++-M), LCM-Dreamshaper (MIT), FLUX.1-schnell, FLUX.2-klein-4B, SANA/SANA-Sprint, Z-Image-Turbo, ERNIE-Image-Turbo, LLaDA-Image-Turbo (all Apache-2.0).
   **Avoid:** FLUX.2-klein-9B (FLUX Non-Commercial), Qwen-Image-2.1 (research licence), Ideogram 4 (non-commercial), Hyper-SD FLUX LoRAs (FLUX.1-dev NC), PCM weights (no licence), anything depending on InsightFace (non-commercial).
7. **Cloud** is cheap (≈USD 0.003–0.014 per image) but adds venue Wi-Fi dependency and a data transfer. If ever used, prefer **BFL's EU endpoint `api.eu.bfl.ai`** (FLUX.2-klein-4B from USD 0.014/image) over US-only services, and send only the closed-vocabulary prompt plus sketch [S78].
8. **Compliance:** Art. 50 AI Act applies from 2 Aug 2026 with **no grace period** for a system put into service in 2027. Show an on-screen AI label and mark any image that leaves the stand machine-readably (the prototype already writes IPTC `trainedAlgorithmicMedia` into XMP [S82][S83]). The new Art. 5(1)(ba)/(bb) bans (NCII/CSAM generation) apply from 2 Dec 2026; non-human subject + closed vocabulary + no camera input keep us far from them.
9. **Prototype action item:** `prototype/robotsees/render/imagination.py` currently runs SD-Turbo text-to-image in PyTorch on the CPU (docstring: ~20–35 s). Switch it to the OpenVINO GenAI iGPU img2img recipe in §11.1 (≈2–2.6 s, attributes carried by the Layer A pixels).

---

## 1. Requirements the generator must satisfy

| Requirement | Implication for the generator |
|---|---|
| 3–5 min interaction with 4–6 visible "evolution" stages | Each update lands within ≤1–3 s of a new inference, or is visibly staged ("the robot is painting…") |
| Visitor toggles sensors (camera/mic) | The image must *lose* attributes too. Missing = rendered as "unknown" (neutral grey), never as a random invention |
| XAI: which sensor led to which inference, with uncertainty | Explanation lives in the deterministic Layer A. Diffusion output cannot faithfully encode confidence |
| Children 8–14; privacy-by-design; no sensitive attributes | No face/identity conditioning, no photoreal humans, closed vocabulary, output safety check |
| Robust over 16 fair hours (17 Mar 4 h, 18–19 Mar 6 h each) | Offline, deterministic fallback, pinned weights (models disappear, §2.3), watchdog |
| Feasibility first; robot budget ~USD 600 | Must run on a mid-range gaming laptop; the dev laptop must at least prototype |

---

## 2. Model landscape (verified 2026-10-01/02)

### 2.1 Fast / small text-to-image models

Params from the HF model card or the HF API `safetensors.total`. "OK for us?" = usable for a public non-commercial outreach exhibit and for later reuse.

| Model (org, date) | Params (denoiser) | Steps | Native res | Licence (verified) | OK for us? | Notes |
|---|---|---|---|---|---|---|
| **SD-Turbo** (Stability) | 0.87B UNet | 1–4 | 512 | Stability AI **Community Licence** (LICENSE.md, 5 Jul 2024) [S2] | Yes. Non-commercial free; commercial free < USD 1M revenue; "Powered by Stability AI" + licence notice whenever distributed or offered (Distribution section) [S4] | Distilled from SD 2.1, which Stability deprecated and removed from HF (15 Nov 2025) [S7]. SD-Turbo still online on 2026-10-02 — **mirror the weights**. ONNX build for AMD Ryzen AI NPUs exists (`sd-turbo-amdnpu`, Feb 2026) [S72] |
| **SDXL-Turbo** (Stability) | 2.57B UNet ("3B" incl. TEs) | 1–4 | 512 | HF tag still `sai-nc-community`, LICENSE.md = Community Licence [S3][S5] | As SD-Turbo | 207 ms on A100 for 512 px, 1 step [S6]. `sdxl-turbo-amdnpu` exists [S72] |
| **SDXL-Lightning** (ByteDance) | ~2.6B UNet | 1/2/4/8 | 1024 | **OpenRAIL++** | Yes (use restrictions) | Full UNet or LoRA; 1-step "experimental" [S9] |
| **LCM / LCM-LoRA** | LoRA 67.5M (SD1.5) | 2–8 | 512/1024 | LoRA OpenRAIL++; **LCM_Dreamshaper_v7 MIT** | Yes | Works with ControlNet [S11]; native in OpenVINO GenAI [S33]; **tested here** |
| **Hyper-SD** (ByteDance) | LoRAs SD1.5/SDXL/SD3/FLUX | 1–16 | — | `LICENSE.md` per variant: SD1.5/SDXL **OpenRAIL++-M**; SD3 Stability Community; FLUX **FLUX.1-dev Non-Commercial** [S10] | SD1.5/SDXL yes; FLUX no | ControlNet-compatible [S10] |
| **PCM** | LoRAs SD1.5/SDXL/SD3 | 1–16 | — | Code Apache-2.0; HF weights **no licence file or tag** [S13] | Unclear — avoid | — |
| **SDXS-512** (IDKiro) | 0.3B | 1 | 512 | OpenRAIL++ | Yes | 0.82 s on i7-12700 CPU, OpenVINO+TAESD [S38] |
| **SANA 0.6B / 1.6B** (NVIDIA/MIT) | 0.59B / 1.65B | ~20 | 512–4K | **Apache-2.0** since 2026-07-31 (HF commit "Relicense model under Apache-2.0") + Gemma terms for the TE [S14] | Yes | Gemma-2-2B TE; DC-AE 32×; "<8 GB VRAM via 4-bit" on laptop GPUs [S74] |
| **SANA-Sprint 0.6B / 1.6B** | 0.6B / 1.6B | 1–4 | 1024 | **Apache-2.0** (+ Gemma) | Yes | **0.10 s H100, 0.31 s RTX 4090** at 1024²; 0.25 s with ControlNet on H100 [S16]. Not in OpenVINO GenAI (request open since May 2025 [S62]); FastSD has an OpenVINO port [S63] |
| **PixArt-Σ** | 0.6B | ~20 | 1024–4K | OpenRAIL++ | Yes | T5-XXL encoder (heavy) [S17] |
| **FLUX.1-schnell** (BFL) | 12B | 1–4 | ~1024 | **Apache-2.0** (gated click-through) | Yes | Too big for 8 GB without 4-bit; Nunchaku INT4 [S20] |
| **FLUX.2 [klein] 4B** (BFL, 15 Jan 2026) | 3.88B | 4 | ≤4 MP | **Apache-2.0** | Yes | Qwen3-4B TE. ~13 GB VRAM BF16; official **FP8** and **NVFP4** repos (Apache-2.0) [S19][S65]. Built-in NSFW/CSAM data filtering [S19]. **FLUX.2-small-decoder** (Apr 2026, Apache-2.0, ~28M vs ~50M params, ~1.4× faster decode, ~1.4× less decode VRAM) [S64]. OpenVINO int4 IR = 4.57 GB on disk [S63] |
| FLUX.2 [klein] 9B / 9B-KV | 9B + 8B TE | 4 | — | **FLUX Non-Commercial** [S19][S65] | **No** | — |
| FLUX 3 (BFL, announced 23 Jul 2026) | — | — | — | Not published | **Not available** | Image/video early access only; open-weight "FLUX 3 Dev" promised for later in 2026 [S66]. "FLUX 3 Action" robot-action models (Sep 2026, licence "other") are unrelated to image generation [S65] |
| **SD 3.5 Medium** | 2.47B | ~40 | ≤1440 | Community Licence | As SD-Turbo | Not distilled → too slow [S21] |
| **SD 3.5 Large Turbo** | 8.15B | 4 | 1024 | Community Licence | As SD-Turbo | T5-XXL; too large for 8 GB without 4-bit [S21] |
| **BK-SDM-Small / Tiny** (Nota) | 0.49B / ~0.33B UNet | 25+ | 512 | CreativeML OpenRAIL-M | Yes | Undistilled steps [S22] |
| **Segmind Tiny-SD / Small-SD** | — | 25+ | 512 | CreativeML OpenRAIL-M | Yes | "up to 80% faster than SD1.5" [S22] |
| **Segmind Vega** | 0.7B | 25 (VegaRT: few) | 1024 | **Apache-2.0** | Yes | [S22] |
| **Kandinsky 5.0 T2I Lite** (Nov 2025) | 6B | 100 NFE | 1K | **MIT** | Yes | 13 s on H100 → too slow [S24] |
| **Z-Image-Turbo** (Alibaba Tongyi, Nov 2025) | 6.15B | 8 NFE | 1024 | **Apache-2.0** | Yes | Fits 16 GB; ≤4 GB via stable-diffusion.cpp GGUF [S37]; ControlNet-Union (Apache-2.0) [S25]. Undistilled **Z-Image** base released 2026-01-23 (Apache-2.0) [S71] |
| **ERNIE-Image-Turbo** (Baidu, Apr 2026) | 8B DiT | 8 | 1024 | **Apache-2.0** [S68] | Yes | "consumer GPUs with 24G VRAM" [S68]; Nunchaku 4-bit supported [S73] |
| **LLaDA-Image-Turbo** (Ant Group inclusionAI, 4 Sep 2026) | 6.54B | 4 (2–4) | 1024 | **Apache-2.0** (HF metadata, 2026-10-02) [S67] | Yes (very new; a secondary article said "undeclared licence" — re-check) | No latency figures published [S67] |
| **Krea 2 Turbo** (Krea, 22 Jun 2026) | 12.8B | 8 | ≤2048 | **Krea 2 Community Licence** (gated, PDF) [S69] | Check terms | Too big for 8 GB without 4-bit; Nunchaku-supported [S73] |
| **Ideogram 4** (Jun 2026) | 9.3B | — | ≤2048 | **Ideogram 4 Non-Commercial** [S70] | **No** for later reuse | Qwen3-VL-8B TE [S70] |
| Qwen-Image / -2512 | 20.4B | 4–8 (Lightning LoRA) | 1328 | Apache-2.0 [S84] | Yes | Far too big for 8 GB unless 4-bit + offload |
| **Qwen-Image-2.1** (14 Sep 2026) | 7.1B | — | — | **`qwen-research`** (HF tag "other") [S26][S84] | **No** | Supported by OpenVINO GenAI, stable-diffusion.cpp and mflux — tooling support does not make it usable [S33][S37][S55] |
| Lumina-Image 2.0 | 2B | ~50 | 1024 | Apache-2.0 | Yes | No distilled version found |
| HiDream-I1-Fast | 17B | few | 1024 | MIT (TE: Llama 3.1 licence) | Yes | Far too big |

### 2.2 What this means for an 8 GB laptop GPU

- **Comfortable (fp16, all in VRAM):** SD-Turbo, SD1.5-LCM (+ControlNet), SDXS, Segmind models; SDXL-Turbo/Lightning (~7 GB weights: cache or offload the two text encoders). Reported: an RTX 4060 Laptop runs SDXL 1024², 20 steps, in 15.8 s at 5.6 GB peak [S76, secondary].
- **Feasible with tricks:**
  - SANA-Sprint 0.6B: small DiT, but the Gemma-2-2B TE is 2.61B params (≈5.2 GB bf16). Precompute embeddings (our prompt is a fixed style prompt) or 8/4-bit the TE [S74].
  - FLUX.2-klein-4B: official FP8 checkpoint (Apache-2.0) [S65]; the TE (Qwen3-4B, ≈8 GB bf16) must be quantised or offloaded, or its output cached for the fixed style prompt. **UNVERIFIED** latency on 8 GB; secondary sources range from "fully fits at FP8" to "60–90 s with Q4 + CPU offload", which shows how much depends on TE handling.
  - Z-Image-Turbo / FLUX.1-schnell: Nunchaku INT4 or GGUF.
- **Not sensible:** SD3.5 Large Turbo, Qwen-Image, HiDream, Kandinsky 5, ERNIE-Image, Krea 2, Ideogram 4, LLaDA-Image.

### 2.3 Availability risk (observed)

- Stability **deprecated SD 2.0/2.1 and removed the HF repos**, citing consolidation and "upcoming compliance requirements for the EU AI Act in 2026" [S7]. `stabilityai/stable-diffusion-2-1` returned HTTP 401 on 2026-10-02; a community mirror exists [S8].
- RunwayML's SD 1.5 repo vanished in 2024; now mirrored at `stable-diffusion-v1-5/stable-diffusion-v1-5` (OpenRAIL-M).
- **Vendor the exact weight files plus SHA-256 hashes.** Never call `from_pretrained()` at the venue.

---

## 3. Latency evidence by hardware

### 3.1 Measured on our dev laptop (Intel Core Ultra 7 255U, 32 GB, Windows 11)

Hardware per Intel ARK [S41]: 2P+8E+2LPE cores, 14 threads, 15 W base / 57 W turbo; iGPU "Intel Graphics" with **4 Xe-cores (8 INT8 TOPS)**; **NPU 12 INT8 TOPS**. OpenVINO / OpenVINO GenAI **2026.4.1**; devices CPU, GPU ("Intel(R) Graphics (iGPU)") and NPU ("Intel(R) AI Boost") detected. 512×512, `Text2ImagePipeline` / `Image2ImagePipeline`, static reshape, compile cache, 1 warm-up run, then mean of 3 (round 1) or 5 (round 2) runs.

Models: `OpenVINO/LCM_Dreamshaper_v7-int8-ov` (MIT; UNet ≈0.86 GB) [S34]; `rupeshs/sd-turbo-openvino` (FP32 IR; tokenizer converted with `openvino-tokenizers`, TE input patched to i64) [S34]; "+TAESD" = VAE folders replaced by `rupeshs/taesd-ov` (MIT) [S59].

**Load caveat:** both rounds ran while *other project jobs* shared the laptop (round 1: YOLO/CLIP exports and downloads; round 2: the prototype's `experiments/build_sessions.py` and a CLAP benchmark). **CPU figures are therefore upper bounds and noisy** (SD-Turbo 1-step CPU: 6.9 s in round 1, 11.0 s in round 2). **iGPU figures were stable** across rounds (LCM 4-step t2i: 2.50 s vs 2.53 s).

**Round 1 (2026-10-01)**

| # | Pipeline (512×512) | TE / UNet / VAE | Steps | First compile → cached (s) | **Mean (s)** | Min (s) |
|---|---|---|---|---|---|---|
| 1 | LCM int8, full VAE | iGPU | 4 | 43.9 (uncached) | **3.25** | 3.13 |
| 2 | LCM int8, full VAE | iGPU | 2 | 7.7 | **2.13** | 2.12 |
| 3 | LCM int8 **+TAESD** | iGPU | 4 | 14.9 | **2.50** | 2.49 |
| 4 | LCM int8 **+TAESD** | iGPU | 2 | 9.1 | **1.24** | 1.24 |
| 5 | LCM int8, full VAE | CPU / **NPU** / iGPU | 4 | **154** (NPU compile) | **3.00** | 2.92 |
| 6 | LCM int8, full VAE | NPU/NPU/NPU | 4 | 95 | 4.31 | 3.15 |
| 7 | LCM int8 img2img 0.5, full VAE | iGPU | 4 | 21.4 | 3.72 | 3.59 |
| 8 | LCM int8, full VAE | CPU | 4 | 3.6 | 31.4 | 29.8 |
| 9 | LCM int8, full VAE | CPU | 2 | 4.8 / 11.3 | 27.9 / 21.2 | 23.4 / 19.8 |
| 10 | LCM int8 +TAESD | CPU | 2 | 8.6 | 12.3 | 10.5 |
| 11 | LCM int8 img2img 0.5, full VAE | CPU | 4 | 11.3 | 46.8 | 43.5 |
| 12 | **SD-Turbo +TAESD** | iGPU | 1 | 32.3 | **0.81** | 0.75 |
| 13 | SD-Turbo, full VAE | iGPU | 1 | 36.2 | 1.49 | 1.47 |
| 14 | SD-Turbo +TAESD img2img 2×0.5 | iGPU | 1 executed | 12.8 | 0.62 | 0.61 |
| 15 | SD-Turbo +TAESD | CPU | 1 | 17.3 | 6.9 | 6.1 |
| 16 | SD-Turbo, UNet on NPU | CPU/NPU/iGPU | 1 | — | **failed**: "UNet input shape is dynamic" — the 2023-era community IR did not reshape; re-export with current optimum-intel | — |

**Round 2 (2026-10-02): the hybrid recipe (img2img from a procedural Layer A render, style-only prompt) with executed steps counted via the GenAI step callback** (`research/assets-06/bench2.py`).

| # | Pipeline (512×512, +TAESD) | Device | steps × strength | **Steps executed** | **Mean (s)** | Min–max (s) |
|---|---|---|---|---|---|---|
| 17 | SD-Turbo t2i | iGPU | 1 | 1 | **0.58** | 0.57–0.61 |
| 18 | SD-Turbo hybrid | iGPU | 2 × 0.5 | 1 | 0.65 | 0.63–0.69 |
| 19 | SD-Turbo hybrid | iGPU | 4 × 0.5 | 2 | 1.15 | 1.10–1.17 |
| 20 | SD-Turbo hybrid | iGPU | 4 × 0.7 | 2 | 1.13 | 1.09–1.16 |
| 21 | SD-Turbo hybrid | iGPU | 4 × 0.9 | 3 | **1.67** | 1.62–1.76 |
| 22 | LCM t2i | iGPU | 4 | 4 | 2.53 | 2.51–2.59 |
| 23 | LCM hybrid | iGPU | 4 × 0.5 | **4** | 2.69 | 2.60–2.88 |
| 24 | LCM hybrid | iGPU | 4 × 0.6 | **4** | 2.64 | 2.54–2.77 |
| 25 | **LCM hybrid** | iGPU | **4 × 0.7** | **4** | **2.61** | 2.54–2.64 |
| 26 | **LCM hybrid** | iGPU | **3 × 0.7** | 3 | **1.99** | 1.94–2.10 |
| 27 | LCM hybrid | iGPU | 6 × 0.7 | 6 | 3.74 | 3.67–3.89 |
| 28 | SD-Turbo t2i | CPU | 1 | 1 | 11.0 | 9.0–12.7 |
| 29 | SD-Turbo hybrid | CPU | 4 × 0.7 | 2 | 25.6 | 23.6–27.2 |
| 30 | LCM t2i | CPU | 4 | 4 | 32.8 | 28.0–40.5 |
| 31 | LCM hybrid | CPU | 4 × 0.7 | 4 | 40.9 | 35.0–46.3 |
| 32 | LCM int8 t2i, full VAE | CPU | 4 | 4 | 52.8 | 49.3–55.2 |
[[FLUX2_ROWS]]

What the numbers say:

- **iGPU vs CPU: ≈10–20×.** The 4-Xe-core iGPU is the only usable accelerator for Layer B on this laptop. The NPU matches the iGPU for the UNet (rows 1 vs 5), so one accelerator can run perception while the other generates.
- **Per-step cost on the iGPU ≈0.5–0.57 s** (SD-Turbo FP32 IR and LCM int8 alike; int8 weights do not speed up the iGPU much). Fixed overhead with TAESD (TE + TAESD encode/decode) ≈0.1 s. **The full VAE decode costs ≈1 s on the iGPU and ≈9 s on the CPU** (rows 1–4, 9–10) — always use TAESD.
- **Step mechanics (important for design):**
  - **LCM img2img always runs `num_inference_steps`** (rows 23–25: 4 steps at strength 0.5, 0.6 and 0.7). The LCM scheduler shortens the *origin schedule* to `original_steps × strength` and then still picks `num_inference_steps` timesteps from it (diffusers `LCMScheduler.set_timesteps`, same behaviour in OpenVINO GenAI) [S60]. Cost depends on steps only; strength controls how far the image may drift.
  - **SD-Turbo (Euler-ancestral) img2img runs `int(steps × strength)` steps** (rows 18–20), so "4 × 0.7" is really 2 steps. Distilled pipelines need `steps × strength ≥ 1` [S57].
- **NPU compile is slow** (95–154 s first time). Keep `CACHE_DIR` and warm the cache before opening.
- **Usable on the dev laptop:** LCM hybrid **3–4 steps ≈2.0–2.6 s per stage**. SD-Turbo hybrid ≈0.65–1.15 s, but see the quality finding below.

**Quality findings (contact sheets `research/assets-06/hybrid_sheet.png`, `hybrid_sheet_r2.png`, `t2i_sheet.png`):**

- **Text-to-image is the wrong mode.** Prompt "…red striped shirt and a yellow hat": LCM drew a *red* hat and a red/yellow shirt; SD-Turbo drew a correct shirt but a blue-and-yellow hat. Both drew a **human child** with hair, skin tone and facial features that no sensor inferred.
- **Hybrid img2img from Layer A** (grey robot head, blue- or green-striped body, yellow hat, waving arm, orange cat; style-only prompt "children's crayon drawing of a cute friendly robot mascot and a small cat…"):
  - **SD-Turbo with 1–2 executed steps** (rows 18–20): output is a cleaned-up copy of the sketch; the cat lost its ears. Not a restyle.
  - **SD-Turbo 4 × 0.9 (3 executed steps, 1.67 s):** a lively crayon restyle that keeps the blue stripes and the orange cat, but **turns the grey robot head into an orange cat-like head and drops the yellow hat**, and adds a second waving arm — it re-interprets the subject.
  - **LCM 4 × 0.5–0.6:** light restyle that keeps everything, but at 0.6 the model **gave the mascot a frowning mouth** that Layer A never drew. Generated faces can show expressions the system never inferred (see §12).
  - **LCM 3–4 × 0.7 (2.0–2.6 s):** a genuinely restyled, appealing robot mascot that **keeps stripe colour (blue vs green swapped correctly), stripes, cat companion and raised arm**. Drift: the yellow hat becomes an orange cap/hair-like shape and a second arm is raised. **Best trade-off on the iGPU: 3 × 0.7 at ≈2.0 s.**
  - **LCM 6 × 0.7 or strength ≥0.85:** invents more (animal-ear hat, extra grey cat in round 1, head colour changes).
  - Fixes for the drift: draw a fixed, neutral (or no) face and a high-contrast hat in Layer A, use ControlNet line art on NVIDIA, or inpaint only the changed region (§4).
- **img2img cannot change an attribute through the prompt at low strength** ("red"→"blue" at 0.5 kept red stripes; only the collar turned blue). Attribute changes must come through the init/control image or masked inpainting.
- **Teaching opportunity:** strength is a ready-made **"imagination slider"**: low = "draw only what I sensed", high = "the AI makes things up" — and the drift (hat colour, extra arm) is itself a visible, explainable hallucination.

A parallel track ran SD-Turbo in **PyTorch fp32 on the CPU** (diffusers 0.40, torch 2.14 CPU, `scratch/bench_sd.json`): 22.2 s (1 step), 31.8 s (2 steps), 36.2 s (img2img 2 × 0.5) for 512² [measured-here, contended]. **Use OpenVINO, not PyTorch, on Intel.**

**Concurrency with perception (round 2).** The prototype's real `VisionPerception.analyse_frame` (MediaPipe face + pose, CLIP ViT-B/32 via open_clip on the CPU) was run back-to-back on stored 360×640 frames for 40 s, alone and while the iGPU generated Layer B images in a loop (`concurrency.py`):

| Condition (2026-10-02, other project jobs also running) | Perception, frames/s (mean ms/frame) | Layer B on iGPU, s/image |
|---|---|---|
| Perception alone, 4 runs between 02:19 and 02:38 | **0.93 / 1.53 / 1.72 / 2.93 fps** (1075 / 652 / 580 / 341 ms) — varies with the other jobs | — |
| Perception + continuous **LCM hybrid 3 × 0.7** | **0.49 fps** (2047 ms, p95 4.5 s) | 1.97 (vs 1.99 alone, n=20/22) |
| Perception + continuous **SD-Turbo hybrid 4 × 0.9** | **0.97 fps** (1036 ms, p95 3.4 s) | 1.68 (vs 1.70 alone, n=24/26) |

- **Generation on the iGPU is not slowed by CPU perception** (≤1% difference).
- **CPU perception drops to roughly a third to a half** of its alone-rate while the iGPU generates *continuously*. The 15 W package shares power and memory bandwidth between CPU and iGPU, and the OpenVINO GPU plugin also uses host threads. The alone-baseline itself swung 3× because of other jobs, so treat the factor as indicative.
- **Design consequence:** generate only once per stage (≈2 s out of every 30–60 s), pause or slow perception during the "painting" animation (natural in the UI anyway), and consider moving perception models to the NPU via OpenVINO. On an exhibition laptop with a discrete NVIDIA GPU and an H-class CPU this contention should be much smaller (**UNVERIFIED**).

### 3.2 Reported numbers (other hardware)

| Hardware | Model / setting | Latency / throughput | Source |
|---|---|---|---|
| Core i7-12700 (desktop CPU) | SDXS-512 1 step, OpenVINO + TAESD | **0.82 s** | [S38] |
| Core i7-12700 | SD-Turbo 1 step 512: PyTorch / OV / OV+TAESD | 7.8 / 5.0 / **1.7 s** | [S38] |
| Core i7-12700 | SDXL-Turbo 1 step 512: PyTorch / OV / OV+TAESDXL | 10 / 5.6 / **2.5 s** | [S38] |
| Core i7-12700 | Hyper-SD 1 step 768 (OV+TAESDXL) | 6.3 s | [S38] |
| Core i7-12700 | SDXL-Lightning 2 steps 768 (OV+TAESDXL) | 10 s | [S38] |
| Core i7-12700 | FLUX.1-schnell OpenVINO int4 | 4 min 30 s | [S38] |
| Intel i9-10980XE CPU | SDXL + LCM-LoRA 4 steps 1024² | 29 s | [S12] |
| Intel Core Ultra iGPU ("Arc Graphics", MTL/ARL-H) | SD1.5-class 512², community | median **0.74 it/s** (n=29) | SD.Next DB [S42] |
| **RTX 4060 Laptop** (8 GB GDDR6, 3,072 CUDA cores, 233 AI TOPS, 35–115 W [S77]) | SD1.5-class 512², batch 1, no TensorRT | median **6.5 it/s** (n=203, IQR 3.6–7.9) | [S42] |
| **RTX 4070 Laptop** (8 GB GDDR6, 4,608 CUDA cores, 321 AI TOPS [S77]) | same | median **7.0 it/s** (n=62) | [S42] |
| RTX 3060 Laptop / desktop | same | 4.75 / 6.16 it/s | [S42] |
| RTX 4060 / 4070 desktop | same | 6.8 / 11.8 it/s | [S42] |
| RTX 3090 / 4090 desktop | same | 12.95 / 18.9 it/s | [S42] |
| RTX 4060 Laptop | SDXL 1024², 20 steps, fp16 | 15.8 s, 5.6 GB peak | [S76] (secondary aggregator) |
| RTX 4090 | SD-Turbo 1 step, StreamDiffusion + TensorRT | **106 fps** t2i, 94 fps img2img | [S29] |
| RTX 4090 | LCM-LoRA + KohakuV2 4 steps, StreamDiffusion | 38 fps | [S29] |
| RTX 3090 / 4090 / 2080 Ti / T4 | SDXL + LCM-LoRA 4 steps 1024² | 1.4 / 0.7 / 4.7 / 8.4 s | [S12] |
| H100 / RTX 4090 | SANA-Sprint 0.6B 1 step 1024² | 0.10 / 0.31 s | [S16] |
| H100 | FLUX.1-schnell 1024² | 1.1 s | [S16] |
| "modern hardware" / fal.ai server | FLUX.2-klein-4B 4 steps | "<0.5 s"; fal demo ≈0.17 s inference + 0.02 s safety check | [S19][S51] |
| Laptop RTX 4090 (16 GB) | FLUX.1-dev Nunchaku INT4 vs BF16+offload | 8.7–10.1× faster | [S20] |
| RTX PRO 6000 / RTX 5090 | ERNIE-Image-Turbo 1024², Nunchaku NVFP4 | 1.68–2.27 s / ≈1.7 s, ≈12 GB | [S73] |
| **Apple Silicon** (chip not recorded, MPS) | SD1.5-class 512², community | median **2.0 it/s** (n=209, IQR 1.3–2.6) | SD.Next DB, computed here [S42] |
| Mac M1 Max | SDXL + LCM-LoRA 4 steps 1024² | 6.5 s | [S12] |
| iPad Pro M2 (Core ML, ANE) | SD 2.1-base 20 steps 512² | 7.0 s | [S43] |
| MacBook Pro M2 Max (Core ML GPU) | SDXL-base 20 steps 1024² | 37 s | [S43] |
| Mac M4 Max (Core AI) | FLUX.2-klein-4B 4 steps 1024², incl. cold load | ≈17 s; ≈6.5 GB peak | [S75] |
| Apple M-series (chip unstated), mflux 4-bit | FLUX.2-klein-4B 4 steps 512² | ≈9 s | [S75] |
| Mac mini M4 Pro 24 GB (ComfyUI MPS) | SD1.5 512² 20 steps / SDXL 1024² 25 steps / Z-Image-Turbo 1024² 9 steps | 5–10 s / 20–40 s / 60–80 s | [S75] (blog, secondary) |

### 3.3 Estimated latency for the exhibition laptop (RTX 4060/4070 Laptop, 8 GB)

Method: SD1.5 UNet at 512² ≈ 1/6.5 s per CFG iteration on a 4060 Laptop [S42]; LCM/Turbo need no CFG, so a step is ≈0.08–0.15 s. SDXL ≈3× SD1.5 per step at equal latent size. A 4060 Laptop ≈0.5× a 3090 and ≈0.33× a 4090 [S42], used to scale [S12][S16]. Our measured iGPU per-step cost (≈0.55 s) is ≈5–7× slower than this, consistent with the 0.74 vs 6.5 it/s community medians. VAE ≈50–100 ms full, ≈10 ms TAESD (**UNVERIFIED** absolutes). All rows **[estimate]** — validate on the purchased machine.

| Pipeline on 4060/4070 Laptop | Per stage update | Fits 8 GB? |
|---|---|---|
| SD-Turbo 1 step 512 + TAESD (diffusers fp16) | ≈0.15–0.3 s | yes |
| **Hybrid: SD1.5-LCM img2img from Layer A, 4 steps, TAESD** | **≈0.4–0.7 s** (2.6 s measured on the dev iGPU) | yes |
| Same via StreamDiffusion + TensorRT | ≈30–50 ms (live morphing possible) | yes |
| **SD1.5-LCM 4 steps + ControlNet lineart/scribble img2img** | **≈0.6–1.2 s** | yes |
| SD1.5-LCM 4 steps + T2I-Adapter sketch | ≈0.5–0.9 s (adapter runs once) | yes |
| SDXL-Turbo 2–4 steps 512 + T2I-Adapter sketch SDXL + TAESDXL | ≈0.6–1.5 s | yes, TE embeddings cached |
| SDXL-Lightning 4 steps 1024 + ControlNet-Union | ≈3–4 s | tight (~7.5 GB) |
| SANA-Sprint 0.6B 2 steps 1024 | ≈1–1.5 s (512 px ≈0.3–0.5 s) | yes, with TE offload/precomputed embeddings |
| FLUX.2-klein-4B 4 steps 1024 (FP8, cached TE output) | ≈2–5 s **UNVERIFIED** | marginal |
| FLUX.1-schnell 4 steps 1024 (Nunchaku INT4) | ≈3–6 s **UNVERIFIED** | yes (≥4 GB with offload) |
| Z-Image-Turbo 8 NFE 1024 (INT4/GGUF) | ≈4–10 s **UNVERIFIED** | yes |

---

## 4. Making the picture evolve over stages without "jumping"

| Technique | How | Continuity | Cost/stage | Verdict |
|---|---|---|---|---|
| Fixed seed + growing prompt | Same seed, append attribute tokens | Poor: 1–4-step models re-compose globally | 1 gen | Only with the techniques below |
| **img2img from the coloured Layer A render** (hybrid) | init = current Layer A raster (flat colours, layout, sprites), style-only prompt, fixed seed. **LCM 3–4 steps × 0.6–0.7** | **Very good.** Attributes are pixels, so they bind correctly; every stage restarts from the same layout, so no drift accumulates | iGPU 2.0–2.6 s measured; NVIDIA ≈0.4–0.7 s est. | **Core recipe on every machine** |
| img2img chain from the *previous output* | init = stylised_{k−1}, low strength | Good for style, but new attributes did not appear (red→blue failed at 0.5) and artefacts accumulate | 1 gen | Only as a light "polish" |
| Masked inpainting of the changed region | Layer A knows where the new element is (hat), mask it | Rest stays pixel-identical | 1 gen (OpenVINO `InpaintingPipeline`: SD/LCM/SDXL/SD3/FLUX.1; **not FLUX.2-klein, not Qwen-Image** [S33]) | Good for adding accessories one at a time |
| **ControlNet / T2I-Adapter on a procedural sketch** | Layer A SVG → line art / scribble / segmentation | **Best structure**; new elements appear exactly where Layer A draws them (fixes the "extra arm" drift) | ControlNet every step; T2I-Adapter once (79M vs 1.25B params for ControlNet-SDXL) [S30]. **Not in OpenVINO GenAI** (§7) | Recommended add-on on NVIDIA |
| ControlNet + img2img combined | control = line art, init = colour raster | Layout from sketch, colours from init | ≈1.3× ControlNet alone. `StableDiffusionControlNetImg2ImgPipeline`, SDXL and ControlNet-Union SDXL img2img [S57] | **Recommended on NVIDIA** |
| Prompt-embedding interpolation | slerp between stage N and N+1 embeddings, fixed seed, 5–10 frames | Smooth morph | 5–10 gens | GPU nice-to-have |
| Latent (noise) slerp | Interpolate initial noise between seeds | Smooth, random-looking | 5–10 gens | Idle "daydreaming" animation only |
| Show the denoising trajectory | GenAI step callback + `pipe.decode(latent)` [S33]; diffusers `callback_on_step_end` | "The robot is painting…" | +1 TAESD decode per step (~tens of ms) | **Good on the dev iGPU**, where steps take ~0.5 s each |
| Front-end crossfade | CSS/canvas blend of consecutive images | Hides small jumps | ~0 | Always |
| StreamDiffusion (v1 / daydream fork) | Pipelined 1-step img2img, TensorRT, similarity filter, ControlNet + IP-Adapter (fork) [S29] | Real-time | NVIDIA only; Apache-2.0 | Optional "live morph" mode |
| StreamDiffusionV2 | Video-to-video on Wan 2.1 [S29] | — | Big GPUs; transforms *live video of the visitor* | **Don't** |

**Stage recipe (all machines):**
- `init = rasterise(LayerA_state_k)` at 512² (flat colours, no uncertainty overlays; unknown attributes drawn neutral grey)
- `prompt = STYLE_PROMPT` (fixed) + only harmless scene tokens (companion animal, theme)
- `seed = session_seed`; LCM+TAESD, **4 steps × 0.65** (dev iGPU: 3 steps for ≈2 s)
- NVIDIA: add `control = lineart(LayerA_state_k)` (SD1.5 ControlNet v1.1 lineart/scribble, or SDXL ControlNet-Union)
- output → safety classifiers (§8) → crossfade; optionally stream intermediate TAESD decodes as the "painting" effect.

**Stage plan** (ties to the sensing tracks):

| Stage (t) | Sensor | Layer A shows | Layer B (stylised Layer A) shows |
|---|---|---|---|
| 0 (0 s) | none | Grey "?" character, everything "unknown" | Grey neutral mascot (or no Layer B) |
| 1 (~20–40 s) | camera *or* mic | Presence, position/direction, distance band | Mascot placed left/right/near/far |
| 2 (~60 s) | camera | Dominant top colour / pattern (with %) | Body in that colour/pattern (from pixels) |
| 3 (~90–120 s) | camera | Glasses / backpack yes-no, waving | Accessory sprites restyled; waving arm |
| 4 (~150 s) | mic (+ASR keyword whitelist) | Loud/quiet, talkative, chosen "favourite animal/colour" | Companion sprite; background theme |
| 5 (~180–240 s) | all enabled | Final card: what I know, how sure, from which sensor, what I could NOT know | Final stylised "sticker" with AI label + optional imagination slider |

(Headwear: the legal track flags it as potentially revealing religion; the prototype vision module deliberately does not compute it [S83]. Use a *robot* hat sprite chosen by the visitor or a neutral accessory instead.)

When a sensor is switched off its attributes revert to "unknown": grey/dashed in Layer A and plain grey in the init image, so Layer B shows neutral grey instead of inventing a colour. Show a side panel: "when the robot doesn't know, its imagination makes things up."

---

## 5. Procedural / parametric avatar (Layer A)

Fully deterministic; every element traceable to one attribute and one sensor.

| Visual element | Attribute (closed vocabulary) | Sensor | Uncertainty encoding |
|---|---|---|---|
| Body fill colour | top colour ∈ {red, orange, yellow, green, blue, purple, pink, brown, black, white, grey, unknown} | camera | Fill opacity = confidence; runner-up colour as a striped swatch |
| Body pattern | {plain, stripes, dots, checks, print, unknown} | camera | Dashed outline if p < 0.6 |
| Glasses / backpack sprites | boolean each | camera | Ghosted sprite + "?" badge between thresholds |
| Position / size on canvas | x-position, distance band | camera (or mic DOA) | Blur radius = position uncertainty |
| Arm pose | waving / still | camera | — |
| Speech bubble size | voice activity / loudness band | mic | Bubble fill = confidence |
| Companion animal sprite | ASR keyword → whitelist | mic + ASR | Top-2 guesses if ASR confidence is low |
| Sensor "wires" | which sensor fed which element | XAI | Wire greys out when the sensor is toggled off |

- **Not present by design:** face, skin, hair, age, gender, ethnicity, emotion, body shape, headwear. Emotion recognition in education settings is prohibited (AI Act Art. 5(1)(f)) and biometric categorisation of protected traits is banned (Art. 5(1)(g)) [S46]; other biometric categorisation (age, gender, hair colour) triggers Art. 50(3) notices (`09-ethics-law.md`).
- **Implementation:** SVG + small state machine in the browser (or Python front-end); stage graph and confidences via WebSocket from the sensing back-end. The same SVG, rasterised, is the img2img init image; rasterised as line art, it is the ControlNet/T2I-Adapter control image.

---

## 6. Face/identity conditioning: why not (IP-Adapter, InstantID, PhotoMaker)

| Issue | Evidence |
|---|---|
| **Biometric data** | GDPR Art. 4(14): biometric data = personal data from technical processing of physical characteristics "which allow or confirm the unique identification … such as facial images" [S49]. InstantID and IP-Adapter-FaceID compute an ArcFace-type identity embedding (InsightFace `antelopev2` / `buffalo_l`) [S32] — an identification-grade face template of **children**, i.e. Art. 9 territory. |
| **Licence** | InsightFace pretrained models: "non-commercial research purposes only"; IP-Adapter-FaceID "exclusively for research purposes"; InstantID checkpoints research-only [S32]. PhotoMaker V2 pins `insightface==0.7.3` and runs its detection + recognition modules, so it inherits the restriction [S32]. |
| **Deepfake transparency** | AI Act Art. 50(4) deep fakes: content that "resembles existing persons … and would falsely appear … authentic" (Art. 3(60)) [S46]. A stylised portrait of a recognisable child is at least arguably in scope. |
| **New prohibitions** | Omnibus (Reg. (EU) 2026/1744) adds Art. 5(1)(ba) (non-consensual intimate imagery of identifiable persons) and 5(1)(bb) (CSAM), applying from **2 Dec 2026** [S46][S47]. Identity-conditioned generation of minors plus fallible safety filters [S44] is exactly the targeted risk surface. |
| **Training-data provenance** | LAION-5B (SD 1.x training data) contained "many hundreds of instances of known CSAM" (Stanford, Dec 2023) [S53]. |
| **Pedagogy** | It would teach "AI can copy your face" instead of "AI builds a model from evidence", and it undermines the privacy-by-design story. |

**Rule:** the generator never receives camera pixels. Inputs: (1) closed-vocabulary tokens, (2) the procedural sketch.

---

## 7. Tooling

| Tool | Licence | Strengths for us | Weaknesses (verified 2026-10-02) |
|---|---|---|---|
| **diffusers** (HF) | Apache-2.0 | Every model above; ControlNet/T2I-Adapter img2img; callbacks; TAESD; diffusers 0.40 ships SANA-Sprint img2img, SANA ControlNet, FLUX.2-klein, Z-Image img2img/ControlNet pipelines [S57]; Nunchaku 4-bit integration (Jul 2026) [S73] | PyTorch-CPU path is slow on Intel (§3.1) |
| **OpenVINO GenAI** `Text2Image` / `Image2Image` / `InpaintingPipeline` | Apache-2.0 | Native C++/Python/JS. Supported: LCM, SD1.x/2.x, SDXL, SD3/3.5, FLUX.1, **FLUX.2-klein** (t2i, i2i, LoRA; no inpainting), Qwen-Image (t2i, i2i) [S33]. Step callback with intermediate decode; heterogeneous TE/UNet/VAE on CPU/GPU/NPU; static reshape for NPU; compile cache. **Tested here (2026.4.1)** on CPU, iGPU and NPU; TAESD swap works | **No ControlNet**: not in the supported-features list [S33]; the GSoC-2024 ControlNet pipeline PR #740 was **closed without merge** (Dec 2024) [S61]. **No SANA/SANA-Sprint** (feature request #2224 open since May 2025) [S62]. Old community IRs need tokenizer conversion and an i64 TE patch |
| **optimum-intel** (`OVDiffusionPipeline`, `optimum-cli export openvino`) | Apache-2.0 | Exports SD/SDXL/LCM/SD3/FLUX/FLUX.2/SANA/SANA-Sprint/Qwen-Image/Z-Image to OpenVINO IR with INT8/INT4 weights [S35] | Needs Python + torch for export |
| **FastSD CPU** | MIT | Ready-made OpenVINO app: LCM/SD-Turbo/SDXS, TAESD, SANA-Sprint (OpenVINO), FLUX.2-klein-4B OpenVINO int4 (Jun 2026) and GGUF (Jul 2026), image editing, REST/MCP API, NPU support for an SD1.5-LCM int8 model [S63] | **ControlNet only in "LCM-LoRA mode" (PyTorch), not OpenVINO** [S63]. NPU documented for Meteor Lake / Lunar Lake only (our Arrow Lake-U not listed). A SANA-Sprint int4 blank-image bug was reported (issue #359). Hobby project |
| **stable-diffusion.cpp** | MIT | C/C++ (ggml), GGUF q4/q8; CPU/CUDA/Vulkan/SYCL/OpenCL/Metal; SD1.x/2.x/SDXL/Turbo, SD3, FLUX.1/FLUX.2-klein, Z-Image (≤4 GB VRAM), Qwen-Image(-2.1), ControlNet, LCM, TAESD. Release master-929 on 2026-09-27 [S37] | Fewer conditioning options than diffusers |
| **ComfyUI** | **GPL-3.0** | Fastest graph prototyping (ControlNet, GGUF, Nunchaku nodes); API mode | **No built-in safety checker** — only optional community nodes (e.g. YetAnotherSafetyChecker) [S81]. GPL if distributed with modifications. Graph JSON brittle at a venue |
| **Nunchaku** (SVDQuant INT4/NVFP4) | Apache-2.0 | FLUX.1, SANA, PixArt-Σ, Qwen-Image, Z-Image-Turbo, FLUX.2-klein-4B, ERNIE-Image-Turbo, Krea-2-Turbo at 4-bit; INT4 on Turing/Ampere/Ada, NVFP4 on Blackwell [S20][S73] | NVIDIA only |
| **StreamDiffusion** (+ daydream fork) | Apache-2.0 | 100+ fps SD-Turbo on a 4090 with TensorRT; fork adds SDXL, ControlNet, IP-Adapter, TemporalNet [S29] | NVIDIA + TensorRT only |
| **ONNX Runtime DirectML** | MIT | Vendor-neutral on Windows | **"Sustained engineering"**; new work moved to WinML [S36] |
| **Intel AI Playground** | MIT | ComfyUI-based app with FLUX.2-klein-4B fp8 and Z-Image-Turbo | Officially Core Ultra Series 3, Series 2 **V/H**, Series 1 H or Arc dGPU; **U-series (our 255U) not listed** [S40] |
| **mflux** (Apple MLX) | MIT | FLUX.2-klein, Z-Image, Qwen-Image(-2.1), Krea 2, Ideogram 4 etc. on Apple Silicon [S55] | No official timing table |

---

## 8. Safety layer (child-safe by construction)

1. **Closed-vocabulary prompt templating.** The prompt is assembled only from enumerated tokens; in the hybrid recipe it is a *fixed style prompt* plus at most companion/theme tokens. **No free ASR text ever reaches the prompt** (keyword → whitelist, else "unknown"). A negative prompt (`person, human, child, face, realistic, photo, text, nsfw, nude, weapon, blood`) only works with CFG; LCM uses guidance embedding and Turbo models run at `guidance_scale=0`, so rely on points 2–4.
2. **Non-human subject**, which removes most demographic and likeness issues (§3.1).
3. **Output classifiers on every image before display:** an NSFW classifier, e.g. `Falconsai/nsfw_image_detection` (Apache-2.0, ViT) [S45] or ShieldGemma-2-4B (Gemma licence, gated) [S45]; plus a "contains a human face?" check (small face detector or CLIP zero-shot). If either trips, **fall back to Layer A only**. The classic SD safety checker targets only sexual content and is easy to bypass [S44]; ComfyUI ships none [S81].
4. **Pre-flight exhaustive test.** The vocabulary is closed and seeds are fixed, so every combination can be **generated and reviewed offline**. Maximum robustness: ship a **pre-rendered, human-reviewed asset library** and composite at runtime — zero runtime generation risk, still "AI-made" art.
5. **Logging:** prompts and classifier scores only, never visitor images.

---

## 9. Compliance notes specific to generation (cross-check with `09-ethics-law.md`)

- **Art. 50(2) (providers):** synthetic images must be "marked in a machine-readable format and detectable as artificially generated" [S46]. The Omnibus (Reg. (EU) 2026/1744, OJ 24 Jul 2026) grants a grace period to 2 Dec 2026 **only for systems on the market before 2 Aug 2026** [S47] — none for a 2027 exhibit.
- The Commission's **Code of Practice on marking and labelling AI-generated content** was finalised **10 Jun 2026**; it asks for marking solutions that are "effective, interoperable, robust, and reliable as far as technically feasible", and the EU published icons deployers may use [S48]. Whether it prescribes a specific multi-layer combination (metadata + watermark) is **UNVERIFIED** here.
- Practical answer: visible on-screen label + EU icon. The prototype already writes IPTC `DigitalSourceType = trainedAlgorithmicMedia` ("created algorithmically using an AI model trained on captured content" [S82]) into XMP and an EXIF description [S83]. Metadata is trivially stripped, so if images ever leave the stand (print, QR) add C2PA and an invisible watermark. Simplest: **images never leave the stand.**
- **Art. 2(6)** exempts systems "specifically developed and put into service for the sole purpose of scientific research and development"; a public exhibit is not sole-purpose R&D, and Art. 2(8) excludes real-world testing from the pre-market exemption [S46]. Pilot sessions with children are not exempt.
- **Art. 5(1)(f)/(g):** no emotion inference, no biometric categorisation [S46].
- **GDPR:** if §6 and §8 are followed, the generator receives only coarse, transient appearance tokens and a procedural sketch. Whether such tokens are personal data while the visitor stands in front of the camera is a DPIA question for the legal track; design so that nothing generated is stored or linked.

---

## 10. Cloud alternatives

| Service | Model | Price (accessed 2026-10-02) | Latency | Data location / GDPR |
|---|---|---|---|---|
| fal.ai | FLUX.1-schnell | USD 0.003 / MP | **UNVERIFIED** end-to-end | "fal is based in the United States"; processing in the US "and other countries"; contractual clauses; DPA page [S51]. No EU region found (**UNVERIFIED**) |
| fal.ai | Z-Image-Turbo / FLUX.2-klein-4B | USD 0.005 / MP | klein demo ≈0.17 s inference + 0.02 s safety check, server-side | same |
| Replicate | flux-schnell | USD 3.00 / 1,000 images | **UNVERIFIED** | US company; GPU from USD 0.000225/s (T4) to 0.001525/s (H100) [S52] |
| **BFL API** (Black Forest Labs, Germany) | FLUX.2-klein-4B / 9B | **from USD 0.014 / 0.015 per image** (first MP; +0.001/0.002 per extra MP) [S78] | **UNVERIFIED** | **EU endpoint `api.eu.bfl.ai`: "multi-cluster routing limited to EU regions", "GDPR compliant"**; US-only `api.us.bfl.ai`; global `api.bfl.ai`. Result URLs expire after 10 min [S78] |
| Stability API | SD 3.5 Large Turbo / Core / Flash | 4 / 3 / 2.5 credits per image, 1 credit = USD 0.01 (secondary source; official page JS-rendered) [S79] | **UNVERIFIED** | **UNVERIFIED** |

- **Cost is negligible.** At ~5 images per session and a few hundred sessions over 16 fair hours, total cost is a few US dollars (USD 4–70 even for 5,000 images).
- **Real costs:** venue Wi-Fi reliability; round-trip and queueing (**UNVERIFIED**, typically sub-second to a few seconds); AI Act provider role stays with us; and for US services an EU→US transfer. The EU-US DPF adequacy decision (10 Jul 2023) was upheld by the General Court on 3 Sep 2025 (*Latombe*, T-553/23), but an appeal (C-703/25 P) is pending at the CJEU [S50][S80] — a residual risk during 2027. **An EU-routed endpoint avoids the transfer question.**
- **Allowed only if** the payload is the closed-vocabulary prompt plus the procedural sketch — never camera or audio data — and with a local fallback.

---

## 11. Recommendations for our demonstrator

### 11.1 Dev laptop prototype now (Core Ultra 7 255U, 32 GB, no NVIDIA)

1. **Build Layer A first** (SVG avatar + XAI panel + sensor toggles). It is the real deliverable.
2. **Layer B = OpenVINO GenAI `Image2ImagePipeline` on the iGPU** (`pip install openvino-genai`, 2026.4.1 tested):
   - Model `OpenVINO/LCM_Dreamshaper_v7-int8-ov` (MIT) with `rupeshs/taesd-ov` (MIT) copied into `vae_decoder/` and `vae_encoder/`.
   - `pipe.reshape(1, 512, 512, guidance_scale)`, `pipe.compile("GPU", "GPU", "GPU", config={"CACHE_DIR": ...})`.
   - Per stage: `pipe.generate(STYLE_PROMPT, ov.Tensor(layerA_rgb[None]), strength=0.65, num_inference_steps=3 or 4, rng_seed=session_seed)` → **≈2.0 s (3 steps) / ≈2.6 s (4 steps)** [measured-here].
   - Run it asynchronously after each stage update; show the step-callback partial decodes as the "painting" effect; crossfade.
   - Don't use SD-Turbo for the hybrid on this machine: at the strengths that preserve attributes it executes only 1–2 steps and doesn't restyle (§3.1).
   - Never use the CPU for diffusion here (26–53 s per hybrid image [measured-here]).
3. **Integrate into the prototype:** replace the `Imagination` backend in `prototype/robotsees/render/imagination.py` (currently diffusers SD-Turbo text-to-image on the CPU, documented 20–35 s) with the call above; keep its closed phrase list only for scene tokens, keep `save_marked()` (IPTC marking), and feed the Layer A raster as init image. Expected effect: ≈10× faster and correct colour binding.
4. **Scheduling against perception:** iGPU generation was not slowed by CPU perception, but CPU perception fell to roughly ⅓–½ of its rate while the iGPU generated continuously (§3.1, concurrency). Generate once per stage, pause or slow perception during the ~2 s "painting" animation, and keep the camera/mic pipeline's own timing independent of Layer B.
5. **NPU:** a heterogeneous pipeline works (TE on CPU, UNet on NPU, VAE on iGPU: 3.0 s at 4 steps) but needs a static reshape and a ~2.5 min first compile; persist `CACHE_DIR`. Better use of the NPU: run perception models there (OpenVINO) so that CPU, iGPU and NPU each carry one job.
5. **ControlNet on Intel:** not available in OpenVINO GenAI [S33][S61]; FastSD's ControlNet runs in PyTorch LCM-LoRA mode only [S63] (CPU speed). On the dev laptop rely on img2img from the coloured Layer A raster (measured to preserve structure); add ControlNet only on the NVIDIA machine.
6. **Parallel path:** use the dev laptop offline to pre-render a curated sprite/scene library (all colour × pattern × accessory × companion combinations at fixed seeds) — the guaranteed-safe fallback for the fair.

### 11.2 Exhibition laptop (RTX 4060/4070 Laptop, 8 GB; better: 12 GB)

Preferred stack (one codebase with the dev laptop): **diffusers fp16 + SD1.5-LCM (Dreamshaper-LCM, MIT) + `StableDiffusionControlNetImg2ImgPipeline`** [S57], ControlNet v1.1 lineart/scribble (OpenRAIL) on the Layer A line art, init = Layer A colour raster, strength ≈0.65, 4 steps, TAESD, fixed session seed.
- **≈0.6–1.2 s per stage update**; without ControlNet ≈0.4–0.7 s [estimate].
- Keep the OpenVINO path as a fallback (it also runs on this laptop's CPU/iGPU).

Better-looking alternative: **SDXL-Turbo (Community Licence) or SDXL-Lightning (OpenRAIL++) + ControlNet-Union-SDXL img2img (xinsir, Apache-2.0) or T2I-Adapter-sketch-SDXL (Apache-2.0, 79M) + TAESDXL**, 512–768 px, 2–4 steps: **≈0.6–1.5 s** [estimate]. Cache text-encoder outputs (fixed prompt) to stay under 8 GB. Optional 4–6-frame interpolation morph ≈2–4 s.

"Wow" options, only after measuring on the actual machine:
- **SANA-Sprint 0.6B** (Apache-2.0; img2img and ControlNet pipelines in diffusers [S57]; 0.25 s ControlNet on H100 [S16]): 1024 px ≈1–1.5 s [estimate].
- **FLUX.2-klein-4B FP8** (Apache-2.0) with cached TE output and the FLUX.2-small-decoder [S64][S65]: ≈2–5 s **UNVERIFIED**.

Run the generator as a **separate local service** (FastAPI) with a watchdog: if generation exceeds 3 s, the classifier rejects the output or the GPU errors, the UI silently stays on Layer A.

Hardware advice: 8 GB VRAM is the binding constraint and a 4070 Laptop adds only ≈10–20% over a 4060 Laptop [S42]. If buying in 2026–27, target an **RTX 5070 Ti Laptop (12 GB GDDR7, 992 AI TOPS)** or a verified 12 GB RTX 5070 Laptop configuration (the 5070 Laptop ships with 8 GB or 12 GB; 5060/5050 Laptop = 8 GB) [S77]; Blackwell also unlocks NVFP4 (Nunchaku, FLUX.2 NVFP4) [S19][S73]. Laptop prices **UNVERIFIED**. If the purchased laptop is AMD Ryzen AI instead, Stability's `sd-turbo-amdnpu` / `sdxl-turbo-amdnpu` ONNX builds exist [S72] (latency **UNVERIFIED**).

### 11.3 Model shortlist (in order)

1. **SD1.5-LCM (Dreamshaper-LCM, MIT), img2img from Layer A (+ ControlNet on NVIDIA).** Measured 2.0–2.6 s on the dev iGPU; runs on every target; best structure–style trade-off we observed.
2. SDXL-Turbo / SDXL-Lightning + ControlNet-Union or T2I-Adapter sketch: NVIDIA, better look.
3. SD-Turbo + TAESD: fastest (0.58 s t2i on the iGPU), but a poor *restyler* at attribute-preserving strengths, weak ControlNet ecosystem for the SD 2.1 base, and SD 2.x is deprecated [S7].
4. SANA-Sprint 0.6B: NVIDIA, 1024 px, permissive licence; not in OpenVINO GenAI.
5. FLUX.2-klein-4B: NVIDIA (FP8), best quality and multi-reference editing, heaviest; runs on the Intel iGPU only as a slow demo (§3.1).

---

## 12. Pitfalls / what not to do

- **Don't put the webcam frame into img2img/ControlNet/IP-Adapter**, and don't run any face-ID adapter (InstantID, IP-Adapter-FaceID, PhotoMaker): biometric, licence-restricted, deepfake-adjacent, children (§6).
- **Don't draw a human "portrait of you".** The model invents hair, skin tone, gender and age (observed, §3.1).
- **Don't use the diffusion image as the explanation.** Attribute binding fails in text-to-image and small details drift in img2img (hat colour, extra arm). XAI belongs on Layer A.
- **Don't drive attribute changes through the prompt** (text-to-image, or low-strength img2img from the previous frame): "red→blue" didn't take.
- **Don't assume strength lowers cost.** LCM always runs `num_inference_steps`; SD-Turbo runs `int(steps × strength)` (so "4 × 0.7" = 2 steps and almost no restyle) [S60].
- **Don't let the model invent the mascot's facial expression.** At LCM 4 × 0.6 it drew a frowning mouth Layer A never had. A child may read that as "the robot thinks I'm sad" — it looks like emotion inference even though none happened (Art. 5(1)(f) bans *recognising* emotions in education settings; the exhibit should not even appear to). Draw a fixed friendly face (or no face) in Layer A and check generated faces in the offline review.
- **Don't use high img2img strength (≥0.85) or many LCM steps by default** — it invents animals and accessories. Make that the explicit "imagination" mode.
- **Don't use 2023-era community OpenVINO IRs on the NPU** (dynamic-shape failure, tokenizer/i64 patches). Re-export with current `optimum-cli export openvino` or use official `OpenVINO/*` models.
- **Don't expect ControlNet or SANA in OpenVINO GenAI**, and don't count on FastSD for OpenVINO ControlNet (its ControlNet is PyTorch LCM-LoRA mode) [S33][S61][S62][S63].
- **Don't feed ASR text or any free text into prompts.** Whitelist only.
- **Don't rely on the SD safety checker alone or on ComfyUI defaults** (ComfyUI has none) [S44][S81].
- **Don't download models at the venue or depend on HF repos staying up** (SD 2.x vanished [S7]). Vendor weights + hashes.
- **Don't run diffusion on the CPU** of a 15 W U-series chip, nor PyTorch-CPU on Intel: iGPU 0.6–2.6 s vs CPU 7–53 s [measured-here].
- **Don't pick FLUX.2-klein-9B, Qwen-Image-2.1, Ideogram 4, IP-Adapter-FaceID, InstantID, Hyper-SD FLUX LoRAs or PCM weights** (non-commercial, research-only or unlicensed).
- **Don't start new work on ONNX Runtime DirectML** (sustained engineering only) [S36].
- **Don't ship a ComfyUI graph** (GPL-3.0, brittle). Prototype there, ship a small diffusers/OpenVINO service.
- **Don't let generated images leave the stand unmarked** (Art. 50(2)); show the on-screen AI label and the "Powered by Stability AI" notice if Stability models are used [S4].
- **Don't use cloud APIs with sensor data**, nor make the exhibit depend on venue Wi-Fi; if cloud is ever used, prefer an EU-routed endpoint [S78].
- **Don't benchmark (or exhibit) with other heavy jobs on the same laptop.** Our CPU numbers swung by 60% between rounds because of other jobs; pin generation and perception to separate devices.

---

## 13. Unverified / open items

- Exact latency of every NVIDIA pipeline in §3.3 on an RTX 4060/4070 *Laptop* (all estimates). Benchmark on the purchased machine.
- FLUX.2-klein-4B FP8 latency and memory on 8 GB with TE caching; SANA-Sprint on 8 GB.
- Whether the Code of Practice prescribes a specific multi-layer marking combination.
- Stability API pricing (secondary source only) and data location; fal.ai EU region; end-to-end cloud latency from Brussels.
- RTX 50-series laptop prices for 2026–27.
- Whether SD-Turbo stays downloadable (SD 2.1 base deprecated).
- CPU figures were measured under contention from other project jobs in both rounds; re-run on an idle machine if CPU numbers matter (they don't for the recommendation).
- The hybrid quality judgement rests on one sketch and one seed per setting. Run a small user test with children before committing to a style (note: real-world testing is not covered by the AI Act R&D exemption, Art. 2(8)).
- LLaDA-Image-Turbo licence: HF metadata says Apache-2.0 (2026-10-02) while a secondary article reported "no licence tag" at launch; re-check before use.
- Latency of `sd-turbo-amdnpu` on AMD Ryzen AI NPUs.

---

## Sources

- [S1] SD-Turbo model card: https://huggingface.co/stabilityai/sd-turbo
- [S2] SD-Turbo LICENSE (Stability AI Community Licence, 5 Jul 2024): https://huggingface.co/stabilityai/sd-turbo/blob/main/LICENSE.md
- [S3] SDXL-Turbo card + LICENSE: https://huggingface.co/stabilityai/sdxl-turbo , https://huggingface.co/stabilityai/sdxl-turbo/blob/main/LICENSE.md
- [S4] Stability AI Community Licence: https://stability.ai/community-license-agreement
- [S5] Stability licence overview: https://stability.ai/license
- [S6] SDXL-Turbo launch post: http://stability.ai/news-updates/stability-ai-sdxl-turbo
- [S7] Stability statement deprecating SD 2.0/2.1 (15 Nov 2025): https://huggingface.co/spaces/stabilityai/stable-diffusion-3.5-large/discussions/648
- [S8] SD 2.1 community mirror: https://huggingface.co/sd2-community/stable-diffusion-2-1
- [S9] SDXL-Lightning: https://huggingface.co/ByteDance/SDXL-Lightning
- [S10] Hyper-SD + LICENSE.md: https://huggingface.co/ByteDance/Hyper-SD , https://huggingface.co/ByteDance/Hyper-SD/blob/main/LICENSE.md
- [S11] LCM-LoRA SD1.5: https://huggingface.co/latent-consistency/lcm-lora-sdv1-5 ; LCM Dreamshaper (MIT): https://huggingface.co/SimianLuo/LCM_Dreamshaper_v7
- [S12] HF blog, LCM-LoRA benchmarks: https://huggingface.co/blog/lcm_lora
- [S13] PCM weights: https://huggingface.co/wangfuyun/PCM_Weights ; code: https://github.com/G-U-N/Phased-Consistency-Model
- [S14] SANA: https://github.com/NVlabs/Sana ; relicensing commits: https://huggingface.co/Efficient-Large-Model/Sana_1600M_1024px_diffusers/commits/main , https://huggingface.co/Efficient-Large-Model/Sana_Sprint_0.6B_1024px_diffusers/commits/main
- [S15] SANA paper: https://arxiv.org/abs/2410.10629
- [S16] SANA-Sprint paper + card: https://arxiv.org/abs/2503.09641 , https://huggingface.co/Efficient-Large-Model/Sana_Sprint_0.6B_1024px_diffusers ; SANA ControlNet HED: https://huggingface.co/Efficient-Large-Model/Sana_600M_1024px_ControlNet_HED
- [S17] PixArt-Σ: https://huggingface.co/PixArt-alpha/PixArt-Sigma-XL-2-1024-MS
- [S18] FLUX.1-schnell: https://huggingface.co/black-forest-labs/FLUX.1-schnell
- [S19] FLUX.2 [klein]: https://huggingface.co/black-forest-labs/FLUX.2-klein-4B , https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence , https://huggingface.co/black-forest-labs/FLUX.2-klein-9B
- [S20] Nunchaku / SVDQuant: https://github.com/nunchaku-tech/nunchaku , https://arxiv.org/abs/2411.05007
- [S21] SD 3.5: https://huggingface.co/stabilityai/stable-diffusion-3.5-medium , https://huggingface.co/stabilityai/stable-diffusion-3.5-large-turbo
- [S22] Small SD: https://huggingface.co/nota-ai/bk-sdm-small , https://huggingface.co/segmind/tiny-sd , https://huggingface.co/segmind/Segmind-Vega
- [S23] SDXS: https://huggingface.co/IDKiro/sdxs-512-0.9
- [S24] Kandinsky: https://huggingface.co/kandinskylab/Kandinsky-5.0-T2I-Lite , https://huggingface.co/kandinsky-community/kandinsky-3
- [S25] Z-Image-Turbo: https://huggingface.co/Tongyi-MAI/Z-Image-Turbo ; ControlNet: https://huggingface.co/alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union
- [S26] Qwen-Image: https://github.com/QwenLM/Qwen-Image , https://huggingface.co/Qwen/Qwen-Image-2512 , https://huggingface.co/Qwen/Qwen-Image-2.1
- [S27] Lumina-Image 2.0: https://huggingface.co/Alpha-VLLM/Lumina-Image-2.0
- [S28] HiDream-I1-Fast: https://huggingface.co/HiDream-ai/HiDream-I1-Fast
- [S29] StreamDiffusion: https://github.com/cumulo-autumn/StreamDiffusion , https://arxiv.org/html/2312.12491 , https://github.com/daydreamlive/StreamDiffusion , https://github.com/chenfengxu714/StreamDiffusionV2
- [S30] T2I-Adapter SDXL: https://huggingface.co/blog/t2i-sdxl-adapters , https://huggingface.co/TencentARC/t2i-adapter-sketch-sdxl-1.0
- [S31] ControlNets: https://huggingface.co/xinsir/controlnet-union-sdxl-1.0 , https://huggingface.co/lllyasviel/control_v11p_sd15_scribble
- [S32] Face adapters: https://huggingface.co/h94/IP-Adapter-FaceID , https://github.com/instantX-research/InstantID , https://github.com/deepinsight/insightface , https://huggingface.co/TencentARC/PhotoMaker-V2 , https://raw.githubusercontent.com/TencentARC/PhotoMaker/main/requirements.txt
- [S33] OpenVINO GenAI: https://openvinotoolkit.github.io/openvino.genai/docs/supported-models/ , https://openvinotoolkit.github.io/openvino.genai/docs/use-cases/image-generation/ , https://github.com/openvinotoolkit/openvino.genai/blob/master/samples/python/image_generation/README.md , https://github.com/openvinotoolkit/openvino.genai/blob/master/samples/python/image_generation/heterogeneous_stable_diffusion.py
- [S34] OpenVINO models used: https://huggingface.co/OpenVINO/LCM_Dreamshaper_v7-int8-ov , https://huggingface.co/rupeshs/sd-turbo-openvino , https://huggingface.co/OpenVINO/FLUX.1-schnell-int4-ov
- [S35] optimum-intel supported models: https://github.com/huggingface/optimum-intel/blob/main/docs/source/openvino/models.mdx
- [S36] ONNX Runtime DirectML EP: https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html
- [S37] stable-diffusion.cpp: https://github.com/leejet/stable-diffusion.cpp , https://github.com/leejet/stable-diffusion.cpp/releases
- [S38] FastSD CPU benchmarks: https://github.com/rupeshs/fastsdcpu
- [S39] ComfyUI (GPL-3.0): https://github.com/Comfy-Org/ComfyUI
- [S40] Intel AI Playground: https://github.com/intel/AI-Playground
- [S41] Intel Core Ultra 7 255U (ARK): https://www.intel.com/content/www/us/en/products/sku/241860/intel-core-ultra-7-processor-255u-12m-cache-up-to-5-20-ghz/specifications.html
- [S42] SD.Next community benchmark DB (raw JSON re-downloaded 2026-10-02, 16,635 rows, latest 2026-01-07; Apple rows identified by `system:Darwin`, chip not recorded): https://vladmandic.github.io/sd-extension-system-info/pages/benchmark.html , https://vladmandic.github.io/sd-data/pages/benchmark-data.json
- [S43] Apple Core ML Stable Diffusion: https://github.com/apple/ml-stable-diffusion
- [S44] Rando et al., "Red-Teaming the Stable Diffusion Safety Filter": https://arxiv.org/abs/2210.04610
- [S45] Safety classifiers: https://huggingface.co/Falconsai/nsfw_image_detection , https://huggingface.co/google/shieldgemma-2-4b-it
- [S46] AI Act (consolidated incl. Omnibus): https://artificialintelligenceact.eu/article/50/ , https://artificialintelligenceact.eu/article/5/ , https://artificialintelligenceact.eu/article/2/
- [S47] AI Omnibus (Reg. (EU) 2026/1744): https://cdp.cooley.com/digital-ai-omnibus-delays-key-deadlines-introduces-new-rules/ , https://www.williamfry.com/knowledge/eu-ai-act-omnibus-deal-reached-postponed-deadlines-watermarking-compromise-and-the-nudificiation-prohibition/ , https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32026R1744
- [S48] EU Code of Practice on AI-generated content: https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content
- [S49] GDPR Art. 4: https://gdpr-info.eu/art-4-gdpr/
- [S50] EU-US data transfers / DPF: https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/eu-us-data-transfers_en
- [S51] fal.ai: https://fal.ai/pricing , https://fal.ai/models/fal-ai/flux-2/klein/4b , https://fal.ai/privacy
- [S52] Replicate: https://replicate.com/pricing , https://replicate.com/black-forest-labs/flux-schnell
- [S53] Thiel (Stanford), CSAM in generative ML training data (20 Dec 2023): https://purl.stanford.edu/kh752sm9123
- [S54] TAESD (MIT): https://huggingface.co/madebyollin/taesd , https://github.com/madebyollin/taesd
- [S55] mflux (MIT): https://github.com/filipstrand/mflux
- [S56] NVIDIA laptop GPU pages: https://www.nvidia.com/en-us/geforce/laptops/40-series/ , https://www.nvidia.com/en-us/geforce/laptops/50-series/
- [S57] diffusers ControlNet img2img and SDXL-Turbo guide (`steps × strength ≥ 1`): https://huggingface.co/docs/diffusers/main/en/api/pipelines/controlnet , https://huggingface.co/docs/diffusers/main/en/using-diffusers/sdxl_turbo ; checked locally in diffusers 0.40.0 (`pipeline_sana_sprint_img2img.py`, `pipeline_sana_controlnet.py`, `pipeline_flux2_klein*.py`, `pipeline_z_image_{img2img,controlnet}.py`)
- [S58] Qwen-Image-Lightning (Apache-2.0): https://huggingface.co/lightx2v/Qwen-Image-Lightning
- [S59] TAESD OpenVINO export (MIT): https://huggingface.co/rupeshs/taesd-ov
- [S60] diffusers `LCMScheduler.set_timesteps` strength logic (origin schedule truncated to `original_steps × strength`, then `num_inference_steps` picked): https://github.com/huggingface/diffusers/blob/main/src/diffusers/schedulers/scheduling_lcm.py (read locally in 0.40.0); confirmed by our step-callback counts (§3.1 rows 18–27)
- [S61] OpenVINO GenAI ControlNet: GSoC 2024 project https://github.com/openvinotoolkit/openvino/wiki/OpenVINO-at-Google-Summer-Of-Code-in-the-past ; PR #740 closed without merge (23 Dec 2024): https://github.com/openvinotoolkit/openvino.genai/pull/740
- [S62] OpenVINO GenAI SANA-Sprint request #2224 (open, May 2025): https://github.com/openvinotoolkit/openvino.genai/issues/2224
- [S63] FastSD CPU README (news 2025-05-17 SANA Sprint OpenVINO; 2026-06-21 FLUX.2-klein-4B OpenVINO; 2026-07-05 FLUX.2 klein GGUF; "We can use ControlNet in LCM-LoRA mode"; NPU tested on Meteor Lake / Lunar Lake): https://github.com/rupeshs/fastsdcpu ; FLUX.2-klein OpenVINO int4 IR (Apache-2.0, 4.57 GB): https://huggingface.co/rupeshs/flux2-klein-4b-int4-ov ; SANA-Sprint int4 bug: https://github.com/rupeshs/fastsdcpu/issues/359
- [S64] FLUX.2-small-decoder: https://huggingface.co/black-forest-labs/FLUX.2-small-decoder
- [S65] BFL HF org listing (FLUX.2-klein FP8/NVFP4, 9B-KV, FLUX 3 Action): https://huggingface.co/api/models?author=black-forest-labs&sort=createdAt&direction=-1
- [S66] FLUX 3 launch (23 Jul 2026; no open weights yet): https://venturebeat.com/technology/black-forest-labs-launches-flux-3-capable-of-generating-images-and-20-second-video-with-audio-but-in-limited-release-to-start
- [S67] LLaDA-Image-Turbo: https://huggingface.co/inclusionAI/LLaDA-Image-Turbo , https://huggingface.co/api/models/inclusionAI/LLaDA-Image-Turbo ; launch article: https://www.orcarouter.ai/blog/llada-image-turbo-release
- [S68] ERNIE-Image-Turbo: https://huggingface.co/baidu/ERNIE-Image-Turbo , https://github.com/baidu/ernie-image
- [S69] Krea 2 Turbo: https://huggingface.co/krea/Krea-2-Turbo , https://huggingface.co/api/models/krea/Krea-2-Turbo
- [S70] Ideogram 4: https://huggingface.co/ideogram-ai/ideogram-4-nf4 ; https://blog.buildfastwithai.com/ideogram-4-open-weight-image-model
- [S71] Z-Image (base): https://huggingface.co/api/models?search=Z-Image&author=Tongyi-MAI
- [S72] Stability AMD NPU builds: https://huggingface.co/stabilityai/sd-turbo-amdnpu , https://huggingface.co/api/models?author=stabilityai&sort=createdAt&direction=-1
- [S73] HF blog "Bringing Nunchaku 4-bit Diffusion Inference to Diffusers" (23 Jul 2026): https://huggingface.co/blog/nunchaku-diffusers
- [S74] SANA README (laptop "<8GB VRAM via 4-bit"): https://github.com/NVlabs/Sana
- [S75] Apple Silicon FLUX.2-klein: https://huggingface.co/mlboydaisuke/FLUX.2-klein-4B-CoreAI , https://huggingface.co/ar9av/FLUX.2-klein-4B-mflux-4bit ; Mac mini M4 Pro comparison (blog): https://www.heyuan110.com/posts/ai/2026-02-15-mac-mini-local-image-generation/
- [S76] 8 GB VRAM aggregator (RTX 4060 Laptop SDXL 15.8 s; secondary): https://heiss-ui.vercel.app/hardware/8gb-vram/
- [S77] NVIDIA laptop GPU comparison (CUDA cores, AI TOPS, VRAM, TGP): https://www.nvidia.com/en-us/geforce/laptops/compare/
- [S78] BFL API: regional endpoints https://docs.bfl.ai/api_integration/integration_guidelines ; pricing https://docs.bfl.ai/quick_start/pricing
- [S79] Stability API pricing (secondary): https://developer.puter.com/tutorials/stability-ai-api-pricing/ ; official (JS-rendered): https://platform.stability.ai/pricing
- [S80] DPF litigation: https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20251201-european-court-of-justice-to-review-challenge-to-eu-us-data-privacy-framework , http://eulawanalysis.blogspot.com/2025/10/the-general-court-of-european-union.html
- [S81] ComfyUI has no built-in safety checker (community sources): https://offlinecreator.com/tool/comfyui/for/uncensored , https://github.com/BetaDoggo/ComfyUI-YetAnotherSafetyChecker
- [S82] IPTC DigitalSourceType `trainedAlgorithmicMedia`: https://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia
- [S83] Internal: `prototype/robotsees/render/imagination.py`, `prototype/robotsees/perception/vision.py`, `research/01-call-and-tuai.md`, `research/09-ethics-law.md`
- [S84] Qwen HF listing (licence tags): https://huggingface.co/api/models?author=Qwen&search=Qwen-Image&sort=createdAt&direction=-1

---

## Verification log

Round 1 claims were independently re-checked on 2026-10-02 with fresh fetches of primary sources; corrections from that pass are now merged into the body. Measured-here numbers were not re-verified by a third party; round 2 re-measured the key iGPU configurations and found them stable.

| # | Claim | Verdict | Source |
|---|---|---|---|
| 1 | SANA and SANA-Sprint weights relicensed to Apache-2.0 on 31 Jul 2026 | Confirmed (Sana_1600M commit ac0da2f, Sana_Sprint_0.6B commit aa76e7f; Gemma ToU for the TE) | [S14] |
| 2 | SANA-Sprint 0.10 s H100 / 0.31 s RTX 4090 (1024² T2I), 0.25 s ControlNet H100; FLUX-schnell 1.1 s H100 | Confirmed | [S16] |
| 3 | FLUX.2-klein-4B Apache-2.0, 15 Jan 2026, ~13 GB VRAM, FP8 up to 40% less, NVFP4 2.7×; 9B non-commercial | Confirmed (HF API 3.875B params; FP8/NVFP4 repos Apache-2.0) | [S19][S65] |
| 4 | SD-Turbo / SDXL-Turbo under Community Licence; attribution is a distribution duty | Confirmed | [S2][S3][S4] |
| 5 | SD 2.0/2.1 deprecated; SD 2.1 repo 401; SD-Turbo 200 | Confirmed 2026-10-02 | [S7] |
| 6 | Qwen-Image-2.1: 14 Sep 2026, 7.1B, `qwen-research` | Confirmed | [S26][S84] |
| 7 | Z-Image-Turbo Apache-2.0, ~6B, 8 NFE; ≤4 GB via stable-diffusion.cpp | Confirmed | [S25][S37] |
| 8 | Kandinsky 5.0 T2I Lite MIT, 6B, 13 s H100, 100 NFE | Confirmed (corrected from "~50 steps") | [S24] |
| 9 | HiDream-I1-Fast 17B, MIT, Llama 3.1 TE | Confirmed | [S28] |
| 10 | Hyper-SD licence per variant; PCM no licence | Confirmed | [S10][S13] |
| 11 | LCM_Dreamshaper_v7, OpenVINO int8 IR, taesd-ov are MIT | Confirmed | [S11][S34][S59] |
| 12 | Core Ultra 7 255U specs | Confirmed | [S41] |
| 13 | SD.Next medians: 4060L 6.47, 4070L 7.02, 3090 12.95, 4090 18.88, Arc iGPU 0.74 it/s | Confirmed from raw JSON | [S42] |
| 14 | HF LCM-LoRA blog SDXL 4-step timings | Confirmed | [S12] |
| 15 | InsightFace / IP-Adapter-FaceID research-only; PhotoMaker pins insightface | Confirmed | [S32] |
| 16 | Omnibus Reg. (EU) 2026/1744, OJ 24 Jul 2026; Art. 50(2) grace only for pre-2 Aug 2026 systems | Confirmed via legal summaries (EUR-Lex text did not render) | [S47] |
| 17 | Art. 5(1)(ba)/(bb) from 2 Dec 2026; 5(1)(f) emotion recognition in education | Confirmed | [S46] |
| 18 | Code of Practice finalised 10 Jun 2026 with deployer icons | Confirmed | [S48] |
| 19 | Art. 2(6) wording; Art. 2(8) real-world testing not exempt | Confirmed | [S46] |
| 20 | fal.ai prices and US processing | Confirmed (accessed 2026-10-02) | [S51] |
| 21 | Replicate prices | Confirmed (accessed 2026-10-02) | [S52] |
| 22 | DirectML sustained engineering | Confirmed | [S36] |
| 23 | Intel AI Playground hardware list (U-series not listed) | Confirmed | [S40] |
| 24 | OpenVINO GenAI image models; no ControlNet; no SANA; FLUX.2-klein no inpainting | Confirmed 2026-10-02 | [S33] |
| 25 | stable-diffusion.cpp backends and master-929 (27 Sep 2026) | Confirmed | [S37] |
| 26 | FastSD i7-12700 timings | Confirmed | [S38] |
| 27 | RTX 4060/4070 Laptop: 3,072/4,608 CUDA cores, 233/321 AI TOPS, 8 GB GDDR6, 35–115 W | **Confirmed in round 2** on NVIDIA's comparison page | [S77] |
| 28 | EU-US DPF in force | Confirmed; plus *Latombe* upheld 3 Sep 2025, appeal C-703/25 P pending | [S50][S80] |
| 29 | (round 2) FastSD ControlNet runs only in LCM-LoRA (PyTorch) mode — round 1 had implied OpenVINO | **Corrected** | [S63] |
| 30 | (round 2) OpenVINO GenAI ControlNet: GSoC PR closed unmerged | Confirmed | [S61] |
| 31 | (round 2) LCM img2img cost independent of strength; SD-Turbo runs int(steps × strength) | Confirmed in diffusers source and by callback counts | [S60] |
| 32 | (round 2) BFL EU endpoint and FLUX.2-klein pricing | Confirmed (docs.bfl.ai, accessed 2026-10-02) | [S78] |
| 33 | (round 2) ComfyUI has no built-in safety checker | Community sources only (consistent; no official statement found) | [S81] |
