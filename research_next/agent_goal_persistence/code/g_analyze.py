"""PREREG_G analysis, fixed before data: does steering an agent's own goal note toward "given" make it more binding than
the best natural placement, on the 3-way world (goal pick / pressure pick / contrarian trap separated)?

Usage: python g_analyze.py --root <out_g folder holding Qwen3-8B, Qwen3-14B, OLMo-2-1124-7B-Instruct>
Seeds 1300-1359 (n 60, fresh). Outcome p_goal = probability of the low-emission (goal) pick, averaged over test steps.
Per Qwen model (primary), all of:
  C1 p_goal(oF_dir) - p_goal(gF_base) > 0 and C2 p_goal(oF_dir) - p_goal(uF_base) > 0: paired sign-flip tests,
     each Holm-corrected across the two Qwen models, p < 0.05;
  C3 beyond random: p_goal(oF_dir) - p_goal(oF_rand) > 0, sign-flip p < 0.05;
  gate: p_contra(oF_dir) - p_contra(oF_base) <= 0.02, and mean ticker mass(oF_dir) >= 0.8 x mass(oF_base).
Verdict: PASS if both Qwen models pass everything; PARTIAL if one does; FAIL if neither.
Reported, not gating: the boost (gF_boost against gF, uF and gF_randboost); the natural gaps gF - oF and uF - gF;
OLMo-2-7B with the same tests (cross-family check).
"""
import argparse
import json
import os

from fam_analyze import holm, mean, test

QWEN = ("Qwen3-8B", "Qwen3-14B")
OTHER = ("OLMo-2-1124-7B-Instruct",)


def load(d):
    C = {}
    for f in os.listdir(d):
        if f.endswith(".json"):
            C[f[:-5]] = {r["seed"]: r for r in json.load(open(os.path.join(d, f)))["runs"]}
    return C


def diff(C, x, y, m, S):
    return test([C[x][s][f"mean_p_{m}"] - C[y][s][f"mean_p_{m}"] for s in S])


def model_tests(C):
    S = sorted(C["oF_dir"])
    t = {"C1_vs_system": diff(C, "oF_dir", "gF_base", "goal", S), "C2_vs_user": diff(C, "oF_dir", "uF_base", "goal", S),
         "C3_vs_random": diff(C, "oF_dir", "oF_rand", "goal", S),
         "contra_change": round(mean(C["oF_dir"][s]["mean_p_contra"] - C["oF_base"][s]["mean_p_contra"] for s in S), 4),
         "mass_ratio": round(mean(C["oF_dir"][s]["mean_mass"] for s in S) / mean(C["oF_base"][s]["mean_mass"] for s in S), 4),
         "max_ctx": max(r["max_ctx"] for c in C.values() for r in c.values()),
         "means": {k: {m: round(mean(v[s][f"mean_p_{m}"] for s in S), 4) for m in ("goal", "press", "contra")} for k, v in C.items()},
         "boost_vs_system": diff(C, "gF_boost", "gF_base", "goal", S), "boost_vs_user": diff(C, "gF_boost", "uF_base", "goal", S),
         "boost_vs_random": diff(C, "gF_boost", "gF_randboost", "goal", S),
         "natural_gap_gF_minus_oF": diff(C, "gF_base", "oF_base", "goal", S),
         "user_minus_system": diff(C, "uF_base", "gF_base", "goal", S)}
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    R = {m: model_tests(load(os.path.join(a.root, m))) for m in QWEN + OTHER if os.path.isdir(os.path.join(a.root, m))}
    for key in ("C1_vs_system", "C2_vs_user"):
        ps = holm([R[m][key]["p"] for m in QWEN])
        for m, p in zip(QWEN, ps):
            R[m][key]["p_holm"] = round(p, 5)
    passed = {}
    for m in QWEN:
        t = R[m]
        ok = (t["C1_vs_system"]["mean"] > 0 and t["C1_vs_system"]["p_holm"] < 0.05
              and t["C2_vs_user"]["mean"] > 0 and t["C2_vs_user"]["p_holm"] < 0.05
              and t["C3_vs_random"]["mean"] > 0 and t["C3_vs_random"]["p"] < 0.05
              and t["contra_change"] <= 0.02 and t["mass_ratio"] >= 0.8)
        passed[m] = ok
        t["pass"] = ok
    n = sum(passed.values())
    verdict = "PASS" if n == 2 else "PARTIAL" if n == 1 else "FAIL"
    print(json.dumps({"verdict": verdict, "passed": passed, "models": R}, indent=1))


if __name__ == "__main__":
    main()
