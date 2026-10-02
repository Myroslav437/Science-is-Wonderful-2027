"""Find Seamless Interaction participants wearing hats/glasses (sparse download: index + first seconds)."""
import os, sys, json, random, urllib.request, cv2, numpy as np, pandas as pd
sys.path.insert(0, 'prototype')
from robotsees.perception.vision import VisionPerception
B = 'https://dl.fbaipublicfiles.com/seamless_interaction'
D = 'data/seamless/scan'; os.makedirs(D, exist_ok=True)
fl = pd.read_csv('data/seamless/filelist.csv')
ids = fl[(fl.label == 'naturalistic') & (fl.split == 'dev')].file_id.tolist()
random.seed(3); random.shuffle(ids); ids = ids[:160]
def sparse_get(url, dst, head=4_000_000, tail=2_500_000):
    req = urllib.request.Request(url, method='HEAD'); size = int(urllib.request.urlopen(req, timeout=30).headers['Content-Length'])
    with open(dst, 'wb') as f:
        f.truncate(size)
        for a, b in [(0, head - 1), (max(0, size - tail), size - 1)]:
            r = urllib.request.Request(url, headers={'Range': f'bytes={a}-{b}'}); data = urllib.request.urlopen(r, timeout=60).read()
            f.seek(a); f.write(data)
vp = VisionPerception(); out = []
for i, fid in enumerate(ids):
    dst = f'{D}/{fid}.mp4'
    try:
        sparse_get(f'{B}/naturalistic/dev/video/{fid}.mp4', dst)
        cap = cv2.VideoCapture(dst); cap.set(cv2.CAP_PROP_POS_MSEC, 800); ok, bgr = cap.read(); cap.release()
        if not ok: raise RuntimeError('decode')
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        k = 960 / max(rgb.shape[:2]); rgb = cv2.resize(rgb, (int(rgb.shape[1]*k), int(rgb.shape[0]*k)))
        r = vp.analyse_frame(rgb, 0.0)
        rec = {'file_id': fid, 'shape': list(rgb.shape), 'person': r.person,
               'hat': r.scores.get('hat', {}).get('p'), 'glasses': r.scores.get('glasses', {}).get('p'), 'swatch': r.swatch}
        out.append(rec)
        if (rec['hat'] or 0) > 0.75 or (rec['glasses'] or 0) > 0.85:
            cv2.imwrite(f'{D}/{fid}.jpg', cv2.resize(bgr, (int(bgr.shape[1]*480/max(bgr.shape[:2])), int(bgr.shape[0]*480/max(bgr.shape[:2])))))
            print('CANDIDATE', rec, flush=True)
    except Exception as e:
        print('skip', fid, e, flush=True)
    finally:
        try:
            os.remove(dst)
        except OSError:
            pass
json.dump(out, open('data/seamless/accessory_scan.json', 'w'), indent=1)
print('done', len(out))
