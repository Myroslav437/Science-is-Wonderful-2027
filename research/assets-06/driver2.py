import subprocess, sys, os, time
here = os.path.dirname(os.path.abspath(__file__))
models = os.path.join(os.path.dirname(here), "models")
py = sys.executable
which = sys.argv[1]
C = {
    "gpu": [
        ("sdturbo_taesd_ov", "t2i", "GPU", 1, 1.0),
        ("sdturbo_taesd_ov", "hyb", "GPU", 2, 0.5),
        ("sdturbo_taesd_ov", "hyb", "GPU", 4, 0.5),
        ("sdturbo_taesd_ov", "hyb", "GPU", 4, 0.7),
        ("lcm_taesd_ov", "t2i", "GPU", 4, 1.0),
        ("lcm_taesd_ov", "hyb", "GPU", 4, 0.5),
        ("lcm_taesd_ov", "hyb", "GPU", 4, 0.7),
        ("lcm_taesd_ov", "hyb", "GPU", 6, 0.7),
    ],
    "sweep": [
        ("lcm_taesd_ov", "hyb", "GPU", 4, 0.6),
        ("lcm_taesd_ov", "hyb", "GPU", 3, 0.7),
        ("sdturbo_taesd_ov", "hyb", "GPU", 4, 0.9),
    ],
    "cpu": [
        ("sdturbo_taesd_ov", "t2i", "CPU", 1, 1.0),
        ("sdturbo_taesd_ov", "hyb", "CPU", 4, 0.7),
        ("lcm_taesd_ov", "t2i", "CPU", 4, 1.0),
        ("lcm_taesd_ov", "hyb", "CPU", 4, 0.7),
        ("lcm_int8_ov", "t2i", "CPU", 4, 1.0),
    ],
}
for c in C[which]:
    args = [py, os.path.join(here, "bench2.py"), os.path.join(models, c[0])] + [str(x) for x in c[1:]] + [os.environ.get("TAG", "")]
    t = time.time()
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=1500)
        line = [l for l in p.stdout.splitlines() if l.startswith("RESULT ")]
        print(line[-1] if line else f"NORESULT {c} rc={p.returncode} err={p.stderr[-600:]}", flush=True)
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT {c} after {time.time()-t:.0f}s", flush=True)
