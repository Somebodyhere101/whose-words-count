"""PREREG_T analysis, fixed before data: where is the source signal that each behaviour uses?

Usage: python t_analyze.py --root <out_t folder with one sub-folder per model holding patch.json>
Per model, pair (own->usr, sys->usr) and behaviour b (obey = behaviour prompts of instruction items, believe = behaviour
prompts of fact items, attribute = attribution prompts of all items), values are averaged over the two orders per item.
- gap = mean(donor - recipient). INFORMATIVE if |gap| >= 0.05 with sign-flip p < 0.05 over items.
- Transfer T_s(l) = mean(patched_s,l - recipient) / gap, for s in M (marker tokens), C (content tokens), D (after the turn).
- Sanity: T_ALL within [0.9, 1.1] at the check layers; a model-pair failing it for an informative behaviour is excluded.
- Handoff h = the first layer with T_D(l) >= 0.5 (n_layers + 1 if never).
- Carrier before the handoff: A_M = mean of T_M(l) over l < h, A_C likewise. MARKER if A_M >= 2 A_C and A_M >= 0.2;
  CONTENT if A_C >= 2 A_M and A_C >= 0.2; SHARED if both >= 0.2 otherwise; WEAK if both < 0.2; NONE if h = 1.
- Bootstrap over items (1000 resamples, seed 0) for handoff layers and their within-pair differences.
H1 (where obeying and believing read the source): a model is MARKER if every informative obey/believe curve (both pairs)
   is MARKER, CONTENT if every one is CONTENT. Overall MARKER_CARRIES or CONTENT_CARRIES if a majority of models
   (3 of 4) agree, else MIXED.
H2 (do behaviours read it differently): a model is DISSOCIATED if, within a pair, two informative behaviours have
   different carriers both in {MARKER, CONTENT}, or handoff layers that differ by >= 3 with the bootstrap 95% CI of the
   difference excluding 0. SHARED if, in every pair, all informative behaviours share one carrier and handoffs within
   2 layers. UNCLEAR otherwise. Overall DISSOCIATED or SHARED by majority (3 of 4), else UNCLEAR.
"""
import argparse
import json
import os

import numpy as np

N_PERM, N_BOOT = 20000, 1000


def signflip(d, seed=0):
    d = np.asarray(d, dtype=float)
    m = float(d.mean())
    s = np.random.default_rng(seed).choice((-1.0, 1.0), size=(N_PERM, d.size))
    return m, (int((np.abs(s @ d / d.size) >= abs(m) - 1e-12).sum()) + 1) / (N_PERM + 1)


def by_item(jobs, vals, keep):
    """item id -> mean over orders, for item ids in keep (ordered as keep)."""
    acc = {}
    for (iid, _), v in zip(jobs, vals):
        if iid in keep:
            acc.setdefault(iid, []).append(v)
    return np.array([np.mean(acc[i]) for i in keep])


def curves(don, rec, pat, alls, idx):
    """Transfer curves for the item subset idx (array of row indices)."""
    gap = (don[idx] - rec[idx]).mean()
    T = {s: np.array([(pat[s][l][idx] - rec[idx]).mean() / gap for l in range(pat[s].shape[0])]) for s in pat}
    A = {l: float((v[idx] - rec[idx]).mean() / gap) for l, v in alls.items()}
    return T, A


def summarize(T, nl):
    hit = np.nonzero(T["D"] >= 0.5)[0]
    h = int(hit[0]) + 1 if hit.size else nl + 1
    if h == 1:
        return h, "NONE", 0.0, 0.0
    am, ac = float(T["M"][:h - 1].mean()), float(T["C"][:h - 1].mean())
    if am >= 2 * ac and am >= 0.2:
        c = "MARKER"
    elif ac >= 2 * am and ac >= 0.2:
        c = "CONTENT"
    elif am >= 0.2 and ac >= 0.2:
        c = "SHARED"
    else:
        c = "WEAK"
    return h, c, am, ac


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    out, h1s, h2s = {}, [], []
    for m in sorted(os.listdir(a.root)):
        f = os.path.join(a.root, m, "patch.json")
        if not os.path.exists(f):
            continue
        R = json.load(open(f))
        nl = R["n_layers"]
        kinds = {it["id"]: it["kind"] for it in R["items"]}
        mres, ob_bel_carriers, model_dis, model_shared, n_comp = {}, [], False, True, 0
        for pair, P in R["pairs"].items():
            pres, info = {}, {}
            for b, (rk, ik) in {"obey": ("beh", "obey"), "believe": ("beh", "believe"), "attribute": ("attr", None)}.items():
                rr = P[rk]
                jobs = [tuple(j) for j in rr["jobs"]]
                keep = [i for i in dict.fromkeys(j[0] for j in jobs) if ik is None or kinds[i] == ik]
                don, rec = by_item(jobs, rr["donor"], keep), by_item(jobs, rr["recip"], keep)
                pat = {s: np.stack([by_item(jobs, rr["patched"][s][l], keep) for l in range(nl)]) for s in ("M", "C", "D")}
                alls = {int(l): by_item(jobs, v, keep) for l, v in rr["all"].items()}
                gm, p = signflip(don - rec)
                inf = abs(gm) >= 0.05 and p < 0.05
                r = {"gap": round(gm, 4), "p": round(p, 5), "informative": inf, "n_items": len(keep)}
                if inf:
                    idx = np.arange(len(keep))
                    T, A = curves(don, rec, pat, alls, idx)
                    h, c, am, ac = summarize(T, nl)
                    sane = all(0.9 <= v <= 1.1 for v in A.values())
                    rng = np.random.default_rng(0)
                    boots = []
                    for _ in range(N_BOOT):
                        bi = rng.integers(0, len(keep), len(keep))
                        if abs((don[bi] - rec[bi]).mean()) < 1e-9:
                            boots.append(np.nan)
                            continue
                        boots.append(summarize(curves(don, rec, pat, alls, bi)[0], nl)[0])
                    r.update({"curves": {s: [round(float(x), 3) for x in T[s]] for s in T}, "all_check": {l: round(v, 3) for l, v in A.items()},
                              "sane": sane, "handoff": h, "carrier": c, "A_M": round(am, 3), "A_C": round(ac, 3)})
                    info[b] = (h, c, np.array(boots), sane)
                pres[b] = r
            # within-pair comparisons among informative, sane behaviours
            ok = {b: v for b, v in info.items() if v[3]}
            comps = {}
            names = sorted(ok)
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    x, y = ok[names[i]], ok[names[j]]
                    d = x[2] - y[2]
                    d = d[~np.isnan(d)]
                    lo, hi = (np.percentile(d, 2.5), np.percentile(d, 97.5)) if d.size else (np.nan, np.nan)
                    dis = (x[1] != y[1] and {x[1], y[1]} <= {"MARKER", "CONTENT"}) or (abs(x[0] - y[0]) >= 3 and (lo > 0 or hi < 0))
                    same = x[1] == y[1] and abs(x[0] - y[0]) <= 2
                    comps[f"{names[i]}-{names[j]}"] = {"handoff_diff": x[0] - y[0], "ci95": [round(float(lo), 2), round(float(hi), 2)],
                                                      "carriers": [x[1], y[1]], "dissociated": bool(dis), "same": bool(same)}
                    model_dis |= bool(dis)
                    model_shared &= bool(same)
                    n_comp += 1
            pres["comparisons"] = comps
            pres["excluded_insane"] = [b for b, v in info.items() if not v[3]]
            for b in ("obey", "believe"):
                if b in ok:
                    ob_bel_carriers.append(ok[b][1])
            mres[pair] = pres
        h1 = ("MARKER" if ob_bel_carriers and all(c == "MARKER" for c in ob_bel_carriers) else
              "CONTENT" if ob_bel_carriers and all(c == "CONTENT" for c in ob_bel_carriers) else "MIXED")
        h2 = "DISSOCIATED" if model_dis else "SHARED" if (model_shared and n_comp) else "UNCLEAR"   # SHARED needs a comparison
        mres["H1"], mres["H2"] = h1, h2
        h1s.append(h1)
        h2s.append(h2)
        out[m] = mres
    need = len(h1s) // 2 + 1
    o1 = "MARKER_CARRIES" if h1s.count("MARKER") >= need else "CONTENT_CARRIES" if h1s.count("CONTENT") >= need else "MIXED"
    o2 = "DISSOCIATED" if h2s.count("DISSOCIATED") >= need else "SHARED" if h2s.count("SHARED") >= need else "UNCLEAR"
    print(json.dumps({"overall_H1": o1, "overall_H2": o2, "per_model": {m: {"H1": out[m]["H1"], "H2": out[m]["H2"]} for m in out},
                      "models": out}, indent=1))


if __name__ == "__main__":
    main()
