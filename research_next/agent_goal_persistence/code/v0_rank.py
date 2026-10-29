"""PLAN_BIGGER Phase 0, between stages: choose the recipes to rerun with generation. Rules fixed in PILOT_V0.md.

Per model and configuration (first-token readout, items averaged over the two orders, against the plain tool run):
  d_obey = the mean change on instruction items, d_bel = the mean change on fact items, sel = d_bel - d_obey.
A recipe is one configuration key, 'direction|depth|scale|tokens'. Recipes are ranked by sel averaged over models,
among non-random recipes whose mean d_obey is <= -0.05. The top 8 are kept; if fewer qualify, the list is filled
from the remaining non-random recipes by mean sel. Two controls are added: the random direction at the depth,
scale and token set of each of the top 2.
Usage: python v0_rank.py --root ../out_v0 --out ../out_v0/recipes.json
"""
import argparse
import json
import os

import numpy as np


def per_item(jobs, vals, ids):
    acc = {}
    for (iid, _), v in zip(jobs, vals):
        acc.setdefault(iid, []).append(v)
    return np.array([np.mean(acc[i]) for i in ids])


def summarize(R):
    jobs = [tuple(j) for j in R["jobs"]]
    ins = [it["id"] for it in R["items"] if it["kind"] == "obey"]
    fac = [it["id"] for it in R["items"] if it["kind"] == "believe"]
    sc = lambda k: [x[0] for x in R["res"][k]]
    bo, bb = per_item(jobs, sc("base"), ins), per_item(jobs, sc("base"), fac)
    out = {}
    for k in R["res"]:
        if k == "base":
            continue
        do = float((per_item(jobs, sc(k), ins) - bo).mean())
        db = float((per_item(jobs, sc(k), fac) - bb).mean())
        out[k] = (do, db, db - do)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    S = {}
    for m in sorted(os.listdir(a.root)):
        f = os.path.join(a.root, m, "screen.json")
        if os.path.exists(f):
            S[m] = summarize(json.load(open(f)))
    keys = sorted(set.intersection(*[set(v) for v in S.values()]))
    mo = {k: float(np.mean([S[m][k][0] for m in S])) for k in keys}
    mb = {k: float(np.mean([S[m][k][1] for m in S])) for k in keys}
    ms = {k: float(np.mean([S[m][k][2] for m in S])) for k in keys}
    real = [k for k in keys if not k.startswith("random")]
    cands = sorted([k for k in real if mo[k] <= -0.05], key=lambda k: -ms[k])
    top = cands[:8]
    if len(top) < 8:
        top += [k for k in sorted(real, key=lambda k: -ms[k]) if k not in top][:8 - len(top)]
    ctrl = []
    for k in top[:2]:
        _, d, sc, ts = k.split("|")
        c = f"random|{d}|{sc}|{ts}"
        if c not in ctrl:
            ctrl.append(c)
    table = {k: {"mean_d_obey": round(mo[k], 4), "mean_d_bel": round(mb[k], 4), "mean_sel": round(ms[k], 4),
                 "per_model": {m: [round(x, 4) for x in S[m][k]] for m in S}} for k in top + ctrl}
    json.dump({"models": list(S), "n_qualifying": len(cands), "recipes": top + ctrl, "table": table},
              open(a.out, "w"), indent=1)
    print(f"models {list(S)}; {len(cands)} recipes with mean d_obey <= -0.05")
    for k in top + ctrl:
        print(f"  {k:28s} d_obey {mo[k]:+.3f} d_bel {mb[k]:+.3f} sel {ms[k]:+.3f}")
    print("RANK_DONE")


if __name__ == "__main__":
    main()
