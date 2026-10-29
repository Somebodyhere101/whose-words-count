"""PREREG_S analysis, fixed before data: is there one source monitor, or is source information fragmented?

Usage: python s_analyze.py --root <out_s folder with one sub-folder per model> [--jspace <s_jspace.json>]
Per model (src_monitor.py outputs behaviour.json and edits.json):
(a) READABLE if the leave-one-sentence-out 5-way source accuracy at the decision layer is >= 0.8 (chance 0.2).
(c) Behaviour. Per source: obey authority A_o = mean score of obey items, believe authority A_b = mean score of
    believe items (score = P(own answer) / P(own + competitor's), averaged over both orders), attribution = mean
    P(correct letter). A behaviour is INFORMATIVE if its best and worst sources differ by >= 0.05 with sign-flip
    p < 0.05 over items. UNIFIED if both are informative, Kendall tau between the two 5-source orders >= 0.6 and mean
    attribution accuracy >= 0.6; FRAGMENTED if tau <= 0.2 or mean attribution <= 0.3; UNINFORMATIVE if either
    behaviour is not informative; MIXED otherwise.
(d) Causal edit, primary scale x1. For statements in 'usr', adding c_own - c_usr should move each behaviour toward
    its 'own' value: obey and believe in the sign of base(own) - base(usr), attribution as P(letter C, 'own').
    Per item (averaged over orders): delta(edit) - delta(random), sign-flip in the predicted direction, Holm over the
    informative behaviours. CAUSALLY_UNIFIED if every informative behaviour (attribution always counts) moves as
    predicted; PARTIAL if some do; NONE if none.
Headline per model: SOURCE_MONITOR if READABLE, UNIFIED and CAUSALLY_UNIFIED; FRAGMENTED if (c) FRAGMENTED or
(d) NONE; PARTIAL otherwise. Overall: SOURCE_MONITOR if a majority of models (3 of 4), FRAGMENTED if a majority,
else PARTIAL.
(b) J-space (Qwen3-1.7B only, from s_jspace.py): reported with its own rule there.
"""
import argparse
import json
import os

import numpy as np

SOURCES = ("sys", "usr", "own", "doc", "tool")
N_PERM = 20000


def signflip(d, seed=0):
    d = np.asarray(d, dtype=float)
    m = float(d.mean())
    s = np.random.default_rng(seed).choice((-1.0, 1.0), size=(N_PERM, d.size))
    hits = int((np.abs(s @ d / d.size) >= abs(m) - 1e-12).sum())
    return {"mean": round(m, 5), "p": round((hits + 1) / (N_PERM + 1), 5)}


def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    out, run = [0.0] * len(ps), 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - r) * ps[i]))
        out[i] = run
    return out


def kendall(x, y):
    n, c, d = len(x), 0, 0
    for i in range(n):
        for j in range(i + 1, n):
            s = np.sign(x[i] - x[j]) * np.sign(y[i] - y[j])
            c += s > 0
            d += s < 0
    return (c - d) / (n * (n - 1) / 2)


def per_item(rows, kind, src, key):
    """item id -> value averaged over the two orders."""
    acc = {}
    for r in rows:
        if r["src"] == src and (kind is None or r["kind"] == kind):
            acc.setdefault(r["id"], []).append(r[key])
    return {k: float(np.mean(v)) for k, v in acc.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--jspace")
    a = ap.parse_args()
    res, heads = {}, []
    for m in sorted(os.listdir(a.root)):
        d = os.path.join(a.root, m)
        if not os.path.exists(os.path.join(d, "edits.json")):
            continue
        B = json.load(open(os.path.join(d, "behaviour.json")))
        E = json.load(open(os.path.join(d, "edits.json")))["edits"]
        rows, L = B["rows"], str(B["layer"])
        acc = B["probe_acc"][L]
        r = {"probe_acc": B["probe_acc"], "readable": acc >= 0.8, "authority": {}, "attribution": {}}
        for kind in ("obey", "believe"):
            r["authority"][kind] = {s: round(float(np.mean(list(per_item(rows, kind, s, "score").values()))), 4) for s in SOURCES}
        r["attribution"] = {s: round(float(np.mean(list(per_item(rows, None, s, "attr").values()))), 4) for s in SOURCES}
        info = {}
        for kind in ("obey", "believe"):
            A = r["authority"][kind]
            hi, lo = max(A, key=A.get), min(A, key=A.get)
            x, y = per_item(rows, kind, hi, "score"), per_item(rows, kind, lo, "score")
            t = signflip([x[k] - y[k] for k in x])
            info[kind] = (A[hi] - A[lo] >= 0.05) and t["p"] < 0.05
            r[f"{kind}_range"] = {"best": hi, "worst": lo, **t}
        tau = kendall([r["authority"]["obey"][s] for s in SOURCES], [r["authority"]["believe"][s] for s in SOURCES])
        mean_attr = float(np.mean(list(r["attribution"].values())))
        r["kendall_tau"], r["mean_attribution"] = round(tau, 3), round(mean_attr, 4)
        if not (info["obey"] and info["believe"]):
            beh = "UNINFORMATIVE"
        elif tau >= 0.6 and mean_attr >= 0.6:
            beh = "UNIFIED"
        elif tau <= 0.2 or mean_attr <= 0.3:
            beh = "FRAGMENTED"
        else:
            beh = "MIXED"
        r["behaviour_verdict"] = beh
        # causal edit, usr -> own at x1 against the random edit
        ed, rd = E["usr2own_x1"], E["usr_rand_x1"]
        tests, names = [], []
        for kind in ("obey", "believe"):
            if not info[kind]:
                continue
            sign = np.sign(r["authority"][kind]["own"] - r["authority"][kind]["usr"])
            if sign == 0:
                continue
            b, e, q = (per_item(x, kind, "usr", "score") for x in (rows, ed, rd))
            tests.append(signflip([sign * ((e[k] - b[k]) - (q[k] - b[k])) for k in b]))
            names.append(kind)
        pc = lambda rows_: {k: v for k, v in per_item([dict(x, c=x["attr_dist"][2]) for x in rows_], None, "usr", "c").items()}
        b, e, q = pc(rows), pc(ed), pc(rd)
        tests.append(signflip([(e[k] - b[k]) - (q[k] - b[k]) for k in b]))
        names.append("attribution_to_own")
        hp = holm([t["p"] for t in tests])
        moved = []
        for nm, t, p in zip(names, tests, hp):
            t["p_holm"] = round(p, 5)
            t["moved"] = t["mean"] > 0 and p < 0.05
            moved.append(t["moved"])
        r["edit_tests"] = dict(zip(names, tests))
        r["edit_verdict"] = "CAUSALLY_UNIFIED" if all(moved) else "PARTIAL" if any(moved) else "NONE"
        if r["readable"] and beh == "UNIFIED" and r["edit_verdict"] == "CAUSALLY_UNIFIED":
            h = "SOURCE_MONITOR"
        elif beh == "FRAGMENTED" or r["edit_verdict"] == "NONE":
            h = "FRAGMENTED"
        else:
            h = "PARTIAL"
        r["headline"] = h
        heads.append(h)
        res[m] = r
    need = len(heads) // 2 + 1                                       # a majority of models (3 of 4)
    overall = ("SOURCE_MONITOR" if heads.count("SOURCE_MONITOR") >= need else
               "FRAGMENTED" if heads.count("FRAGMENTED") >= need else "PARTIAL")
    out = {"overall": overall, "models": res}
    if a.jspace and os.path.exists(a.jspace):
        out["jspace"] = json.load(open(a.jspace))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
