"""REVPILOT 3 analysis (pilot 2 rules unchanged; order-balanced training data), written before data (rules in ../REVPILOT.md, "Pilot 2" amendment): pilot 1 rules plus the
no-reminder guard (an adapter whose p_goal with no reminder exceeds 0.50 is BROKEN: the reminder no longer matters).

Usage: python rev_pilot_analyze.py <out_rev folder>   (holds <model>/<condition>/{1,gF,uF,oF}_base.json)
"""
import json
import os
import random
import sys

ROOT = sys.argv[1]
SYS, USR = ("sys4000", "sys5000"), ("usr4000", "usr5000")


def load(d):
    out = {}
    for c in ("1", "gF", "uF", "oF"):
        f = os.path.join(d, f"{c}_base.json")
        if os.path.exists(f):
            out[c] = {r["seed"]: r["mean_p_goal"] for r in json.load(open(f))["runs"]}
    return out


def stats(xs, B=4000):
    m = sum(xs) / len(xs)
    rng, hits = random.Random(1), 0
    for _ in range(B):
        if abs(sum(x if rng.random() < 0.5 else -x for x in xs) / len(xs)) >= abs(m):
            hits += 1
    r2 = random.Random(0)
    bs = sorted(sum(r2.choice(xs) for _ in xs) / len(xs) for _ in range(B))
    return {"mean": round(m, 4), "ci": [round(bs[int(.025 * B)], 4), round(bs[int(.975 * B)], 4)],
            "pos": f"{sum(x > 0 for x in xs)}/{len(xs)}", "p": round((hits + 1) / (B + 1), 4)}


res = {}
for m in sorted(os.listdir(ROOT)):
    md = os.path.join(ROOT, m)
    if not os.path.isdir(md):
        continue
    C = {c: load(os.path.join(md, c)) for c in sorted(os.listdir(md)) if os.path.isdir(os.path.join(md, c))}
    if "base" not in C or len(C["base"]) < 4:
        continue
    seeds = sorted(C["base"]["gF"])
    D = lambda c: [C[c]["gF"][s] - C[c]["uF"][s] for s in seeds]
    R = {"means": {c: {k: round(sum(v.values()) / len(v), 4) for k, v in P.items()} for c, P in C.items()}}
    for c, P in C.items():
        if len(P) < 4:
            continue
        R[c] = {"D": stats(D(c)), "competence": stats([P["gF"][s] - P["1"][s] for s in seeds])}
        if c != "base":
            R[c]["shift"] = stats([a - b for a, b in zip(D(c), D("base"))])
    have = lambda cs: all(c in R for c in cs)
    lab = {}
    if have(SYS + USR):
        lab["BROKEN"] = any(R[c]["competence"]["mean"] < 0.10 or R["means"][c]["1"] > 0.50 for c in SYS + USR)
        lab["REVERSED"] = all(R[c]["D"]["mean"] >= 0.02 and R[c]["D"]["p"] < 0.05 for c in SYS)
        lab["SHIFTED"] = (not lab["REVERSED"]) and all(R[c]["shift"]["mean"] >= 0.03 and R[c]["shift"]["p"] < 0.05 for c in SYS)
        lab["OPPOSITE"] = all(R[c]["shift"]["mean"] <= 0 for c in USR)
        lab["GO"] = (lab["REVERSED"] or lab["SHIFTED"]) and lab["OPPOSITE"] and not lab["BROKEN"]
    R["labels"] = lab
    res[m] = R
    print("==", m, lab)
    for c in C:
        if c in R:
            print(f"  {c:8s} D {R[c]['D']}  comp {R[c]['competence']['mean']}  shift {R[c].get('shift', {}).get('mean')}")
go = any(R["labels"].get("GO") for R in res.values())
print("PILOT VERDICT:", "GO" if go else "NO_REVERSAL")
json.dump({"models": res, "verdict": "GO" if go else "NO_REVERSAL"}, open(os.path.join(ROOT, "..", "rev_pilot3.json"), "w"), indent=1)
