import json, statistics, collections
d = json.load(open("C:/Users/myros/AppData/Local/Temp/claude/c--Users-myros-projects-Science-Is-Wonderful-2027/a8081b5d-514e-41ee-a70c-c9654d0fce7d/scratchpad/sdnext_bench.json", encoding="utf-8"))
mac = [r for r in d if "system:Darwin" in r[4]]
c = collections.Counter(r[6][:60] for r in mac)
print(len(mac)); print(c.most_common(8))
v = []
for r in mac:
    try: v.append(float(r[2].split("/")[0]))
    except: pass
print("mac all: n", len(v), "median", statistics.median(v), "IQR", statistics.quantiles(v, n=4))
print("latest", max(r[1] for r in mac)[:10], "earliest", min(r[1] for r in mac)[:10])
