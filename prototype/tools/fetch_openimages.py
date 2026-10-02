"""Open Images V7 validation subset for hat / glasses zero-shot validation.
Positives: face boxes overlapped by a Hat-family / Glasses-family box in images
where that label is human-verified present. Negatives: faces in images where the
label is human-verified ABSENT (confidence 0). Images with Boy/Girl labels are
skipped (we do not evaluate on minors)."""
import os, csv, io, random, json, time, urllib.request
import pandas as pd
random.seed(1)
D = 'data/openimages'; os.makedirs(D + '/img', exist_ok=True)
def get(url, dst):
    if not os.path.exists(dst):
        for a in range(4):
            try:
                urllib.request.urlretrieve(url, dst + '.part'); os.replace(dst + '.part', dst); return
            except Exception as e:
                print('retry', url, e, flush=True); time.sleep(5)
get('https://openimages.storage.googleapis.com/v7/oidv7-class-descriptions-boxable.csv', D + '/classes.csv')
get('https://openimages.storage.googleapis.com/v5/validation-annotations-human-imagelabels-boxable.csv', D + '/val_labels.csv')
get('https://openimages.storage.googleapis.com/v5/validation-annotations-bbox.csv', D + '/val_bbox.csv')
cls = pd.read_csv(D + '/classes.csv', header=None, names=['id', 'name'])
cid = {n: i for i, n in zip(cls.id, cls.name)}
HAT = [cid[n] for n in ['Hat', 'Sun hat', 'Fedora', 'Cowboy hat', 'Sombrero']]
GLS = [cid[n] for n in ['Glasses', 'Sunglasses']]
MINOR = [cid[n] for n in ['Boy', 'Girl']]
FACE = cid['Human face']
lab = pd.read_csv(D + '/val_labels.csv')
box = pd.read_csv(D + '/val_bbox.csv')
minors = set(lab[(lab.LabelName.isin(MINOR)) & (lab.Confidence == 1)].ImageID)
faces = box[(box.LabelName == FACE) & (box.IsGroupOf == 0) & (box.IsDepiction == 0)]
faces = faces[~faces.ImageID.isin(minors)]
faces = faces[((faces.XMax - faces.XMin) > 0.08)]   # reasonably large faces only

def overlaps(f, b):
    # expanded head region: face box + 60% upward
    h = f.YMax - f.YMin
    x0, x1, y0, y1 = f.XMin, f.XMax, max(0, f.YMin - 0.6 * h), f.YMax
    ix = max(0, min(x1, b.XMax) - max(x0, b.XMin)); iy = max(0, min(y1, b.YMax) - max(y0, b.YMin))
    return ix * iy > 0.3 * (b.XMax - b.XMin) * (b.YMax - b.YMin)

rows = []
for attr, ids in [('hat', HAT), ('glasses', GLS)]:
    present = set(lab[(lab.LabelName.isin(ids)) & (lab.Confidence == 1)].ImageID)
    absent = set(lab[(lab.LabelName.isin(ids)) & (lab.Confidence == 0)].ImageID) - present
    pos, neg = [], []
    attr_boxes = box[box.LabelName.isin(ids)].groupby('ImageID')
    for f in faces[faces.ImageID.isin(present)].itertuples():
        bs = attr_boxes.get_group(f.ImageID) if f.ImageID in attr_boxes.groups else []
        if len(bs) and any(overlaps(f, b) for b in bs.itertuples()):
            pos.append(f)
    neg = list(faces[faces.ImageID.isin(absent)].itertuples())
    random.shuffle(pos); random.shuffle(neg)
    pos, neg = pos[:120], neg[:120]
    print(attr, 'pos', len(pos), 'neg', len(neg), flush=True)
    for label, group in [(1, pos), (0, neg)]:
        for f in group:
            rows.append({'attr': attr, 'label': label, 'image': f.ImageID,
                         'box': [f.XMin, f.YMin, f.XMax, f.YMax]})
json.dump(rows, open(D + '/headcrops.json', 'w'))
ids = sorted({r['image'] for r in rows})
print('images to fetch', len(ids), flush=True)
for i, im in enumerate(ids):
    get(f'https://open-images-dataset.s3.amazonaws.com/validation/{im}.jpg', f'{D}/img/{im}.jpg')
    if i % 50 == 0: print(i, flush=True)
print('OI DONE', flush=True)
