#!/usr/bin/env python3
"""fig_bimodal.pdf: posterior modality tracks receiver-geometry invertibility.

Left: mirror-symmetric array (y unobservable) -> the CFM posterior for a high-|y|
point is BIMODAL (true mode + its y-mirror), so the posterior mean (the point
estimate) falls between the two modes and is misleading.
Right: anti-symmetric side-wall array (y observable) -> the same kind of high-|y| point
has a UNIMODAL posterior centred on the truth.

Real posterior samples:
  experiments/uq_bakeoff/mirror_cfm_samples.npz                 (200,2388,3)
  experiments/uq_bakeoff/combined_cfm_samples/cfm_samples_seed1_fold1.npz (200,790,3)
All values are full-wave CST SIMULATION.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from paperstyle import COLORS, MARKERS, W2, panel_letter, save

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
EXP = os.path.join(HERE, "..", "..", "experiments", "uq_bakeoff")


def pick_bimodal(samples, targets):
    """High-|y| point whose y-posterior most straddles the mirror plane y=0."""
    y_t = targets[:, 1]
    hi = np.where(np.abs(y_t) > 0.7 * np.abs(y_t).max())[0]
    # mirror capture = fraction of y-samples on the opposite side of 0 from truth
    cap = np.array([np.mean(np.sign(samples[:, i, 1]) != np.sign(y_t[i])) for i in hi])
    return hi[np.argmin(np.abs(cap - 0.45))]          # closest to a clean 2-mode split


def pick_unimodal(samples, targets, match_absy):
    """Anti-symmetric-array high-|y| point with |y_true| closest to the mirror point's, for a fair
    same-scale comparison; its posterior is concentrated (unimodal)."""
    y_t = targets[:, 1]
    hi = np.where(np.abs(y_t) > 0.5 * np.abs(y_t).max())[0]
    return hi[np.argmin(np.abs(np.abs(y_t[hi]) - match_absy))]


mir = np.load(os.path.join(EXP, "mirror_cfm_samples.npz"))
v4 = np.load(os.path.join(EXP, "combined_cfm_samples", "cfm_samples_seed1_fold1.npz"))
ms, mt = mir["samples"] * 100, mir["targets"] * 100
vs, vt = v4["samples"] * 100, v4["targets"] * 100

im = pick_bimodal(ms, mt)
iv = pick_unimodal(vs, vt, abs(mt[im, 1]))

fig, (a1, a2) = plt.subplots(1, 2, figsize=(W2, 2.6))
panels = [
    (a1, ms[:, im, :], mt[im], COLORS["purple"], MARKERS[0], True),
    (a2, vs[:, iv, :], vt[iv], COLORS["green"], MARKERS[1], False),
]
all_dx = []
for _ax, s, t, _col, _marker, _mirror in panels:
    all_dx.extend((s[:, 0] - t[0]).tolist())
    all_dx.append(float(s.mean(0)[0] - t[0]))
xlim = max(1.0, float(np.nanmax(np.abs(all_dx))) * 1.08)

for ax, s, t, col, marker, mirror in panels:
    mean = s.mean(0)
    dx = s[:, 0] - t[0]
    ax.scatter(dx, s[:, 1], s=10, alpha=0.34, color=col, marker=marker,
               edgecolor="black", linewidth=0.25, label="200 posterior samples",
               rasterized=False)
    if mirror:
        ax.axhline(0, color=COLORS["dark"], ls="--", lw=0.9, zorder=1)
        ax.scatter(0.0, -t[1], s=130, marker="*", facecolor="white",
                   edgecolor=COLORS["dark"], lw=0.9, zorder=5)
        ax.annotate("mirror mode", (0.0, -t[1]), textcoords="offset points",
                    xytext=(6, 6), fontsize=7, color=COLORS["dark"])
    ax.scatter(0.0, t[1], s=130, marker="*", facecolor="black",
               edgecolor="white", linewidth=0.5, zorder=6)
    ax.scatter(mean[0] - t[0], mean[1], s=80, marker="X",
               facecolor=COLORS["det"], edgecolor="white", linewidth=0.6,
               zorder=7)
    ax.set_xlabel("$x - x_{true}$ (cm)")
    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-7.5, 7.5)
    ax.grid(True, axis="both")
a1.set_ylabel("y (cm)")
panel_letter(a1, "a")
panel_letter(a2, "b")
legend_handles = [
    Line2D([0], [0], marker=MARKERS[0], color="none", markerfacecolor=COLORS["purple"],
           markeredgecolor="black", markeredgewidth=0.4, markersize=4.5,
           label="mirror-array samples"),
    Line2D([0], [0], marker=MARKERS[1], color="none", markerfacecolor=COLORS["green"],
           markeredgecolor="black", markeredgewidth=0.4, markersize=4.5,
           label="anti-symmetric samples"),
    Line2D([0], [0], marker="*", color="none", markerfacecolor="black",
           markeredgecolor="white", markeredgewidth=0.5, markersize=8,
           label="true position"),
    Line2D([0], [0], marker="X", color="none", markerfacecolor=COLORS["det"],
           markeredgecolor="white", markeredgewidth=0.6, markersize=6,
           label="posterior mean"),
    Line2D([0], [0], marker="*", color="none", markerfacecolor="white",
           markeredgecolor=COLORS["dark"], markeredgewidth=0.9, markersize=8,
           label="y-mirror"),
    Line2D([0], [0], color=COLORS["dark"], ls="--", lw=0.9, label="y = 0"),
]
fig.legend(handles=legend_handles, loc="upper center", ncol=6, frameon=False,
           bbox_to_anchor=(0.5, 0.985), handletextpad=0.35, columnspacing=0.8)
fig.subplots_adjust(left=0.07, right=0.99, bottom=0.18, top=0.76, wspace=0.22)
save(fig, "fig_bimodal.pdf")
print(f"mirror point idx={im}, y_true={mt[im,1]:.2f} cm, "
      f"mirror-capture={np.mean(np.sign(ms[:,im,1])!=np.sign(mt[im,1])):.2f}")
print(f"anti-symmetric point idx={iv}, y_true={vt[iv,1]:.2f} cm")
