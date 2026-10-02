import time, statistics, torch, open_clip, cv2, sys
from PIL import Image
pil = Image.open("models/zidane.jpg").convert("RGB")
for arch, tag in [("ViT-B-32", "laion2b_s34b_b79k"), ("ViT-B-16-SigLIP2", "webli")]:
    model, _, pre = open_clip.create_model_and_transforms(arch, pretrained=tag); model.eval()
    x = pre(pil).unsqueeze(0)
    for th in [2, 4, 8, 12]:
        torch.set_num_threads(th)
        with torch.inference_mode():
            for _ in range(3): model.encode_image(x)
            ts=[]
            for _ in range(15):
                t=time.perf_counter(); model.encode_image(x); ts.append((time.perf_counter()-t)*1000)
        print(f"{arch} threads={th}: median {statistics.median(ts):.0f} ms, min {min(ts):.0f} ms", flush=True)
