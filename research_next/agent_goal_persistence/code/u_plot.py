"""PREREG_U figure (descriptive, not a gate): the splice sweep. One panel per model; the change in obeying and in
believing tool text when the framed run's statement tokens are spliced in after each layer, with the sealed layer
marked and the framing (F) and prompting (P) baselines as dots at the right edge.

Usage: python u_plot.py --analysis <u_analysis.json> --out <png>
Palette: dataviz reference slots 1-2 (validated on all pairs, light); each line also has its own dash pattern.
"""
import argparse
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
OBEY, BEL = ("#2a78d6", "-"), ("#eb6834", "--")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = json.load(open(a.analysis))
    models = list(d["models"])
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK})
    fig, axes = plt.subplots(1, len(models), figsize=(3.4 * len(models), 3.2), sharey=True, facecolor=SURFACE)
    for ax, m in zip(axes, models):
        r = d["models"][m]
        sw = r["U_sweep"]
        x = [s["layer"] for s in sw]
        ax.set_facecolor(SURFACE)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.grid(axis="y", color=GRID, linewidth=0.6)
        ax.axhline(0, color=INK2, linewidth=0.6)
        ax.plot(x, [s["d_obey"] for s in sw], color=OBEY[0], linestyle=OBEY[1], linewidth=2)
        ax.plot(x, [s["d_bel"] for s in sw], color=BEL[0], linestyle=BEL[1], linewidth=2)
        ax.axvline(r["layer"], color=INK, linewidth=0.8)
        xr = max(x) + 1.5
        for c, mk in (("F", "o"), ("P", "s")):
            cc = r["conditions"][c]
            ax.plot([xr], [cc["d_obey"]], marker=mk, color=OBEY[0], markersize=7, clip_on=False)
            ax.plot([xr], [cc["d_bel"]], marker=mk, color=BEL[0], markersize=7, clip_on=False, markerfacecolor=SURFACE)
            ax.annotate(c, (xr, cc["d_obey"]), xytext=(6, 0), textcoords="offset points", va="center", fontsize=8, color=INK2)
        ax.set_xlim(1, max(x) + 3)
        ax.set_title(f"{m}\n{r['verdict']} · splice at L{r['layer']}", fontsize=9, color=INK)
        ax.set_xlabel("splice layer", color=INK2)
    axes[0].set_ylabel("change vs. plain tool output", color=INK)
    handles = [plt.Line2D([], [], color=OBEY[0], linestyle=OBEY[1], linewidth=2, label="obeying tool instructions"),
               plt.Line2D([], [], color=BEL[0], linestyle=BEL[1], linewidth=2, label="believing tool facts"),
               plt.Line2D([], [], color=INK, linewidth=0.8, label="sealed layer (from PREREG_T)"),
               plt.Line2D([], [], color=INK2, marker="o", linestyle="", label="F: framing in the input"),
               plt.Line2D([], [], color=INK2, marker="s", linestyle="", label="P: defensive system prompt")]
    fig.legend(handles=handles, loc="upper center", ncol=5, frameon=False, fontsize=8, bbox_to_anchor=(0.5, 1.08))
    fig.tight_layout()
    fig.savefig(a.out, dpi=160, facecolor=SURFACE, bbox_inches="tight")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
