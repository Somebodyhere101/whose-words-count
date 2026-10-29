"""Preregistered analysis for run B (see ../PREREG_B.md): analyze.py with run-B cells and seeds.

Usage: python analyze_b.py ../main_b      (writes ../main_b_results.json)
"""
import json
import os
import sys

import analyze

analyze.CELLS = {"gF": ("fixed", "given"), "oF": ("fixed", "own"), "gN": ("note", "given"), "oN": ("note", "own")}
analyze.SEEDS = range(200, 240)
ALIAS = {"gF": "2", "oF": "3f", "gN": "2p", "oN": "3"}   # analyze.main's tests refer to these names

if __name__ == "__main__":
    d = sys.argv[1]
    tmp = d.rstrip("/\\") + "_alias"
    os.makedirs(tmp, exist_ok=True)
    for new, old in ALIAS.items():
        for s in analyze.SEEDS:
            f = os.path.join(d, f"c{new}_s{s}.json")
            if os.path.exists(f):
                json.dump(json.load(open(f)), open(os.path.join(tmp, f"c{old}_s{s}.json"), "w"))
    analyze.CELLS = {"2": 0, "3f": 0, "2p": 0, "3": 0}
    analyze.main(tmp)
    os.replace(os.path.join(os.path.dirname(os.path.abspath(tmp)), "main_results.json"),
               os.path.join(os.path.dirname(os.path.abspath(d)), "main_b_results.json"))
