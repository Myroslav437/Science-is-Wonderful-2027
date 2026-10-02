# Data and model files not stored in this repository

Three local folders are left out of git:

| Folder | Size | Why it is excluded |
|---|---|---|
| `.venv/` | about 2.4 GB | Platform-specific Python environment |
| `models/` | about 5.8 GB | Re-downloadable model weights and the OpenVINO compile cache |
| `data/` | about 1.7 GB | Re-downloadable public dataset subsets, with unpixelated recordings of real people |

Together they would also go far beyond GitHub's free LFS quota.

Everything the exhibition screen needs is in the repo:

- `prototype/demo/sessions/*.json`: pixelated frames, beliefs, explanations and imagination images;
- `prototype/demo/audio/*.mp3`: the visitors' voices;
- `prototype/experiments/results/`: all results and figures.

## Re-create the environment

```bash
python -m uv venv --python 3.12 .venv
python -m uv pip install --python .venv/Scripts/python.exe -r prototype/requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu
.venv/Scripts/python.exe -m playwright install chromium
```

## Re-download data (run from the project root)

| Command | What it fetches | Licence |
|---|---|---|
| `python prototype/tools/fetch_seamless.py` | The 6 prototype visitors (video + audio, about 700 MB) and the dataset file list | Seamless Interaction, Meta 2025, CC BY-NC 4.0 |
| `python prototype/tools/fetch_data.py` | Lombard GRID subset (192 utterances, used for the audio evaluation and the crowd-babble noise) and a few RAVDESS trials. It uses HTTP range requests, so no full zips are downloaded | GRID: CC BY 4.0; RAVDESS: CC BY-NC-SA 4.0 |
| `python prototype/tools/fetch_openimages.py` | Open Images V7 validation head crops for the glasses/hat calibration (adults only) | Annotations CC BY 4.0, images CC BY 2.0 |
| `python prototype/tools/scan_seamless.py` | Seamless transcripts searched for the robot's word list (how the visitors were chosen) | as above |
| `python prototype/tools/scan_accessories.py` | Partial downloads used to find participants wearing glasses | as above |

## Re-download models

`python prototype/tools/fetch_models.py` fetches:

- LCM-Dreamshaper v7 (OpenVINO int8) and TAESD, for the robot's imagination;
- the Piper voice used in the demo video.

The following download themselves on first use:

- CLIP ViT-B/32, faster-whisper `small`, SD-Turbo and Silero VAD go into the Hugging Face and torch caches;
- the MediaPipe files are already in `prototype/models/`.

## Then rebuild (from `prototype/`)

```bash
python experiments/build_sessions.py        # about 5-8 min per visitor on a laptop CPU
python experiments/build_visitor_audio.py
python experiments/build_imagination.py
python experiments/analyze_ablation.py
python video/render_video.py
```
