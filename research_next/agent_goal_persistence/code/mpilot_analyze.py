"""Score MPILOT against MPILOT_PRED.md: gates, O1-O7, the secondary interaction, and Brier scores for both bets.

Usage: python mpilot_analyze.py <out_mp folder>
"""
import glob
import json
import os
import random
import sys

D = sys.argv[1]
SEEDS = list(range(3000, 3040))
P = {}
for f in glob.glob(os.path.join(D, "*.json")):
    r = json.load(open(f))
    P.setdefault(r["cond"], {})[r["seed"]] = r["mean_p_goal"]
assert all(len(v) == 40 for v in P.values()), {k: len(v) for k, v in P.items() if len(v) != 40}


def diff(a, b):
    """Per-seed p(a) - p(b); a and b are cell names or lists of cells to average."""
    g = lambda c, s: sum(P[x][s] for x in c) / len(c) if isinstance(c, list) else P[c][s]
    return [g(a, s) - g(b, s) for s in SEEDS]


def gu(h1, h2):
    """Mean over system and user turns of p(h1) - p(h2)."""
    return [(x + y) / 2 for x, y in zip(diff(f"g:{h1}", f"g:{h2}"), diff(f"u:{h1}", f"u:{h2}"))]


def stats(xs, B=4000):
    m = sum(xs) / len(xs)
    rng = random.Random(0)
    bs = sorted(sum(rng.choice(xs) for _ in xs) / len(xs) for _ in range(B))
    pos = sum(1 for x in xs if x > 0)
    # sign-flip permutation p (two-sided)
    rng2, ab, hits = random.Random(1), abs(m), 0
    for _ in range(B):
        if abs(sum(x if rng2.random() < 0.5 else -x for x in xs) / len(xs)) >= ab:
            hits += 1
    return {"mean": round(m, 4), "ci": [round(bs[int(.025 * B)], 4), round(bs[int(.975 * B)], 4)],
            "pos": f"{pos}/{len(xs)}", "p": round((hits + 1) / (B + 1), 4)}


R = {}
R["gate_competence"] = stats(diff("gF", "1"))
R["gate_calibration_D0"] = stats(gu("o0", "s0"))
comp = R["gate_competence"]["mean"] >= 0.10 and R["gate_competence"]["p"] < 0.05
calib = R["gate_calibration_D0"]["ci"][1] < 0
R["gates_pass"] = comp and calib
R["O1"] = stats(gu("n0", "o0"))
R["O2"] = stats(gu("s0", "n0"))
R["O3_g"], R["O3_u"] = stats(diff("g:s0", "g:my0")), stats(diff("u:s0", "u:my0"))
R["O4"] = stats(gu("dana0", "n0"))
R["O5"] = stats(diff("gF", "oF"))
sets = [sum(gu(f"o{k}", f"s{k}")) / 40 for k in range(10)]
mean_sets = sum(sets) / 10
R["O6_sets_o_minus_s"] = [round(x, 4) for x in sets]
R["O7"] = stats(diff("a:my0", "g:my0"))
R["secondary_interaction"] = stats([(a - b) - (c - d) for a, b, c, d in zip(
    [P["a:my0"][s] for s in SEEDS], [P["a:s0"][s] for s in SEEDS], [P["g:my0"][s] for s in SEEDS], [P["g:s0"][s] for s in SEEDS])])
R["means"] = {c: round(sum(v.values()) / 40, 4) for c, v in sorted(P.items())}
out = {
    "O1": R["O1"]["mean"] >= 0.02,
    "O2": R["O2"]["mean"] >= 0.02,
    "O3": R["O3_g"]["mean"] >= 0.02 and R["O3_u"]["mean"] >= 0.02,
    "O4": abs(R["O4"]["mean"]) < 0.02,
    "O5": R["O5"]["mean"] >= 0.02,
    "O6": sum(1 for x in sets if (x > 0) == (mean_sets > 0)) >= 8,
    "O7": R["O7"]["mean"] > 0,
}
R["outcomes"] = out
R["O6_count_same_sign"] = sum(1 for x in sets if (x > 0) == (mean_sets > 0))
bets = {"codex": dict(O1=.78, O2=.50, O3=.62, O4=.35, O5=.80, O6=.80, O7=.18),
        "claude": dict(O1=.70, O2=.40, O3=.55, O4=.30, O5=.65, O6=.70, O7=.20)}
R["brier"] = {k: round(sum((p - out[o]) ** 2 for o, p in b.items()) / len(b), 4) for k, b in bets.items()}
json.dump(R, open(os.path.join(D, "..", "mpilot_analysis.json"), "w"), indent=1)
for k, v in R.items():
    if k != "means":
        print(k, v)
