"""PREREG_J analysis, fixed before data: does the role direction track social authority within a role?

Usage: python j_analyze.py --root <out_j folder with one sub-folder per model>
Each model folder holds g_eval --probe --frames --rand 50 outputs (3-way world): 1_base, gF/uF/oF_probe and the
framed cells g-<frame>_probe and u-<frame>_probe for the headers in agp_fast.FRAMES.

Competence gate per model: p_goal(gF) - p_goal(1) >= 0.10 with sign-flip p < 0.05; otherwise the model is excluded.
Primary pairs, per included model and role (g, u): the high- and the low-source header of each dimension (auth, exp,
cons), so 6 pairs per model.
  behaviour  db = p_goal(hi) - p_goal(lo), sign-flip test; the pair is DECIDED if p < 0.05 (either sign);
  projection dp = proj(lo) - proj(hi) (text that is obeyed more should sit lower on vR, i.e. more "given");
  a decided pair AGREES if dp has the sign of db with p < 0.05, DISAGREES if it has the opposite sign with p < 0.05,
  and is UNRESOLVED otherwise.
Null: the same rule on the same decided pairs, for each of the 50 seeded random unit directions (mean_proj_r),
gives 50 null agreement rates.
Verdict: UNINFORMATIVE if fewer than 8 decided pairs; PASS if agree / decided >= 0.8 and above the 95th percentile
of the null rates (the 48th of 50, sorted); FAIL if agree / decided < 0.5; otherwise MIXED.
Reported, not gating: per model and role, the Spearman correlation across that role's 8 cells (plain, neu, six
framed) between mean p_goal and minus mean projection; the plain-role order (u, g, o) in behaviour and projection;
framed system cells that beat the plain user cell in behaviour (p < 0.05), and whether they also sit lower on vR.
Sign-flip tests: two-sided, 20,000 random sign vectors, p = (hits + 1) / 20,001, as in analyze.signflip.
"""
import argparse
import json
import os

import numpy as np

FR = ("neu", "auth_hi", "auth_lo", "exp_hi", "exp_lo", "cons_hi", "cons_lo")
DIMS = ("auth", "exp", "cons")
N_PERM = 20000


def signflip(d, seed=0):
    d = np.asarray(d, dtype=float)
    m = float(d.mean())
    s = np.random.default_rng(seed).choice((-1.0, 1.0), size=(N_PERM, d.size))
    hits = int((np.abs(s @ d / d.size) >= abs(m) - 1e-12).sum())
    return {"mean": round(m, 5), "p": round((hits + 1) / (N_PERM + 1), 5), "pos": int((d > 0).sum()), "neg": int((d < 0).sum())}


def status(db, dp):
    if dp["p"] >= 0.05:
        return "UNRESOLVED"
    return "AGREE" if (dp["mean"] > 0) == (db["mean"] > 0) else "DISAGREE"


def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    r, i = [0.0] * len(v), 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    return round(float(np.corrcoef(ranks(list(x)), ranks(list(y)))[0, 1]), 3)


def load(d):
    return {f[:-5]: {r["seed"]: r for r in json.load(open(os.path.join(d, f)))["runs"]}
            for f in os.listdir(d) if f.endswith("_probe.json") or f == "1_base.json"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    res, decided, null = {}, [], None
    for m in sorted(os.listdir(a.root)):
        d = os.path.join(a.root, m)
        if not os.path.isdir(d) or not os.path.exists(os.path.join(d, "gF_probe.json")):
            continue
        C = load(d)
        S = sorted(C["gF_probe"])
        goal = lambda c: np.array([C[c][s]["mean_p_goal"] for s in S])
        proj = lambda c: np.array([C[c][s]["mean_proj"] for s in S])
        projr = lambda c: np.array([C[c][s]["mean_proj_r"] for s in S])
        comp = signflip(goal("gF_probe") - goal("1_base"))
        r = {"n": len(S), "competence": comp, "included": comp["mean"] >= 0.10 and comp["p"] < 0.05, "pairs": {}}
        if r["included"]:
            K = projr("gF_probe").shape[1]
            null = null if null is not None else [[] for _ in range(K)]
            for ro in "gu":
                for dm in DIMS:
                    hi, lo = f"{ro}-{dm}_hi_probe", f"{ro}-{dm}_lo_probe"
                    db = signflip(goal(hi) - goal(lo))
                    dp = signflip(proj(lo) - proj(hi))
                    st = "UNDECIDED"
                    if db["p"] < 0.05:
                        st = status(db, dp)
                        decided.append(st)
                        for k in range(K):
                            null[k].append(status(db, signflip(projr(lo)[:, k] - projr(hi)[:, k])))
                    r["pairs"][f"{ro}-{dm}"] = {"behaviour": db, "projection": dp, "status": st}
                cells = [{"g": "gF_probe", "u": "uF_probe"}[ro]] + [f"{ro}-{f}_probe" for f in FR]
                r[f"spearman_{ro}"] = spearman([goal(c).mean() for c in cells], [-proj(c).mean() for c in cells])
            plain = {"u": "uF_probe", "g": "gF_probe", "o": "oF_probe"}
            r["behaviour_order"] = "".join(sorted(plain, key=lambda k: -goal(plain[k]).mean()))
            r["projection_order"] = "".join(sorted(plain, key=lambda k: proj(plain[k]).mean()))
            r["reversals"] = {}
            for f in FR:
                db = signflip(goal(f"g-{f}_probe") - goal("uF_probe"))
                if db["p"] < 0.05 and db["mean"] > 0:
                    r["reversals"][f"g-{f}"] = {"behaviour": db,
                                                "lower_on_vR": bool(proj(f"g-{f}_probe").mean() < proj("uF_probe").mean())}
        res[m] = r
    n_dec, n_agree = len(decided), decided.count("AGREE")
    rate = n_agree / n_dec if n_dec else float("nan")
    null_rates = sorted(s.count("AGREE") / n_dec for s in null) if (null and n_dec) else []
    q95 = null_rates[int(np.ceil(0.95 * len(null_rates))) - 1] if null_rates else float("nan")
    if n_dec < 8:
        verdict = "UNINFORMATIVE"
    elif rate >= 0.8 and rate > q95:
        verdict = "PASS"
    elif rate < 0.5:
        verdict = "FAIL"
    else:
        verdict = "MIXED"
    print(json.dumps({"verdict": verdict, "decided_pairs": n_dec, "agree": n_agree, "disagree": decided.count("DISAGREE"),
                      "unresolved": decided.count("UNRESOLVED"), "agree_rate": round(rate, 3),
                      "null_q95": round(q95, 3), "null_median": round(float(np.median(null_rates)), 3) if null_rates else None,
                      "models": res}, indent=1))


if __name__ == "__main__":
    main()
