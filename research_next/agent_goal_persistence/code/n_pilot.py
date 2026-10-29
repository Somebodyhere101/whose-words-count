"""Fix-test pilot (before PREREG_N): summarise plain / emph / steer2 / steer4 / steer8 per model and choose alpha.

Rule (logged before the pilot ran): among the steer conditions whose degenerate rate is <= plain + 0.05 and whose
mean words are within 0.5-1.5 x plain, take the one with the highest system-constraint rate (met1). GO if that rate
beats plain by >= 0.03 in at least one model; otherwise the sealed run is skipped.

Usage: python n_pilot.py --root <out_np folder>
"""
import argparse
import json
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    out, go = {}, False
    for m in sorted(os.listdir(a.root)):
        d = os.path.join(a.root, m)
        S = {}
        for f in sorted(os.listdir(d)):
            if f.endswith("_scored.json"):
                recs = json.load(open(os.path.join(d, f)))["records"]
                n = len(recs)
                S[f[:-12]] = {"n": n, "met1": round(sum(r["met1"] for r in recs) / n, 3),
                              "met2": round(sum(r["met2"] for r in recs) / n, 3),
                              "degenerate": round(sum(r["degenerate"] for r in recs) / n, 3),
                              "words": round(sum(r["words"] for r in recs) / n, 1)}
        p = S["plain"]
        ok = {c: s for c, s in S.items() if c.startswith("steer") and s["degenerate"] <= p["degenerate"] + 0.05
              and 0.5 * p["words"] <= s["words"] <= 1.5 * p["words"]}
        best = max(ok, key=lambda c: ok[c]["met1"]) if ok else None
        gain = round(ok[best]["met1"] - p["met1"], 3) if best else None
        go = go or (gain is not None and gain >= 0.03)
        out[m] = {"conditions": S, "best": best, "alpha": float(best[5:]) if best else None, "gain_vs_plain": gain}
        print(f"\n== {m}")
        for c, s in S.items():
            print(f"  {c:8s} system wins {s['met1']:.3f}  user wins {s['met2']:.3f}  degenerate {s['degenerate']:.3f}  words {s['words']:.0f}")
        print(f"  chosen: {best} (gain vs plain {gain})")
    print("\nGO" if go else "\nNO-GO: no alpha raised system adherence by >= 0.03")
    json.dump({"go": go, "models": out}, open(os.path.join(a.root, "pilot_choice.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
