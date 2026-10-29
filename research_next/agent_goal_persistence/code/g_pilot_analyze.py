"""Pilot for goal authority by steering on the 3-way world (exploratory): per model, from g_eval.py outputs.

Usage: python g_pilot_analyze.py --dir ../out_g/Qwen3-8B
Reports p_goal / p_press / p_contra for each condition, and paired sign-flip contrasts on p_goal (and p_contra):
  drift: gF - 1;  natural role gap: gF - oF;  steering: oF_dir - oF_rand, oF_dir - oF_base;
  capability preview: oF_dir - gF_base (steered own note against the system placement);
  boost: gF_boost - gF_randboost, gF_boost - gF_base.
"""
import argparse
import json
import os

from fam_analyze import mean, test


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    a = ap.parse_args()
    C = {}
    for f in sorted(os.listdir(a.dir)):
        if f.endswith(".json"):
            d = json.load(open(os.path.join(a.dir, f)))
            C[f[:-5]] = {r["seed"]: r for r in d["runs"]}
    S = sorted(next(iter(C.values())))
    res = {"conditions": {k: {m: round(mean(v[s][f"mean_p_{m}"] for s in S), 4) for m in ("goal", "press", "contra", "filler")}
                          | {"mass": round(mean(v[s]["mean_mass"] for s in S), 4)} for k, v in C.items()}}
    pairs = {"drift_gF_minus_1": ("gF_base", "1_base"), "role_gap_gF_minus_oF": ("gF_base", "oF_base"),
             "steer_oFdir_minus_oFrand": ("oF_dir", "oF_rand"), "steer_oFdir_minus_oFbase": ("oF_dir", "oF_base"),
             "capability_oFdir_minus_gFbase": ("oF_dir", "gF_base"),
             "boost_minus_randboost": ("gF_boost", "gF_randboost"), "boost_minus_gFbase": ("gF_boost", "gF_base")}
    res["contrasts"] = {}
    for name, (x, y) in pairs.items():
        if x in C and y in C:
            res["contrasts"][name] = {m: test([C[x][s][f"mean_p_{m}"] - C[y][s][f"mean_p_{m}"] for s in S])
                                      for m in ("goal", "contra")}
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
