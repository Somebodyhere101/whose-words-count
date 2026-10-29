"""PREREG_T figure (descriptive, not a gate): transfer curves by layer, one figure per pair.

Usage: python t_plot.py --root <out_t> --out <folder>
Rows are models, columns behaviours. Lines: M (marker tokens), C (content tokens), D (after the turn).
Same curve computation as t_analyze.py. Palette: dataviz reference slots 1-3, validated on all pairs (light):
CVD worst dE 9.2, normal 24.0; aqua is below 3:1 on the surface, so every line also has its own dash pattern.
"""
import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import t_analyze as TA

SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
STYLE = {"M": ("#2a78d6", "-", "role-marker tokens (M)"), "C": ("#eb6834", "--", "statement's own tokens (C)"),
         "D": ("#1baf7a", ":", "everything after the turn (D)")}
BEH = {"obey": ("beh", "obey"), "believe": ("beh", "believe"), "attribute": ("attr", None)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    models = [m for m in sorted(os.listdir(a.root)) if os.path.exists(os.path.join(a.root, m, "patch.json"))]
    data = {m: json.load(open(os.path.join(a.root, m, "patch.json"))) for m in models}
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2, "xtick.color": INK2,
                         "ytick.color": INK2, "text.color": INK, "font.family": "DejaVu Sans"})
    for pair in ("own->usr", "sys->usr"):
        fig, axes = plt.subplots(len(models), 3, figsize=(10, 2.3 * len(models)), sharey=True, facecolor=SURFACE)
        axes = np.atleast_2d(axes)
        for r, m in enumerate(models):
            R = data[m]
            nl, L = R["n_layers"], R["layer"]
            kinds = {it["id"]: it["kind"] for it in R["items"]}
            for c, (b, (rk, ik)) in enumerate(BEH.items()):
                ax = axes[r, c]
                ax.set_facecolor(SURFACE)
                for s in ("top", "right"):
                    ax.spines[s].set_visible(False)
                ax.grid(axis="y", color=GRID, linewidth=0.6)
                ax.set_axisbelow(True)
                rr = R["pairs"][pair][rk]
                jobs = [tuple(j) for j in rr["jobs"]]
                keep = [i for i in dict.fromkeys(j[0] for j in jobs) if ik is None or kinds[i] == ik]
                don, rec = TA.by_item(jobs, rr["donor"], keep), TA.by_item(jobs, rr["recip"], keep)
                gm, p = TA.signflip(don - rec)
                if r == 0:
                    ax.set_title(b, color=INK, fontsize=10)
                if c == 0:
                    ax.set_ylabel(f"{m}\ntransfer", color=INK, fontsize=9)
                ax.set_xlim(1, nl)
                ax.set_ylim(-0.25, 1.3)
                ax.axvline(L, color=INK2, linewidth=0.6, linestyle=(0, (1, 2)))
                if not (abs(gm) >= 0.05 and p < 0.05):
                    ax.text(0.5, 0.5, f"gap not informative\n(gap {gm:+.3f}, p {p:.2g})", transform=ax.transAxes,
                            ha="center", va="center", color=INK2, fontsize=8, bbox=dict(facecolor=SURFACE, edgecolor="none", pad=2))
                    continue
                pat = {s: np.stack([TA.by_item(jobs, rr["patched"][s][l], keep) for l in range(nl)]) for s in ("M", "C", "D")}
                alls = {int(l): TA.by_item(jobs, v, keep) for l, v in rr["all"].items()}
                T, _ = TA.curves(don, rec, pat, alls, np.arange(len(keep)))
                h, carrier, _, _ = TA.summarize(T, nl)
                x = np.arange(1, nl + 1)
                for s in ("M", "C", "D"):
                    col, ls, _ = STYLE[s]
                    ax.plot(x, T[s], color=col, linestyle=ls, linewidth=2)
                if h <= nl:
                    ax.axvline(h, color=INK, linewidth=0.8)
                ax.text(0.98, 0.95, f"gap {gm:+.2f} · handoff L{h} · {carrier}", transform=ax.transAxes, ha="right",
                        va="top", color=INK2, fontsize=7.5, bbox=dict(facecolor=SURFACE, edgecolor="none", alpha=0.9, pad=1.5))
            axes[r, 1].set_xlabel("") if r < len(models) - 1 else axes[r, 1].set_xlabel("layer patched", color=INK2)
        handles = [plt.Line2D([], [], color=col, linestyle=ls, linewidth=2, label=lab) for col, ls, lab in STYLE.values()]
        handles += [plt.Line2D([], [], color=INK, linewidth=0.8, label="handoff (D reaches 0.5)"),
                    plt.Line2D([], [], color=INK2, linewidth=0.6, linestyle=(0, (1, 2)), label="decision layer")]
        fig.legend(handles=handles, loc="upper center", ncol=5, frameon=False, fontsize=8, bbox_to_anchor=(0.5, 1.0))
        donor = pair.split("->")[0]
        fig.suptitle(f"Where is \"who said this\" read?  Patching the {donor}-turn run into the user-turn run, layer by layer",
                     y=1.035, fontsize=11, color=INK)
        fig.tight_layout(rect=(0, 0, 1, 0.97))
        fn = os.path.join(a.out, f"prereg_t_{donor}_to_usr.png")
        fig.savefig(fn, dpi=160, facecolor=SURFACE, bbox_inches="tight")
        plt.close(fig)
        print("wrote", fn)


if __name__ == "__main__":
    main()
