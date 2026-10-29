"""PREREG_K analysis, fixed before data: is the role direction necessary for the authority order?

Usage: python k_analyze.py --root <out_k folder with one sub-folder per model>
Each model folder holds g_eval --ablate outputs (3-way world): 1_base and gF/uF/oF_base (plain), gF/uF/oF_abl (unit vR
projected out of the embedding and every layer output while the reminder is read) and gF/uF/oF_ablrand (the same
with the seeded random direction of g_eval).

Per model, with S = p_goal(uF) - p_goal(oF), the spread of the authority order, per seed:
  gate (else UNINFORMATIVE): competence p_goal(gF) - p_goal(1) >= 0.10 and plain S > 0, both sign-flip p < 0.05;
  guards (else INVALID): under vR ablation, the mean over placements of p_goal - p_goal(1) is >= 0.10 and >= half the
  plain value; the mean ticker mass under ablation is >= 0.8 x plain;
  T1 flattening: S_plain - S_abl > 0; T2 specificity: S_ablrand - S_abl > 0 (sign-flip; Holm over the models that pass
  gate and guards, separately for T1 and T2); F = 1 - mean(S_abl) / mean(S_plain).
  FLATTENS if T1 and T2 hold and F >= 0.5; PARTIAL if T1 and T2 hold and 0.2 <= F < 0.5; otherwise NO.
Verdict over the models that pass gate and guards: NECESSARY if at least 3 FLATTEN and they are at least 60% of those
models; NOT_NECESSARY if none FLATTENS or is PARTIAL; otherwise PARTIAL. UNINFORMATIVE if fewer than 3 such models.
Reported, not gating: the pair spreads u-g and g-o plain / ablated / random, per-placement p_goal, and ticker mass.
Sign-flip tests: two-sided, 20,000 random sign vectors, p = (hits + 1) / 20,001.
"""
import argparse
import json
import os

import numpy as np

N_PERM = 20000


def signflip(d, seed=0):
    d = np.asarray(d, dtype=float)
    m = float(d.mean())
    s = np.random.default_rng(seed).choice((-1.0, 1.0), size=(N_PERM, d.size))
    hits = int((np.abs(s @ d / d.size) >= abs(m) - 1e-12).sum())
    return {"mean": round(m, 5), "p": round((hits + 1) / (N_PERM + 1), 5), "pos": int((d > 0).sum()), "neg": int((d < 0).sum())}


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    out, run = [0.0] * len(ps), 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - r) * ps[i]))
        out[i] = run
    return out


def load(d):
    return {f[:-5]: {r["seed"]: r for r in json.load(open(os.path.join(d, f)))["runs"]}
            for f in os.listdir(d) if f.endswith(".json")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    res, ok = {}, []
    for m in sorted(os.listdir(a.root)):
        d = os.path.join(a.root, m)
        if not os.path.isdir(d) or not os.path.exists(os.path.join(d, "gF_base.json")):
            continue
        C = load(d)
        S_ = sorted(C["gF_base"])
        goal = lambda c: np.array([C[c][s]["mean_p_goal"] for s in S_])
        mass = lambda t: float(np.mean([np.mean([C[f"{c}_{t}"][s]["mean_mass"] for s in S_]) for c in ("gF", "uF", "oF")]))
        none = goal("1_base")
        spread = {t: goal(f"uF_{t}") - goal(f"oF_{t}") for t in ("base", "abl", "ablrand")}
        comp = {t: float(np.mean([goal(f"{c}_{t}").mean() for c in ("gF", "uF", "oF")]) - none.mean())
                for t in ("base", "abl", "ablrand")}
        r = {"n": len(S_), "competence": signflip(goal("gF_base") - none), "spread_plain": signflip(spread["base"]),
             "p_goal": {f"{c}_{t}": round(float(goal(f"{c}_{t}").mean()), 4) for t in ("base", "abl", "ablrand")
                        for c in ("gF", "uF", "oF")} | {"none": round(float(none.mean()), 4)},
             "competence_by_arm": {k: round(v, 4) for k, v in comp.items()},
             "mass_by_arm": {t: round(mass(t), 4) for t in ("base", "abl", "ablrand")},
             "pairs": {t: {"u-g": round(float((goal(f"uF_{t}") - goal(f"gF_{t}")).mean()), 4),
                           "g-o": round(float((goal(f"gF_{t}") - goal(f"oF_{t}")).mean()), 4)}
                       for t in ("base", "abl", "ablrand")}}
        gate = (r["competence"]["mean"] >= 0.10 and r["competence"]["p"] < 0.05 and r["spread_plain"]["mean"] > 0
                and r["spread_plain"]["p"] < 0.05)
        guards = (comp["abl"] >= 0.10 and comp["abl"] >= 0.5 * comp["base"]
                  and r["mass_by_arm"]["abl"] >= 0.8 * r["mass_by_arm"]["base"])
        r["status"] = "UNINFORMATIVE" if not gate else ("INVALID" if not guards else "TESTED")
        if r["status"] == "TESTED":
            r["T1"] = signflip(spread["base"] - spread["abl"])
            r["T2"] = signflip(spread["ablrand"] - spread["abl"])
            r["F"] = round(1 - float(spread["abl"].mean()) / float(spread["base"].mean()), 4)
            ok.append(m)
        res[m] = r
    h1 = holm([res[m]["T1"]["p"] for m in ok])
    h2 = holm([res[m]["T2"]["p"] for m in ok])
    for m, p1, p2 in zip(ok, h1, h2):
        r = res[m]
        r["T1"]["p_holm"], r["T2"]["p_holm"] = round(p1, 5), round(p2, 5)
        both = p1 < 0.05 and p2 < 0.05 and r["T1"]["mean"] > 0 and r["T2"]["mean"] > 0
        r["result"] = "FLATTENS" if (both and r["F"] >= 0.5) else "PARTIAL" if (both and r["F"] >= 0.2) else "NO"
    n_flat = sum(res[m]["result"] == "FLATTENS" for m in ok)
    n_part = sum(res[m]["result"] == "PARTIAL" for m in ok)
    if len(ok) < 3:
        verdict = "UNINFORMATIVE"
    elif n_flat >= 3 and n_flat >= 0.6 * len(ok):
        verdict = "NECESSARY"
    elif n_flat + n_part == 0:
        verdict = "NOT_NECESSARY"
    else:
        verdict = "PARTIAL"
    print(json.dumps({"verdict": verdict, "tested_models": len(ok), "flattens": n_flat, "partial": n_part,
                      "models": res}, indent=1))


if __name__ == "__main__":
    main()
