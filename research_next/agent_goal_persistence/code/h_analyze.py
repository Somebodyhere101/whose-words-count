"""PREREG_H analysis, fixed before data: is authority one axis? Does the role direction order system, user and own
reminders the way the agents obey them?

Usage: python h_analyze.py --root <out_h folder holding Qwen3-8B, Qwen3-14B, OLMo-2-1124-7B-Instruct>
Seeds 1400-1459 (n 60, fresh), 3-way world, cells 1 / gF / oF / uF with the probe: per run, the mean projection of the
reminder's tokens (the fixed goal text without its first and last word, identical across roles) onto unit vR at the
steering layer. Lower projection = represented more like given text.
Per model, paired sign-flip tests over seeds, each Holm-corrected across the three models:
  A1 p_goal(uF) - p_goal(gF) > 0 and A2 p_goal(gF) - p_goal(oF) > 0: the authority order user > system > own;
  P1 proj(gF) - proj(uF) > 0 and P2 proj(oF) - proj(gF) > 0: the projection order user < system < own.
Per model: ORDER REPLICATED if A1 and A2 pass. ONE AXIS if P1 and P2 pass as well. TWO FACTORS if A1 passes but the
projection order of user and system is significantly reversed (mean P1 < 0, Holm p < 0.05). Otherwise MIXED.
Overall: ONE AXIS if every model with a replicated order is ONE AXIS and there are at least two such models;
TWO FACTORS if at least two models are TWO FACTORS; otherwise MIXED.
Exploratory: per model, the across-seed correlation of projection and p_goal within each placement.
"""
import argparse
import json
import os

from fam_analyze import holm, mean, test

MODELS = ("Qwen3-8B", "Qwen3-14B", "OLMo-2-1124-7B-Instruct")


def load(d):
    return {f[:-5]: {r["seed"]: r for r in json.load(open(os.path.join(d, f)))["runs"]} for f in os.listdir(d) if f.endswith(".json")}


def corr(x, y):
    mx, my = mean(x), mean(y)
    sx = sum((a - mx) ** 2 for a in x) ** 0.5
    sy = sum((b - my) ** 2 for b in y) ** 0.5
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    R = {}
    for m in MODELS:
        d = os.path.join(a.root, m)
        if not os.path.isdir(d):
            continue
        C = load(d)
        S = sorted(C["gF_probe"])
        g = lambda c, k: [C[c][s][k] for s in S]
        R[m] = {"means": {c: {"goal": round(mean(g(c, "mean_p_goal")), 4),
                              "proj": round(mean(g(c, "mean_proj")), 4) if "mean_proj" in C[c][S[0]] else None}
                          for c in C},
                "A1_user_minus_system": test([x - y for x, y in zip(g("uF_probe", "mean_p_goal"), g("gF_probe", "mean_p_goal"))]),
                "A2_system_minus_own": test([x - y for x, y in zip(g("gF_probe", "mean_p_goal"), g("oF_probe", "mean_p_goal"))]),
                "P1_proj_system_minus_user": test([x - y for x, y in zip(g("gF_probe", "mean_proj"), g("uF_probe", "mean_proj"))]),
                "P2_proj_own_minus_system": test([x - y for x, y in zip(g("oF_probe", "mean_proj"), g("gF_probe", "mean_proj"))]),
                "within_cell_corr_proj_goal": {c: round(corr(g(c, "mean_proj"), g(c, "mean_p_goal")), 3)
                                               for c in ("gF_probe", "oF_probe", "uF_probe")}}
    ms = list(R)
    for key in ("A1_user_minus_system", "A2_system_minus_own", "P1_proj_system_minus_user", "P2_proj_own_minus_system"):
        for m, p in zip(ms, holm([R[m][key]["p"] for m in ms])):
            R[m][key]["p_holm"] = round(p, 5)
    ok = lambda t: t["mean"] > 0 and t["p_holm"] < 0.05
    verdicts = {}
    for m in ms:
        t = R[m]
        order = ok(t["A1_user_minus_system"]) and ok(t["A2_system_minus_own"])
        if order and ok(t["P1_proj_system_minus_user"]) and ok(t["P2_proj_own_minus_system"]):
            v = "ONE AXIS"
        elif ok(t["A1_user_minus_system"]) and t["P1_proj_system_minus_user"]["mean"] < 0 and t["P1_proj_system_minus_user"]["p_holm"] < 0.05:
            v = "TWO FACTORS"
        else:
            v = "MIXED"
        t["order_replicated"], t["verdict"] = order, v
        verdicts[m] = v
    rep = [m for m in ms if R[m]["order_replicated"]]
    if len(rep) >= 2 and all(verdicts[m] == "ONE AXIS" for m in rep):
        overall = "ONE AXIS"
    elif sum(v == "TWO FACTORS" for v in verdicts.values()) >= 2:
        overall = "TWO FACTORS"
    else:
        overall = "MIXED"
    print(json.dumps({"overall": overall, "order_replicated_in": rep, "verdicts": verdicts, "models": R}, indent=1))


if __name__ == "__main__":
    main()
