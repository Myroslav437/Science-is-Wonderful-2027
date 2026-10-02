# robotsees: "How does a robot see you?" prototype

A working software prototype of the exhibit. The full chain runs with real models on real recordings of real people:

camera + microphone → perception → evidence memory → sensor fusion → representation → explanations → avatar and optional generated image

It runs entirely offline on a laptop CPU, with no GPU and no cloud.

## What is real, simulated, or still to build

| Part | Status in this prototype |
|---|---|
| Camera perception: face box, body pose, clothes colour, glasses, movement | **Real.** MediaPipe face detector and pose landmarker, CLIP ViT-B/32 with Platt calibration on Open Images, k-means in CIELAB, run on real video. |
| Microphone perception: speech detection, speech recognition, closed word list, loudness | **Real.** Silero VAD, faster-whisper `small` (multilingual), EN/FR/NL/DE/PL lexicon, run on real audio. |
| Evidence memory, sensor fusion, uncertainty | **Real.** Implemented and unit-tested (`tests/`). |
| Explanations: clue balance (exact Shapley), what-if per sensor configuration, evidence cards, certainty words, template sentences | **Real.** Faithfulness is unit-tested: clues = Shapley = leave-one-sensor-out = sum of evidence cards. |
| Sensor switches | **Real in software.** A switched-off sensor's evidence is never used (marginalisation). In live mode, frames and samples are dropped before any model sees them. The physical switch box is not built yet. |
| "Noisy room" and "foggy lens" | **Simulated.** Crowd babble mixed in at 0 dB SNR (from Lombard GRID talkers); blur, darkening and sensor noise on the frames. |
| Visitors | **Real people from public datasets, not children.** Six adults from Seamless Interaction (Meta 2025, CC BY-NC 4.0). They talk freely; they are not answering our robot's questions. Faces are pixelated on screen. |
| Robot body, robot voice, robot questions | **Simulated.** An illustrated robot on screen; robot lines use the offline Piper TTS voice. |
| Robot's imagination image | **Real** SD-Turbo on CPU (about 20–35 s per image here). Its prompt is built only from the words the robot is sure about, never from a camera image. Each image carries machine-readable "AI-generated" metadata. |
| Live mode: webcam or PiDog MJPEG stream + microphone | **Real code, tested on recordings only.** Not yet tested with a real webcam or a PiDog. |
| Robot integration (PiDog SDK poses, LEDs, sensor gating on the Pi), physical switch box, close-talk mic, card printer, multilingual robot voice, engagement detection | **To be built for the exhibit.** See `docs/02_architecture.md`. |

## Layout

```
robotsees/
  config.py          6 child-safe slots, sensor relevance, the "never guess" list
  fusion.py          Observation, EvidenceMemory, tempered log-opinion-pool fusion, clues, Shapley
  xai.py             per-slot explanations, evidence ranking, counterfactuals, snapshot()
  perception/
    vision.py        camera -> observations (no identity, age, gender, emotion, skin, hair or headwear)
    audio.py         microphone -> observations (only closed-vocabulary words leave this module)
    lexicon.py       EN/FR/NL/DE/PL colour and animal words, language-aware
  session.py         run a recording through the pipeline; pixelated robot's-eye frames
  ui_export.py       compact session JSON for the exhibition screen
  render/imagination.py   SD-Turbo "robot's imagination" + AI-generated marking
experiments/
  calibrate_vision.py   glasses/hat zero-shot calibration on Open Images (results/vision_calibration.json)
  eval_audio_grid.py    colour words + loudness on Lombard GRID, clean vs crowd babble (results/audio_grid.json)
  visitors.json         the 6 prototype visitors, segments and hand-annotated ground truth
  build_sessions.py     visitors x {clean, noisy-ears, foggy-eyes} -> demo/sessions + results/sessions
  build_visitor_audio.py  the visitors' voices for the screen (clean + the noisy-room mix) -> demo/audio/*.mp3
  build_imagination.py  the robot's imagination images (LCM img2img from the avatar, OpenVINO)
  analyze_ablation.py   sensor-configuration ablation table and figures (results/ablation*.*, fig_*.png)
demo/                   exhibition screen (app.html, artifact-compatible; local.html for local use) + sessions/
live/run_live.py        live mode server (camera/PiDog stream + microphone), same UI
video/render_video.py   renders the partner demo video from the real UI (Playwright + Piper TTS + ffmpeg)
tools/                  data download, transcript scan and benchmark scripts (run from the repo root)
tests/                  unit tests (fusion, faithfulness of explanations)
```

## Run it

Python 3.12, CPU only. From the project root:

```bash
python -m uv venv --python 3.12 .venv
python -m uv pip install --python .venv/Scripts/python.exe torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
python -m uv pip install --python .venv/Scripts/python.exe transformers diffusers accelerate open_clip_torch librosa soundfile \
    opencv-python mediapipe faster-whisper silero-vad imageio-ffmpeg playwright remotezip piper-tts sounddevice scikit-learn matplotlib pandas pytest
.venv/Scripts/python.exe -m playwright install chromium
cd prototype
../.venv/Scripts/python.exe -m pytest -q tests
```

1. **Explore the prototype (no models needed).** Serve the demo folder and open the replay player:
   ```bash
   cd prototype/demo && ../../.venv/Scripts/python.exe build_local.py && ../../.venv/Scripts/python.exe -m http.server 8765
   # open http://localhost:8765/local.html
   ```
   Keyboard: E toggles the eyes, H toggles the ears, Space plays or pauses, the arrow keys move 1 s, M mutes the visitor's voice. Press Play to hear the visitor; in the noisy-room variant you hear the crowd mix the robot heard.
2. **Rebuild sessions from the data.** Download the recordings and models first with the scripts in `prototype/tools/` (see `DATA.md` in the repo root), then run `python experiments/build_sessions.py` (about 5–8 min per visitor on a laptop CPU), `python experiments/build_visitor_audio.py`, `python experiments/build_imagination.py` and `python experiments/analyze_ablation.py`.
3. **Live mode on your own camera and microphone.** Nothing is recorded:
   ```bash
   python live/run_live.py --camera 0 --mic default --language en
   # open http://127.0.0.1:8800/local.html#live and switch the eyes and ears on
   # with the PiDog: --camera http://<pidog-ip>:9000/mjpg
   ```
4. **Render the demo video:** `python video/render_video.py`. It writes `video/out/how_does_a_robot_see_you.mp4` and `storyboard.md`.

## Data and licences

- Seamless Interaction (Meta, 2025): CC BY-NC 4.0. Used for the prototype visitors, shown pixelated, non-commercial research and demonstration only.
- Lombard GRID: CC BY 4.0. Used for the audio evaluation and the crowd-babble noise.
- Open Images V7: annotations CC BY 4.0, images CC BY 2.0. Used for glasses/hat calibration; only adult faces were used (images labelled Boy/Girl were excluded); no images are shown.
- Models: MediaPipe (Apache-2.0), OpenCLIP ViT-B/32 LAION-2B (MIT code, model weights per the LAION release), faster-whisper (MIT) with Whisper weights (MIT), Silero VAD (MIT), SD-Turbo (Stability AI Community Licence, 5 Jul 2024: free for research and non-commercial use; show "Powered by Stability AI" and keep the licence notice; its SD 2.1 base was withdrawn from Hugging Face, so mirror the weights), Piper TTS (GPL-3.0 package; voice en_US-amy, see its model card).
- No children's data was used anywhere.
