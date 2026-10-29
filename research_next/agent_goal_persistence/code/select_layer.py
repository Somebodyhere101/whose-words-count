"""Phase-A layer selection for PREREG_C.md, fixed before data.

At alpha 2, per layer: b_own = mean over seeds of -(own_dir - own_rand) (the drop in p_hi beyond random),
b_given = mean of +(given_dir - given_rand) (the rise beyond random). The selected layer maximises
min(b_own, b_given); ties go to the shallower layer. Prints the layer, or NONE when that maximum is <= 0,
and writes selection.json next to the phase-A results.

Usage: python select_layer.py --dir ../out_cA_<model> --cells gF,oF
"""
import argparse
import json
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--cells", required=True)
    a = ap.parse_args()
    g, o = a.cells.split(",")

    def y(n):
        return {r["seed"]: r["mean_p_hi"] for r in json.load(open(os.path.join(a.dir, n + ".json")))["runs"]}
    layers = sorted({int(f.split("_L")[1].split("_")[0]) for f in os.listdir(a.dir) if "_L" in f})
    best, rows = None, []
    for L in layers:
        od, orr = y(f"{o}_L{L}_dir_a-2"), y(f"{o}_L{L}_rand_a-2")
        gd, gr = y(f"{g}_L{L}_dir_a+2"), y(f"{g}_L{L}_rand_a+2")
        b_own = sum(orr[s] - od[s] for s in od) / len(od)
        b_given = sum(gd[s] - gr[s] for s in gd) / len(gd)
        m = min(b_own, b_given)
        rows.append({"layer": L, "b_own": round(b_own, 4), "b_given": round(b_given, 4), "min": round(m, 4)})
        if best is None or m > best[1]:
            best = (L, m)
    sel = best[0] if best[1] > 0 else None
    json.dump({"rows": rows, "selected": sel}, open(os.path.join(a.dir, "selection.json"), "w"), indent=1)
    print(sel if sel is not None else "NONE")


if __name__ == "__main__":
    main()
