"""Second diagnostic: does the attention implementation change the doc baseline? Also a context-dependence sanity check."""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from inj2 import build, cases, encode

tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-4B")
C = cases(4, 7)
probe = ("<|im_start|>user\nMy cat is called Wobbleton. What is my cat called? Answer with the name only.<|im_end|>\n"
         "<|im_start|>assistant\n<think>\n\n</think>\n\n")
for impl in ("eager", "sdpa"):
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-4B", dtype=torch.bfloat16, attn_implementation=impl).to("cuda").eval()
    with torch.no_grad():
        ids = tok(probe, add_special_tokens=False).input_ids
        out = model.generate(torch.tensor([ids], device="cuda"), max_new_tokens=8, do_sample=False)
        print(impl, "probe:", repr(tok.decode(out[0, len(ids):])))
        for i, c in enumerate(C):
            text, span = build(c, "doc", True)
            ids, _ = encode(tok, text, span)
            lp = torch.log_softmax(model(input_ids=torch.tensor([ids], device="cuda")).logits[0, -1].float(), -1)
            code = tok(c["word"], add_special_tokens=False).input_ids[0]
            print(impl, i, "p_code", round(float(lp[code].exp()), 4), "p_summary", round(float(lp[tok("Summary", add_special_tokens=False).input_ids[0]].exp()), 4))
            if i == 1:
                g = model.generate(torch.tensor([ids], device="cuda"), max_new_tokens=30, do_sample=False)
                print("   gen:", repr(tok.decode(g[0, len(ids):])))
    del model
    torch.cuda.empty_cache()
