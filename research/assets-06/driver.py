import subprocess, sys, os, json, time
here = os.path.dirname(os.path.abspath(__file__))
py = sys.executable
models = os.path.join(os.path.dirname(here), "models")
which = sys.argv[1]
CONFIGS = {
    "lcm": [
        ("lcm_int8_ov", "t2i", "CPU", "CPU", "CPU", 4),
        ("lcm_int8_ov", "t2i", "CPU", "CPU", "CPU", 2),
        ("lcm_int8_ov", "t2i", "GPU", "GPU", "GPU", 4),
        ("lcm_int8_ov", "t2i", "GPU", "GPU", "GPU", 2),
        ("lcm_int8_ov", "t2i", "CPU", "NPU", "GPU", 4),
        ("lcm_int8_ov", "t2i", "NPU", "NPU", "NPU", 4),
        ("lcm_int8_ov", "i2i", "GPU", "GPU", "GPU", 4, 0.5),
        ("lcm_int8_ov", "i2i", "CPU", "CPU", "CPU", 4, 0.5),
    ],
    "taesd": [
        ("lcm_taesd_ov", "t2i", "GPU", "GPU", "GPU", 4),
        ("lcm_taesd_ov", "t2i", "GPU", "GPU", "GPU", 2),
        ("lcm_taesd_ov", "t2i", "CPU", "CPU", "CPU", 2),
        ("lcm_int8_ov", "t2i", "CPU", "CPU", "CPU", 2),
    ],
    "turbo": [
        ("sdturbo_taesd_ov", "t2i", "GPU", "GPU", "GPU", 1),
        ("sdturbo_ov", "t2i", "GPU", "GPU", "GPU", 1),
        ("sdturbo_taesd_ov", "t2i", "CPU", "NPU", "GPU", 1),
        ("sdturbo_taesd_ov", "i2i", "GPU", "GPU", "GPU", 2, 0.5),
        ("sdturbo_taesd_ov", "t2i", "CPU", "CPU", "CPU", 1),
    ],
}
for c in CONFIGS[which]:
    args = [py, os.path.join(here, "ov_bench.py"), os.path.join(models, c[0])] + [str(x) for x in c[1:]]
    t = time.time()
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=1200)
        line = [l for l in p.stdout.splitlines() if l.startswith("RESULT ")]
        print(line[-1] if line else f"NORESULT {c} rc={p.returncode} err={p.stderr[-600:]}", flush=True)
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT {c} after {time.time()-t:.0f}s", flush=True)
