import sys, os
import openvino as ov
from transformers import AutoTokenizer
from openvino_tokenizers import convert_tokenizer
d = os.path.join(sys.argv[1], "tokenizer")
tok = AutoTokenizer.from_pretrained(d)
ov_tok, ov_detok = convert_tokenizer(tok, with_detokenizer=True)
ov.save_model(ov_tok, os.path.join(d, "openvino_tokenizer.xml"))
ov.save_model(ov_detok, os.path.join(d, "openvino_detokenizer.xml"))
print("ok", os.listdir(d))
