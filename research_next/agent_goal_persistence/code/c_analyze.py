"""PREREG_C analysis, fixed before data: phase-A depth curves (exploratory) and the phase-B confirmatory gate.

Usage: python c_analyze.py --root <folder holding out_cA_<model> and out_cB_<model>>
Phase B gate per model, at the layer phase A selected (selection.json), seeds 500-539, alpha 2:
  (a) own text pushed toward given lowers p_hi vs own base by >= 0.05, and the drop beyond the random control is > 0
      with sign-flip p < 0.05 after Holm across the models that reach phase B;
  (b) given text pushed toward own raises p_hi vs given base by >= 0.05, beyond random likewise;
  (c) mean ticker mass of each steered cell >= 80% of its base.
Verdicts: PASS; PRESENT BUT WEAK (both beyond-random tests pass, a shift is under 0.05); NOT FOUND (otherwise).
A model whose readouts exceed its context window (OLMo: 4,096) is marked INVALID.
"""
import argparse
import json
import os

from fam_analyze import holm, mean, test

MODELS = (("OLMo-2-1124-7B-Instruct", "gF", "oF", 4096), ("granite-3.3-8b-instruct", "gW", "oW", None),
          ("SmolLM3-3B", "gW", "oW", None))


def load(d, n):
    return {r["seed"]: r for r in json.load(open(os.path.join(d, n + ".json")))["runs"]}


def contrast(d, L, g, o):
    out = {}
    for cell, sg, want in ((o, "-", -1), (g, "+", 1)):
        b, dd, rr = load(d, f"{cell}_base"), load(d, f"{cell}_L{L}_dir_a{sg}2"), load(d, f"{cell}_L{L}_rand_a{sg}2")
        S = sorted(b)
        out[cell] = {"push": "toward given" if cell == o else "toward own",
                     "base": round(mean(b[k]["mean_p_hi"] for k in S), 4),
                     "steered": round(mean(dd[k]["mean_p_hi"] for k in S), 4),
                     "random": round(mean(rr[k]["mean_p_hi"] for k in S), 4),
                     "shift": test([want * (dd[k]["mean_p_hi"] - b[k]["mean_p_hi"]) for k in S]),
                     "beyond_random": test([want * (dd[k]["mean_p_hi"] - rr[k]["mean_p_hi"]) for k in S]),
                     "mass_ratio": round(mean(dd[k]["mean_mass"] for k in S) / mean(b[k]["mean_mass"] for k in S), 4),
                     "max_ctx": max(r.get("max_ctx", 0) for x in (b, dd, rr) for r in x.values())}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    res = {"phase_A": {}, "phase_B": {}}
    for M, g, o, win in MODELS:
        dA = os.path.join(a.root, f"out_cA_{M}")
        if not os.path.isdir(dA):
            continue
        sel = json.load(open(os.path.join(dA, "selection.json")))
        layers = [r["layer"] for r in sel["rows"]]
        res["phase_A"][M] = {"selection": sel, "layers": {L: contrast(dA, L, g, o) for L in layers}}
        dB = os.path.join(a.root, f"out_cB_{M}")
        if sel["selected"] is not None and os.path.isdir(dB):
            res["phase_B"][M] = {"layer": sel["selected"], "cells": (g, o), "window": win,
                                 "contrast": contrast(dB, sel["selected"], g, o)}
    B = res["phase_B"]
    for role in (0, 1):   # 0: given cell, 1: own cell; Holm across models within each contrast
        ms = list(B)
        ps = holm([B[m]["contrast"][B[m]["cells"][role]]["beyond_random"]["p"] for m in ms])
        for m, p in zip(ms, ps):
            B[m]["contrast"][B[m]["cells"][role]]["beyond_random"]["p_holm"] = round(p, 5)
    for m, r in B.items():
        cs = list(r["contrast"].values())
        if r["window"] is not None and max(c["max_ctx"] for c in cs) > r["window"]:
            r["verdict"] = "INVALID (context window exceeded)"
            continue
        beyond = all(c["beyond_random"]["mean"] > 0 and c["beyond_random"]["p_holm"] < 0.05 for c in cs)
        big = all(c["shift"]["mean"] >= 0.05 for c in cs)
        mass = all(c["mass_ratio"] >= 0.8 for c in cs)
        r["verdict"] = "PASS" if (beyond and big and mass) else ("PRESENT BUT WEAK" if beyond else "NOT FOUND")
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
