"""PREREG_W analysis, fixed before data: does the PREREG_T source map hold in new families and sizes?

Usage: python w_analyze.py --root <out_w> [--old <out_t of PREREG_T>]

Per model, the PREREG_T rules (t_analyze.py) are applied unchanged, generalized to sweeps that skip layers:
- Curves are computed at the swept layers.
- The handoff h is the first swept layer with T_D >= 0.5 (n_layers + 1 if never).
- A_M and A_C average over the swept layers below h.
- With stride 1 this is exactly t_analyze.py (checked against PREREG_T's verdicts before sealing).

Hypotheses over the NEW models; a majority means n // 2 + 1:
  W1 dissociation:  PREREG_T's H2 is DISSOCIATED in a majority of the new models.
  W2 markers carry: among informative, sane curves (obey, believe, attribute; both pairs), the share with carrier
                    MARKER is >= 0.6. In PREREG_T it was 11 of 13.
  W3 obey later:    a model is OBEY_LATER if, in some pair where obey and attribute are both informative and sane,
                    h_obey - h_attr > 0 with its bootstrap 95% CI above 0, and no pair has the CI below 0. It is
                    OBEY_EARLIER in the mirror case, and UNDECIDED otherwise. SUPPORTED if a majority of the models
                    that have such a pair are OBEY_LATER.
  W4 no single tag: the PREREG_S behaviour rule on s_beh.py data. SUPPORTED if a majority of the new models with an
                    informative verdict are not UNIFIED; the FRAGMENTED count is reported.
  W5 content phase: a model is OBEY_CONTENT if some informative, sane obey curve has max T_C >= 0.5, and
                    ATTR_NO_CONTENT if every informative, sane attribute curve has max T_C < 0.2. SUPPORTED if a
                    majority of the models with an informative obey curve are OBEY_CONTENT, and a majority of the
                    models with an informative attribute curve are ATTR_NO_CONTENT. The relative depth of the obey
                    content peak is reported against the 0.45-0.75 band used in PREREG_U.
Reported, not gating:
- the relative obey lag (h_obey - h_attr) / n_layers against log size, within the Qwen3 ladder and the OLMo-2 ladder
  (PREREG_T's models are added with --old);
- every per-model PREREG_T verdict.
"""
import argparse
import json
import os

import numpy as np

import s_analyze as SA
import t_analyze as TA

N_BOOT = 1000
SIZES = {"Qwen3-0.6B": 0.6, "Qwen3-1.7B": 1.7, "Qwen3-4B": 4.0, "Qwen3-8B": 8.2, "Qwen3-14B": 14.8, "Qwen3-32B": 32.8,
         "OLMo-2-1124-7B-Instruct": 7.3, "OLMo-2-1124-13B-Instruct": 13.7, "OLMo-2-0325-32B-Instruct": 32.2}


def curves(don, rec, pat, alls, idx):
    gap = (don[idx] - rec[idx]).mean()
    T = {s: np.array([(row[idx] - rec[idx]).mean() / gap for row in pat[s]]) for s in pat}
    A = {l: float((v[idx] - rec[idx]).mean() / gap) for l, v in alls.items()}
    return T, A


def summ(T, layers, nl):
    hit = [l for l, v in zip(layers, T["D"]) if v >= 0.5]
    h = hit[0] if hit else nl + 1
    if h == 1:
        return h, "NONE", 0.0, 0.0
    pre = [i for i, l in enumerate(layers) if l < h]
    am, ac = float(np.mean(T["M"][pre])), float(np.mean(T["C"][pre]))
    if am >= 2 * ac and am >= 0.2:
        c = "MARKER"
    elif ac >= 2 * am and ac >= 0.2:
        c = "CONTENT"
    elif am >= 0.2 and ac >= 0.2:
        c = "SHARED"
    else:
        c = "WEAK"
    return h, c, am, ac


def model_map(R):
    nl = R["n_layers"]
    layers = R.get("swept") or list(range(1, nl + 1))
    kinds = {it["id"]: it["kind"] for it in R["items"]}
    mres, ob_bel, dis, shared, n_comp = {}, [], False, True, 0
    for pair, P in R["pairs"].items():
        pres, info = {}, {}
        for b, (rk, ik) in {"obey": ("beh", "obey"), "believe": ("beh", "believe"), "attribute": ("attr", None)}.items():
            rr = P[rk]
            jobs = [tuple(j) for j in rr["jobs"]]
            keep = [i for i in dict.fromkeys(j[0] for j in jobs) if ik is None or kinds[i] == ik]
            don, rec = TA.by_item(jobs, rr["donor"], keep), TA.by_item(jobs, rr["recip"], keep)
            pat = {s: np.stack([TA.by_item(jobs, rr["patched"][s][l - 1], keep) for l in layers]) for s in ("M", "C", "D")}
            alls = {int(l): TA.by_item(jobs, v, keep) for l, v in rr["all"].items()}
            gm, p = TA.signflip(don - rec)
            inf = abs(gm) >= 0.05 and p < 0.05
            r = {"gap": round(gm, 4), "p": round(p, 5), "informative": inf, "n_items": len(keep)}
            if inf:
                T, A = curves(don, rec, pat, alls, np.arange(len(keep)))
                h, c, am, ac = summ(T, layers, nl)
                sane = all(0.9 <= v <= 1.1 for v in A.values())
                rng = np.random.default_rng(0)
                boots = []
                for _ in range(N_BOOT):
                    bi = rng.integers(0, len(keep), len(keep))
                    if abs((don[bi] - rec[bi]).mean()) < 1e-9:
                        boots.append(np.nan)
                        continue
                    boots.append(summ(curves(don, rec, pat, alls, bi)[0], layers, nl)[0])
                kc = int(np.argmax(T["C"]))
                r.update({"curves": {s: [round(float(x), 3) for x in T[s]] for s in T}, "layers": layers,
                          "all_check": {l: round(v, 3) for l, v in A.items()}, "sane": sane, "handoff": h, "carrier": c,
                          "A_M": round(am, 3), "A_C": round(ac, 3), "max_T_C": round(float(T["C"][kc]), 3),
                          "max_T_C_depth": round(layers[kc] / nl, 3)})
                info[b] = (h, c, np.array(boots), sane, float(T["C"][kc]))
            pres[b] = r
        ok = {b: v for b, v in info.items() if v[3]}
        comps, names = {}, sorted(ok)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                x, y = ok[names[i]], ok[names[j]]
                d = x[2] - y[2]
                d = d[~np.isnan(d)]
                lo, hi = (np.percentile(d, 2.5), np.percentile(d, 97.5)) if d.size else (np.nan, np.nan)
                di = (x[1] != y[1] and {x[1], y[1]} <= {"MARKER", "CONTENT"}) or (abs(x[0] - y[0]) >= 3 and (lo > 0 or hi < 0))
                same = x[1] == y[1] and abs(x[0] - y[0]) <= 2
                comps[f"{names[i]}-{names[j]}"] = {"handoff_diff": x[0] - y[0], "ci95": [round(float(lo), 2), round(float(hi), 2)],
                                                  "carriers": [x[1], y[1]], "dissociated": bool(di), "same": bool(same)}
                dis |= bool(di)
                shared &= bool(same)
                n_comp += 1
        pres["comparisons"] = comps
        pres["excluded_insane"] = [b for b, v in info.items() if not v[3]]
        for b in ("obey", "believe"):
            if b in ok:
                ob_bel.append(ok[b][1])
        mres[pair] = (pres, ok)
    h1 = ("MARKER" if ob_bel and all(c == "MARKER" for c in ob_bel) else
          "CONTENT" if ob_bel and all(c == "CONTENT" for c in ob_bel) else "MIXED")
    h2 = "DISSOCIATED" if dis else "SHARED" if (shared and n_comp) else "UNCLEAR"
    return mres, h1, h2, nl


def frag(B):
    rows, auth, attr, info = B["rows"], {}, {}, {}
    for kind in ("obey", "believe"):
        auth[kind] = {s: float(np.mean(list(SA.per_item(rows, kind, s, "score").values()))) for s in SA.SOURCES}
        A = auth[kind]
        hi, lo = max(A, key=A.get), min(A, key=A.get)
        x, y = SA.per_item(rows, kind, hi, "score"), SA.per_item(rows, kind, lo, "score")
        t = SA.signflip([x[k] - y[k] for k in x])
        info[kind] = (A[hi] - A[lo] >= 0.05) and t["p"] < 0.05
    for s in SA.SOURCES:
        attr[s] = float(np.mean(list(SA.per_item(rows, None, s, "attr").values())))
    tau = SA.kendall([auth["obey"][s] for s in SA.SOURCES], [auth["believe"][s] for s in SA.SOURCES])
    ma = float(np.mean(list(attr.values())))
    if not (info["obey"] and info["believe"]):
        v = "UNINFORMATIVE"
    elif tau >= 0.6 and ma >= 0.6:
        v = "UNIFIED"
    elif tau <= 0.2 or ma <= 0.3:
        v = "FRAGMENTED"
    else:
        v = "MIXED"
    return {"verdict": v, "kendall_tau": round(tau, 3), "mean_attribution": round(ma, 4),
            "authority": {k: {s: round(x, 4) for s, x in A.items()} for k, A in auth.items()},
            "attribution": {s: round(x, 4) for s, x in attr.items()}}


def lag(mres, nl):
    out = {}
    for pair, (pres, ok) in mres.items():
        if "obey" in ok and "attribute" in ok:
            out[pair] = round((ok["obey"][0] - ok["attribute"][0]) / nl, 4)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--old")
    a = ap.parse_args()
    new, old = {}, {}
    for root, store in ((a.root, new), (a.old, old)):
        if not root:
            continue
        for m in sorted(os.listdir(root)):
            f = os.path.join(root, m, "patch.json")
            if os.path.exists(f):
                store[m] = model_map(json.load(open(f)))
    out, w1, curves_n, curves_m, w3, w5o, w5a = {}, [], 0, 0, [], [], []
    for m, (mres, h1, h2, nl) in new.items():
        r = {"H1": h1, "H2": h2, "pairs": {}}
        later = earlier = False
        oc, has_o, ac_ok, has_a = False, False, True, False
        for pair, (pres, ok) in mres.items():
            r["pairs"][pair] = pres
            for b, v in ok.items():
                curves_n += 1
                curves_m += v[1] == "MARKER"
            if "obey" in ok and "attribute" in ok:
                d = ok["obey"][2] - ok["attribute"][2]
                d = d[~np.isnan(d)]
                if d.size:
                    lo, hi = np.percentile(d, 2.5), np.percentile(d, 97.5)
                    later |= bool(lo > 0 and ok["obey"][0] > ok["attribute"][0])
                    earlier |= bool(hi < 0 and ok["obey"][0] < ok["attribute"][0])
            if "obey" in ok:
                has_o = True
                oc |= ok["obey"][4] >= 0.5
            if "attribute" in ok:
                has_a = True
                ac_ok &= ok["attribute"][4] < 0.2
        r["W3"] = "OBEY_LATER" if later and not earlier else "OBEY_EARLIER" if earlier and not later else "UNDECIDED"
        r["W5"] = {"obey_content": oc if has_o else None, "attr_no_content": ac_ok if has_a else None}
        r["obey_lag_rel"] = lag(mres, nl)
        w1.append(h2)
        if any("obey" in ok and "attribute" in ok for _, ok in mres.values()):
            w3.append(r["W3"])
        if has_o:
            w5o.append(oc)
        if has_a:
            w5a.append(ac_ok)
        f = os.path.join(a.root, m, "behaviour.json")
        if os.path.exists(f):
            r["W4"] = frag(json.load(open(f)))
        out[m] = r
    maj = lambda n: n // 2 + 1
    w4 = [out[m]["W4"]["verdict"] for m in out if "W4" in out[m] and out[m]["W4"]["verdict"] != "UNINFORMATIVE"]
    verdicts = {
        "W1": "SUPPORTED" if w1.count("DISSOCIATED") >= maj(len(w1)) else "NOT_SUPPORTED",
        "W2": "SUPPORTED" if curves_n and curves_m / curves_n >= 0.6 else "NOT_SUPPORTED",
        "W3": "SUPPORTED" if w3 and w3.count("OBEY_LATER") >= maj(len(w3)) else "NOT_SUPPORTED",
        "W4": "SUPPORTED" if w4 and sum(v != "UNIFIED" for v in w4) >= maj(len(w4)) else "NOT_SUPPORTED",
        "W5": "SUPPORTED" if (w5o and sum(w5o) >= maj(len(w5o)) and w5a and sum(w5a) >= maj(len(w5a))) else "NOT_SUPPORTED"}
    counts = {"W1_dissociated": f"{w1.count('DISSOCIATED')}/{len(w1)}", "W2_marker_curves": f"{curves_m}/{curves_n}",
              "W3_obey_later": f"{w3.count('OBEY_LATER')}/{len(w3)}", "W4_not_unified": f"{sum(v != 'UNIFIED' for v in w4)}/{len(w4)}",
              "W4_fragmented": f"{w4.count('FRAGMENTED')}/{len(w4)}",
              "W5_obey_content": f"{sum(w5o)}/{len(w5o)}", "W5_attr_no_content": f"{sum(w5a)}/{len(w5a)}"}
    trend = {}
    allm = {**{m: v for m, v in old.items()}, **new}
    for fam, pref in (("Qwen3", "Qwen3-"), ("OLMo-2", "OLMo-2-")):
        pts = []
        for m, (mres, h1, h2, nl) in allm.items():
            if m.startswith(pref) and m in SIZES:
                for pair, v in lag(mres, nl).items():
                    pts.append((SIZES[m], pair, v))
        trend[fam] = {"points": pts}
        if len({p[0] for p in pts}) >= 3:
            x, y = np.log([p[0] for p in pts]), np.array([p[2] for p in pts])
            trend[fam]["spearman"] = round(float(np.corrcoef(np.argsort(np.argsort(x)), np.argsort(np.argsort(y)))[0, 1]), 3)
    print(json.dumps({"verdicts": verdicts, "counts": counts, "per_model": {m: {k: out[m][k] for k in ("H1", "H2", "W3", "W5", "obey_lag_rel")}
                      | ({"W4": out[m]["W4"]["verdict"]} if "W4" in out[m] else {}) for m in out},
                      "trend": trend, "old_models": {m: {"H1": v[1], "H2": v[2]} for m, v in old.items()}, "models": out}, indent=1,
                     default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)))


if __name__ == "__main__":
    main()
