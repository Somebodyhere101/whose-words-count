"""Diagnose why inj2's doc-placement baseline doesn't reproduce: print top next tokens for cases 0-3."""
import sys

import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

from inj2 import DEV, build, cases, encode

dev = sys.argv[1] if len(sys.argv) > 1 else DEV
dt = torch.float32 if dev == "cpu" else torch.bfloat16
print("transformers", transformers.__version__, "torch", torch.__version__, "device", dev, dt)
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-4B", dtype=dt).to(dev).eval()
print("attn impl", model.config._attn_implementation)
C = cases(4, 7)
with torch.no_grad():
    for i, c in enumerate(C):
        text, span = build(c, "doc", True)
        ids, m = encode(tok, text, span)
        lp = torch.log_softmax(model(input_ids=torch.tensor([ids], device=dev)).logits[0, -1].float(), -1)
        top = torch.topk(lp, 5)
        print(i, c["word"], len(ids), [(tok.decode([int(t)]), round(float(v.exp()), 4)) for v, t in zip(top.values, top.indices)])
        if i == 0:
            print(repr(text[-200:]))
