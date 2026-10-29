"""PREREG_X figure (descriptive, not a gate): attack success on SEP and InjecAgent, per model, under no defence, the
best prompt defence for that model and benchmark, the map-guided steering recipe (DEF), and DEF stacked on datamarking.

Usage: python x_plot.py --analysis <x_analysis.json> --out <png>
Palette: dataviz reference slots 1-3 (validated earlier), plus a neutral grey for the undefended baseline. Each
condition also gets its own hatch, so identity does not rest on colour alone.
"""
import argparse
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
STYLE = {"none": ("#b9b8b3", ""), "best prompt": ("#1baf7a", "//"), "steering (DEF)": ("#2a78d6", ""),
         "DEF + datamarking": ("#eb6834", "..")}
PROMPTS = ("P", "SPOT", "REMIND")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = json.load(open(a.analysis))
    models = list(d["models"])
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK})
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), facecolor=SURFACE)
    for ax, (bench, key, label) in zip(axes, (("sep", "E_data", "SEP: probe executed from the data"),
                                              ("injecagent", "ASR_valid", "InjecAgent: attacker tool called"))):
        ax.set_facecolor(SURFACE)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.grid(axis="y", color=GRID, linewidth=0.6)
        ax.set_axisbelow(True)
        x = np.arange(len(models))
        w = 0.19
        for k, (cond, (col, hatch)) in enumerate(STYLE.items()):
            vals = []
            for m in models:
                r = d["models"][m][bench]["rates"]
                if cond == "none":
                    vals.append(r["none"][key])
                elif cond == "best prompt":
                    vals.append(min(r[p][key] for p in PROMPTS))
                elif cond == "steering (DEF)":
                    vals.append(r["DEF"][key])
                else:
                    vals.append(r["DEF+SPOT"][key])
            ax.bar(x + (k - 1.5) * w, [100 * v for v in vals], w * 0.92, color=col, hatch=hatch, edgecolor=SURFACE,
                   linewidth=0.6, label=cond)
        ax.set_xticks(x, [m.replace("-Instruct", "").replace("-instruct", "") for m in models], rotation=20, ha="right")
        ax.set_ylabel("attack success (%)", color=INK)
        ax.set_title(label, fontsize=10, color=INK)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, frameon=False, fontsize=9, bbox_to_anchor=(0.5, 1.06))
    fig.tight_layout()
    fig.savefig(a.out, dpi=170, facecolor=SURFACE, bbox_inches="tight")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
