"""Scan Seamless Interaction transcripts (naturalistic/dev) for our closed lexicon words."""
import json, os, sys, time, urllib.request, pandas as pd
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'prototype')
from robotsees.perception.lexicon import find_keywords
B = 'https://dl.fbaipublicfiles.com/seamless_interaction'
D = 'data/seamless/transcripts'; os.makedirs(D, exist_ok=True)
fl = pd.read_csv('data/seamless/filelist.csv')
ids = fl[(fl.label == 'naturalistic') & (fl.split == 'dev')].file_id.tolist()[:600]
def get(fid):
    dst = f'{D}/{fid}.jsonl'
    if not os.path.exists(dst):
        try: urllib.request.urlretrieve(f'{B}/naturalistic/dev/metadata/transcript/{fid}.jsonl', dst)
        except Exception as e: return fid, None
    return fid, dst
with ThreadPoolExecutor(8) as ex: res = list(ex.map(get, ids))
hits = []
for fid, p in res:
    if not p: continue
    for line in open(p, encoding='utf-8'):
        seg = json.loads(line)
        words = seg.get('words') or []
        ws = [(w.get('word', ''), w.get('start', 0), w.get('end', 0), w.get('score', 1)) for w in words] if words else [(seg.get('transcript', ''), seg.get('start', 0), seg.get('end', 0), 1)]
        for slot, val, spoken, start, prob in find_keywords(ws, 'en'):
            hits.append({'file_id': fid, 'slot': slot, 'value': val, 'word': spoken, 'start': start,
                         'seg_start': seg.get('start'), 'seg_end': seg.get('end'), 'text': seg.get('transcript', '')[:160]})
print('transcripts', sum(1 for _, p in res if p), 'hits', len(hits))
json.dump(hits, open('data/seamless/keyword_hits.json', 'w'), indent=1)
df = pd.DataFrame(hits); print(df.groupby(['slot', 'value']).size()); print(df.groupby('file_id').size().sort_values(ascending=False).head(15))
print(open(res[0][1], encoding='utf-8').readline()[:600])
