"""Stage 3 (narrow): does the role representation of the inserted goal text cause the given-vs-own framing effect?

Weak goal text (cells gW / oW) in the fast instrument, Qwen3-1.7B. While the inserted goal text is fed, add
alpha * vR[layer] to the residual stream. vR is the stage-2 own-minus-given direction (role format, training
split); hidden_states[l] = output of layers[l-1].
  oW + (-alpha * vR): own-framed text pushed toward "given"  -> predicted p_hi falls toward gW
  gW + (+alpha * vR): given-framed text pushed toward "own"  -> predicted p_hi rises toward oW
Control: a random direction with the same norm as vR at that layer (fixed seed per layer).

Usage: python steer_run.py --seeds 400-419 --out ../stage3
"""
import argparse
import json
import os
import time

import torch

import agp_batch as AB
import agp_fast as F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="400-419")
    ap.add_argument("--layers", default="5,13,20")
    ap.add_argument("--alphas", default="1,2")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--dirs", default="../stage2/directions.pt")
    ap.add_argument("--model", default="Qwen/Qwen3-1.7B")
    ap.add_argument("--cells", default="gW,oW")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    lo, hi = map(int, a.seeds.split("-"))
    seeds = list(range(lo, hi + 1))
    os.makedirs(a.out, exist_ok=True)
    D = torch.load(a.dirs)
    lm = AB.BatchLM(a.model, 0.7)
    g_cell, o_cell = a.cells.split(",")
    configs = [(g_cell, None), (o_cell, None)]
    for l in map(int, a.layers.split(",")):
        vR = D[l]["vR"]
        g = torch.Generator().manual_seed(1000 + l)
        rnd = torch.randn(vR.shape, generator=g)
        rnd = rnd / rnd.norm() * vR.norm()
        for al in map(float, a.alphas.split(",")):
            for kind, v in (("dir", vR), ("rand", rnd)):
                configs.append((o_cell, (l, v, -al, kind)))
                configs.append((g_cell, (l, v, +al, kind)))
    deadline = float(os.environ.get("GPU_LOCK_DEADLINE") or 0)
    for cell, st in configs:
        name = f"{cell}_base" if st is None else f"{cell}_L{st[0]}_{st[3]}_a{st[2]:+g}"
        f = os.path.join(a.out, name + ".json")
        if os.path.exists(f):
            continue
        if deadline and time.time() > deadline - 300:
            raise SystemExit(3)
        t0 = time.time()
        res = []
        for i in range(0, len(seeds), a.batch):
            rs = F.run_batch(cell, seeds[i:i + a.batch], lm, None,
                             steer=None if st is None else (st[0], st[1], st[2]))
            res += [{"seed": r["seed"], "mean_p_hi": r["mean_p_hi"], "min_mass": r["min_mass"],
                     "mean_mass": sum(x["mass"] for x in r["steps"]) / len(r["steps"]),
                     "max_ctx": max(x["ctx"] for x in r["steps"]),
                     "p_hi_steps": [round(x["p_hi"], 5) for x in r["steps"]]} for r in rs]
        json.dump({"cell": cell, "steer": None if st is None else {"layer": st[0], "alpha": st[2], "kind": st[3]},
                   "runs": res}, open(f, "w"), indent=1)
        print(name, "p_hi", round(sum(r["mean_p_hi"] for r in res) / len(res), 3),
              "mass", round(sum(r["mean_mass"] for r in res) / len(res), 3), round(time.time() - t0, 1), "s", flush=True)
        torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
