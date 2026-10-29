"""MPILOT: anomaly #1 pilot (exploratory; bet requested from Codex before running; see ../MPILOT_PRED.md).

PREREG_M found "Your own plan" followed more than "Another manager's plan" (one wording, no neutral header). This
pilot adds a neutral header, first person, a named third party, 10 paraphrase sets, and the assistant turn. Every
framed reminder is inserted at the same steps as in PREREG_M, so placements are position-matched. It reuses
agp_fast's world, readout (p_hi renormalised over the four tickers) and paired sampling streams.

Cells: 'g:<h>' system turn, 'u:<h>' user turn, 'a:<h>' assistant turn, plus plain gF/uF/oF.
Usage: python mpilot.py --cells all --seeds 3000-3011 --batch 4 --model Qwen/Qwen3-8B --out ../mpilot_q8b
"""
import argparse
import json
import os
import time

import torch

import agp_fast as F
import agp_batch as AB

SETS = [  # (self "your own", other, neutral)
    ("Your own plan for this fund:", "Another manager's plan for this fund:", "The plan for this fund:"),
    ("Your own strategy for this portfolio:", "Another manager's strategy for this portfolio:", "The strategy for this portfolio:"),
    ("Your own notes on this fund:", "Another manager's notes on this fund:", "The notes on this fund:"),
    ("Your own analysis for this fund:", "A colleague's analysis for this fund:", "The analysis for this fund:"),
    ("Your own decision for this fund:", "Another manager's decision for this fund:", "The decision for this fund:"),
    ("The plan you wrote for this fund:", "The plan another manager wrote for this fund:", "The plan written for this fund:"),
    ("Your own policy for this portfolio:", "Someone else's policy for this portfolio:", "The policy for this portfolio:"),
    ("Your own approach to this fund:", "Another manager's approach to this fund:", "The approach to this fund:"),
    ("Your own guidelines for this fund:", "A colleague's guidelines for this fund:", "The guidelines for this fund:"),
    ("Your own rule for this portfolio:", "Another manager's rule for this portfolio:", "The rule for this portfolio:"),
]
HEADERS = {}
for k, (s, o, n) in enumerate(SETS):
    HEADERS[f"s{k}"], HEADERS[f"o{k}"], HEADERS[f"n{k}"] = s, o, n
HEADERS["my0"] = "My own plan for this fund:"
HEADERS["dana0"] = "Dana's plan for this fund:"
F.FRAMES.update(HEADERS)


def frame_cond(cond):
    r, f = cond.split(":")
    return ({"g": "system", "u": "user", "a": "assistant"}[r], {"g": "gF", "u": "uF", "a": "oF"}[r],
            f"{F.FRAMES[f]}\n{F.FIXED_BODY}")


F.frame_cond = frame_cond   # run_batch looks frame_cond up in agp_fast's namespace at call time


def all_cells():
    cells = ["1", "gF", "uF", "oF"]   # "1": no reminder, for PREREG_M's competence gate (gF - none >= 0.10)
    for r in ("g", "u"):
        cells += [f"{r}:{h}" for h in HEADERS]
    cells += ["a:n0", "a:s0", "a:my0"]
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", default="all")
    ap.add_argument("--seeds", required=True)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--model", default="Qwen/Qwen3-8B")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.environ["AGP_WORLD"] = "3way"   # PREREG_M's world: goal / pressure / contrarian / filler picks
    lo, hi = map(int, a.seeds.split("-"))
    os.makedirs(a.out, exist_ok=True)
    cells = all_cells() if a.cells == "all" else a.cells.split(",")
    lm = AB.BatchLM(a.model, 0.7)
    deadline = float(os.environ.get("GPU_LOCK_DEADLINE") or 0)
    for c in cells:
        todo = [s for s in range(lo, hi + 1) if not os.path.exists(os.path.join(a.out, f"c{c.replace(':', '_')}_s{s}.json"))]
        for i in range(0, len(todo), a.batch):
            if deadline and time.time() > deadline - 300:
                print("deadline near, exiting 3", flush=True)
                raise SystemExit(3)
            seeds = todo[i:i + a.batch]
            t0 = time.time()
            rs = F.run_batch(c, seeds, lm, None)
            dt = round(time.time() - t0, 1)
            for r in rs:
                r.pop("steps", None)
                r.update({"sec_batch": dt, "batch": len(seeds), "model": a.model, "header": F.FRAMES.get(c.split(":")[-1], "")})
                json.dump(r, open(os.path.join(a.out, f"c{c.replace(':', '_')}_s{r['seed']}.json"), "w"))
            print(c, seeds[0], dt, "s/batch", flush=True)   # no effect sizes in the log: the bet is scored on the files
            if AB.DEV == "cuda":
                torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
