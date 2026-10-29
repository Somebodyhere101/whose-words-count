"""Binding pilot E2 (rules in PLAN_7DAY.md 2026-10-27 18:10): dose series, shortcut test, injection by dose.

Usage: python e2_analyze.py --root <out_le2 folder> --seeds 300-339
"""
import argparse
import json
import os

from fam_analyze import mean, test

TAGS = ("base", "own16", "given16", "own48", "given48", "own240", "given240")


def cells(d, conds, seeds):
    return {c: [json.load(open(os.path.join(d, f"c{c}_s{s}.json")))["mean_p_hi"] for s in seeds] for c in conds}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--seeds", default="300-339")
    a = ap.parse_args()
    lo, hi = map(int, a.seeds.split("-"))
    seeds = range(lo, hi + 1)
    n = len(seeds)
    Y = {t: cells(os.path.join(a.root, f"fast_{t}"), ("1", "gF", "oF"), seeds) for t in TAGS
         if os.path.isdir(os.path.join(a.root, f"fast_{t}"))}
    gap = {t: [Y[t]["oF"][i] - Y[t]["gF"][i] for i in range(n)] for t in Y}
    res = {"fast": {}, "doses": {}, "swap": {}, "injection": {}, "training": {}}
    for t in Y:
        m = {c: mean(v) for c, v in Y[t].items()}
        res["fast"][t] = {"means": {c: round(x, 4) for c, x in m.items()}, "G": test(gap[t]),
                          "competence": round(m["1"] - m["gF"], 4),
                          "R": round((m["oF"] - m["gF"]) / (m["1"] - m["gF"]), 4) if m["1"] - m["gF"] > 0.05 else None}
    measurable = None
    for d in (16, 48, 240):
        o, g = f"own{d}", f"given{d}"
        if o in Y and g in Y:
            ok = res["fast"][o]["competence"] >= 0.3 and res["fast"][g]["competence"] >= 0.3
            res["doses"][d] = {"measurable": ok, "own_minus_given_gap": test([gap[o][i] - gap[g][i] for i in range(n)])}
            if ok:
                measurable = d
    res["measurable_dose"] = measurable
    if measurable:
        c = res["doses"][measurable]["own_minus_given_gap"]
        res["role_specific_direction_ok"] = c["mean"] < 0
    S = {t: cells(os.path.join(a.root, f"swap_{t}"), ("1", "gF"), seeds) for t in ("base", "own240", "given240")
         if os.path.isdir(os.path.join(a.root, f"swap_{t}"))}
    for t in S:
        res["swap"][t] = {c: round(mean(v), 4) for c, v in S[t].items()}
    for t in ("own240", "given240"):
        if t in S and "base" in S:
            d = test([S[t]["1"][i] - S["base"]["1"][i] for i in range(n)])
            res["swap"][f"{t}_minus_base_cell1"] = d
            res["swap"][f"{t}_verdict"] = ("SHORTCUT" if d["mean"] > 0.10 else "GOAL-FOLLOWING" if d["mean"] <= 0.05 else "UNCLEAR")
    inj = {t: json.load(open(os.path.join(a.root, f"inj_{t}.json")))["places"] for t in TAGS
           if os.path.exists(os.path.join(a.root, f"inj_{t}.json"))}
    for t in inj:
        res["injection"][t] = {p: round(x["mean_p_code"], 4) for p, x in inj[t].items()}
        res["injection"][t]["legit_none"] = round(inj[t]["none"]["mean_p_legit"], 4)
        if t != "base" and "base" in inj:
            res["injection"][t]["asst_minus_base"] = test([u - w for u, w in zip(inj[t]["asst"]["p_code"], inj["base"]["asst"]["p_code"])])
    for t in TAGS[1:]:
        f = os.path.join(a.root, f"lora_{t}", "train_log.json")
        if os.path.exists(f):
            x = json.load(open(f))
            res["training"][t] = {k: x[k] for k in ("steps", "loss_first20", "loss_last20", "sec")}
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
