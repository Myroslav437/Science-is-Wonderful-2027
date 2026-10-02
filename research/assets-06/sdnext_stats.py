import json, re, statistics, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
def first(s):
    try: return float(s.split("/")[0])
    except: return None
pats = {
 "Apple M1 (base)": r"device:.*\bM1\b(?!\s*(Pro|Max|Ultra))",
 "Apple M1 Pro/Max": r"device:.*\bM1 (Pro|Max)",
 "Apple M2 (base)": r"device:.*\bM2\b(?!\s*(Pro|Max|Ultra))",
 "Apple M2 Pro/Max": r"device:.*\bM2 (Pro|Max)",
 "Apple M3 (any)": r"device:.*\bM3\b",
 "Apple M4 (any)": r"device:.*\bM4\b",
 "RTX 3060 Laptop": r"device:.*RTX 3060 Laptop",
 "RTX 4060 Laptop": r"device:.*RTX 4060 Laptop",
 "RTX 4070 Laptop": r"device:.*RTX 4070 Laptop",
 "RTX 4080 Laptop": r"device:.*RTX 4080 Laptop",
 "RTX 5060 Laptop": r"device:.*RTX 5060 Laptop",
 "RTX 5070 Laptop": r"device:.*RTX 5070 Laptop",
 "RTX 5070 Ti Laptop": r"device:.*RTX 5070 Ti Laptop",
 "Intel Arc iGPU (Core Ultra)": r"device:.*Intel\(R\) Arc\(TM\) Graphics",
 "Intel Graphics (generic)": r"device:Intel\(R\) Graphics",
}
for name, p in pats.items():
    rx = re.compile(p)
    v = []; dates = []
    for r in d:
        dev = r[6] if len(r) > 6 else ""
        if not rx.search(dev): continue
        if "width:512 height:512" not in (r[8] if len(r) > 8 else ""): continue
        x = first(r[2])
        if x: v.append(x); dates.append(r[1][:10])
    if v:
        q = statistics.quantiles(v, n=4) if len(v) > 3 else [min(v), statistics.median(v), max(v)]
        print(f"{name:30s} n={len(v):4d} median={statistics.median(v):6.2f} it/s IQR={q[0]:.2f}-{q[2]:.2f} latest={max(dates)}")
    else:
        print(f"{name:30s} n=0")
print("total rows", len(d), "latest", max(r[1] for r in d)[:10])
