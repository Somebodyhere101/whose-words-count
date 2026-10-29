"""Analysis for fast-instrument runs (stage 1 gate in PLAN_7DAY.md).

Usage: python fast_analyze.py ../fast_val 300-339 [--min-mass 0.5]
Outcome: per-run mean p_hi (optionally over steps with ticker mass >= min-mass). Paired by seed.
Tests (sign-flip, two-sided): H1 notes - fixed, H2 oF - gF, S1 oN - gN, C 1 - gF.
"""
import json
import os
import sys

from analyze import signflip


def load(d, c, s, mm):
    f = os.path.join(d, f"c{c}_s{s}.json")
    if not os.path.exists(f):
        return None
    r = json.load(open(f))
    ph = [x["p_hi"] for x in r["steps"] if x["mass"] >= mm]
    return sum(ph) / len(ph) if ph else None


def main():
    d = sys.argv[1]
    lo, hi = map(int, sys.argv[2].split("-"))
    mm = float(sys.argv[sys.argv.index("--min-mass") + 1]) if "--min-mass" in sys.argv else 0.0
    cells = ["1", "gF", "oF", "gN", "oN"]
    Y = {}
    for s in range(lo, hi + 1):
        v = {c: load(d, c, s, mm) for c in cells}
        if all(x is not None for x in v.values()):
            Y[s] = v
    S = sorted(Y)
    out = {"n": len(S), "min_mass": mm, "cell_means": {c: sum(Y[s][c] for s in S) / len(S) for c in cells}, "tests": {}}
    tests = {
        "H1_notes_minus_fixed": [(Y[s]["gN"] + Y[s]["oN"] - Y[s]["gF"] - Y[s]["oF"]) / 2 for s in S],
        "H2_oF_minus_gF": [Y[s]["oF"] - Y[s]["gF"] for s in S],
        "S1_oN_minus_gN": [Y[s]["oN"] - Y[s]["gN"] for s in S],
        "C_1_minus_gF": [Y[s]["1"] - Y[s]["gF"] for s in S],
    }
    for k, v in tests.items():
        m, p, ci = signflip(v)
        out["tests"][k] = {"mean": round(m, 4), "p": round(p, 5), "ci95": [round(ci[0], 4), round(ci[1], 4)],
                           "pos": sum(x > 0 for x in v), "neg": sum(x < 0 for x in v)}
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
