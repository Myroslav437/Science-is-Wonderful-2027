import time, os, json, numpy as np, torch
from PIL import Image
torch.set_num_threads(12)
res = {}
img = Image.fromarray((np.random.rand(480,640,3)*255).astype('uint8'))

# CLIP / SigLIP zero-shot via open_clip
import open_clip
for name, pre in [('ViT-B-32','laion2b_s34b_b79k'), ('ViT-B-16-SigLIP2','webli')]:
    try:
        t=time.time(); m,_,p = open_clip.create_model_and_transforms(name, pretrained=pre); tok=open_clip.get_tokenizer(name); m.eval(); load=time.time()-t
        x=p(img).unsqueeze(0); txt=tok(["a photo of a person wearing a hat"]*20)
        with torch.no_grad():
            m.encode_image(x); m.encode_text(txt)
            t=time.time()
            for _ in range(5): m.encode_image(x)
            ti=(time.time()-t)/5
            t=time.time(); m.encode_text(txt); tt=time.time()-t
        res[name]={'load_s':round(load,1),'image_ms':round(ti*1000),'text20_ms':round(tt*1000)}
    except Exception as e: res[name]=str(e)[:200]
    print(name, res[name], flush=True)

# faster-whisper
from faster_whisper import WhisperModel
audio = (np.random.randn(16000*10)*0.01).astype('float32')
for size in ['base','small']:
    try:
        t=time.time(); wm=WhisperModel(size, device='cpu', compute_type='int8', cpu_threads=12); load=time.time()-t
        t=time.time(); segs,info=wm.transcribe(audio, language='en', beam_size=1, vad_filter=False); list(segs); tr=time.time()-t
        res['whisper_'+size]={'load_s':round(load,1),'10s_audio_s':round(tr,2)}
    except Exception as e: res['whisper_'+size]=str(e)[:200]
    print(size, res['whisper_'+size], flush=True)
json.dump(res, open('scratch/bench_models.json','w'), indent=1)
