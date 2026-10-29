"""Score a second-family model on the stage-1/2/3 criteria of PLAN_7DAY.md (cloud_families results).

Usage: python fam_analyze.py --root C:/Users/caabm/Documents/agp_res/cloud_families --model granite-3.3-8b-instruct
       [--kmax 20]   stage 1 only: mean p_hi over test steps k < kmax (post-hoc restriction for a short context window)
Stage 1: cell means; sign-flip tests H1 notes - fixed, H2 oF - gF, S1 oN - gN, C 1 - gF, W oW - gW (seeds 300-339).
Stage 2: probe layer with the best min(R->A, A->R) held-out transfer, and the sys-vs-user control at that layer.
Stage 3: the PLAN_7DAY.md gate at alpha 2, for the fixed (gF/oF) and the weak (gW/oW) text:
         own text pushed toward given lowers p_hi by >= 0.05, given text pushed toward own raises it by >= 0.05,
         each beyond the same-sign random control (sign-flip, Holm over layers, p < 0.05), ticker mass >= 80% of base.
Results stored in the cloud files are read as they are; the script only summarises.
"""
import argparse
import json
import os

from analyze import signflip

CELLS = ("1", "gF", "oF", "gN", "oN", "gW", "oW")


def mean(v):
    v = list(v)
    return sum(v) / len(v)


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    out, run = [0.0] * len(ps), 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - r) * ps[i]))
        out[i] = run
    return out


def test(d):
    m, p, ci = signflip(d)
    return {"mean": round(m, 4), "p": round(p, 5), "ci95": [round(ci[0], 4), round(ci[1], 4)],
            "pos": sum(x > 0 for x in d), "neg": sum(x < 0 for x in d)}


def stage1(d, kmax, seeds=range(300, 340)):
    Y, mm = {}, []
    for c in CELLS:
        Y[c] = []
        for s in seeds:
            r = json.load(open(os.path.join(d, f"c{c}_s{s}.json")))
            ph = [x["p_hi"] for x in r["steps"] if kmax is None or x["k"] < kmax]
            Y[c].append(mean(ph))
            mm.append(min(x["mass"] for x in r["steps"] if kmax is None or x["k"] < kmax))
    n = len(Y["1"])
    tests = {
        "H1_notes_minus_fixed": [(Y["gN"][i] + Y["oN"][i] - Y["gF"][i] - Y["oF"][i]) / 2 for i in range(n)],
        "H2_oF_minus_gF": [Y["oF"][i] - Y["gF"][i] for i in range(n)],
        "S1_oN_minus_gN": [Y["oN"][i] - Y["gN"][i] for i in range(n)],
        "C_1_minus_gF": [Y["1"][i] - Y["gF"][i] for i in range(n)],
        "W_oW_minus_gW": [Y["oW"][i] - Y["gW"][i] for i in range(n)],
    }
    mm.sort()
    return {"n": n, "kmax": kmax, "cell_means": {c: round(mean(v), 4) for c, v in Y.items()},
            "min_mass_median": round(mm[len(mm) // 2], 4), "min_mass_min": round(mm[0], 4),
            "tests": {k: test(v) for k, v in tests.items()}}


def stage2(d):
    pr = json.load(open(os.path.join(d, "probe_results.json")))["layers"]
    b = max(pr, key=lambda x: min(x["T3_R_to_A_dm"], x["T3_A_to_R_dm"]))
    return {"n_layers": len(pr) - 1, "best_layer": b["layer"], "R_to_A": round(b["T3_R_to_A_dm"], 3),
            "A_to_R": round(b["T3_A_to_R_dm"], 3), "control_sys_vs_user_to_A": round(b["C1_sys_vs_user_to_A_dm"], 3),
            "T1_R_within": round(b["T1_R_within_lr"], 3), "T2_A_within": round(b["T2_A_within_lr"], 3),
            "gate_pass": bool(min(b["T3_R_to_A_dm"], b["T3_A_to_R_dm"]) >= 0.8
                              and b["C1_sys_vs_user_to_A_dm"] <= min(b["T3_R_to_A_dm"], b["T3_A_to_R_dm"]) - 0.15)}


def stage3(d, g, o):
    def y(n):
        return {r["seed"]: r for r in json.load(open(os.path.join(d, n + ".json")))["runs"]}
    base = {c: y(f"{c}_base") for c in (g, o)}
    layers = sorted({int(f.split("_L")[1].split("_")[0]) for f in os.listdir(d) if "_L" in f})
    out = {"base": {c: round(mean(r["mean_p_hi"] for r in base[c].values()), 4) for c in (g, o)},
           "base_mass": {c: round(mean(r["mean_mass"] for r in base[c].values()), 4) for c in (g, o)},
           "layers": layers, "rows": []}
    for a in ("2", "1"):
        for L in layers:
            for cell, sg, want in ((o, "-", -1), (g, "+", 1)):
                b, dd, rr = base[cell], y(f"{cell}_L{L}_dir_a{sg}{a}"), y(f"{cell}_L{L}_rand_a{sg}{a}")
                S = sorted(b)
                sh = test([want * (dd[k]["mean_p_hi"] - b[k]["mean_p_hi"]) for k in S])
                br = test([want * (dd[k]["mean_p_hi"] - rr[k]["mean_p_hi"]) for k in S])
                out["rows"].append({"alpha": int(a), "layer": L, "cell": cell, "push": "toward given" if cell == o else "toward own",
                                    "steered": round(mean(dd[k]["mean_p_hi"] for k in S), 4),
                                    "random": round(mean(rr[k]["mean_p_hi"] for k in S), 4),
                                    "shift_predicted_dir": sh, "beyond_random": br,
                                    "mass_ratio": round(mean(dd[k]["mean_mass"] for k in S) / mean(b[k]["mean_mass"] for k in S), 4)})
    a2 = [r for r in out["rows"] if r["alpha"] == 2]
    for cell in (o, g):
        rs = [r for r in a2 if r["cell"] == cell]
        for r, ph in zip(rs, holm([r["beyond_random"]["p"] for r in rs])):
            r["beyond_random"]["p_holm"] = round(ph, 5)
    passing = []
    for L in layers:
        ok = True
        for cell in (o, g):
            r = next(r for r in a2 if r["cell"] == cell and r["layer"] == L)
            ok &= (r["shift_predicted_dir"]["mean"] >= 0.05 and r["beyond_random"]["mean"] > 0
                   and r["beyond_random"]["p_holm"] < 0.05 and r["mass_ratio"] >= 0.8)
        if ok:
            passing.append(L)
    out["gate_pass_layers"] = passing
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--kmax", type=int, default=None)
    ap.add_argument("--skip3", action="store_true")
    a = ap.parse_args()
    R, M = a.root, a.model
    res = {"model": M, "stage1": stage1(os.path.join(R, f"out_fast_{M}"), a.kmax),
           "stage2": stage2(os.path.join(R, f"out_stage2_{M}"))}
    if not a.skip3:
        res["stage3_fixed"] = stage3(os.path.join(R, f"out_stage3_{M}"), "gF", "oF")
        res["stage3_weak"] = stage3(os.path.join(R, f"out_stage3w_{M}"), "gW", "oW")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
