"""PREREG_M analysis, fixed before data: do models obey what sounds least like themselves?

Usage: python m_analyze.py --root <out_m folder with one sub-folder per model>
Each model folder holds g_eval --probe --frames --frameset m --rand 50 outputs (3-way world): 1_base, gF/uF/oF_probe
and g-<frame>_probe, u-<frame>_probe for the minimal pairs s_/o_ of analysis, plan, fact and source.

Competence gate per model: p_goal(gF) - p_goal(1) >= 0.10 with sign-flip p < 0.05; otherwise excluded.
Two families of pairs: OWN = {analysis, plan} (self vs another person, credibility held fixed) and KNOW = {fact,
source} (established knowledge or a Nature study vs one person's claim; self-likeness against credibility).
Per model and family, per seed, averaged over the family's pairs and both roles (system, user):
  behaviour  D = p_goal(o_) - p_goal(s_)      (self-like text obeyed less => D > 0)
  projection P = proj(s_) - proj(o_) on vR    (self-like text higher on vR, toward "own" => P > 0)
H1 (OWN) and H2 (KNOW), behaviour: sign-flip test of D per model, Holm over the included models within each family.
  SUPPORTED if >= 4 models have D > 0 (Holm p < 0.05) and none has D < 0 (Holm p < 0.05); REVERSED if >= 4 have
  D < 0 and none D > 0; NOT_SUPPORTED if at most 1 model is significant either way; MIXED otherwise.
H3, representation tracks behaviour: over (model, family) cells whose D is significant (Holm p < 0.05, either sign),
  a cell AGREES if P has the sign of D with sign-flip p < 0.05 and |t| of P above the 95th percentile of |t| over the
  50 seeded random directions (same cell, same seeds); DISAGREES if P has the opposite sign with p < 0.05; otherwise
  UNRESOLVED. TRACKS if >= 4 such cells and agree / cells >= 0.8; DOES_NOT_TRACK if agree / cells < 0.5;
  UNINFORMATIVE if fewer than 4 cells; MIXED otherwise.
Headline: SELF_DISCOUNT if H1 SUPPORTED and H3 TRACKS; otherwise the three verdicts are reported as they stand.
Reported, not gating: per pair and role D and P; the plain-role order (u, g, o); replication of PREREG_J's
Nature < blog (pair 'source').
Sign-flip tests: two-sided, 20,000 random sign vectors, p = (hits + 1) / 20,001.
"""
import argparse
import json
import os

import numpy as np

FAM = {"OWN": ("analysis", "plan"), "KNOW": ("fact", "source")}
N_PERM = 20000


def signflip(d, seed=0):
    d = np.asarray(d, dtype=float)
    m = float(d.mean())
    s = np.random.default_rng(seed).choice((-1.0, 1.0), size=(N_PERM, d.size))
    hits = int((np.abs(s @ d / d.size) >= abs(m) - 1e-12).sum())
    return {"mean": round(m, 5), "p": round((hits + 1) / (N_PERM + 1), 5), "pos": int((d > 0).sum()), "neg": int((d < 0).sum())}


def tstat(d):
    d = np.asarray(d, dtype=float)
    sd = d.std(ddof=1)
    return float(d.mean() / (sd / np.sqrt(d.size))) if sd > 0 else 0.0


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    out, run = [0.0] * len(ps), 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - r) * ps[i]))
        out[i] = run
    return out


def load(d):
    return {f[:-5]: {r["seed"]: r for r in json.load(open(os.path.join(d, f)))["runs"]}
            for f in os.listdir(d) if f.endswith("_probe.json") or f == "1_base.json"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    res, inc = {}, []
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
        r = {"n": len(S), "competence": comp, "included": comp["mean"] >= 0.10 and comp["p"] < 0.05, "family": {}, "pairs": {}}
        if r["included"]:
            inc.append(m)
            for fam, pairs in FAM.items():
                cells = [(ro, p) for ro in "gu" for p in pairs]
                D = np.mean([goal(f"{ro}-o_{p}_probe") - goal(f"{ro}-s_{p}_probe") for ro, p in cells], axis=0)
                P = np.mean([proj(f"{ro}-s_{p}_probe") - proj(f"{ro}-o_{p}_probe") for ro, p in cells], axis=0)
                PR = np.mean([projr(f"{ro}-s_{p}_probe") - projr(f"{ro}-o_{p}_probe") for ro, p in cells], axis=0)
                null_t = sorted(abs(tstat(PR[:, k])) for k in range(PR.shape[1]))
                r["family"][fam] = {"D": signflip(D), "P": signflip(P), "t_P": round(tstat(P), 2),
                                    "null_t_q95": round(null_t[int(np.ceil(0.95 * len(null_t))) - 1], 2)}
            for ro in "gu":
                for p in FAM["OWN"] + FAM["KNOW"]:
                    r["pairs"][f"{ro}-{p}"] = {"D": round(float((goal(f"{ro}-o_{p}_probe") - goal(f"{ro}-s_{p}_probe")).mean()), 4),
                                               "P": round(float((proj(f"{ro}-s_{p}_probe") - proj(f"{ro}-o_{p}_probe")).mean()), 4)}
            plain = {"u": "uF_probe", "g": "gF_probe", "o": "oF_probe"}
            r["behaviour_order"] = "".join(sorted(plain, key=lambda k: -goal(plain[k]).mean()))
            r["projection_order"] = "".join(sorted(plain, key=lambda k: proj(plain[k]).mean()))
        res[m] = r
    verdicts, h3 = {}, []
    for fam, name in (("OWN", "H1_own_voice"), ("KNOW", "H2_knowledge_framing")):
        hp = holm([res[m]["family"][fam]["D"]["p"] for m in inc]) if inc else []
        pos = neg = 0
        for m, p in zip(inc, hp):
            f = res[m]["family"][fam]
            f["D"]["p_holm"] = round(p, 5)
            if p < 0.05:
                pos += f["D"]["mean"] > 0
                neg += f["D"]["mean"] < 0
                same = (f["P"]["mean"] > 0) == (f["D"]["mean"] > 0)
                if f["P"]["p"] < 0.05 and same and abs(f["t_P"]) > f["null_t_q95"]:
                    st = "AGREE"
                elif f["P"]["p"] < 0.05 and not same:
                    st = "DISAGREE"
                else:
                    st = "UNRESOLVED"
                f["H3_status"] = st
                h3.append(st)
        if pos >= 4 and neg == 0:
            v = "SUPPORTED"
        elif neg >= 4 and pos == 0:
            v = "REVERSED"
        elif pos + neg <= 1:
            v = "NOT_SUPPORTED"
        else:
            v = "MIXED"
        verdicts[name] = {"verdict": v, "positive": pos, "negative": neg, "models": len(inc)}
    n3, a3 = len(h3), h3.count("AGREE")
    rate = a3 / n3 if n3 else float("nan")
    v3 = "UNINFORMATIVE" if n3 < 4 else "TRACKS" if rate >= 0.8 else "DOES_NOT_TRACK" if rate < 0.5 else "MIXED"
    verdicts["H3_representation"] = {"verdict": v3, "cells": n3, "agree": a3, "disagree": h3.count("DISAGREE"),
                                     "unresolved": h3.count("UNRESOLVED"), "agree_rate": round(rate, 3)}
    head = "SELF_DISCOUNT" if (verdicts["H1_own_voice"]["verdict"] == "SUPPORTED" and v3 == "TRACKS") else "SEE_COMPONENTS"
    print(json.dumps({"headline": head, "verdicts": verdicts, "models": res}, indent=1))


if __name__ == "__main__":
    main()
