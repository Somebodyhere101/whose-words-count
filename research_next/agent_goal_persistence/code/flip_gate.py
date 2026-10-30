"""FLIP format gate for gpt-oss-20b, run before any FLIP data (rules in ../FLIP.md). Exits 1 on any failure.

G1 template: the hand-written harmony wrappers (chat_fmt.harmony) render [system prompt, user, assistant, user] plus
   the generation header exactly as tok.apply_chat_template does (date line normalised; the final-channel header is
   the template's '<|start|>assistant' plus '<|channel|>final<|message|>').
G2 probe tokens: the fixed goal text's probed tokens (agp_fast.content_index) are byte-identical in the system,
   developer, user and assistant wrappers, and the four ticker first tokens of a 3-way quarter are distinct.
G3 cache (needs the model): two sequences of different lengths fed in three pieces through BatchLM's left-padded
   cache give the same next-token distribution as one plain forward pass of each sequence (total variation < 0.02).
Usage: python flip_gate.py --model openai/gpt-oss-20b [--no-model]
"""
import argparse
import os
import re
import sys

import torch

os.environ["AGP_WORLD"] = "3way"
import agp_batch as AB
import agp_fast as F
import chat_fmt


class TokOnly(AB.BatchLM):
    def __init__(self, model):
        from transformers import AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(model)
        self.fmt = chat_fmt.harmony(self.tok)
        self.close_str = self.fmt["assistant"][1]


def g1(lm):
    m = [{"role": "system", "content": "SYSX"}, {"role": "user", "content": "USRX"},
         {"role": "assistant", "content": "ASTX"}, {"role": "user", "content": "USR2"}]
    ref = lm.tok.apply_chat_template(m, tokenize=False, add_generation_prompt=True)
    ref = re.sub(r"Current date: \d{4}-\d{2}-\d{2}", "Current date: 2026-10-30", ref)
    w = lm.fmt
    mine = (chat_fmt.render(w, "system", "SYSX", first=True) + chat_fmt.render(w, "user", "USRX")
            + chat_fmt.render(w, "assistant", "ASTX") + chat_fmt.render(w, "user", "USR2"))
    ok = mine + "<|start|>assistant" == ref and w["header"] == "<|start|>assistant<|channel|>final<|message|>"
    print("G1 template", "PASS" if ok else "FAIL")
    if not ok:
        print(repr(mine)), print(repr(ref))
    return ok


def g2(lm):
    toks = {r: [lm.enc(r, F.FIXED_BODY)[i] for i in F.content_index(lm, r, F.FIXED_BODY)]
            for r in ("system", "developer", "user", "assistant")}
    same = all(t == toks["user"] for t in toks.values()) and len(toks["user"]) > 5
    W = F.make_world3(9100, lm.tok)
    distinct = all(len({s["ft"] for s in q["stocks"]}) == 4 for q in W)
    single = all(len(lm.tok(" " + s["t"], add_special_tokens=False).input_ids) >= 1 for q in W for s in q["stocks"])
    print("G2 probe tokens", "PASS" if same else "FAIL", len(toks["user"]), "tokens;", "tickers distinct",
          distinct and single)
    return same and distinct and single


@torch.no_grad()
def g3(model):
    lm = AB.BatchLM(model, 0.7)
    W = F.make_world3(9100, lm.tok)
    a1 = lm.enc("system", F.SYSTEM, first=True)
    for i in range(F.N_HIST):
        lo = min((s for s in W[i]["stocks"] if s["kind"] == "lo"), key=lambda s: s["em"])
        a1 += lm.enc("user", F.quarter_msg(i, W[i])) + lm.enc("assistant", f"ALLOCATE: {lo['t']}")
    b1 = lm.enc("system", F.SYSTEM, first=True)
    a2, b2 = lm.enc("developer", F.FIXED_BODY), lm.enc("user", F.FIXED_BODY)
    a3 = lm.enc("user", F.quarter_msg(3, W[3], "lo", test=True)) + lm.readout()
    b3 = a3
    lm.start(2)
    lm.feed([a1, b1])
    lm.feed([a2, b2])
    lg = lm.feed([a3, b3])
    worst = 0.0
    for b, seq in enumerate((a1 + a2 + a3, b1 + b2 + b3)):
        ref = lm.m(input_ids=torch.tensor([seq], device=AB.DEV)).logits[0, -1].float()
        tv = 0.5 * (torch.softmax(lg[b], -1) - torch.softmax(ref, -1)).abs().sum().item()
        worst = max(worst, tv)
    ids = torch.tensor([s["ft"] for s in W[3]["stocks"]], device=lg.device)
    mass = torch.softmax(lg[0], -1)[ids].sum().item()
    ok = worst < 0.02
    print(f"G3 cache {'PASS' if ok else 'FAIL'} worst TV {worst:.4f}; ticker mass at the first readout {mass:.3f}")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="openai/gpt-oss-20b")
    ap.add_argument("--no-model", action="store_true")
    a = ap.parse_args()
    lm = TokOnly(a.model)
    ok = g1(lm) & g2(lm)
    if not a.no_model:
        ok &= g3(a.model)
    print("FLIP_GATE", "PASS" if ok else "FAIL", flush=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
