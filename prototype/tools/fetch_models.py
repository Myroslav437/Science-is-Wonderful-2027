"""Download the local model files that are not kept in git (models/).

  models/ov/lcm_taesd   LCM-Dreamshaper v7 int8 for OpenVINO (MIT) with the TAESD
                        decoder/encoder swapped in (MIT) - the robot's imagination
  models/tts/           Piper voice en_US-amy-medium - the robot's voice in the video

CLIP, Whisper, SD-Turbo and Silero download themselves into the Hugging Face /
torch caches on first use; the MediaPipe .task/.tflite files are kept in
prototype/models/.

Run from the project root:  python prototype/tools/fetch_models.py
"""
import os
import shutil
import urllib.request

from huggingface_hub import snapshot_download

OV = os.path.join("models", "ov")
TTS = os.path.join("models", "tts")
PIPER = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/"


def main():
    lcm = snapshot_download("OpenVINO/LCM_Dreamshaper_v7-int8-ov", local_dir=os.path.join(OV, "lcm_dreamshaper_v7_int8"))
    taesd = snapshot_download("rupeshs/taesd-ov", local_dir=os.path.join(OV, "taesd"))
    target = os.path.join(OV, "lcm_taesd")
    if not os.path.exists(target):
        shutil.copytree(lcm, target)
        for part in ("vae_decoder", "vae_encoder"):
            shutil.rmtree(os.path.join(target, part), ignore_errors=True)
            shutil.copytree(os.path.join(taesd, part), os.path.join(target, part))
    os.makedirs(TTS, exist_ok=True)
    for f in ("en_US-amy-medium.onnx", "en_US-amy-medium.onnx.json"):
        dst = os.path.join(TTS, f)
        if not os.path.exists(dst):
            urllib.request.urlretrieve(PIPER + f, dst)
    print("models ready in", os.path.abspath("models"))


if __name__ == "__main__":
    main()
