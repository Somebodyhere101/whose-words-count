"""One-load evaluation for the commitment-binding pilots: the fund task (cells 1/gF/oF), optionally the swapped-growth
shortcut test (cells 1/gF, AGP_SWAP=1), and the injection test, for the base model or one adapter (AGP_LORA).

Usage: AGP_NTEST=22 [AGP_LORA=../lora/own240] python e_eval.py --model M --tag own240 --seeds 300-339 [--swap] --out ../out_le2
"""
import argparse
import json
import os
import time

import torch

import agp_batch as AB
import agp_fast as F
import inj_eval


def fast(lm, conds, seeds, batch, out):
    os.makedirs(out, exist_ok=True)
    for c in conds:
        for i in range(0, len(seeds), batch):
            ss = seeds[i:i + batch]
            t0 = time.time()
            rs = F.run_batch(c, ss, lm, None)
            for r in rs:
                r.update({"sec_batch": round(time.time() - t0, 1), "batch": len(ss), "swap": os.environ.get("AGP_SWAP") == "1",
                          "lora": os.environ.get("AGP_LORA")})
                json.dump(r, open(os.path.join(out, f"c{c}_s{r['seed']}.json"), "w"))
            print(os.path.basename(out), c, ss[0], "p_hi", round(sum(r["mean_p_hi"] for r in rs) / len(rs), 3),
                  round(time.time() - t0, 1), "s", flush=True)
        if AB.DEV == "cuda":
            torch.cuda.empty_cache()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--seeds", default="300-339")
    ap.add_argument("--batch", type=int, default=20)
    ap.add_argument("--swap", action="store_true")
    ap.add_argument("--inj_n", type=int, default=120)
    ap.add_argument("--inj_seed", type=int, default=7)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    lo, hi = map(int, a.seeds.split("-"))
    seeds = list(range(lo, hi + 1))
    lm = AB.BatchLM(a.model, 0.7)
    fast(lm, ["1", "gF", "oF"], seeds, a.batch, os.path.join(a.out, f"fast_{a.tag}"))
    if a.swap:
        os.environ["AGP_SWAP"] = "1"
        fast(lm, ["1", "gF"], seeds, a.batch, os.path.join(a.out, f"swap_{a.tag}"))
        os.environ.pop("AGP_SWAP")
    res = {"model": a.model, "lora": os.environ.get("AGP_LORA"), "inj_seed": a.inj_seed,
           "places": inj_eval.evaluate(lm, a.inj_n, a.inj_seed, 12)}
    json.dump(res, open(os.path.join(a.out, f"inj_{a.tag}.json"), "w"))


if __name__ == "__main__":
    main()
