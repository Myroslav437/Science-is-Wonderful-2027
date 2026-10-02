"""Fetch small, balanced subsets via HTTP range requests (no full-zip downloads)."""
import os, re, random, time, sys
from remotezip import RemoteZip
ROOT = 'data'
random.seed(0)

def fetch(url, wanted, outdir):
    os.makedirs(outdir, exist_ok=True)
    for attempt in range(5):
        try:
            with RemoteZip(url) as z:
                for n in wanted:
                    dst = os.path.join(outdir, os.path.basename(n))
                    if os.path.exists(dst) and os.path.getsize(dst) > 0: continue
                    with open(dst + '.part', 'wb') as f: f.write(z.read(n))
                    os.replace(dst + '.part', dst)
                    time.sleep(0.2)
            return
        except Exception as e:
            print('retry', attempt, e, flush=True); time.sleep(10 * (attempt + 1))

# ---- Lombard GRID: 12 talkers x 4 colours x {plain, lombard} x 2 = 192 clips (audio + front video)
G = 'https://zenodo.org/records/3736465/files/lombardgrid_{}.zip?download=1'
with RemoteZip(G.format('front')) as z:
    names = [n for n in z.namelist() if n.endswith('.mov')]
by = {}
for n in names:
    m = re.match(r'.*/s(\d+)_([lp])_(\w{6})\.mov', n)
    if m: by.setdefault((int(m[1]), m[2], m[3][1]), []).append(m[3])
talkers = sorted({k[0] for k in by})
pick_t = random.sample(talkers, 12)
sel = []
for t in pick_t:
    for cond in 'lp':
        for col in 'bgrw':
            codes = sorted(by.get((t, cond, col), []))
            sel += [f's{t}_{cond}_{c}' for c in random.sample(codes, min(2, len(codes)))]
print('GRID clips:', len(sel), 'talkers', pick_t, flush=True)
fetch(G.format('alignment'), [], ROOT + '/grid')  # placeholder
with RemoteZip(G.format('alignment')) as z:
    al = z.namelist()
print('alignment names sample', al[:3], flush=True)
fetch(G.format('audio'), [f'lombardgrid/audio/{s}.wav' for s in sel], ROOT + '/grid/audio')
fetch(G.format('front'), [f'lombardgrid/front/{s}.mov' for s in sel], ROOT + '/grid/front')
want_al = [n for n in al if any(s in n for s in sel)]
fetch(G.format('alignment'), want_al, ROOT + '/grid/alignment')
print('GRID done', flush=True)

# ---- RAVDESS: 6 actors x AV(01) neutral+calm-normal... only intensity/statement used
R = 'https://zenodo.org/records/1188976/files/Video_Speech_Actor_{:02d}.zip?download=1'
for a in [1, 2, 3, 4, 5, 6]:
    with RemoteZip(R.format(a)) as z:
        av = [n for n in z.namelist() if os.path.basename(n).startswith('01-01-')]
    # both statements, both intensities, repetition 1, three emotion codes as nuisance variety
    want = [n for n in av if re.search(r'01-01-0[1-3]-0[12]-0[12]-01-', os.path.basename(n))]
    fetch(R.format(a), want, ROOT + '/ravdess/av')
    print('RAVDESS actor', a, len(want), flush=True)
print('ALL DONE', flush=True)
