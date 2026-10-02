"""Download the 6 prototype visitors (video + audio) from Seamless Interaction.

Meta's Seamless Interaction dataset (2025), CC BY-NC 4.0, naturalistic/dev split,
served per file from dl.fbaipublicfiles.com. File ids come from
prototype/experiments/visitors.json. Also fetches the dataset's filelist.csv
(needed by scan_seamless.py / scan_accessories.py).

Run from the project root:  python prototype/tools/fetch_seamless.py
Writes data/seamless/{video,audio}/<file_id>.{mp4,wav} and data/seamless/filelist.csv
"""
import json
import os
import urllib.request

BASE = "https://dl.fbaipublicfiles.com/seamless_interaction/naturalistic/dev"
FILELIST = "https://raw.githubusercontent.com/facebookresearch/seamless_interaction/main/assets/filelist.csv"
OUT = os.path.join("data", "seamless")


def get(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    urllib.request.urlretrieve(url, dst + ".part")
    os.replace(dst + ".part", dst)
    print("downloaded", dst, os.path.getsize(dst) // 1_000_000, "MB", flush=True)


def main():
    get(FILELIST, os.path.join(OUT, "filelist.csv"))
    visitors = json.load(open(os.path.join("prototype", "experiments", "visitors.json"), encoding="utf-8"))["visitors"]
    for v in visitors:
        get(f"{BASE}/video/{v['file']}.mp4", os.path.join(OUT, "video", v["file"] + ".mp4"))
        get(f"{BASE}/audio/{v['file']}.wav", os.path.join(OUT, "audio", v["file"] + ".wav"))


if __name__ == "__main__":
    main()
