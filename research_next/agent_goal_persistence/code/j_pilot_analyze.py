"""Framing pilot before PREREG_J: behaviour only.

The pilot checks that social-authority headers on the goal reminder move behaviour, and that the probe ran. The
projection values are checked for presence and finiteness but never read, so the sealed test's agreement between
projection and behaviour is first seen on its own fresh seeds.

Usage: python j_pilot_analyze.py --root <out_jp folder with one sub-folder per model>
Per model: competence (gF - none); p_goal per cell; each framed cell minus the plain cell of its role; each
high-minus-low pair (authority, expertise, consensus) per role; framed system cells minus the plain user cell.
"""
import argparse
import json
import math
import os

from fam_analyze import mean, test

FR = ("neu", "auth_hi", "auth_lo", "exp_hi", "exp_lo", "cons_hi", "cons_lo")
DIMS = ("auth", "exp", "cons")


def load(d):
    return {f[:-5]: {r["seed"]: r for r in json.load(open(os.path.join(d, f)))["runs"]}
            for f in os.listdir(d) if f.endswith(".json") and not f.startswith("probe")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    res = {}
    for m in sorted(os.listdir(a.root)):
        d = os.path.join(a.root, m)
        if not os.path.isdir(d) or not os.path.exists(os.path.join(d, "gF_probe.json")):
            continue
        C = load(d)
        S = sorted(C["gF_probe"])
        g = lambda c: [C[c][s]["mean_p_goal"] for s in S]
        diff = lambda x, y: test([p - q for p, q in zip(g(x), g(y))])
        probed = ["oF_probe", "gF_probe", "uF_probe"] + [f"{r}-{f}_probe" for r in "gu" for f in FR]
        r = {"n": len(S), "competence": diff("gF_probe", "1_base"),
             "p_goal": {c: round(mean(g(c)), 4) for c in ["1_base"] + probed},
             "framed_minus_plain": {f"{r_}-{f}": diff(f"{r_}-{f}_probe", plain)
                                    for r_, plain in (("g", "gF_probe"), ("u", "uF_probe")) for f in FR},
             "hi_minus_lo": {f"{r_}-{dm}": diff(f"{r_}-{dm}_hi_probe", f"{r_}-{dm}_lo_probe")
                             for r_ in "gu" for dm in DIMS},
             "g_framed_minus_u_plain": {f: diff(f"g-{f}_probe", "uF_probe") for f in FR},
             "probe_ok": all(math.isfinite(C[c][s]["mean_proj"]) and len(C[c][s]["mean_proj_r"]) > 0
                             for c in probed for s in S)}
        res[m] = r
        print(f"\n== {m}  n {r['n']}  competence {r['competence']['mean']:+.3f} (p {r['competence']['p']})  "
              f"probe ok {r['probe_ok']}")
        print("  p_goal: " + "  ".join(f"{k.replace('_probe', '')} {v:.3f}" for k, v in r["p_goal"].items()))
        for k, t in list(r["framed_minus_plain"].items()) + list(r["hi_minus_lo"].items()):
            print(f"  {k:12s} {t['mean']:+.4f}  p {t['p']:.4f}  ({t['pos']}/{t['neg']})")
    json.dump(res, open(os.path.join(a.root, "pilot_behaviour.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
