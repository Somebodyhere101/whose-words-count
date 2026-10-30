"""PREREG_R analysis, fixed before data: does the role axis follow a trained priority?

Usage: python r_analyze.py --root <out_r folder>   (<model>/<condition>/{1_base,gF_probe,uF_probe,oF_probe}.json,
conditions base, sys<k>, usr<k>; optional <model>/<condition>/cos.json from the re-extracted vR)

Per adapter a and seed s (3-way world, g_eval --probe with the BASE model's vR and 50 seeded random directions):
  D_a(s) = p_goal(gF) - p_goal(uF)              (> 0: the system reminder is followed more than the user one)
  P_a(s) = proj(gF) - proj(uF) on unit base vR   (lower projection = more like given text; base: user lowest)
Arm means per seed: Dsys(s), Dusr(s), Psys(s), Pusr(s) (mean over the arm's adapters).
  R1 manipulation: dD(s) = Dsys - Dusr > 0, sign-flip p < 0.05, AND every sys adapter's mean D above every usr
     adapter's (3 vs 3: permutation p = 1/20 = 0.05).
  R2 axis follows: dP(s) = Psys - Pusr < 0, sign-flip p < 0.05, AND every sys adapter's mean P below every usr
     adapter's, AND |t| of dP on vR above the 95th percentile of |t| on the 50 random directions (t = mean / (sd /
     sqrt(n)) over seeds).
Per model: NO_MANIPULATION if R1 fails (R2 is then uninterpretable); else AXIS_FOLLOWS if R2 passes; AXIS_AGAINST if
dP > 0 with sign-flip p < 0.05; otherwise LABEL_ONLY.
Overall: AXIS_FOLLOWS if every model with R1 passing is AXIS_FOLLOWS and there is at least one; LABEL_ONLY if every such
model is LABEL_ONLY or AXIS_AGAINST; MIXED otherwise; NO_MANIPULATION if no model passes R1.
Exploratory (reported, not gating): per-arm D and P against base; the no-reminder cell; cos(re-extracted vR, base vR).
"""
import argparse
import itertools
import json
import os
import random

N_FLIP = 20000


def load(d):
    out = {}
    for c, tag in (("1", "base"), ("gF", "probe"), ("uF", "probe"), ("oF", "probe")):
        f = os.path.join(d, f"{c}_{tag}.json")
        if os.path.exists(f):
            out[c] = {r["seed"]: r for r in json.load(open(f))["runs"]}
    return out


def mean(x):
    return sum(x) / len(x)


def signflip(x):
    m, rng, hits = mean(x), random.Random(7), 0
    for _ in range(N_FLIP):
        if abs(mean([v if rng.random() < 0.5 else -v for v in x])) >= abs(m):
            hits += 1
    return (hits + 1) / (N_FLIP + 1)


def tstat(x):
    m = mean(x)
    sd = (sum((v - m) ** 2 for v in x) / (len(x) - 1)) ** 0.5
    return m / (sd / len(x) ** 0.5) if sd else 0.0


def separated(lo, hi):
    """Permutation p for 'every lo value below every hi value' among all equal splits (one-sided)."""
    vals = lo + hi
    k, obs = len(lo), (max(lo) < min(hi))
    splits = list(itertools.combinations(range(len(vals)), k))
    hits = sum(max(vals[i] for i in s) < min(vals[j] for j in range(len(vals)) if j not in s) for s in splits)
    return obs, hits / len(splits)


def model(md):
    C = {c: load(os.path.join(md, c)) for c in sorted(os.listdir(md)) if os.path.isdir(os.path.join(md, c))}
    sysc = [c for c in C if c.startswith("sys")]
    usrc = [c for c in C if c.startswith("usr")]
    seeds = sorted(C["base"]["gF"])
    D = lambda c, s: C[c]["gF"][s]["mean_p_goal"] - C[c]["uF"][s]["mean_p_goal"]
    P = lambda c, s: C[c]["gF"][s]["mean_proj"] - C[c]["uF"][s]["mean_proj"]
    Pr = lambda c, s, k: C[c]["gF"][s]["mean_proj_r"][k] - C[c]["uF"][s]["mean_proj_r"][k]
    arm = lambda cs, f, s: mean([f(c, s) for c in cs])
    dD = [arm(sysc, D, s) - arm(usrc, D, s) for s in seeds]
    dP = [arm(sysc, P, s) - arm(usrc, P, s) for s in seeds]
    K = len(C["base"]["gF"][seeds[0]].get("mean_proj_r", []))
    t_null = sorted(abs(tstat([mean([Pr(c, s, k) for c in sysc]) - mean([Pr(c, s, k) for c in usrc]) for s in seeds]))
                    for k in range(K))
    q95 = t_null[int(0.95 * K + 0.999) - 1] if K else float("nan")
    aD = {c: mean([D(c, s) for s in seeds]) for c in sysc + usrc}
    aP = {c: mean([P(c, s) for s in seeds]) for c in sysc + usrc}
    sepD, pD = separated([aD[c] for c in usrc], [aD[c] for c in sysc])
    sepP, pP = separated([aP[c] for c in sysc], [aP[c] for c in usrc])
    r1 = mean(dD) > 0 and signflip(dD) < 0.05 and sepD
    pflip = signflip(dP)
    r2 = mean(dP) < 0 and pflip < 0.05 and sepP and abs(tstat(dP)) > q95
    verdict = ("NO_MANIPULATION" if not r1 else "AXIS_FOLLOWS" if r2 else
               "AXIS_AGAINST" if (mean(dP) > 0 and pflip < 0.05) else "LABEL_ONLY")
    cos = {c: json.load(open(os.path.join(md, c, "cos.json"))) for c in C if os.path.exists(os.path.join(md, c, "cos.json"))}
    base_D = mean([D("base", s) for s in seeds])
    base_P = mean([P("base", s) for s in seeds])
    return {"verdict": verdict, "R1": r1, "R2": r2,
            "dD": {"mean": round(mean(dD), 4), "p": round(signflip(dD), 4), "adapter_sep": sepD, "perm_p": round(pD, 3)},
            "dP": {"mean": round(mean(dP), 4), "p": round(pflip, 4), "t": round(tstat(dP), 3), "null_q95_abs_t": round(q95, 3),
                   "adapter_sep": sepP, "perm_p": round(pP, 3)},
            "adapter_D": {c: round(v, 4) for c, v in aD.items()}, "adapter_P": {c: round(v, 4) for c, v in aP.items()},
            "base_D": round(base_D, 4), "base_P": round(base_P, 4),
            "no_reminder": {c: round(mean([C[c]["1"][s]["mean_p_goal"] for s in seeds]), 4) for c in C},
            "cos_reextracted": cos}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    res = {m: model(os.path.join(a.root, m)) for m in sorted(os.listdir(a.root)) if os.path.isdir(os.path.join(a.root, m))}
    vs = [r["verdict"] for r in res.values() if r["R1"]]
    overall = ("NO_MANIPULATION" if not vs else "AXIS_FOLLOWS" if all(v == "AXIS_FOLLOWS" for v in vs) else
               "LABEL_ONLY" if all(v in ("LABEL_ONLY", "AXIS_AGAINST") for v in vs) else "MIXED")
    for m, r in res.items():
        print("==", m, r["verdict"], "dD", r["dD"], "dP", r["dP"])
    print("OVERALL", overall)
    json.dump({"models": res, "overall": overall}, open(os.path.join(a.root, "..", "r_analysis.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
