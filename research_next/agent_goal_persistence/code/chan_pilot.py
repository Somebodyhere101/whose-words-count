"""CHANNEL manipulation check, run in-pod before any sealed seed (rules in ../CHANNEL.md).

Usage: python chan_pilot.py --root <out_chan_pilot with one folder per pilot model>
Each folder holds g_eval --chanpilot outputs on held-out seeds 9390-9399: cell 1 (no reminder) in ch0 (no pressure
lines), chU (pressure as its own user turn) and chS (as its own system turn). No reminder cell is run, so no
role contrast is seen. PROCEED if, in at least one pilot model, both p(1_ch0) - p(1_chU) and p(1_ch0) - p(1_chS) are
>= 0.10 with mean readout mass >= 0.5; otherwise STOP (the moved pressure does not bite, and the test cannot work).
"""
import argparse
import json
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    go = False
    for m in sorted(os.listdir(a.root)):
        d = os.path.join(a.root, m)
        p, mass = {}, []
        for ch in ("0", "U", "S"):
            runs = json.load(open(os.path.join(d, f"1_ch{ch}.json")))["runs"]
            p[ch] = sum(r["mean_p_goal"] for r in runs) / len(runs)
            mass.append(sum(r["mean_mass"] for r in runs) / len(runs))
        ok = p["0"] - p["U"] >= 0.10 and p["0"] - p["S"] >= 0.10 and min(mass) >= 0.5
        go |= ok
        print(f"{m}: p_goal none-pressure {p['0']:.3f}, user-turn pressure {p['U']:.3f}, system-turn pressure "
              f"{p['S']:.3f}; mass {min(mass):.3f}; {'bites' if ok else 'does not bite'}", flush=True)
    print("CHAN_PILOT", "PROCEED" if go else "STOP", flush=True)


if __name__ == "__main__":
    main()
