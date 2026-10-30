"""Score AUTHPILOT against AUTH_PRED.md: gates, A1-A6, A2-kill, and Brier scores for both bets.

Usage: python auth_analyze.py <out_auth folder>   (holds one subfolder per model)
"""
import glob
import json
import os
import random
import sys

ROOT = sys.argv[1]
SEEDS = list(range(4000, 4030))
BIND, BACK = ("b0", "b1", "b2"), ("k0", "k1", "k2")


def load(d):
    P = {}
    for f in glob.glob(os.path.join(d, "*.json")):
        r = json.load(open(f))
        P.setdefault(r["cond"], {})[r["seed"]] = r["mean_p_goal"]
    bad = {k: len(v) for k, v in P.items() if len(v) != len(SEEDS)}
    assert not bad and len(P) == 59, (len(P), bad)
    return P


def stats(xs, B=4000):
    m = sum(xs) / len(xs)
    rng = random.Random(0)
    bs = sorted(sum(rng.choice(xs) for _ in xs) / len(xs) for _ in range(B))
    rng2, hits = random.Random(1), 0
    for _ in range(B):
        if abs(sum(x if rng2.random() < 0.5 else -x for x in xs) / len(xs)) >= abs(m):
            hits += 1
    return {"mean": round(m, 4), "ci": [round(bs[int(.025 * B)], 4), round(bs[int(.975 * B)], 4)],
            "pos": f"{sum(x > 0 for x in xs)}/{len(xs)}", "p": round((hits + 1) / (B + 1), 4)}


def run(P):
    def cell(a, ks, s):   # authorship a, authority keys ks: mean over g/u and paraphrases, one seed
        vals = [P[f"{r}:{a}_{k}"][s] for r in ("g", "u") for k in ks]
        return sum(vals) / len(vals)
    pen = lambda ks: [cell("n", ks, s) - cell("o", ks, s) for s in SEEDS]
    R = {"gate_competence": stats([P["gF"][s] - P["1"][s] for s in SEEDS])}
    R["P_x"], R["P_BIND"], R["P_BACK"] = stats(pen(("x",))), stats(pen(BIND)), stats(pen(BACK))
    R["A1"] = stats([cell("n", BIND, s) - cell("n", ("x",), s) for s in SEEDS])
    R["A3"] = stats([a - b for a, b in zip(pen(("x",)), pen(BIND))])
    R["A4"] = stats([sum(cell(a, BACK, s) - cell(a, ("x",), s) for a in "sond") / 4 for s in SEEDS])
    R["A5"] = stats([cell("d", BIND, s) - cell("n", BIND, s) for s in SEEDS])
    R["self_bonus_x"] = stats([cell("s", ("x",), s) - cell("n", ("x",), s) for s in SEEDS])
    R["self_bonus_BIND"] = stats([cell("s", BIND, s) - cell("n", BIND, s) for s in SEEDS])
    R["means"] = {f"{a}_{k}": round(sum(cell(a, (k,), s) for s in SEEDS) / len(SEEDS), 4)
                  for a in "sond" for k in ("x",) + BIND + BACK}
    return R


out, res = {}, {}
for d in sorted(glob.glob(os.path.join(ROOT, "*"))):
    if os.path.isdir(d):
        res[os.path.basename(d)] = run(load(d))
Q, L = res.get("Qwen3-8B"), res.get("OLMo-2-1124-7B-Instruct")
comp = lambda R: R["gate_competence"]["mean"] >= 0.10 and R["gate_competence"]["p"] < 0.05
if Q and comp(Q):
    q_base = Q["P_x"]["mean"] >= 0.05
    out["A1_Q"] = Q["A1"]["mean"] >= 0.02
    if q_base:
        out["A2_Q"] = Q["P_BIND"]["mean"] >= 0.05
        out["A2kill_Q"] = Q["P_BIND"]["ci"][1] < 0.05
        out["A3_Q"] = Q["A3"]["mean"] >= 0.03
    out["A4_Q"] = Q["A4"]["mean"] <= -0.02
    out["A5_Q"] = abs(Q["A5"]["mean"]) < 0.02
if L and comp(L):
    out["A1_L"] = L["A1"]["mean"] >= 0.02
    out["A2_L"] = L["P_BIND"]["mean"] >= 0.05
    out["A2kill_L"] = L["P_BIND"]["ci"][1] < 0.05
    out["A6_L"] = L["P_x"]["mean"] >= 0.05
bets = {"codex": dict(A1_Q=.72, A1_L=.65, A2_Q=.64, A2_L=.42, A2kill_Q=.18, A2kill_L=.34, A3_Q=.72, A4_Q=.84, A5_Q=.72, A6_L=.64),
        "claude": dict(A1_Q=.60, A1_L=.55, A2_Q=.55, A2_L=.35, A2kill_Q=.25, A2kill_L=.35, A3_Q=.70, A4_Q=.75, A5_Q=.65, A6_L=.55)}
brier = {k: round(sum((b[o] - out[o]) ** 2 for o in out) / len(out), 4) for k, b in bets.items()} if out else {}
json.dump({"models": res, "outcomes": out, "brier": brier}, open(os.path.join(ROOT, "..", "auth_analysis.json"), "w"), indent=1)
for m, R in res.items():
    print("==", m)
    for k, v in R.items():
        if k != "means":
            print(" ", k, v)
print("outcomes", out)
print("brier", brier)
