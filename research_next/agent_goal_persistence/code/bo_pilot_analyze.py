"""Believe-or-obey pilot, steps 1 and 3 of the plan (calibration and validity), Qwen3-1.7B, seeds 300-319.

Usage: python bo_pilot_analyze.py --root C:/Users/caabm/Documents/agp_res/bo_pilot
Cells: O{n,g,o}0 (obey arm, anchor none/given/own); Bg0 (believe arm, no counter-claims); B{n,g,o}{1,2,3}.
  Calibration, per dose d: Arm B given-anchor uptake U_d = p_hi(Bg d) lies in 0.1-0.9 and within 0.15 of p_hi(Og0),
  and deleting the anchor raises it: p_hi(Bn d) - p_hi(Bg d) > 0 (sign-flip p < 0.05).
  Validity: across Arm B runs with claims, r(mean p_believe_c, mean p_c) >= 0.5, where p_c is the decision probability
  on the contested ticker and p_believe_c the side-question probability that it has the lowest emissions.
Natural gaps own - given are reported for both arms.
"""
import argparse
import json
import os

from fam_analyze import mean, test


def cell(root, name, seeds):
    rs = [json.load(open(os.path.join(root, f"{name}_s{s}.json"))) for s in seeds]
    for r in rs:
        st = [x for x in r["steps"] if x["k"] >= 3]
        r["mean_p_c"] = mean(x["p_c"] for x in st)
        r["mean_mass"] = mean(x["mass"] for x in r["steps"])
    return rs


def pearson(x, y):
    mx, my = mean(x), mean(y)
    sx = sum((a - mx) ** 2 for a in x) ** 0.5
    sy = sum((b - my) ** 2 for b in y) ** 0.5
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--seeds", default="300-319")
    a = ap.parse_args()
    lo, hi = map(int, a.seeds.split("-"))
    seeds = range(lo, hi + 1)
    names = ["On0", "Og0", "Oo0", "Bg0"] + [f"B{p}{d}" for d in (1, 2, 3) for p in "ngo"]
    C = {n: cell(a.root, n, seeds) for n in names if os.path.exists(os.path.join(a.root, f"{n}_s{lo}.json"))}
    y = {n: [r["mean_p_hi"] for r in rs] for n, rs in C.items()}
    res = {"cells": {n: {"p_hi": round(mean(y[n]), 4), "p_c": round(mean(r["mean_p_c"] for r in C[n]), 4),
                         "p_believe_c": round(mean(r["mean_p_believe_c"] for r in C[n]), 4),
                         "mass": round(mean(r["mean_mass"] for r in C[n]), 4)} for n in C}}
    diff = lambda a_, b_: test([u - v for u, v in zip(y[a_], y[b_])])
    if "Oo0" in y and "Og0" in y:
        res["obey_gap_own_minus_given"] = diff("Oo0", "Og0")
    if "On0" in y and "Og0" in y:
        res["obey_anchor_effect_none_minus_given"] = diff("On0", "Og0")
    cal = {}
    for d in (1, 2, 3):
        g, n_, o = f"Bg{d}", f"Bn{d}", f"Bo{d}"
        if g not in y:
            continue
        U = mean(y[g])
        cal[d] = {"U_given": round(U, 4), "U_none": round(mean(y[n_]), 4) if n_ in y else None,
                  "U_own": round(mean(y[o]), 4) if o in y else None,
                  "in_range": 0.1 <= U <= 0.9, "near_obey": abs(U - mean(y["Og0"])) <= 0.15 if "Og0" in y else None,
                  "delete_raises": diff(n_, g) if n_ in y else None, "believe_gap_own_minus_given": diff(o, g) if o in y else None}
        cal[d]["pass"] = bool(cal[d]["in_range"] and cal[d]["near_obey"] and cal[d]["delete_raises"]
                              and cal[d]["delete_raises"]["mean"] > 0 and cal[d]["delete_raises"]["p"] < 0.05)
    res["calibration"] = cal
    xs, ys = [], []
    for n, rs in C.items():
        if n.startswith("B") and not n.endswith("0"):
            xs += [r["mean_p_believe_c"] for r in rs]
            ys += [r["mean_p_c"] for r in rs]
    res["validity_r_believe_vs_act"] = round(pearson(xs, ys), 3) if xs else None
    res["validity_pass"] = bool(xs) and pearson(xs, ys) >= 0.5
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
