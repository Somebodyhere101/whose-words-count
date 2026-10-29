"""Logical context length at every readout of a fast-instrument run, rebuilt with the model's own tokenizer.

Rebuilds each episode exactly as agp_fast.run_batch fed it (world from the seed, recorded picks and notes; a rewound
note request does not count, as in agp_batch), and checks every recorded pick against the rebuilt world.
The readout token sits at position length - 1, so a step is inside a window W if length <= W.

Usage: python ctx_positions.py --model allenai/OLMo-2-1124-7B-Instruct --dir <out_fast dir> --window 4096
"""
import argparse
import json
import os

from transformers import AutoTokenizer

import agp_batch as AB
import agp_fast as F
import chat_fmt


class TokOnly:
    """The encoding half of agp_batch.BatchLM, without loading weights."""
    enc = AB.BatchLM.enc
    header = AB.BatchLM.header
    readout = AB.BatchLM.readout

    def __init__(self, name):
        self.tok = AutoTokenizer.from_pretrained(name)
        self.qwen3 = "Qwen3" in name or "SmolLM3" in name
        chatml = self.qwen3 or "<|im_start|>" in (self.tok.chat_template or "")
        if os.environ.get("AGP_FMT") == "plain":
            self.fmt = chat_fmt.plain(self.tok)
        else:
            self.fmt = None if chatml else chat_fmt.wrappers(self.tok)
        self.close_str = "<|im_end|>\n" if self.fmt is None else self.fmt["assistant"][1]


def lengths(lm, cond, r, notes_from):
    n = lambda ids: len(ids)
    W = F.make_world(r["seed"], lm.tok)
    L = n(lm.enc("system", F.SYSTEM, first=True))
    for i in range(F.N_HIST):
        lo = min((s for s in W[i]["stocks"] if s["kind"] == "lo"), key=lambda s: s["em"])
        L += n(lm.enc("user", F.quarter_msg(i, W[i]))) + n(lm.enc("assistant", f"ALLOCATE: {lo['t']}"))
    ro = lm.readout()
    out, prev = [], "lo"
    for k in range(F.N_TEST):
        i = F.N_HIST + k
        if k in F.INSERT_AT:
            j = F.INSERT_AT.index(k)
            if cond == "oN":
                L += n(lm.enc("assistant", r["notes"][j]))
            elif cond in ("gF", "oF", "uF"):
                L += n(lm.enc({"gF": "system", "oF": "assistant", "uF": "user"}[cond], F.FIXED_BODY))
            elif cond == "gN":
                L += n(lm.enc("system", notes_from[j]))
            elif cond in ("gW", "oW"):
                L += n(lm.enc("system" if cond == "gW" else "assistant", F.FIXED_WEAK))
        L += n(lm.enc("user", F.quarter_msg(i, W[i], prev, test=True))) + n(ro)
        out.append(L)
        st = r["steps"][k]
        assert st["k"] == k and st["pick"] in [s["t"] for s in W[i]["stocks"]], (cond, r["seed"], k)
        prev = st["kind"]
        L += n(lm.tok(" " + st["pick"] + lm.close_str, add_special_tokens=False).input_ids)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--window", type=int, default=4096)
    ap.add_argument("--seeds", default="300-339")
    a = ap.parse_args()
    lo, hi = map(int, a.seeds.split("-"))
    lm = TokOnly(a.model)
    res = {"model": a.model, "window": a.window, "cells": {}}
    first_out = []
    for c in F.CONDS:
        per = {}
        for s in range(lo, hi + 1):
            r = json.load(open(os.path.join(a.dir, f"c{c}_s{s}.json")))
            nf = json.load(open(os.path.join(a.dir, f"coN_s{s}.json")))["notes"] if c == "gN" else None
            per[s] = lengths(lm, c, r, nf)
        ks = [next((k for k, L in enumerate(v) if L > a.window), F.N_TEST) for v in per.values()]
        first_out.extend(ks)
        res["cells"][c] = {"len_step0_mean": round(sum(v[0] for v in per.values()) / len(per), 1),
                           "len_last_mean": round(sum(v[-1] for v in per.values()) / len(per), 1),
                           "len_last_max": max(v[-1] for v in per.values()),
                           "first_step_outside_min": min(ks), "first_step_outside_median": sorted(ks)[len(ks) // 2],
                           "lengths": {str(s): v for s, v in per.items()}}
        print(c, {k: v for k, v in res["cells"][c].items() if k != "lengths"}, flush=True)
    res["kmax_all_inside"] = min(first_out)
    print("steps k < kmax are inside the window for every run of every cell: kmax =", res["kmax_all_inside"])
    json.dump(res, open(os.path.join(a.dir, "..", "ctx_positions_" + a.model.split("/")[-1] + ".json"), "w"))


if __name__ == "__main__":
    main()
