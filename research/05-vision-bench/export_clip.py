import torch, open_clip
for arch, tag, out in [("ViT-B-32","laion2b_s34b_b79k","clip_b32_visual.onnx"),("ViT-B-16-SigLIP2","webli","siglip2_b16_visual.onnx")]:
    m,_,_ = open_clip.create_model_and_transforms(arch, pretrained=tag); m.eval()
    v = m.visual
    x = torch.randn(1,3,224,224)
    torch.onnx.export(v, (x,), out, input_names=["pixel"], output_names=["emb"], opset_version=17, dynamo=False)
    print("exported", out)
