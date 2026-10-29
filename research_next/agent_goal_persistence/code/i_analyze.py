"""PREREG_I analysis, fixed before data: does the role direction predict the authority order across families and sizes?

Usage: python i_analyze.py --root <out_i folder with one sub-folder per model>
Each model folder holds g_eval --probe outputs (cells 1_base, gF_probe, oF_probe, uF_probe; the 3-way world).
Competence gate per model: p_goal(gF) - p_goal(1) >= 0.10 with sign-flip p < 0.05; otherwise the model is excluded.
For each included model and each pair of placements (u,g), (g,o), (u,o):
  behaviour  db = p_goal(x) - p_goal(y), sign-flip test; the pair is DECIDED if p < 0.05 (either sign);
  projection dp = proj(y) - proj(x) (more authority should sit lower on vR, i.e. more "given");
  a decided pair AGREES if dp has the sign of db with sign-flip p < 0.05, DISAGREES if dp has the opposite sign with
  p < 0.05, and is UNRESOLVED otherwise.
Verdict over all included models: PASS if at least 8 decided pairs and agree / decided >= 0.8; FAIL if agree /
decided < 0.5; otherwise MIXED. Reported per model: the behavioural and projection orders, and whether they match fully.
"""
import argparse
import json
import os

from fam_analyze import mean, test

CELL = {"u": "uF_probe", "g": "gF_probe", "o": "oF_probe"}
PAIRS = (("u", "g"), ("g", "o"), ("u", "o"))


def load(d):
    return {f[:-5]: {r["seed"]: r for r in json.load(open(os.path.join(d, f)))["runs"]}
            for f in os.listdir(d) if f.endswith(".json") and not f.startswith("probe")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    res, decided = {}, []
    for m in sorted(os.listdir(a.root)):
        d = os.path.join(a.root, m)
        if not os.path.isdir(d) or not os.path.exists(os.path.join(d, "gF_probe.json")):
            continue
        C = load(d)
        S = sorted(C["gF_probe"])
        g = lambda c, k: [C[c][s][k] for s in S]
        comp = test([x - y for x, y in zip(g("gF_probe", "mean_p_goal"), g("1_base", "mean_p_goal"))])
        r = {"n": len(S), "competence": comp, "included": comp["mean"] >= 0.10 and comp["p"] < 0.05,
             "goal": {k: round(mean(g(c, "mean_p_goal")), 4) for k, c in CELL.items()},
             "proj": {k: round(mean(g(c, "mean_proj")), 4) for k, c in CELL.items()}, "pairs": {}}
        if r["included"]:
            for x, y in PAIRS:
                db = test([p - q for p, q in zip(g(CELL[x], "mean_p_goal"), g(CELL[y], "mean_p_goal"))])
                dp = test([p - q for p, q in zip(g(CELL[y], "mean_proj"), g(CELL[x], "mean_proj"))])
                if db["p"] < 0.05:
                    same = (dp["mean"] > 0) == (db["mean"] > 0)
                    status = "AGREE" if (same and dp["p"] < 0.05) else "DISAGREE" if (not same and dp["p"] < 0.05) else "UNRESOLVED"
                    decided.append(status)
                else:
                    status = "UNDECIDED"
                r["pairs"][f"{x}-{y}"] = {"behaviour": db, "projection": dp, "status": status}
            r["behaviour_order"] = "".join(sorted(CELL, key=lambda k: -r["goal"][k]))
            r["projection_order"] = "".join(sorted(CELL, key=lambda k: r["proj"][k]))
            r["orders_match"] = r["behaviour_order"] == r["projection_order"]
        res[m] = r
    n_dec, n_agree = len(decided), decided.count("AGREE")
    rate = n_agree / n_dec if n_dec else float("nan")
    verdict = "PASS" if (n_dec >= 8 and rate >= 0.8) else "FAIL" if (n_dec and rate < 0.5) else "MIXED"
    print(json.dumps({"verdict": verdict, "decided_pairs": n_dec, "agree": n_agree, "disagree": decided.count("DISAGREE"),
                      "unresolved": decided.count("UNRESOLVED"), "agree_rate": round(rate, 3), "models": res}, indent=1))


if __name__ == "__main__":
    main()
