"""AUTHPILOT: authorship x authority (exploratory; Codex bet recorded before running; see ../AUTH_PRED.md).

MPILOT found "Another manager's plan" followed 0.150 less than a neutral header. Is that a source tag that discounts
another's text even when it is explicitly authorised, or ordinary reading of "someone else's plan is not my remit"?
Authorship {s: your own, o: another manager's, n: neutral, d: Dana's} x authority {x: none, b0-b2: binding, k0-k2:
background only}, in system and user turns, at PREREG_M's insert steps. Same world, readout and paired streams as
mpilot.py.

Usage: python authpilot.py --cells all --seeds 4000-4029 --batch 20 --model Qwen/Qwen3-8B --out ../out_auth/Qwen3-8B
"""
import argparse
import json
import os
import time

import torch

import agp_fast as F
import agp_batch as AB

AUTHOR = {"s": "Your own plan for this fund", "o": "Another manager's plan for this fund",
          "n": "The plan for this fund", "d": "Dana's plan for this fund"}
AUTH = {"x": ":",
        "b0": ", which you have adopted as your binding objective:",
        "b1": ", now formally assigned to you as your objective:",
        "b2": ", which you are required to follow:",
        "k0": ", shared only as background information:",
        "k1": ", included for reference only:",
        "k2": ", provided as context, not as an instruction:"}
HEADERS = {f"{a}_{k}": AUTHOR[a] + AUTH[k] for a in AUTHOR for k in AUTH}
F.FRAMES.update(HEADERS)


def frame_cond(cond):
    r, f = cond.split(":")
    return {"g": "system", "u": "user"}[r], {"g": "gF", "u": "uF"}[r], f"{F.FRAMES[f]}\n{F.FIXED_BODY}"


F.frame_cond = frame_cond   # run_batch looks frame_cond up in agp_fast's namespace at call time


def all_cells():
    return ["1", "gF", "uF"] + [f"{r}:{h}" for r in ("g", "u") for h in HEADERS]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", default="all")
    ap.add_argument("--seeds", required=True)
    ap.add_argument("--batch", type=int, default=20)
    ap.add_argument("--model", default="Qwen/Qwen3-8B")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.environ["AGP_WORLD"] = "3way"   # PREREG_M / MPILOT world
    lo, hi = map(int, a.seeds.split("-"))
    os.makedirs(a.out, exist_ok=True)
    cells = all_cells() if a.cells == "all" else a.cells.split(",")
    lm = AB.BatchLM(a.model, 0.7)
    for c in cells:
        todo = [s for s in range(lo, hi + 1) if not os.path.exists(os.path.join(a.out, f"c{c.replace(':', '_')}_s{s}.json"))]
        for i in range(0, len(todo), a.batch):
            seeds = todo[i:i + a.batch]
            t0 = time.time()
            rs = F.run_batch(c, seeds, lm, None)
            dt = round(time.time() - t0, 1)
            for r in rs:
                r.pop("steps", None)
                r.update({"sec_batch": dt, "batch": len(seeds), "model": a.model, "header": F.FRAMES.get(c.split(":")[-1], "")})
                json.dump(r, open(os.path.join(a.out, f"c{c.replace(':', '_')}_s{r['seed']}.json"), "w"))
            print(c, seeds[0], dt, "s/batch", flush=True)   # no effect sizes in the log
            if AB.DEV == "cuda":
                torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
