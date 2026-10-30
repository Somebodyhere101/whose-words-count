"""CHANNEL render gate, run locally with tokenizers only, before sealing (rules in ../CHANNEL.md). Exits 1 on failure.

A recording stand-in for BatchLM (tokenizer and wrappers real, logits flat) runs agp_fast.run_batch, so every token
fed in an episode is captured.
C1 sealed layout: in channel N the new code feeds exactly the token streams of the sealed agp_fast (--sealed copy, the
   FLIP-sealed file) for cells 1, operator and uF.
C2 moved pressure: in channels U and S each test step is the quarter message without the praise/pressure lines, then
   those lines as their own turn; the lines' content tokens are identical in the user and the --srole wrapper.
C3 shared streams: a seed's world and sampling stream are the same in every channel (same picks under flat logits).
Usage: python chan_gate.py --sealed <dir with sealed agp_fast.py> --models Qwen/Qwen3-8B,... [--srole-dev gpt-oss]
"""
import argparse
import importlib.util
import os
import sys

import torch

os.environ["AGP_WORLD"] = "3way"
os.environ.setdefault("AGP_DEVICE", "cpu")
import agp_batch as AB
import agp_fast as F
import chat_fmt


class Rec(AB.BatchLM):
    """Real tokenizer and wrappers, no weights: feed() records tokens and returns flat logits."""
    def __init__(self, model):
        from transformers import AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(model)
        self.qwen3 = "Qwen3" in model or "SmolLM3" in model
        chatml = self.qwen3 or "<|im_start|>" in (self.tok.chat_template or "")
        self.fmt = chat_fmt.harmony(self.tok) if "gpt-oss" in model else (None if chatml else chat_fmt.wrappers(self.tok))
        self.close_str = "<|im_end|>\n" if self.fmt is None else self.fmt["assistant"][1]
        self.V = len(self.tok)

    def start(self, n):
        self.n, self.pos, self.log = n, [0] * n, [[] for _ in range(n)]

    def feed(self, new):
        for b, x in enumerate(new):
            self.log[b] += list(x)
            self.pos[b] += len(x)
        return torch.zeros(self.n, self.V)


def load_sealed(d):
    spec = importlib.util.spec_from_file_location("agp_fast_sealed", os.path.join(d, "agp_fast.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def episode(mod, lm, cell, seeds, **kw):
    out = mod.run_batch(cell, seeds, lm, None, **kw)
    return [list(x) for x in lm.log], [[s["pick"] for s in r["steps"]] for r in out]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sealed", required=True)
    ap.add_argument("--models", required=True)
    a = ap.parse_args()
    S = load_sealed(a.sealed)
    ok = True
    seeds = [9390, 9391]
    for model in a.models.split(","):
        lm = Rec(model)
        harm = "gpt-oss" in model
        op, srole = ("dF", "developer") if harm else ("gF", "system")
        c1 = all(episode(S, lm, c, seeds) == episode(F, lm, c, seeds, press="N", srole=srole) for c in ("1", op, "uF"))
        # C2: the moved lines' content tokens, trimmed of first and last word as in content_index
        W = F.make_world3(9390, lm.tok)
        c2 = True
        for prev in ("hi", "lo"):
            txt = F.press_lines(W[3], prev)
            u = [lm.enc("user", txt)[i] for i in F.content_index(lm, "user", txt)]
            s = [lm.enc(srole, txt)[i] for i in F.content_index(lm, srole, txt)]
            q = F.test_msgs(lm, 3, W[3], prev, "U", srole)
            c2 &= u == s and len(u) > 5 and q == lm.enc("user", F.quarter_msg(3, W[3])) + lm.enc("user", txt)
            c2 &= F.test_msgs(lm, 3, W[3], prev, "S", srole) == lm.enc("user", F.quarter_msg(3, W[3])) + lm.enc(srole, txt)
            c2 &= F.test_msgs(lm, 3, W[3], prev, "N", srole) == lm.enc("user", F.quarter_msg(3, W[3], prev, test=True))
            c2 &= F.test_msgs(lm, 3, W[3], prev, "Ns", srole) == (lm.enc("user", F.quarter_msg(3, W[3], prev, test=True))
                                                                  + lm.enc(srole, F.NEUTRAL[(3 + W[3]["budget"]) % 6]))
        picks = [episode(F, lm, "uF", seeds, press=p, srole=srole)[1] for p in ("0", "N", "U", "S", "Ns")]
        c3 = all(p == picks[0] for p in picks)
        print(f"{model}: C1 sealed layout {'PASS' if c1 else 'FAIL'}; C2 moved pressure {'PASS' if c2 else 'FAIL'}; "
              f"C3 shared streams {'PASS' if c3 else 'FAIL'}", flush=True)
        ok &= c1 and c2 and c3
    print("CHAN_GATE", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
