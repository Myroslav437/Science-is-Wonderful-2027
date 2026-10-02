import json, os, sys, numpy as np, torch, open_clip
from PIL import Image
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict
OI = '../data/openimages'
rows = [r for r in json.load(open(f'{OI}/headcrops.json')) if r['attr'] == 'hat' and os.path.exists(f"{OI}/img/{r['image']}.jpg")]
y = np.array([r['label'] for r in rows])
def crop(img, box, up, side):
    w, h = img.size; x0, y0, x1, y1 = box[0]*w, box[1]*h, box[2]*w, box[3]*h; fw, fh = x1-x0, y1-y0
    return img.crop((max(0, x0-side*fw), max(0, y0-up*fh), min(w, x1+side*fw), min(h, y1+0.15*fh)))
model, _, pre = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k'); model.eval(); tok = open_clip.get_tokenizer('ViT-B-32')
imgs = [Image.open(f"{OI}/img/{r['image']}.jpg").convert('RGB') for r in rows]
def enc_t(t):
    with torch.no_grad(): e = model.encode_text(tok(t)); return e / e.norm(dim=-1, keepdim=True)
PROMPTS = {
 'orig': (["a photo of a person wearing a hat", "a photo of a person wearing a cap", "a photo of a person wearing a beanie", "a close-up photo of a head with a hat on it"],
          ["a photo of a person's bare head with visible hair", "a close-up photo of a person's hair", "a photo of a bald head", "a close-up photo of a person's forehead and hair"]),
 'simple': (["a photo of a person wearing a hat"], ["a photo of a person"]),
 'hat_vs_hair': (["a person wearing a hat", "a person wearing a cap", "a person wearing a sun hat", "a person wearing a cowboy hat", "a person wearing a fedora"],
                 ["a person with their hair showing", "a person's face and hair", "a person with short hair", "a person with long hair"]),
}
for up, side in [(0.7, 0.3), (1.2, 0.4), (1.6, 0.6)]:
    cr = [crop(im, r['box'], up, side) for im, r in zip(imgs, rows)]
    with torch.no_grad():
        f = torch.cat([model.encode_image(torch.stack([pre(c) for c in cr[i:i+32]])) for i in range(0, len(cr), 32)]); f = f / f.norm(dim=-1, keepdim=True)
    out = {}
    for k, (p, n) in PROMPTS.items():
        s = ((f @ enc_t(p).T).mean(-1) - (f @ enc_t(n).T).mean(-1)).numpy(); out[k] = round(roc_auc_score(y, s), 3)
    X = f.numpy()
    for C in [0.1, 1.0]:
        pr = cross_val_predict(LogisticRegression(C=C, max_iter=2000), X, y, cv=StratifiedKFold(5, shuffle=True, random_state=0), method='predict_proba')[:, 1]
        out[f'probe_C{C}'] = round(roc_auc_score(y, pr), 3)
    print(f'crop up={up} side={side}:', out, flush=True)
