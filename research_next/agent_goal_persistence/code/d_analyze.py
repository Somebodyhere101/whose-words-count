"""PREREG_D analysis, fixed before data: which post-training stage installs the own-text discount (OLMo-2 lineage).

Usage: python d_analyze.py --root <folder holding fast_<checkpoint> and probe_<checkpoint>>
Per size (7B, 13B) and stage (SFT, DPO, Instruct); native template; cells 1/gF/oF/uF; seeds 600-679; N_TEST 22.
  competence gate: p_hi(1) - p_hi(gF) >= 0.05 with sign-flip p < 0.01, and mean ticker mass >= 0.3;
  G_s = mean over seeds of p_hi(oF) - p_hi(gF), with its sign-flip p;
  arrival stage A = the first stage that passes the gate with G_s > 0 at p < 0.01 and G_s >= 0.5 * G_Instruct;
  amplification at stage s: paired sign-flip on the per-seed gap_s - gap_{s-1}, mean > 0 at p < 0.01.
Verdict per size:
  H-SFT          : A = SFT and no amplification at DPO or at Instruct;
  H-pref         : A = DPO or Instruct; or A = SFT with amplification at DPO or Instruct and G_Instruct >= 2 * G_SFT;
  MIXED          : A = SFT with amplification at DPO or Instruct but G_Instruct < 2 * G_SFT;
  NO GAP         : G_Instruct is not > 0 at p < 0.01 (this size cannot locate the stage);
  UNINTERPRETABLE: a stage fails the competence gate;
  INVALID        : a readout's context exceeds 4,096 tokens.
Combined: a claim needs the same verdict at 7B and 13B; otherwise AMBIGUOUS.
Exploratory: user gap uF - gF, own - none, given - none, logit-scale gap; 7B probes (best transfer, cos to Instruct vR).
"""
import argparse
import json
import math
import os

from fam_analyze import mean, test

STAGES = ("SFT", "DPO", "Instruct")
SEEDS = range(600, 680)
WINDOW = 4096


def load(d, c):
    rs = [json.load(open(os.path.join(d, f"c{c}_s{s}.json"))) for s in SEEDS]
    return [r["mean_p_hi"] for r in rs], [x for r in rs for x in r["steps"]]


def logit(p, eps=1e-4):
    p = min(max(p, eps), 1 - eps)
    return math.log(p / (1 - p))


def stage_stats(d):
    Y, steps = {}, []
    for c in ("1", "gF", "oF", "uF"):
        Y[c], st = load(d, c)
        steps += st
    n = len(Y["1"])
    gap = [Y["oF"][i] - Y["gF"][i] for i in range(n)]
    comp = test([Y["1"][i] - Y["gF"][i] for i in range(n)])
    mass = mean(x["mass"] for x in steps)
    return {"means": {c: round(mean(v), 4) for c, v in Y.items()}, "gap_per_seed": gap,
            "G": test(gap), "competence": comp, "mass_mean": round(mass, 4),
            "gate": comp["mean"] >= 0.05 and comp["p"] < 0.01 and mass >= 0.3,
            "max_ctx": max(x["ctx"] for x in steps),
            "user_gap_uF_minus_gF": test([Y["uF"][i] - Y["gF"][i] for i in range(n)]),
            "own_minus_none": test([Y["oF"][i] - Y["1"][i] for i in range(n)]),
            "given_minus_none": test([Y["gF"][i] - Y["1"][i] for i in range(n)]),
            "logit_gap": test([logit(Y["oF"][i]) - logit(Y["gF"][i]) for i in range(n)])}


def verdict(S):
    if any(s["max_ctx"] > WINDOW for s in S.values()):
        return "INVALID", None, {}
    if not all(s["gate"] for s in S.values()):
        return "UNINTERPRETABLE", None, {}
    GI = S["Instruct"]["G"]
    if not (GI["mean"] > 0 and GI["p"] < 0.01):
        return "NO GAP", None, {}
    A = next((st for st in STAGES if S[st]["G"]["mean"] > 0 and S[st]["G"]["p"] < 0.01
              and S[st]["G"]["mean"] >= 0.5 * GI["mean"]), None)
    amp = {}
    for prev, cur in (("SFT", "DPO"), ("DPO", "Instruct")):
        d = [a - b for a, b in zip(S[cur]["gap_per_seed"], S[prev]["gap_per_seed"])]
        t = test(d)
        amp[cur] = {"diff": t, "amplified": t["mean"] > 0 and t["p"] < 0.01}
    any_amp = any(v["amplified"] for v in amp.values())
    if A in ("DPO", "Instruct"):
        v = "H-pref"
    elif A == "SFT" and not any_amp:
        v = "H-SFT"
    elif A == "SFT" and any_amp:
        v = "H-pref" if GI["mean"] >= 2 * S["SFT"]["G"]["mean"] else "MIXED"
    else:
        v = "NO GAP"
    return v, A, amp


def probes(root):
    try:
        import torch
    except ImportError:
        return {"note": "torch not available"}
    out, D = {}, {}
    for st in STAGES:
        d = os.path.join(root, f"probe_OLMo-2-1124-7B-{st}")
        if not os.path.isdir(d):
            continue
        pr = json.load(open(os.path.join(d, "probe_results.json")))["layers"]
        b = max(pr, key=lambda x: min(x["T3_R_to_A_dm"], x["T3_A_to_R_dm"]))
        D[st] = torch.load(os.path.join(d, "directions.pt"))
        out[st] = {"best_layer": b["layer"], "R_to_A": round(b["T3_R_to_A_dm"], 3), "A_to_R": round(b["T3_A_to_R_dm"], 3),
                   "control": round(b["C1_sys_vs_user_to_A_dm"], 3), "T1_role_within_L10": round(pr[10]["T1_R_within_lr"], 3)}
    if "Instruct" in D:
        for st in D:
            out[st]["cos_vR_to_Instruct"] = {L: round(float(torch.nn.functional.cosine_similarity(
                D[st][L]["vR"], D["Instruct"][L]["vR"], 0)), 3) for L in (10, 15)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    res = {}
    for size in ("7B", "13B"):
        S = {}
        for st in STAGES:
            d = os.path.join(a.root, f"fast_OLMo-2-1124-{size}-{st}")
            if os.path.isdir(d):
                S[st] = stage_stats(d)
        if len(S) < 3:
            res[size] = {"verdict": "MISSING", "stages": list(S)}
            continue
        v, A, amp = verdict(S)
        for s in S.values():
            s.pop("gap_per_seed")
        res[size] = {"verdict": v, "arrival": A, "amplification": amp, "stages": S}
    vs = [res[s]["verdict"] for s in ("7B", "13B")]
    res["combined"] = vs[0] if vs[0] == vs[1] else "AMBIGUOUS"
    res["probes_7B"] = probes(a.root)
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
