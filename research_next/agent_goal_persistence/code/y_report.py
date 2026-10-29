"""Descriptive tables for PREREG_Y (not a gate; the verdicts are y_analyze.py's).

Usage: python y_report.py --y <y_analysis.json> --x <x_analysis.json>
Prints markdown:
  1. the Qwen3 size series (1.7B and 8B from PREREG_X, 14B and 32B from PREREG_Y): SEP attack success and utility,
     InjecAgent attack success, each against the best prompt defence, with the per-model verdicts;
  2. Y2's held-out SEP models, with X1, X2 and the SEP half of X5.
"""
import argparse
import json
import sys

PROMPTS = ("P", "SPOT", "REMIND")


def pct(v):
    return f"{100 * v:.1f}%"


def sep_cells(s):
    r = s["rates"]
    best = min(PROMPTS, key=lambda c: r[c]["E_data"])
    return (f"{pct(r['none']['E_data'])} → {pct(r['DEF']['E_data'])} (U {pct(r['none']['U'])} → {pct(r['DEF']['U'])})",
            f"{best} {pct(r[best]['E_data'])}")


def ia_cells(i):
    r = i["rates"]
    best = min(PROMPTS, key=lambda c: r[c]["ASR_valid"])
    return (f"{pct(r['none']['ASR_valid'])} → {pct(r['DEF']['ASR_valid'])} (valid {pct(r['none']['valid'])} → {pct(r['DEF']['valid'])})",
            f"{best} {pct(r[best]['ASR_valid'])}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--y", required=True)
    ap.add_argument("--x", required=True)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    y, x = json.load(open(a.y)), json.load(open(a.x))
    print(f"**Y1: {y['Y1']}. Y2: {y['Y2']}.**" + (f" Missing: {', '.join(y['missing'])}." if y["missing"] else ""))
    print()
    print("| Model | Source | SEP attack none → steering (utility) | SEP best prompt | InjecAgent ASR none → steering (valid) | InjecAgent best prompt | Verdict / X6 |")
    print("|---|---|---|---|---|---|---|")
    rows = [(m, "PREREG_X", x["models"][m]) for m in ("Qwen3-1.7B", "Qwen3-8B") if m in x["models"]]
    rows += [(m, "PREREG_Y", d) for m, d in y["y1"].items() if not d.get("missing")]
    for m, src, d in rows:
        s1, s2 = sep_cells(d["sep"])
        i1, i2 = ia_cells(d["injecagent"])
        print(f"| {m} | {src} | {s1} | {s2} | {i1} | {i2} | {d['verdict']} / {d['additive']} |")
    print()
    print("| Held-out model (Y2, SEP only) | SEP attack none → steering (utility) | SEP best prompt | X1 | X2 | X5 (SEP) | Verdict |")
    print("|---|---|---|---|---|---|---|")
    for m, d in y["y2"].items():
        if d.get("missing"):
            print(f"| {m} | missing | | | | | NONE |")
            continue
        s1, s2 = sep_cells(d["sep"])
        h = d["hyp"]
        print(f"| {m} | {s1} | {s2} | {h['X1']} | {h['X2']} | {h['X5_sep']} | {d['verdict']} |")


if __name__ == "__main__":
    main()
