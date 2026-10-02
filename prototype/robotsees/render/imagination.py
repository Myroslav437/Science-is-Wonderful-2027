"""The robot's imagination: a generated picture made ONLY from words.

The image generator never sees a camera frame. It receives a prompt assembled
from a closed phrase list, and only for slots the robot is "sure" or "thinks"
about. The character is a cartoon robot friend, not a human portrait, so the
generator cannot invent a face, skin tone, gender or age for the visitor.
The prompt words are shown next to the picture: they are its full explanation.

Backend: SD-Turbo (Stability AI, 1-2 steps) via diffusers. ~20-35 s per 512 px
image on the dev laptop CPU; well under 1 s on a mid-range NVIDIA GPU.
"""
from __future__ import annotations

import base64
import io

BASE = ("a cute friendly cartoon robot character, children's picture book illustration, "
        "simple rounded shapes, soft crayon texture, plain light background")

PHRASES = {
    "shirt": lambda v: f"wearing {'an' if v[0] in 'aeiou' else 'a'} {v} t-shirt",
    "glasses": lambda v: "wearing round glasses" if v == "glasses" else None,
    "animal": lambda v: f"with a small friendly pet {v}",
    "colour": lambda v: f"{v} background",
    "energy": lambda v: {"still": "standing calmly", "moving": "waving hello", "very active": "jumping happily"}[v],
    "voice": lambda v: {"quiet": "whispering", "normal": None, "loud": "singing loudly"}[v],
}
ORDER = ("shirt", "glasses", "energy", "voice", "animal", "colour")


def prompt_from_snapshot(snap: dict, min_level=("sure", "think")) -> tuple[str, list[str]]:
    words = []
    for slot in ORDER:
        s = snap["slots"][slot]
        if s["certainty"] in min_level:
            phrase = PHRASES[slot](s["best"])
            if phrase:
                words.append(phrase)
    prompt = BASE + (", " + ", ".join(words) if words else ", with a big question mark")
    return prompt, words


XMP = ('<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?><x:xmpmeta xmlns:x="adobe:ns:meta/">'
       '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description '
       'xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/" '
       'Iptc4xmpExt:DigitalSourceType="http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia"/>'
       '</rdf:RDF></x:xmpmeta><?xpacket end="w"?>')


def save_marked(img, fp, prompt: str, quality: int = 82) -> None:
    """JPEG with machine-readable 'AI-generated' marking (AI Act Art. 50(2)):
    IPTC DigitalSourceType=trainedAlgorithmicMedia in XMP + EXIF description."""
    exif = img.getexif()
    exif[0x010E] = "AI-generated image (SD-Turbo). Made only from these words: " + prompt
    exif[0x0131] = "robotsees prototype (TUAI)"
    img.convert("RGB").save(fp, "JPEG", quality=quality, exif=exif.tobytes(), xmp=XMP.encode())


class Imagination:
    def __init__(self, model: str = "stabilityai/sd-turbo", device: str = "cpu", steps: int = 2,
                 size: int = 512):
        import torch
        from diffusers import AutoPipelineForText2Image
        self.torch = torch
        dtype = torch.float16 if device == "cuda" else torch.float32
        self.pipe = AutoPipelineForText2Image.from_pretrained(model, torch_dtype=dtype).to(device)
        self.pipe.set_progress_bar_config(disable=True)
        self.steps, self.size = steps, size

    def draw(self, prompt: str, seed: int = 7):
        g = self.torch.Generator().manual_seed(seed)
        return self.pipe(prompt, num_inference_steps=self.steps, guidance_scale=0.0,
                         height=self.size, width=self.size, generator=g).images[0]

    def draw_for(self, snap: dict, seed: int = 7) -> dict:
        prompt, words = prompt_from_snapshot(snap)
        img = self.draw(prompt, seed)
        buf = io.BytesIO()
        save_marked(img, buf, prompt)
        return {"img": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(),
                "prompt": prompt, "words": words, "pil": img}
