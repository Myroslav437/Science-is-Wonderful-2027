Micro-benchmarks used for research/04-audio-models.md
Run 2026-10-02 on the dev laptop (Intel Core Ultra 7 255U, 12C/14T, 32 GB, Windows 11, no NVIDIA GPU),
project .venv: Python 3.12, torch 2.14.1+cpu, faster-whisper 1.2.1 (CTranslate2 4.8.2), silero-vad 6.2.3,
librosa 1.0.0, onnxruntime 1.30.0, transformers 5.18.0.

IMPORTANT: other benchmark jobs were running at the same time (Windows reported 100 % CPU load),
so all timings are pessimistic. Re-run on the exhibition machine with vision running concurrently.

Extra packages were installed into separate folders and NOT into the project .venv:
  pylib/   onnx-asr 0.12.0 (pip install --target pylib --no-deps onnx-asr)
  ttslib/  piper-tts 1.8.0 (pip install --target ttslib --no-deps --only-binary=:all: --python-version 3.12 --platform win_amd64 piper-tts)
  voices/  Piper medium voices from https://huggingface.co/rhasspy/piper-voices (+ MODEL_CARD per voice)
  llm/     llama.cpp b11327 win-cpu-x64 (https://github.com/ggml-org/llama.cpp/releases) + Q4_K_M GGUFs

Scripts (expect these folders next to them; data from data/grid = Lombard GRID, CC BY 4.0):
  bench_audio.py  Silero VAD, faster-whisper tiny/base/small/medium/turbo, Parakeet-TDT-0.6B-v3 (onnx-asr int8),
                  librosa pyin/yin/rms, AST AudioSet, multilingual-e5-small     -> bench_audio.json
                  (its CLAP part failed on transformers 5 API; superseded by bench_clap.py)
  bench_clap.py   LAION-CLAP zero-shot prompts on 192 Lombard-GRID utterances    -> bench_clap.json
  bench_piper.py  Piper TTS latency, 5 languages                                  -> bench_piper.json
  bench_llm.txt   llama-bench -t 8 -p 128 -n 48 -r 2 output for 7 small LLMs (Q4_K_M)
Set HF_HUB_OFFLINE=1 once models are cached.
