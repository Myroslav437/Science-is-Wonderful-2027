import torch, open_clip
from PIL import Image
img = Image.open("models/zidane.jpg").convert("RGB")
crops = {"left person (Zidane, no glasses, tie)": img.crop((100, 180, 760, 720)), "right person (Ancelotti, no glasses, tie)": img.crop((740, 30, 1180, 720))}
attrs = {"glasses": ("a photo of a person wearing glasses", "a photo of a person without glasses"),
         "tie": ("a photo of a person wearing a tie", "a photo of a person without a tie"),
         "hat": ("a photo of a person wearing a hat", "a photo of a person with no hat"),
         "backpack": ("a photo of a person carrying a backpack", "a photo of a person without a backpack"),
         "striped shirt": ("a photo of a person wearing a striped shirt", "a photo of a person wearing a plain shirt"),
         "pointing": ("a photo of a person pointing with a finger", "a photo of a person with hands down")}
for arch, tag in [("ViT-B-32", "laion2b_s34b_b79k"), ("ViT-B-16-SigLIP2", "webli")]:
    m, _, pre = open_clip.create_model_and_transforms(arch, pretrained=tag); m.eval(); tok = open_clip.get_tokenizer(arch)
    print("==", arch, "logit_scale", round(float(m.logit_scale.exp()), 1), "bias", (round(float(m.logit_bias), 2) if getattr(m, "logit_bias", None) is not None else None))
    with torch.inference_mode():
        for cname, c in crops.items():
            fi = m.encode_image(pre(c).unsqueeze(0)); fi = fi / fi.norm(dim=-1, keepdim=True)
            row = []
            for a, (pos, neg) in attrs.items():
                ft = m.encode_text(tok([pos, neg])); ft = ft / ft.norm(dim=-1, keepdim=True)
                cos = (fi @ ft.T)[0]
                if getattr(m, "logit_bias", None) is not None:
                    p_sig = torch.sigmoid(cos[0] * m.logit_scale.exp() + m.logit_bias).item()
                    row.append(f"{a}: cos+={cos[0]:.3f} sigmoidP={p_sig:.3f} pair-softmax={torch.softmax(cos*m.logit_scale.exp(),0)[0]:.2f}")
                else:
                    row.append(f"{a}: cos+={cos[0]:.3f} pair-softmax={torch.softmax(cos*m.logit_scale.exp(),0)[0]:.2f}")
            print(" ", cname); [print("     ", r) for r in row]
