"""CPU latency of tiny VLMs (transformers, fp32, greedy) on the dev laptop."""
import os, sys, time, torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForImageTextToText

HERE = os.path.dirname(os.path.abspath(__file__))
img = Image.open(os.path.join(HERE, "models", "zidane.jpg")).convert("RGB")
print("torch", torch.__version__, "threads", torch.get_num_threads(), flush=True)
for mid in sys.argv[1:] or ["HuggingFaceTB/SmolVLM2-256M-Video-Instruct", "HuggingFaceTB/SmolVLM2-500M-Video-Instruct"]:
    try:
        t0 = time.perf_counter()
        proc = AutoProcessor.from_pretrained(mid)
        model = AutoModelForImageTextToText.from_pretrained(mid, dtype=torch.float32).eval()
        print(f"{mid}: load {time.perf_counter()-t0:.1f}s", flush=True)
        msgs = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": "Describe the clothing of the people in one sentence."}]}]
        prompt = proc.apply_chat_template(msgs, add_generation_prompt=True)
        inp = proc(text=prompt, images=[img], return_tensors="pt")
        print("   input tokens:", inp["input_ids"].shape[1], flush=True)
        for run in range(3):
            t = time.perf_counter()
            with torch.inference_mode():
                out = model.generate(**inp, max_new_tokens=40, do_sample=False)
            dt = time.perf_counter() - t
            n_new = out.shape[1] - inp["input_ids"].shape[1]
            txt = proc.batch_decode(out[:, inp["input_ids"].shape[1]:], skip_special_tokens=True)[0]
            print(f"   run{run}: {dt:.2f}s for {n_new} new tokens -> {txt!r}", flush=True)
    except Exception as e:
        print("FAIL", mid, repr(e)[:400], flush=True)
