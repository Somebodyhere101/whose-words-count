"""RNDCTL: is the inj2 random control direction-free? (exploratory; predictions in ../RNDCTL_PRED.md)

Reuses inj2's prompts, hook placement and first-token readout. Adds 16 isotropic random draws at +2 and -2,
the original inj2 draw at +-2, the learned direction at +-2, and an 'inflate' arm that scales the span's
hidden state up to the norm of h + 2r without adding any direction.

Usage: python rndctl.py --dirs ../stage2_Qwen3-4B/directions.pt --layer 17 --out ../rndctl_q4b
"""
import argparse
import json
import os
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

import inj2
from inj2 import DEV, build, cases, encode


class InflateHook:
    """Scale h on masked tokens by sqrt(1 + (norm/||h||)^2): same norm as h + v, no added direction."""

    def __init__(self, model, layer, norm, mask):
        self.norm, self.mask = norm, mask
        self.h = model.model.layers[layer - 1].register_forward_hook(self.fn)

    def fn(self, mod, inp, out):
        h = out[0] if isinstance(out, tuple) else out
        if h.shape[1] == self.mask.shape[1]:
            hn = h.float().norm(dim=-1, keepdim=True)
            f = torch.sqrt(1 + (self.norm / hn) ** 2)
            m = self.mask[..., None].to(h.device)
            h = (h.float() * (1 + m * (f - 1))).to(h.dtype)
        return (h,) + tuple(out[1:]) if isinstance(out, tuple) else h

    def remove(self):
        self.h.remove()


@torch.no_grad()
def inflate_readout(model, tok, c, place, layer, norm):
    text, span = build(c, place, True)
    ids, m = encode(tok, text, span)
    hook = InflateHook(model, layer, norm, m.to(DEV))
    try:
        out = model(input_ids=torch.tensor([ids], device=DEV))
        lp = torch.log_softmax(out.logits[0, -1].float(), -1)
        code_ids = {tok(" " + c["word"], add_special_tokens=False).input_ids[0], tok(c["word"], add_special_tokens=False).input_ids[0]}
        legit_ids = {tok("Summary", add_special_tokens=False).input_ids[0], tok(" Summary", add_special_tokens=False).input_ids[0]}
        return {"p_code": float(sum(lp[t].exp() for t in code_ids)), "p_legit": float(sum(lp[t].exp() for t in legit_ids))}
    finally:
        hook.remove()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3-4B")
    ap.add_argument("--dirs", required=True)
    ap.add_argument("--layer", type=int, required=True)
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--draws", type=int, default=16)
    ap.add_argument("--places", default="doc,asst,sys")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(a.model)
    if os.environ.get("AGP_4BIT") == "1":                     # inj2 on Qwen3-4B ran in 4-bit (PLAN_7DAY.md:146)
        from transformers import BitsAndBytesConfig
        q = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_quant_type="nf4")
        model = AutoModelForCausalLM.from_pretrained(a.model, quantization_config=q, device_map={"": 0}).eval()
    else:
        model = AutoModelForCausalLM.from_pretrained(a.model, dtype=torch.bfloat16).to(DEV).eval()
    vR = torch.load(a.dirs)[a.layer]["vR"].float()
    g = torch.Generator().manual_seed(2000 + a.layer)          # the original inj2 draw
    orig = torch.randn(vR.shape, generator=g)
    orig = orig / orig.norm() * vR.norm()
    g2 = torch.Generator().manual_seed(9100)                   # new draws
    draws = []
    for _ in range(a.draws):
        r = torch.randn(vR.shape, generator=g2)
        draws.append(r / r.norm() * vR.norm())
    C = cases(a.n, 7)
    res, t0 = {}, time.time()
    run = lambda p, v: [inj2.readout(model, tok, c, p, (a.layer, v)) for c in C]
    for p in a.places.split(","):
        res[f"{p}_base"] = [inj2.readout(model, tok, c, p) for c in C]
        for s in (2.0, -2.0):
            res[f"{p}_dir_{s:+g}"] = run(p, s * vR)
            res[f"{p}_orig_{s:+g}"] = run(p, s * orig)
            for i, r in enumerate(draws):
                res[f"{p}_rnd{i:02d}_{s:+g}"] = run(p, s * r)
        res[f"{p}_inflate"] = [inflate_readout(model, tok, c, p, a.layer, float(2 * vR.norm())) for c in C]
        m = lambda k: sum(x["p_code"] for x in res[k]) / len(res[k])
        print(p, "base", round(m(f"{p}_base"), 3), "dir+2", round(m(f"{p}_dir_+2"), 3), "orig+2", round(m(f"{p}_orig_+2"), 3),
              "orig-2", round(m(f"{p}_orig_-2"), 3), "inflate", round(m(f"{p}_inflate"), 3),
              f"[{time.time() - t0:.0f}s]", flush=True)
        json.dump({"model": a.model, "layer": a.layer, "n": a.n, "draws": a.draws, "res": res},
                  open(os.path.join(a.out, "rndctl.json"), "w"))


if __name__ == "__main__":
    main()
