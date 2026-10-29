"""Recheck of PREREG_S claims that have no stored statistic. Reads raw out_s files only; writes nothing in RF.
Uses the sealed s_analyze.py conventions: per-item values averaged over the two orders, sign-flip with seed 0, 20000 perms.
"""
import json
import os
import sys

import numpy as np

ROOT = sys.argv[1]
SOURCES = ("sys", "usr", "own", "doc", "tool")
N_PERM = 20000


def signflip(d, seed=0):
    d = np.asarray(d, dtype=float)
    m = float(d.mean())
    s = np.random.default_rng(seed).choice((-1.0, 1.0), size=(N_PERM, d.size))
    hits = int((np.abs(s @ d / d.size) >= abs(m) - 1e-12).sum())
    return m, (hits + 1) / (N_PERM + 1)


def per_item(rows, kind, src, key):
    acc = {}
    for r in rows:
        if r["src"] == src and (kind is None or r["kind"] == kind):
            acc.setdefault(r["id"], []).append(r[key] if not callable(key) else key(r))
    return {k: float(np.mean(v)) for k, v in acc.items()}


out = {}
for m in sorted(os.listdir(ROOT)):
    d = os.path.join(ROOT, m)
    B = json.load(open(os.path.join(d, "behaviour.json")))
    E = json.load(open(os.path.join(d, "edits.json")))["edits"]
    rows = B["rows"]
    A = {k: {s: float(np.mean(list(per_item(rows, k, s, "score").values()))) for s in SOURCES} for k in ("obey", "believe")}
    attr = {s: float(np.mean(list(per_item(rows, None, s, "attr").values()))) for s in SOURCES}
    r = {"authority_full": A, "attribution_full": attr}
    # attribution vs chance 0.2: per item, mean over sources and orders
    pi = {}
    for x in rows:
        pi.setdefault(x["id"], []).append(x["attr"])
    t = signflip([np.mean(v) - 0.2 for v in pi.values()])
    r["mean_attr_vs_chance"] = {"mean_minus_0.2": round(t[0], 4), "p": round(t[1], 5), "n_items": len(pi)}
    # edits: every direction and scale, every behaviour; raw and beyond-random, with fraction of the own-usr gap
    ed = {}
    for direction, src, rnd_src, tgt in (("usr2own", "usr", "usr", "own"), ("own2usr", "own", "own", "usr")):
        for sc in ("1", "2"):
            e_rows, q_rows = E[f"{direction}_x{sc}"], E[f"{rnd_src}_rand_x{sc}"]
            res = {}
            for kind in ("obey", "believe"):
                sign = np.sign(A[kind][tgt] - A[kind][src])
                b, e, q = (per_item(x, kind, src, "score") for x in (rows, e_rows, q_rows))
                raw = signflip([sign * (e[k] - b[k]) for k in b])
                br = signflip([sign * ((e[k] - b[k]) - (q[k] - b[k])) for k in b])
                gap = abs(A[kind][tgt] - A[kind][src])
                res[kind] = {"pred_sign": int(sign), "raw": round(raw[0], 5), "raw_p": round(raw[1], 5),
                             "beyond_rand": round(br[0], 5), "beyond_rand_p": round(br[1], 5),
                             "gap_own_usr": round(gap, 4), "frac_of_gap_beyond_rand": round(br[0] / gap, 3) if gap else None,
                             "frac_of_gap_raw": round(raw[0] / gap, 3) if gap else None}
            # attribution: P(letter of target) and P(letter of the statement's true source), all items
            idx = {"sys": 0, "usr": 1, "own": 2, "doc": 3, "tool": 4}
            for lab, li in (("P_target_letter", idx[tgt]), ("P_true_letter", idx[src])):
                f = lambda x, li=li: x["attr_dist"][li]
                b, e, q = (per_item(x, None, src, f) for x in (rows, e_rows, q_rows))
                raw = signflip([e[k] - b[k] for k in b])
                br = signflip([(e[k] - b[k]) - (q[k] - b[k]) for k in b])
                res[lab] = {"raw": round(raw[0], 5), "raw_p": round(raw[1], 5), "beyond_rand": round(br[0], 5),
                            "beyond_rand_p": round(br[1], 5)}
            ed[f"{direction}_x{sc}"] = res
    r["edits"] = ed
    out[m] = r
print(json.dumps(out, indent=1))
