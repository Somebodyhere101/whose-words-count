"""Goal authority by steering, on the 3-way world (AGP_WORLD=3way, see agp_fast.make_world3).

One model load, then the plan of conditions on the given seeds:
  base cells 1 (no reminder), gF (reminder as a system turn), oF (reminder as the agent's own turn), uF (user turn);
  oF with -alpha*vR while the reminder is read (own note pushed toward "given"), and with a same-norm random direction;
  gF with -alpha*vR (system note pushed further from the assistant role, "boost"), and with the random direction.
vR is the stage-2 own-minus-given direction at --layer. One JSON per condition: per run mean_p_hi (= 1 - p_goal),
mean_p_goal / press / contra / filler, mean ticker mass and the largest readout context.

Usage: python g_eval.py --model Qwen/Qwen3-8B --dirs ../dirs/dirs_q8.pt --layer 17 --seeds 1200-1219 --out ../out_g/Qwen3-8B
"""
import argparse
import json
import os
import time

import torch

import agp_batch as AB
import agp_fast as F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--dirs", help="stage-2 direction file (not needed with --plain)")
    ap.add_argument("--layer", type=int, help="layer of vR in --dirs (not needed with --plain)")
    ap.add_argument("--plain", action="store_true", help="cells 1/gF/uF/oF only, no direction (size sweep, PREREG_L)")
    ap.add_argument("--alpha", type=float, default=2.0)
    ap.add_argument("--seeds", required=True)
    ap.add_argument("--batch", type=int, default=20)
    ap.add_argument("--probe", action="store_true", help="base cells only, recording each reminder's projection on unit vR")
    ap.add_argument("--frames", action="store_true", help="with --probe: add the framed cells g:<frame> and u:<frame> "
                    "(agp_fast.FRAMES), each probed on the goal text's own tokens")
    ap.add_argument("--frameset", default="j", help="with --frames: which agp_fast.FRAMESETS entry (j: PREREG_J, m: PREREG_M)")
    ap.add_argument("--rand", type=int, default=0, help="with --probe: also project on this many seeded random unit "
                    "directions (null projections, 'mean_proj_r')")
    ap.add_argument("--ablate", action="store_true", help="cells 1/gF/uF/oF plain, then gF/uF/oF with vR projected out "
                    "at every layer while the reminder is read ('abl'), and with the same-seed random direction ('ablrand')")
    ap.add_argument("--dev", action="store_true", help="with --probe: add cell dF, the reminder as a developer turn "
                    "(harmony models, FLIP.md); with --chan: the operator reminder is dF instead of gF")
    ap.add_argument("--chan", action="store_true", help="CHANNEL.md: cell 1 with no pressure lines (ch0), then cells "
                    "1 / operator / uF with the pressure inline (chN), as its own user turn (chU), as its own --srole "
                    "turn (chS), and inline plus a neutral --srole turn (chNs, placebo); no direction")
    ap.add_argument("--chanpilot", action="store_true", help="CHANNEL.md manipulation check: cell 1 in ch0, chU, chS only")
    ap.add_argument("--srole", default="system", help="role of the chS pressure turn (developer for harmony models)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.environ["AGP_WORLD"] = "3way"
    lo, hi = map(int, a.seeds.split("-"))
    seeds = list(range(lo, hi + 1))
    os.makedirs(a.out, exist_ok=True)
    lm = AB.BatchLM(a.model, 0.7)
    if a.plain or a.chan or a.chanpilot:
        a.dirs, a.layer, a.alpha = None, None, 0.0
    v = torch.load(a.dirs)[a.layer]["vR"] if a.dirs else torch.zeros(1)
    g = torch.Generator().manual_seed(1000 + (a.layer or 0))
    r = torch.randn(v.shape, generator=g)
    rnd = r / r.norm() * v.norm()
    plan = [("1", None, "base"), ("gF", None, "base"), ("oF", None, "base"), ("uF", None, "base"),
            ("oF", (a.layer, v, -a.alpha), "dir"), ("oF", (a.layer, rnd, -a.alpha), "rand"),
            ("gF", (a.layer, v, -a.alpha), "boost"), ("gF", (a.layer, rnd, -a.alpha), "randboost")]
    probe, abl = None, {}
    if a.plain:
        plan = [("1", None, "base"), ("gF", None, "base"), ("uF", None, "base"), ("oF", None, "base")]
    if a.ablate:
        plan = [("1", None, "base"), ("gF", None, "base"), ("uF", None, "base"), ("oF", None, "base")]
        plan += [(c, None, t) for t in ("abl", "ablrand") for c in ("gF", "uF", "oF")]
        abl = {"abl": v / v.norm(), "ablrand": rnd / rnd.norm()}
    if a.probe:
        plan = [("1", None, "base"), ("gF", None, "probe"), ("oF", None, "probe"), ("uF", None, "probe")]
        probe = (a.layer, v / v.norm())
        if a.dev:
            plan.append(("dF", None, "probe"))
        if a.frames:
            plan += [(f"{r_}:{fr}", None, "probe") for r_ in ("g", "u") for fr in F.FRAMESETS[a.frameset]]
        if a.rand:
            R = torch.randn(a.rand, v.numel(), generator=torch.Generator().manual_seed(2000 + a.layer))
            probe += (R / R.norm(dim=1, keepdim=True),)
    if a.chan:   # one tag per channel, same cell names, so a seed's channels share its world and sampling stream
        op = "dF" if a.dev else "gF"
        plan = [("1", None, "ch0")] + [(c, None, "ch" + p) for p in ("N", "U", "S", "Ns") for c in ("1", op, "uF")]
    if a.chanpilot:
        plan = [("1", None, "ch0"), ("1", None, "chU"), ("1", None, "chS")]
    for cell, st, tag in plan:
        f = os.path.join(a.out, f"{cell.replace(':', '-')}_{tag}.json")
        if os.path.exists(f):
            continue
        t0, res = time.time(), []
        for i in range(0, len(seeds), a.batch):
            press = tag[2:] if tag.startswith("ch") else "N"
            for r_ in F.run_batch(cell, seeds[i:i + a.batch], lm, None, steer=st, probe=probe, ablate=abl.get(tag),
                                  press=press, srole=a.srole):
                res.append({"seed": r_["seed"], "mean_p_hi": r_["mean_p_hi"],
                            **{k: r_[k] for k in ("mean_p_goal", "mean_p_press", "mean_p_contra", "mean_p_filler")},
                            **({"mean_proj": r_["mean_proj"]} if "mean_proj" in r_ else {}),
                            **({"mean_proj_r": r_["mean_proj_r"]} if "mean_proj_r" in r_ else {}),
                            "min_mass": r_["min_mass"], "mean_mass": sum(x["mass"] for x in r_["steps"]) / len(r_["steps"]),
                            "max_ctx": max(x["ctx"] for x in r_["steps"])})
            if AB.DEV == "cuda":
                torch.cuda.empty_cache()
        json.dump({"cell": cell, "tag": tag, "layer": a.layer, "alpha": a.alpha, "model": a.model, "runs": res}, open(f, "w"))
        m = lambda k: round(sum(x[k] for x in res) / len(res), 3)
        print(f"{cell}_{tag} goal {m('mean_p_goal')} press {m('mean_p_press')} contra {m('mean_p_contra')} "
              f"mass {m('mean_mass')} {round(time.time() - t0, 1)} s", flush=True)


if __name__ == "__main__":
    main()
