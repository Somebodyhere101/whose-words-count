"""System-vs-user instruction conflicts from Control Illusion (Geng et al., AAAI 2026; data copied from
github.com/yilin-geng/llm-instruction-conflicts, files conflicting_instructions[_reversed].jsonl).

Each row gives a task and two mutually exclusive constraints. As in their BasicSeparationPolicy, the system prompt
holds constraint1 (the one that should win) and the user prompt holds the task and constraint2. Greedy decoding.
Conditions:
  plain   their BasicSeparationPolicy;
  emph    their EmphasizedSeparationPolicy (system: "You must always follow this constraint: <constraint1>");
  steer   plain, with alpha * (-vR) added at --layer to every token of the system message (role wrapper and text)
          while the prompt is read; vR is the stage-2 own-minus-given direction, so -vR points toward "given";
  rand    plain, with alpha times a same-norm random direction (seed 1000 + layer, as in g_eval) on the same tokens.
'steer<a>' / 'rand<a>' set alpha for that condition (pilot); otherwise --alpha is used. Generated tokens are never
steered. One JSON per condition: one record per prompt with the response and the number of new tokens.

Usage: python ci_eval.py --model Qwen/Qwen3-8B --dirs ../dirs/dirs_q8.pt --layer 17 --alpha 2 \
         --data ../data/ci/conflicting_instructions.jsonl,../data/ci/conflicting_instructions_reversed.jsonl \
         --tasks 30-99 --conds plain,emph,steer,rand --batch 32 --out ../out_n/Qwen3-8B
"""
import argparse
import json
import os
import time

import torch

import agp_batch as AB

MAX_NEW = 512


class SpanSteer:
    """Adds `vec` to the output of decoder layer `layer` at the positions in `mask` (a [batch, T] bool tensor), but
    only on the forward pass whose length is T: the prompt read. Decoding steps (length 1) are left alone."""

    def __init__(self, lm, layer, vec):
        self.v = vec.to(lm.m.device, lm.m.dtype)
        self.layer = lm.m.model.layers[layer - 1]   # hidden_states[l] is the output of layers[l-1]
        self.mask, self.h = None, None

    def __enter__(self):
        def hook(mod, inp, out):
            h = out[0] if isinstance(out, tuple) else out
            if self.mask is None or h.shape[1] != self.mask.shape[1]:
                return out
            h = h + self.mask.unsqueeze(-1).to(h.dtype) * self.v
            return (h,) + tuple(out[1:]) if isinstance(out, tuple) else h
        self.h = self.layer.register_forward_hook(hook)
        return self

    def __exit__(self, *a):
        self.h.remove()


def load_rows(paths, tasks):
    lo, hi = map(int, tasks.split("-"))
    rows = []
    for order, p in enumerate(paths):
        bases = []
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            if r["base_instruction"] not in bases:
                bases.append(r["base_instruction"])
            t = bases.index(r["base_instruction"])
            if lo <= t <= hi:
                rows.append({"task": t, "order": order, "conflict": r["conflict_name"], **r})
    return rows


def prompts(cond, r):
    if cond == "emph":
        return f"You must always follow this constraint: {r['constraint1']}", f"{r['base_instruction']} {r['constraint2']}"
    return r["constraint1"], f"{r['base_instruction']} {r['constraint2']}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--dirs", required=True)
    ap.add_argument("--layer", type=int, required=True)
    ap.add_argument("--alpha", type=float, default=2.0)
    ap.add_argument("--data", required=True, help="comma-separated jsonl files (normal, reversed)")
    ap.add_argument("--tasks", required=True, help="base-task index range, e.g. 30-99")
    ap.add_argument("--conds", required=True)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rows = load_rows(a.data.split(","), a.tasks)
    lm = AB.BatchLM(a.model, 0.7)
    lm.tok.padding_side = "left"
    v = torch.load(a.dirs)[a.layer]["vR"]
    g = torch.Generator().manual_seed(1000 + a.layer)
    r_ = torch.randn(v.shape, generator=g)
    rnd = r_ / r_.norm() * v.norm()
    hdr = lm.header()
    for cond in a.conds.split(","):
        f = os.path.join(a.out, f"{cond}.json")
        if os.path.exists(f):
            continue
        kind = "steer" if cond.startswith("steer") else "rand" if cond.startswith("rand") else cond
        alpha = float(cond[len(kind):]) if kind in ("steer", "rand") and len(cond) > len(kind) else a.alpha
        vec = {"steer": -alpha * v, "rand": alpha * rnd}.get(kind)
        t0, recs = time.time(), []
        ctx = SpanSteer(lm, a.layer, vec) if vec is not None else None
        if ctx:
            ctx.__enter__()
        try:
            for i in range(0, len(rows), a.batch):
                chunk = rows[i:i + a.batch]
                seqs, nsys = [], []
                for r in chunk:
                    s_txt, u_txt = prompts(kind, r)
                    s_ids = lm.enc("system", s_txt, first=True)
                    seqs.append(s_ids + lm.enc("user", u_txt) + hdr)
                    nsys.append(len(s_ids))
                T = max(len(s) for s in seqs)
                ids = torch.full((len(seqs), T), lm.pad, dtype=torch.long)
                am = torch.zeros((len(seqs), T), dtype=torch.long)
                mask = torch.zeros((len(seqs), T), dtype=torch.bool)
                for b, s in enumerate(seqs):
                    ids[b, T - len(s):] = torch.tensor(s)
                    am[b, T - len(s):] = 1
                    mask[b, T - len(s):T - len(s) + nsys[b]] = True
                if ctx:
                    ctx.mask = mask.to(AB.DEV)
                with torch.no_grad():
                    out = lm.m.generate(input_ids=ids.to(AB.DEV), attention_mask=am.to(AB.DEV), max_new_tokens=MAX_NEW,
                                        do_sample=False, pad_token_id=lm.pad)
                for b, r in enumerate(chunk):
                    new = out[b, T:].tolist()
                    while new and new[-1] == lm.pad:
                        new.pop()
                    recs.append({"task": r["task"], "order": r["order"], "conflict": r["conflict"],
                                 "constraint1": r["constraint1"], "constraint2": r["constraint2"], "kwargs": r["kwargs"],
                                 "response": lm.tok.decode(new, skip_special_tokens=True).strip(), "n_new": len(new)})
                if AB.DEV == "cuda":
                    torch.cuda.empty_cache()
        finally:
            if ctx:
                ctx.__exit__()
        json.dump({"model": a.model, "cond": cond, "kind": kind, "alpha": alpha if vec is not None else None,
                   "layer": a.layer, "tasks": a.tasks, "records": recs}, open(f, "w"))
        print(f"{cond} n {len(recs)} mean_new {sum(x['n_new'] for x in recs) / len(recs):.0f} {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
