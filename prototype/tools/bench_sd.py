import time, json, torch
from diffusers import AutoPipelineForText2Image, AutoPipelineForImage2Image
torch.set_num_threads(12)
res={}
t=time.time()
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sd-turbo", torch_dtype=torch.float32)
pipe.set_progress_bar_config(disable=True)
res['load_s']=round(time.time()-t,1)
prompt="a friendly cartoon robot-dog's drawing of a child wearing a red striped shirt and a yellow hat, crayon style, white background"
g=torch.Generator().manual_seed(7)
pipe(prompt, num_inference_steps=1, guidance_scale=0.0, height=512, width=512, generator=g)
for steps in [1,2]:
    t=time.time(); im=pipe(prompt, num_inference_steps=steps, guidance_scale=0.0, height=512, width=512, generator=torch.Generator().manual_seed(7)).images[0]; res[f't2i_512_{steps}step_s']=round(time.time()-t,2)
    im.save(f'scratch/sdturbo_{steps}.png')
i2i = AutoPipelineForImage2Image.from_pipe(pipe)
t=time.time(); im2=i2i(prompt.replace('red','blue'), image=im, num_inference_steps=2, strength=0.5, guidance_scale=0.0, generator=torch.Generator().manual_seed(7)).images[0]; res['i2i_512_2step_s0.5_s']=round(time.time()-t,2)
im2.save('scratch/sdturbo_i2i.png')
print(res); json.dump(res, open('scratch/bench_sd.json','w'))
