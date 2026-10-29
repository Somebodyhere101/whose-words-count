"""Lineage pilot (PLAN_LINEAGE_FABLE.md, step 7): can the OLMo-2 lineage design work at all?

Usage: python lineage_pilot_analyze.py --root C:/Users/caabm/Documents/agp_res/lineage_pilot [--model OLMo-2-0425-1B]
Cells: 1 (no reminder), gF (reminder as system), oF (reminder as the agent's own turn); seeds 300-319, N_TEST 22.
Checks:
  (a) ticker mass at the readout >= 0.3 in the base model (share of steps, and the mean);
  (b) competence gate in the base model: p_hi(1) - p_hi(gF) >= 0.05;
  (c) the post-trained gap oF - gF has the same sign in the plain-text and the native format.
"""
import argparse
import json
import os

from fam_analyze import mean, test


def load(d, c, seeds):
    return [json.load(open(os.path.join(d, f"c{c}_s{s}.json"))) for s in seeds]


def summary(d, seeds):
    R = {c: load(d, c, seeds) for c in ("1", "gF", "oF")}
    y = {c: [r["mean_p_hi"] for r in rs] for c, rs in R.items()}
    mass = [x["mass"] for rs in R.values() for r in rs for x in r["steps"]]
    n = len(seeds)
    return {"means": {c: round(mean(v), 4) for c, v in y.items()},
            "mass_mean": round(mean(mass), 4), "mass_share_ge_0.3": round(mean(m >= 0.3 for m in mass), 4),
            "max_ctx": max(x["ctx"] for rs in R.values() for r in rs for x in r["steps"]),
            "competence_1_minus_gF": test([y["1"][i] - y["gF"][i] for i in range(n)]),
            "gap_oF_minus_gF": test([y["oF"][i] - y["gF"][i] for i in range(n)]),
            "own_1_minus_oF": test([y["1"][i] - y["oF"][i] for i in range(n)])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--model", default="OLMo-2-0425-1B")
    ap.add_argument("--seeds", default="300-319")
    a = ap.parse_args()
    lo, hi = map(int, a.seeds.split("-"))
    seeds = range(lo, hi + 1)
    runs = {"base_plain": f"plain_{a.model}", "post_plain": f"plain_{a.model}-Instruct",
            "post_native": f"native_{a.model}-Instruct"}
    S = {k: summary(os.path.join(a.root, v), seeds) for k, v in runs.items() if os.path.isdir(os.path.join(a.root, v))}
    b = S.get("base_plain")
    checks = {}
    if b:
        checks["a_base_mass"] = b["mass_share_ge_0.3"] >= 0.5 and b["mass_mean"] >= 0.3
        checks["b_base_competence"] = b["competence_1_minus_gF"]["mean"] >= 0.05 and b["competence_1_minus_gF"]["p"] < 0.05
    if "post_plain" in S and "post_native" in S:
        gp, gn = S["post_plain"]["gap_oF_minus_gF"]["mean"], S["post_native"]["gap_oF_minus_gF"]["mean"]
        checks["c_plain_native_same_sign"] = (gp > 0) == (gn > 0)
    print(json.dumps({"summaries": S, "checks": checks}, indent=1))


if __name__ == "__main__":
    main()
