#!/usr/bin/env python3
"""Publication-quality figures for the calibrated-posterior WCE paper.

Real per-point data: experiments/uq_bakeoff/combined_cfm_samples/*.npz
  (samples 200xNx3, targets Nx3, preds Nx3, test_idx N) -> error-vs-spread
  scatter (F8) and an example posterior cloud (F9).
Verified-ledger aggregate values are embedded with source comments for the
bar/curve figures. All values are full-wave CST SIMULATION.
Output: reports/paper/figures/*.pdf  (vector).
"""
import os, glob, subprocess
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Ellipse, Polygon, FancyArrowPatch
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
from paperstyle import (
    COLORS as C,
    HATCHES,
    LINESTYLES,
    MARKERS,
    W1,
    W2,
    panel_letter,
    save,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
SAMP = os.path.join(HERE, "..", "..", "experiments", "uq_bakeoff", "combined_cfm_samples")
os.makedirs(OUT, exist_ok=True)

# ========================================================== F1 study overview
# The final submitted PDF is currently overwritten by make_study_overview.mjs
# below. Keep this Matplotlib path styled and runnable, but do not fight the
# SVG-owned export in this Python-only pass.
fig, ax = plt.subplots(figsize=(W2, 3.05))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

panel_w, panel_h, y0 = 0.215, 0.72, 0.16
xs = [0.02, 0.265, 0.51, 0.755]
titles = ["1  Physical question", "2  Full-wave dataset", "3  Posterior model", "4  Reported evidence"]
for x, title in zip(xs, titles):
    ax.add_patch(FancyBboxPatch((x, y0), panel_w, panel_h, boxstyle="round,pad=0.012",
                                fc="white", ec="#c9c9c9", lw=0.9))
    ax.text(x + 0.014, y0 + panel_h - 0.055, title, ha="left", va="center",
            fontsize=8.0, weight="bold", color="#222")
for i in range(3):
    ax.annotate("", (xs[i + 1] - 0.015, 0.52), (xs[i] + panel_w + 0.012, 0.52),
                arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.3))

# Panel 1: tank, four receivers, capsule.
x = xs[0]
ax.add_patch(Rectangle((x + 0.045, y0 + 0.245), 0.125, 0.245,
                       fc=C["tank"], ec=C["det"], lw=0.9))
for rx in [(x + 0.034, y0 + 0.315), (x + 0.164, y0 + 0.315),
           (x + 0.085, y0 + 0.232), (x + 0.085, y0 + 0.480)]:
    ax.add_patch(Rectangle(rx, 0.018, 0.045, fc=C["cfm"], ec="#1a1a1a", lw=0.6))
ax.add_patch(Circle((x + 0.108, y0 + 0.366), 0.018, fc=C["orange"], ec=C["det"], lw=0.7))
for r in [0.035, 0.055, 0.075]:
    ax.add_patch(Ellipse((x + 0.108, y0 + 0.366), 2*r, 1.25*r, fill=False,
                         ec=C["good"], lw=0.7, alpha=0.65))
ax.text(x + 0.108, y0 + 0.555, "capsule RF\nlocalization", ha="center", va="center",
        fontsize=7.1)
ax.text(x + 0.108, y0 + 0.205, "4 side-wall Rx\nMICS/MedRadio budget", ha="center",
        va="top", fontsize=6.6, color="#444")

# Panel 2: CST sweep, RF features, grouped CV.
x = xs[1]
ax.plot([x + 0.040, x + 0.178], [y0 + 0.515, y0 + 0.515], color=C["good"], lw=1.6)
for k, f in enumerate(np.linspace(0.040, 0.178, 6)):
    ax.plot([x + f, x + f], [y0 + 0.505, y0 + 0.525], color=C["good"], lw=0.8)
ax.text(x + 0.109, y0 + 0.555, "0.38-0.43 GHz\nS-parameter sweep", ha="center",
        va="center", fontsize=6.8)
rng = np.random.default_rng(4)
pts = rng.uniform([x + 0.045, y0 + 0.265], [x + 0.175, y0 + 0.425], size=(42, 2))
fold_cols = [C["cfm"], C["warn"], C["good"], C["p1"], C["p2"]]
ax.scatter(pts[:, 0], pts[:, 1], s=8, c=[fold_cols[i % 5] for i in range(len(pts))],
           alpha=0.78, edgecolors="none")
ax.add_patch(Rectangle((x + 0.040, y0 + 0.255), 0.140, 0.180, fc="none",
                       ec="#777", lw=0.6, ls="--"))
ax.text(x + 0.109, y0 + 0.205, "3935 configs\nposition-grouped 5-fold CV\n180-D rich RF features",
        ha="center", va="top", fontsize=6.6, color="#444")

# Panel 3: flow transport from base samples to posterior.
x = xs[2]
base = rng.normal([x + 0.063, y0 + 0.390], [0.023, 0.023], size=(70, 2))
post = rng.normal([x + 0.158, y0 + 0.390], [0.028, 0.010], size=(70, 2))
ax.scatter(base[:, 0], base[:, 1], s=6, color=C["mut"], alpha=0.35, edgecolors="none")
ax.scatter(post[:, 0], post[:, 1], s=6, color=C["cfm"], alpha=0.45, edgecolors="none")
ax.scatter([x + 0.158], [y0 + 0.390], s=65, marker="*", color="#111", zorder=4)
ax.annotate("", (x + 0.128, y0 + 0.390), (x + 0.093, y0 + 0.390),
            arrowprops=dict(arrowstyle="-|>", color=C["cfm"], lw=1.4))
ax.text(x + 0.109, y0 + 0.555, "conditional flow\nmatching", ha="center",
        va="center", fontsize=7.0)
ax.text(x + 0.063, y0 + 0.315, "bounded\nbase", ha="center", va="center",
        fontsize=6.4, color="#555")
ax.text(x + 0.158, y0 + 0.315, "position\nposterior", ha="center", va="center",
        fontsize=6.4, color=C["cfm"])
ax.text(x + 0.109, y0 + 0.205, "posterior mean +\n50/90/95% credible regions",
        ha="center", va="top", fontsize=6.6, color="#444")

# Panel 4: the evidence bundle and scope caveat.
x = xs[3]
metrics = [("point tax-free", "3D MAE 0.354 cm"),
           ("calibrated", "cov90 = 0.970"),
           ("discriminative", "rho ~ 0.60")]
for j, (head, val) in enumerate(metrics):
    yy = y0 + 0.548 - j * 0.120
    ax.add_patch(Rectangle((x + 0.038, yy - 0.019), 0.025, 0.025,
                           fc=C["cfm"], ec="#1a1a1a", lw=0.5))
    ax.text(x + 0.050, yy - 0.006, "OK", ha="center", va="center",
            fontsize=5.3, color="white", weight="bold")
    ax.text(x + 0.073, yy + 0.004, head, ha="left", va="center",
            fontsize=6.9, weight="bold", color="#222")
    ax.text(x + 0.073, yy - 0.030, val, ha="left", va="center",
            fontsize=6.4, color="#444")
ax.add_patch(FancyBboxPatch((x + 0.035, y0 + 0.030), 0.145, 0.065,
                            boxstyle="round,pad=0.010", fc="#fff7f2",
                            ec=C["warn"], lw=0.8))
ax.text(x + 0.108, y0 + 0.062, "simulation only;\nphysical phantom is next gate",
        ha="center", va="center", fontsize=6.2, color=C["warn"])

save(fig, "fig_study_overview.pdf")

# =========================================================== F2 point ranking
# 3D MAE (cm) + 95% paired CIs; rich_benchmark/unified_analysis.json (combined N=3935)
pt = [
    ("GPR", 4.153, 4.037, 4.266), ("Ridge", 2.460, 2.377, 2.553),
    ("AdaBoost", 2.404, 2.334, 2.474), ("MLP", 1.978, 1.941, 2.012),
    ("k-NN", 1.869, 1.813, 1.923), ("NGBoost", 1.382, 1.346, 1.417),
    ("SVR", 1.306, 1.267, 1.342), ("RandomForest", 1.061, 1.026, 1.095),
    ("ExtraTrees", 0.817, 0.788, 0.845), ("HistGB", 0.779, 0.756, 0.801),
    ("Det. backbone", 0.340, None, None), ("Clean CFM", 0.354, 0.339, 0.369),
]
fig, ax = plt.subplots(figsize=(W1, 3.0))
ys = np.arange(len(pt))
for i, (n, m, lo, hi) in enumerate(pt):
    col = C["cfm"] if "CFM" in n else (C["det"] if "backbone" in n else C["classical"])
    hatch = "" if "CFM" in n else ("//" if "backbone" in n else "..")
    err = [[m - lo], [hi - m]] if lo is not None else None
    bars = ax.barh(i, m, color=col, hatch=hatch, edgecolor="#333333", linewidth=0.4,
                   xerr=err, error_kw=dict(ecolor="#333", lw=0.7, capsize=2), zorder=3)
    if "CFM" in n or "backbone" in n:
        ax.bar_label(bars, labels=[f"{m:.3f}"], padding=2, fontsize=7)
ax.set_yticks(ys); ax.set_yticklabels([n for n, *_ in pt])
ax.set_xlabel("3D MAE (cm)")
ax.set_xlim(0, 4.6)
ax.grid(True, axis="x")
ax.axvline(0.354, color=C["cfm"], ls=":", lw=0.9, zorder=0)
fig.subplots_adjust(left=0.34, right=0.97, bottom=0.13, top=0.98)
save(fig, "fig_point_ranking.pdf")

# =========================================================== F3 per-axis error
ax_lbl = ["x", "y", "z"]
per = {"Clean CFM": ([0.143, 0.181, 0.185], C["cfm"]),
       "Det. backbone": ([0.14, 0.17, 0.18], C["det"]),
       "HistGB": ([0.232, 0.540, 0.321], C["warn"]),
       "GPR": ([1.132, 2.872, 2.212], C["mut"])}
fig, ax = plt.subplots(figsize=(W1, 2.7))
w = 0.2
for j, (n, (v, c)) in enumerate(per.items()):
    ax.bar(np.arange(3) + (j - 1.5) * w, v, w, label=n, color=c,
           hatch=HATCHES[j], edgecolor="#333333", linewidth=0.4, zorder=3)
ax.set_xticks(range(3)); ax.set_xticklabels(ax_lbl)
ax.set_ylabel("per-axis MAE (cm)"); ax.set_xlabel("axis")
ax.set_ylim(0, 3.3)
ax.grid(True, axis="y")
fig.legend(loc="upper center", bbox_to_anchor=(0.53, 0.99), ncol=2,
           frameon=False, fontsize=7, handlelength=1.4, columnspacing=0.8)
fig.subplots_adjust(left=0.15, right=0.98, bottom=0.18, top=0.78)
save(fig, "fig_peraxis.pdf")

# =========================================================== F4 reliability
nominal = [0.50, 0.90, 0.95]
methods = {
    "Clean CFM": ([0.766, 0.935, 0.944], MARKERS[0], LINESTYLES[0], C["cfm"], 1.25),
    "Deep ensemble": ([0.402, 0.717, 0.738], MARKERS[1], LINESTYLES[1], C["orange"], 0.95),
    "MC-dropout": ([0.206, 0.464, 0.523], MARKERS[2], LINESTYLES[2], C["classical"], 0.95),
    "MDN-diag": ([0.874, 0.969, 0.978], MARKERS[3], LINESTYLES[3], C["green"], 0.95),
    "MDN-mix2": ([0.837, 0.963, 0.973], MARKERS[4], LINESTYLES[4], C["sky"], 0.95),
    "Split conformal": ([0.483, 0.893, 0.945], MARKERS[5], LINESTYLES[1], C["purple"], 0.95),
}
fig, ax = plt.subplots(figsize=(W1, 2.85))
xpos = np.arange(len(nominal))
ideal = np.asarray(nominal)
ax.plot(xpos, ideal, color="black", ls=":", lw=0.95, label="ideal", zorder=1)
ax.fill_between(xpos, ideal - 0.05, ideal + 0.05, color=C["cfm"], alpha=0.055,
                label=r"$\pm$0.05 band", zorder=0)
for n, (cov, marker, linestyle, c, lw) in methods.items():
    ms = 5.4 if "CFM" in n else 4.7
    alpha = 1.0 if "CFM" in n else 0.78
    ax.plot(xpos, cov, color=c, linestyle=linestyle, marker=marker, lw=lw, ms=ms,
            markeredgecolor="black", markeredgewidth=0.45, alpha=alpha, label=n,
            zorder=5 if "CFM" in n else 3)
ax.annotate("CFM", xy=(1, 0.935), xytext=(0.58, 0.96),
            arrowprops=dict(arrowstyle="-", color=C["cfm"], lw=0.8),
            color=C["cfm"], fontsize=7.0, weight="bold")
ax.text(0.02, 0.27, "under-\ncoverage", ha="center", va="center", fontsize=7, color=C["dark"])
ax.text(1.50, 0.995, "near nominal", ha="center", va="center", fontsize=7, color=C["dark"])
ax.set_xlabel("nominal coverage"); ax.set_ylabel("empirical coverage")
ax.set_xlim(-0.15, 2.15); ax.set_ylim(0.15, 1.03)
ax.set_xticks(xpos); ax.set_xticklabels(["50%", "90%", "95%"])
ax.grid(True)
fig.legend(loc="lower center", bbox_to_anchor=(0.52, 0.02), ncol=3,
           frameon=False, fontsize=6.4, handlelength=1.7, columnspacing=0.75)
fig.subplots_adjust(bottom=0.31, left=0.16, right=0.99, top=0.96)
save(fig, "fig_reliability.pdf")

# ====================================================== F5 calibration vs disc
# (cov90, rho) per method, N=1980 uncertainty comparison
cd = {"Clean CFM": (0.935, 0.601, C["cfm"], MARKERS[7]),
      "Deep ensemble": (0.717, 0.705, C["orange"], MARKERS[1]),
      "MC-dropout": (0.464, 0.648, C["classical"], MARKERS[3]),
      "MDN-diag": (0.969, 0.015, C["green"], MARKERS[0]),
      "MDN-mix2": (0.963, 0.097, C["sky"], MARKERS[2]),
      "Split conformal": (0.893, 0.002, C["purple"], MARKERS[5])}
fig, ax = plt.subplots(figsize=(W1, 2.85))
ax.add_patch(Rectangle((0.88, 0.40), 0.08, 0.42, fc=C["cfm"], ec=C["cfm"],
                       alpha=0.08, lw=0.8, zorder=0))
ax.axvline(0.90, color="#222", ls=":", lw=0.9)
ax.axhline(0.40, color="#777", ls=":", lw=0.8)
offsets = {
    "Clean CFM": (-25, 12), "Deep ensemble": (-25, 9), "MC-dropout": (16, 10),
    "MDN-diag": (-42, 13), "MDN-mix2": (-38, 10), "Split conformal": (-45, 12),
}
for n, (cov, rho, c, marker) in cd.items():
    is_cfm = "CFM" in n
    ax.scatter(cov, rho, s=130 if is_cfm else 60, color=c,
               edgecolor="black", linewidth=0.5,
               zorder=5 if is_cfm else 3, marker=marker)
    ax.annotate(n, xy=(cov, rho), xytext=offsets[n], textcoords="offset points",
                fontsize=7, color=c, ha="center",
                arrowprops=dict(arrowstyle="-", color=c, lw=0.55, shrinkA=2, shrinkB=2))
ax.text(0.92, 0.79, "target region", fontsize=7, ha="center", color=C["cfm"], weight="bold")
ax.text(0.505, 0.08, "wide but\nnot useful", fontsize=7, color=C["dark"], ha="center")
ax.set_xlabel("empirical 90% coverage"); ax.set_ylabel(r"error--spread rank correlation $\rho$")
ax.set_xlim(0.40, 1.0); ax.set_ylim(-0.09, 0.85)
fig.subplots_adjust(left=0.17, right=0.98, bottom=0.18, top=0.96)
save(fig, "fig_cal_vs_disc.pdf")

# =========================================================== F6 deployability
S = ["S1\nmag\n1-tone", "S2\n+phase\n1-tone", "S3\ncoherent\nband", "S4\nmulti-f\nmag", "S5\nfull\nrich"]
dep = {"HistGB": ([1.550, 0.970, 1.063, 1.652, 1.050], C["warn"]),
       "ExtraTrees": ([1.731, 1.239, 1.140, 1.688, 1.146], C["mut"]),
       "Clean CFM": ([1.519, 0.524, 0.481, 1.191, 0.512], C["cfm"])}
fig, ax = plt.subplots(figsize=(W2, 2.65))
w = 0.26
for j, (n, (v, c)) in enumerate(dep.items()):
    ax.bar(np.arange(5) + (j - 1) * w, v, w, label=n, color=c,
           hatch=HATCHES[j], edgecolor="#333333", linewidth=0.4, zorder=3)
ax.axhline(1.0, color="#555", ls=":", lw=0.8)
ax.text(4.65, 1.03, "1 cm", fontsize=7, color=C["dark"], va="bottom", ha="right")
ax.set_xticks(range(5)); ax.set_xticklabels(S, fontsize=6.6)
ax.set_ylabel("3D MAE (cm)")
ax.grid(True, axis="y")
fig.legend(loc="upper center", bbox_to_anchor=(0.52, 0.98), ncol=3,
           frameon=False, fontsize=7, handlelength=1.5)
fig.subplots_adjust(left=0.08, right=0.99, bottom=0.18, top=0.82)
save(fig, "fig_deployability.pdf")

# ===================================================== F7 orientation marginal
on = [0.50, 0.80, 0.90, 0.95]; oe = [0.747, 0.965, 1.0, 1.0]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(W2, 2.55), gridspec_kw=dict(width_ratios=[1.2, 1]))
a1.plot([0.45, 1.0], [0.45, 1.0], "k:", lw=1, label="ideal")
a1.plot(on, oe, color=C["cfm"], marker=MARKERS[0], linestyle=LINESTYLES[0],
        markeredgecolor="black", ms=5, label="orientation-marginal")
a1.set_xlabel("nominal coverage"); a1.set_ylabel("empirical coverage")
a1.set_xlim(0.45, 1.0); a1.set_ylim(0.45, 1.03); a1.legend(fontsize=7, frameon=False)
bars = a2.bar(["x", "y", "z"], [1.247, 1.199, 1.355], color=C["cfm"],
              edgecolor="#333333", linewidth=0.4, zorder=3)
for bar, hatch in zip(bars, HATCHES[:3]):
    bar.set_hatch(hatch)
a2.axhline(1.0, color="#555", ls=":", lw=0.8)
a2.set_ylabel("posterior width ratio"); a2.set_ylim(0.9, 1.45)
a2.grid(True, axis="y")
panel_letter(a1, "a"); panel_letter(a2, "b")
fig.subplots_adjust(left=0.08, right=0.99, bottom=0.18, top=0.96, wspace=0.28)
save(fig, "fig_orient.pdf")

# =============================================== F2 CFM method schematic (posterior transport)
# This fallback is styled, but the final PDF is SVG/D3-owned when
# make_method_cfm_d3.mjs exists and is run at the bottom of this script.
fig, ax = plt.subplots(figsize=(W2, 2.55))
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
rng = np.random.default_rng(22)

# Conditioning input: RF feature vector plus fixed receiver geometry.
ax.add_patch(FancyBboxPatch((0.035, 0.62), 0.185, 0.255, boxstyle="round,pad=0.018",
                            fc="#f3f7ff", ec=C["good"], lw=1.1))
for i, h in enumerate(rng.uniform(0.035, 0.135, 28)):
    x0 = 0.055 + i * 0.0051
    ax.add_patch(Rectangle((x0, 0.665), 0.0032, h, fc=C["good"], ec="none", alpha=0.75))
for px, py, col in [(0.065, 0.815, C["cfm"]), (0.095, 0.795, C["warn"]),
                    (0.150, 0.820, C["cfm"]), (0.180, 0.790, C["warn"])]:
    ax.add_patch(Rectangle((px, py), 0.010, 0.028, fc=col, ec="#222", lw=0.35))
ax.text(0.128, 0.600, "condition $c$\nRF features\n+ Rx geometry",
        ha="center", va="top", fontsize=6.8, color="#20364f")

# Bounded base cloud in the cuboid support.
base_c = np.array([0.250, 0.410])
post_c = np.array([0.735, 0.425])
base = rng.uniform([-0.055, -0.080], [0.055, 0.080], size=(85, 2)) + base_c
posterior = rng.multivariate_normal(post_c, [[0.00135, 0.00030], [0.00030, 0.00045]], size=140)
ax.add_patch(Polygon([(0.170, 0.295), (0.285, 0.295), (0.335, 0.385),
                      (0.335, 0.570), (0.220, 0.570), (0.170, 0.480)],
                     closed=True, fc="#f7f7f4", ec="#777", lw=0.9, alpha=0.95))
ax.plot([0.285, 0.335], [0.295, 0.385], color=C["dark"], lw=0.8)
ax.plot([0.285, 0.285], [0.295, 0.480], color=C["dark"], lw=0.8)
ax.plot([0.285, 0.335], [0.480, 0.570], color=C["dark"], lw=0.8)
ax.scatter(base[:, 0], base[:, 1], s=8, color=C["classical"], alpha=0.42,
           edgecolor="black", linewidth=0.25, marker=MARKERS[0])
ax.text(base_c[0], 0.245, "bounded base\nuniform in cuboid",
        ha="center", va="top", fontsize=7.2, color="#555")

# Learned conditional transport trajectories.
for i in range(18):
    b = base[rng.integers(0, len(base))]
    p = posterior[rng.integers(0, len(posterior))]
    rad = rng.uniform(-0.25, 0.25)
    ax.add_patch(FancyArrowPatch((b[0], b[1]), (p[0], p[1]),
                                 connectionstyle=f"arc3,rad={rad:.2f}",
                                 arrowstyle="-|>", mutation_scale=8.5,
                                 lw=0.85, color=C["good"], alpha=0.33, zorder=1))
ax.add_patch(FancyBboxPatch((0.405, 0.325), 0.165, 0.220, boxstyle="round,pad=0.018",
                            fc="white", ec=C["cfm"], lw=1.2, alpha=0.96, zorder=4))
ax.text(0.487, 0.455, "learned vector field", ha="center", va="center",
        fontsize=7.1, weight="bold", color=C["cfm"], zorder=5)
ax.text(0.487, 0.388, "$\\dot{x}=v_\\theta(x,t\\,|\\,c)$\nFiLM blocks, EMA 0.999",
        ha="center", va="center", fontsize=6.7, color="#333", zorder=5)
ax.add_patch(FancyArrowPatch((0.222, 0.680), (0.487, 0.545),
                             connectionstyle="arc3,rad=-0.12", arrowstyle="-|>",
                             mutation_scale=9.5, lw=1.0, color=C["good"],
                             ls=":", alpha=0.95))
ax.text(0.360, 0.725, "conditioning signal", ha="center",
        fontsize=6.5, color=C["good"],
        bbox=dict(boxstyle="round,pad=0.08", fc="white", ec="none", alpha=0.85))

# Posterior sample cloud and credible regions.
ax.scatter(posterior[:, 0], posterior[:, 1], s=8, color=C["cfm"], alpha=0.38,
           edgecolor="none", zorder=3)
for idx, (scale, label, alpha) in enumerate([(1.15, "50%", 0.95), (1.75, "90%", 0.72), (2.20, "95%", 0.48)]):
    ax.add_patch(Ellipse(post_c, 0.105 * scale, 0.045 * scale, angle=12,
                         fc="none", ec=C["cfm"], lw=1.0, alpha=alpha,
                         linestyle=LINESTYLES[idx], zorder=4))
ax.scatter([post_c[0]], [post_c[1]], s=95, marker="*", color="#111", zorder=5)
ax.text(post_c[0], 0.245, "conditional posterior\n$p_\\theta(x\\,|\\,c)$ from 200 samples",
        ha="center", va="top", fontsize=7.2, color=C["cfm"])
ax.text(0.825, 0.550, "credible regions\n50 / 90 / 95%", ha="left", va="center",
        fontsize=6.9, color=C["cfm"])
ax.text(0.825, 0.410, "posterior mean\n= point estimate", ha="left", va="center",
        fontsize=6.9, color="#222")

# Sampling clock.
ax.plot([0.255, 0.735], [0.112, 0.112], color="#777", lw=0.8)
for t, lab in [(0.255, "$t=0$"), (0.495, "Euler integration"), (0.735, "$t=1$")]:
    ax.plot([t, t], [0.099, 0.125], color="#777", lw=0.8)
    ax.text(t, 0.070, lab, ha="center", va="top", fontsize=6.6, color="#555")
save(fig, "fig_method_cfm.pdf")

# =============================================== F12 proper scores (CRPS / energy)
crps = {"Clean CFM*": (0.127, 0.277), "Deep ensemble": (0.131, 0.237),
        "MC-dropout": (0.188, 0.399), "MDN-diag": (0.247, 0.504),
        "MDN-mix2": (0.269, 0.545)}
names = list(crps); x = np.arange(len(names)); w = 0.38
fig, ax = plt.subplots(figsize=(W1, 2.6))
ax.bar(x - w / 2, [crps[n][0] for n in names], w, color=C["cfm"],
       edgecolor="#333333", linewidth=0.4, label="CRPS", zorder=3)
ax.bar(x + w / 2, [crps[n][1] for n in names], w, color=C["orange"],
       hatch="//", edgecolor="#333333", linewidth=0.4, label="energy score", zorder=3)
ax.set_xticks(x); ax.set_xticklabels(names, rotation=22, ha="right", fontsize=6.8)
ax.set_ylabel("score (cm)")
ax.grid(True, axis="y")
ax.legend(fontsize=7, frameon=False, loc="upper left")
fig.subplots_adjust(left=0.15, right=0.98, bottom=0.27, top=0.97)
save(fig, "fig_crps.pdf")

# ===================================================== real per-point samples (cm)
files = sorted(glob.glob(os.path.join(SAMP, "*.npz")))
if files:
    from scipy.stats import spearmanr
    sp_all, er_all, clouds, P_all, T_all = [], [], [], [], []
    for f in files:
        z = np.load(f, allow_pickle=True)
        s = z["samples"] * 100.0; t = z["targets"] * 100.0; p = z["preds"] * 100.0  # m -> cm
        sp_all.append(np.linalg.norm(s.std(axis=0), axis=1))
        er_all.append(np.linalg.norm(p - t, axis=1))
        ky = int(np.argmax(np.abs(t[:, 1])))                # most extreme |y| example
        clouds.append((s[:, ky, :], t[ky], p[ky], abs(t[ky, 1])))
        P_all.append(p); T_all.append(t)
    sp = np.concatenate(sp_all); er = np.concatenate(er_all)
    rho = spearmanr(sp, er).statistic

    # F10 error vs spread (hexbin density + binned-median trend)
    fig, ax = plt.subplots(figsize=(W1, 2.75))
    xm, ym = np.percentile(sp, 99), np.percentile(er, 99)
    hb = ax.hexbin(sp, er, gridsize=32, cmap="viridis", mincnt=1, bins="log",
                   extent=(0, xm, 0, ym), rasterized=True)
    edges = np.linspace(0, np.percentile(sp, 98), 11); mid = 0.5 * (edges[:-1] + edges[1:])
    med = [np.median(er[(sp >= a) & (sp < b)]) if ((sp >= a) & (sp < b)).sum() > 5 else np.nan
           for a, b in zip(edges[:-1], edges[1:])]
    ax.plot(mid, med, color=C["orange"], marker=MARKERS[0], linestyle=LINESTYLES[0],
            markeredgecolor="black", ms=3.5, lw=1.0, label="binned median")
    ax.set_xlabel("posterior spread (cm)"); ax.set_ylabel("realized 3D error (cm)")
    ax.set_xlim(0, xm); ax.set_ylim(0, ym); ax.legend(fontsize=7, loc="upper left", frameon=False)
    ax.text(0.96, 0.08, rf"$\rho={rho:.2f}$", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=7, color=C["dark"])
    cb = fig.colorbar(hb, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label("count", fontsize=7)
    cb.ax.tick_params(labelsize=6.5, width=0.5, length=2)
    fig.subplots_adjust(left=0.15, right=0.88, bottom=0.18, top=0.97)
    save(fig, "fig_error_spread.pdf")

    # F11 example posterior cloud: x-y and x-z (anisotropy)
    s_k, t_k, p_k, _ = max(clouds, key=lambda c: c[3])
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(W2, 2.75))
    for ax, (i, j, xl, yl) in zip((a1, a2), [(0, 1, "x", "y"), (0, 2, "x", "z")]):
        ax.scatter(s_k[:, i], s_k[:, j], s=10, alpha=0.34, color=C["cfm"],
                   edgecolor="white", linewidth=0.25, marker=MARKERS[0],
                   label="200 samples")
        ax.scatter(t_k[i], t_k[j], s=120, marker="*", facecolor="black",
                   edgecolor="white", linewidth=0.5, zorder=5, label="true")
        ax.scatter(p_k[i], p_k[j], s=80, marker="X", facecolor=C["det"],
                   edgecolor="white", linewidth=0.6, zorder=6, label="mean")
        ax.set_xlabel(f"{xl} (cm)"); ax.set_ylabel(f"{yl} (cm)"); ax.set_aspect("equal", "datalim")
        ax.grid(True)
    panel_letter(a1, "a"); panel_letter(a2, "b")
    handles, labels = a1.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.98),
               ncol=3, frameon=False, fontsize=7)
    fig.subplots_adjust(left=0.08, right=0.99, bottom=0.16, top=0.82, wspace=0.28)
    save(fig, "fig_posterior_cloud.pdf")

    # F6 hero grid: per-axis predicted-vs-true (CFM, combined)
    P = np.concatenate(P_all); T = np.concatenate(T_all)
    fig, axes = plt.subplots(1, 3, figsize=(W2, 2.72))
    for ax, k in zip(axes, range(3)):
        lab = ["x", "y", "z"][k]
        lo = min(T[:, k].min(), P[:, k].min()); hi = max(T[:, k].max(), P[:, k].max())
        pad = 0.06 * (hi - lo)
        lo, hi = lo - pad, hi + pad
        ax.scatter(T[:, k], P[:, k], s=3.4, alpha=0.14, color=C["cfm"],
                   edgecolor="none", zorder=2, rasterized=True)
        ax.plot([lo, hi], [lo, hi], color="white", lw=2.2, zorder=5)
        ax.plot([lo, hi], [lo, hi], color="black", ls=":", lw=0.9, zorder=6)
        mae = np.abs(P[:, k] - T[:, k]).mean()
        panel_letter(ax, "abc"[k])
        ax.text(0.06, 0.86, f"MAE {mae:.3f} cm", transform=ax.transAxes,
                ha="left", va="top", fontsize=8.0, weight="bold",
                bbox=dict(boxstyle="round,pad=0.20", fc="white", ec="none", alpha=0.82))
        ax.set_xlabel(f"true {lab} (cm)"); ax.set_ylabel("predicted (cm)" if k == 0 else "")
        ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
        ax.set_aspect("equal", adjustable="box")
        ax.tick_params(pad=1.5)
    fig.subplots_adjust(left=0.070, right=0.995, bottom=0.22, top=0.94, wspace=0.30)
    save(fig, "fig_hero_grid.pdf")

    # F13 risk-coverage (selective prediction): defer the least-confident by spread
    order_conf = np.argsort(sp)              # most confident (smallest spread) first
    order_oracle = np.argsort(er)            # oracle: smallest true error first
    fracs = np.linspace(0.05, 1.0, 40)
    def retained_mae(order):
        return [er[order[:max(1, int(f * len(er)))]].mean() for f in fracs]
    fig, ax = plt.subplots(figsize=(W1, 2.55))
    ax.plot(fracs, retained_mae(order_conf), LINESTYLES[0], color=C["cfm"], lw=1.0,
            label="defer by posterior spread")
    ax.plot(fracs, retained_mae(order_oracle), LINESTYLES[1], color=C["det"], lw=0.95,
            label="oracle (defer by true error)")
    ax.axhline(er.mean(), color=C["dark"], ls=":", lw=0.95, label="random (no deferral)")
    ax.set_xlabel("retained fraction (1 $-$ deferral rate)")
    ax.set_ylabel("3D MAE of retained (cm)")
    ax.legend(fontsize=6.6, loc="upper left", frameon=False); ax.grid(True, alpha=0.22)
    fig.subplots_adjust(left=0.16, right=0.98, bottom=0.20, top=0.97)
    save(fig, "fig_risk_coverage.pdf")
else:
    print("WARN: no combined_cfm_samples npz; skipped F6/F10/F11")

overview_script = os.path.join(HERE, "make_study_overview.mjs")
if os.path.exists(overview_script):
    # SVG-owned figure: another source path writes the final PDF/SVG pair.
    # Keep the Matplotlib fallback above valid, but do not override this handoff.
    subprocess.run(["node", overview_script], check=True)

method_script = os.path.join(HERE, "make_method_cfm_d3.mjs")
if os.path.exists(method_script):
    # SVG-owned figure: leave the D3 export path in control for this asset.
    subprocess.run(["node", method_script], check=True)

print("done:", sorted(os.listdir(OUT)))
