"""FLIP analysis, written before data (rules in ../FLIP.md).

Usage: python flip_analyze.py --dir <out_flip/gpt-oss-20b> [--gate <gate log>] [--out <json>]
The folder holds g_eval --probe --dev outputs: 1_base, gF_probe (harmony system), dF_probe (developer), uF_probe,
oF_probe; 60 seeds; projections at layer 11 on unit vR (mean_proj) and on 50 random unit directions (mean_proj_r).
Validity: gate PASS, mean readout mass >= 0.5 in every cell, and max over gF/dF/uF of p_goal(cell) - p_goal(1)
>= 0.10 with sign-flip p < 0.05, else INVALID.
Behaviour: D = p_goal(dF) - p_goal(uF) per seed; FLIP if D > 0 with p < 0.05, SAME if D < 0 with p < 0.05, else TIE.
Axis: dP = proj(uF) - proj(dF) per seed; t = mean / (sd / sqrt(n)); q95 = 95th percentile of |t| over the 50 random
directions. AGREE if sign(dP) = sign(D), p < 0.05 and |t| > q95; AGAINST if the opposite sign with the same
conditions; else NULL. Reported: orders over g/d/u/o, the six pairs scored as in PREREG_I, the g-vs-u pair.
"""
import argparse
import itertools
import json
import math
import os

from fam_analyze import mean, test

CELL = {"g": "gF_probe", "d": "dF_probe", "u": "uF_probe", "o": "oF_probe"}


def tstat(x):
    m = mean(x)
    sd = math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1))
    return m / (sd / math.sqrt(len(x))) if sd > 0 else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--gate")
    ap.add_argument("--out")
    a = ap.parse_args()
    C = {f[:-5]: {r["seed"]: r for r in json.load(open(os.path.join(a.dir, f)))["runs"]}
         for f in os.listdir(a.dir) if f.endswith(".json") and not f.startswith("probe")}
    S = sorted(C["dF_probe"])
    g = lambda c, k: [C[c][s][k] for s in S]
    gate = "PASS" if a.gate is None else ("PASS" if "FLIP_GATE PASS" in open(a.gate).read() else "FAIL")
    mass = {c: round(mean(g(c, "mean_mass")), 3) for c in ["1_base"] + list(CELL.values())}
    comp = {k: test([x - y for x, y in zip(g(CELL[k], "mean_p_goal"), g("1_base", "mean_p_goal"))]) for k in "gdu"}
    competent = any(r["mean"] >= 0.10 and r["p"] < 0.05 for r in comp.values())
    valid = gate == "PASS" and min(mass.values()) >= 0.5 and competent
    goal = {k: round(mean(g(c, "mean_p_goal")), 4) for k, c in CELL.items()}
    goal["none"] = round(mean(g("1_base", "mean_p_goal")), 4)
    proj = {k: round(mean(g(c, "mean_proj")), 4) for k, c in CELL.items()}
    D = [x - y for x, y in zip(g("dF_probe", "mean_p_goal"), g("uF_probe", "mean_p_goal"))]
    Dt = test(D)
    beh = "FLIP" if (Dt["mean"] > 0 and Dt["p"] < 0.05) else "SAME" if (Dt["mean"] < 0 and Dt["p"] < 0.05) else "TIE"
    dP = [x - y for x, y in zip(g("uF_probe", "mean_proj"), g("dF_probe", "mean_proj"))]
    dPt = test(dP)
    K = len(C["dF_probe"][S[0]]["mean_proj_r"])
    tnull = sorted(abs(tstat([C["uF_probe"][s]["mean_proj_r"][j] - C["dF_probe"][s]["mean_proj_r"][j] for s in S]))
                   for j in range(K))
    q95 = tnull[math.ceil(0.95 * K) - 1]
    t = tstat(dP)
    strong = dPt["p"] < 0.05 and abs(t) > q95
    same_sign = (dPt["mean"] > 0) == (Dt["mean"] > 0)
    axis = "AGREE" if (strong and same_sign) else "AGAINST" if strong else "NULL"
    pairs = {}
    for x, y in itertools.combinations("udgo", 2):
        db = test([p - q for p, q in zip(g(CELL[x], "mean_p_goal"), g(CELL[y], "mean_p_goal"))])
        dp = test([p - q for p, q in zip(g(CELL[y], "mean_proj"), g(CELL[x], "mean_proj"))])
        if db["p"] < 0.05:
            same = (dp["mean"] > 0) == (db["mean"] > 0)
            st = "AGREE" if (same and dp["p"] < 0.05) else "DISAGREE" if (not same and dp["p"] < 0.05) else "UNRESOLVED"
        else:
            st = "UNDECIDED"
        pairs[f"{x}-{y}"] = {"behaviour": db, "projection": dp, "status": st}
    res = {"verdict": "INVALID" if not valid else f"{beh}/{axis}", "valid": valid, "gate": gate, "mass": mass,
           "competence": comp, "n": len(S), "p_goal": goal, "proj": proj,
           "behaviour": {"D_dev_minus_user": Dt, "label": beh},
           "axis": {"dP_user_minus_dev": dPt, "t": round(t, 3), "null_q95_abs_t": round(q95, 3), "label": axis},
           "orders": {"behaviour": "".join(sorted(CELL, key=lambda k: -goal[k])),
                      "projection": "".join(sorted(CELL, key=lambda k: proj[k]))},
           "pairs": pairs}
    print(json.dumps(res, indent=1))
    json.dump(res, open(a.out or os.path.join(a.dir, "..", "flip_analysis.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
