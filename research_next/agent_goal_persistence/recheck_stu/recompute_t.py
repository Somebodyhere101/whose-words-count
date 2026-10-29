"""Recheck of PREREG_T claims with no stored statistic, from raw patch.json files (t_analyze.py conventions).
Writes nothing in RF.
"""
import json
import os
import sys

import numpy as np

ROOT = sys.argv[1]
BEH = {"obey": ("beh", "obey"), "believe": ("beh", "believe"), "attribute": ("attr", None)}


def by_item(jobs, vals, keep):
    acc = {}
    for (iid, _), v in zip(jobs, vals):
        if iid in keep:
            acc.setdefault(iid, []).append(v)
    return np.array([np.mean(acc[i]) for i in keep])


res = {}
for m in sorted(os.listdir(ROOT)):
    R = json.load(open(os.path.join(ROOT, m, "patch.json")))
    nl = R["n_layers"]
    kinds = {it["id"]: it["kind"] for it in R["items"]}
    mr = {"n_layers": nl, "check_layers": R["check_layers"], "seed": R["seed"], "n_items": len(R["items"]),
          "n_kind": {k: sum(1 for it in R["items"] if it["kind"] == k) for k in ("obey", "believe")}}
    for pair, P in R["pairs"].items():
        pr = {"mismatch": {k: P[k]["mismatch"] for k in ("beh", "attr")}}
        for b, (rk, ik) in BEH.items():
            rr = P[rk]
            jobs = [tuple(j) for j in rr["jobs"]]
            keep = [i for i in dict.fromkeys(j[0] for j in jobs) if ik is None or kinds[i] == ik]
            don, rec = by_item(jobs, rr["donor"], keep), by_item(jobs, rr["recip"], keep)
            gap = float((don - rec).mean())
            T = {s: np.array([(by_item(jobs, rr["patched"][s][l], keep) - rec).mean() / gap for l in range(nl)]) for s in ("M", "C", "D")}
            allc = {l: float((by_item(jobs, v, keep) - rec).mean() / gap) for l, v in rr["all"].items()}
            # max |ALL - donor| per item-order row, in probability units
            dv = np.array(rr["donor"])
            max_abs = {l: float(np.max(np.abs(np.array(v) - dv))) for l, v in rr["all"].items()}
            pr[b] = {"gap": round(gap, 4), "T_C": [round(float(x), 3) for x in T["C"]], "T_M": [round(float(x), 3) for x in T["M"]],
                     "T_D": [round(float(x), 3) for x in T["D"]], "all_check": {l: round(v, 3) for l, v in allc.items()},
                     "all_max_abs_prob_diff_vs_donor": {l: round(v, 5) for l, v in max_abs.items()},
                     "maxC": round(float(T["C"].max()), 3), "argmaxC_layer": int(T["C"].argmax()) + 1}
        mr[pair] = pr
    res[m] = mr
print(json.dumps(res))
