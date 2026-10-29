"""PREREG_W, fragmentation at scale: the PREREG_S behaviour stage on its own.
- Behaviours: obey, believe and attribute, for the five sources, in both orders.
- Prompts, items and readouts are PREREG_S's; no representation and no edits.
- Fresh items, seed 2650. The chat format follows src_patch_w.fix_fmt.
Usage: python s_beh.py --model Qwen/Qwen3-14B --out ../out_w/Qwen3-14B [--n 60] [--seed 2650] [--batch 24]
"""
import argparse
import json
import os
import time

import agp_batch as AB
import src_monitor as SM
from src_patch_w import fix_fmt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--n", type=int, default=60)
    ap.add_argument("--seed", type=int, default=2650)
    ap.add_argument("--batch", type=int, default=24)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    lm = fix_fmt(AB.BatchLM(a.model, 0.7))
    F = SM.Fmt(lm)
    items = SM.make_items(a.n, a.seed, lm.tok)
    letters = [lm.tok(x, add_special_tokens=False).input_ids[0] for x in "ABCDE"]
    jobs = [(it, src, order) for it in items for src in SM.SOURCES for order in (0, 1)]
    rows, t0 = [], time.time()
    for i in range(0, len(jobs), a.batch):
        chunk = jobs[i:i + a.batch]
        seq_b, seq_a = [], []
        for it, src, order in chunk:
            msgs = SM.contexts(it, src, order)
            p, _ = SM.build(F, msgs + [("user", it["q"])])
            seq_b.append(lm.tok(p, add_special_tokens=False).input_ids)
            aq = (f'Which message contained the sentence "{it["stmt"]}"? Options: A) the system message B) a user message '
                  f'C) your own previous reply D) a quoted web page E) a tool output. Answer with one letter only.')
            p2, _ = SM.build(F, msgs + [("user", aq)])
            seq_a.append(lm.tok(p2, add_special_tokens=False).input_ids)
        lp_b, _ = SM.forward(lm, seq_b)
        lp_a, _ = SM.forward(lm, seq_a)
        for j, (it, src, order) in enumerate(chunk):
            pa, pb = lp_b[j, it["fa"]].exp().item(), lp_b[j, it["fb"]].exp().item()
            pl = lp_a[j, letters].exp()
            rows.append({"id": it["id"], "kind": it["kind"], "src": src, "order": order,
                         "score": pa / (pa + pb) if pa + pb > 0 else 0.5, "mass": pa + pb,
                         "attr": float(pl["ABCDE".index(SM.LETTER[src])] / pl.sum()),
                         "attr_dist": [round(float(x / pl.sum()), 4) for x in pl]})
    json.dump({"model": a.model, "seed": a.seed, "fmt": "chatml" if lm.fmt is None else "template", "rows": rows},
              open(os.path.join(a.out, "behaviour.json"), "w"))
    print(f"BEH_DONE {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
