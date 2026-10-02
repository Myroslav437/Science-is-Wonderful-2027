"""Does Layer B (iGPU) slow down perception (CPU), and vice versa? Run with the ovenv python."""
import subprocess, sys, os, time, json, statistics
here = os.path.dirname(os.path.abspath(__file__))
models = os.path.join(os.path.dirname(here), "models")
OVPY = sys.executable
PROJPY = r"C:\Users\myros\projects\Science Is Wonderful 2027\.venv\Scripts\python.exe"
PDUR = 40


def perception(tag):
    p = subprocess.run([PROJPY, os.path.join(here, "perc_load.py"), str(PDUR), tag], capture_output=True, text=True, timeout=900)
    line = [l for l in p.stdout.splitlines() if l.startswith("PERC ")]
    if not line:
        print("PERC-ERR rc=", p.returncode, "stdout:", p.stdout[-400:], "stderr:", p.stderr[-800:], flush=True); return None
    return json.loads(line[-1][5:])


def with_gen(model, steps, strength, tag):
    flag = os.path.join(here, f"stop_{tag}.flag")
    if os.path.exists(flag):
        os.remove(flag)
    g = subprocess.Popen([OVPY, os.path.join(here, "gen_loop.py"), os.path.join(models, model), "GPU", str(steps), str(strength), "900", tag],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        l = g.stdout.readline()
        if not l or l.startswith("READY"):
            break
    time.sleep(25)  # gen-only window first
    spawn = time.time()
    pr = perception(tag)
    time.sleep(20)  # gen-only window after perception ends
    open(flag, "w").close()
    out, err = g.communicate(timeout=900)
    if pr is None:
        print("PERC-NONE", tag, flush=True); return
    line = [l for l in out.splitlines() if l.startswith("GEN ")]
    if not line:
        print("GEN-ERR", err[-800:], flush=True); return
    gr = json.loads(line[-1][4:])
    runs = gr["runs"]
    w0, w1 = pr["w0"], pr["w1"]
    alone = [b - a for a, b in runs if b < spawn or a > w1 + 0.5]   # before perception process existed / after it ended
    overl = [b - a for a, b in runs if a >= w0 and b <= w1]         # fully inside the perception measurement loop
    res = dict(tag=tag, model=model, steps=steps, strength=strength,
               gen_alone_mean_s=round(statistics.mean(alone), 3) if alone else None, n_alone=len(alone),
               gen_with_perception_mean_s=round(statistics.mean(overl), 3) if overl else None, n_overlap=len(overl),
               perception=pr)
    print("CONC " + json.dumps(res), flush=True)
    with open(os.path.join(here, "results2.jsonl"), "a") as fh:
        fh.write(json.dumps(res) + "\n")


base = perception("perception_alone_r2a")
print("BASE " + json.dumps(base), flush=True)
with_gen("lcm_taesd_ov", 3, 0.7, "conc_lcm_r2")
with_gen("sdturbo_taesd_ov", 4, 0.9, "conc_sdturbo_r2")
base = perception("perception_alone_r2b")
print("BASE " + json.dumps(base), flush=True)
