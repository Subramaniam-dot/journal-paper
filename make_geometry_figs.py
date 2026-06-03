#!/usr/bin/env python3
"""3D geometry figures for the calibrated-posterior WCE paper.

Reconstructed from CST-derived simulation metadata, not a CST CAD screenshot:
  X = 273 mm  (horizontal)  -> receivers P3 (+x), P4 (-x)
  Y = 278 mm  (HEIGHT = VERTICAL) -> top (+y)/floor (-y) faces: NO Rx
  Z = 380 mm  (horizontal, long side) -> receivers P1 (-z), P2 (+z)
Receivers sit on the four VERTICAL side walls at anti-symmetric heights
(P1/P3 at y=+67.5 mm, P2/P4 at y=-72.5 mm), which breaks the y->-y mirror
symmetry. The +-y (top/floor) faces carry no receiver, so y is the hard axis.

The figure is drawn with Y as the vertical (up) axis: physical (x,y,z) is mapped
to plot (x, z, y) so the matplotlib vertical axis shows the physical height y.

Outputs (vector PDF, shared sans-serif style):
  fig_geometry.pdf           -- four-receiver side-wall array (y up, top/floor labelled)
  fig_geometry_ablation.pdf  -- compact 3-panel receiver-placement ablation
All values are full-wave CST SIMULATION.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
import matplotlib.patheffects as pe
import pickle
from paperstyle import COLORS, LINESTYLES, W1, W2, panel_letter, save

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")
PKL = os.path.join(HERE, "..", "..", "data", "raw_rich_dense_v4_combined.pkl")
os.makedirs(OUT, exist_ok=True)

UPPER = COLORS["cfm"]
LOWER = COLORS["det"]
TANK_EDGE = COLORS["dark"]
REGION = COLORS["dark"]
CLOUD = COLORS["classical"]
CAPSULE = COLORS["orange"]
NO_RX_FACE = "#F0E442"

# ---------------------------------------------------------------- geometry load
d = pickle.load(open(PKL, "rb"))
SP = np.asarray(d["sensor_positions"], dtype=float) * 100.0          # cm, (4,3)
POS = np.asarray(d["positions"], dtype=float) * 100.0                # cm, (N,3)
SWEEP = np.asarray(d["cuboid_dims"], dtype=float) * 100.0            # cm full span

# Paper-coordinate body half-extents (cm): x, y(vertical), z.
HALF = np.array([273.0, 278.0, 380.0]) / 2.0 / 10.0                  # cm: 13.65,13.9,19.0
ANT_SHORT, ANT_LONG = 2.625, 12.0                                   # patch 26.25 x 120 mm


# -------------------------------------------- physical (x,y,z) -> plot (x,z,y)
def TP(a):
    """Map physical coords to plot coords so the vertical plot axis = y."""
    a = np.asarray(a, dtype=float)
    return a[..., [0, 2, 1]]


def box_edges(half, centre=(0, 0, 0)):
    hx, hy, hz = half
    c = np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)])
    v = c * np.array(half) + np.array(centre)
    idx = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
           (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]
    return [[TP(v[i]), TP(v[j])] for i, j in idx]


def y_face(sign, half, inset=0.0):
    """A +-y (top/floor) face rectangle, in plot coords."""
    hx, hy, hz = half
    yv = sign * (hy - inset)
    pts = [[-hx, yv, -hz], [hx, yv, -hz], [hx, yv, hz], [-hx, yv, hz]]
    return [TP(p) for p in pts]


def receiver_patch(centre, wall):
    cx, cy, cz = centre
    hl, hs = ANT_LONG / 2.0, ANT_SHORT / 2.0
    if wall in ("+z", "-z"):                 # patch in x-y plane (short x, long y)
        pts = [[cx - hs, cy - hl, cz], [cx + hs, cy - hl, cz],
               [cx + hs, cy + hl, cz], [cx - hs, cy + hl, cz]]
    else:                                    # +-x: patch in z-y plane (short z, long y)
        pts = [[cx, cy - hl, cz - hs], [cx, cy + hl, cz - hs],
               [cx, cy + hl, cz + hs], [cx, cy - hl, cz + hs]]
    return [TP(p) for p in pts]


def capsule_lines(centre=(0, 0, 0), axis="z", radius=0.55, length=3.0, n=22):
    """Wireframe rings of a small capsule; long axis along the body length (z)."""
    cx, cy, cz = centre
    t = np.linspace(0, 2 * np.pi, n)
    segs = []
    for end in (-length / 2, length / 2):
        if axis == "z":
            ring = np.column_stack([cx + radius * np.cos(t), cy + radius * np.sin(t),
                                    np.full(n, cz + end)])
        else:
            ring = np.column_stack([np.full(n, cx + end), cy + radius * np.cos(t),
                                    cz + radius * np.sin(t)])
        segs += [[TP(ring[i]), TP(ring[i + 1])] for i in range(n - 1)]
    return segs


def wall_of(p):
    ax_i = int(np.argmax(np.abs(p)))
    return {0: ("+x" if p[0] > 0 else "-x"), 2: ("+z" if p[2] > 0 else "-z")}.get(ax_i, "+z")


def style_axes(ax, half, compact=False):
    pad = 2.5
    plo = [TP([-half[0] - pad, -half[1] - pad, -half[2] - pad]),
           TP([half[0] + pad, half[1] + pad, half[2] + pad])]
    lo, hi = plo[0], plo[1]
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
    ax.set_box_aspect((2 * half[0], 2 * half[2], 2 * half[1]))   # x, z(depth), y(up)
    ax.view_init(elev=20, azim=-60)
    if compact:
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        ax.set_xlabel(""); ax.set_ylabel(""); ax.set_zlabel("")
    else:
        ax.set_xlabel("x: length 273 mm", labelpad=8)
        ax.set_ylabel("z: width 380 mm", labelpad=8)
        ax.set_zlabel("y: height 278 mm", labelpad=10)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.yaxis.set_major_locator(MaxNLocator(4))
        ax.zaxis.set_major_locator(MaxNLocator(4))
    for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
        try:
            pane.pane.fill = False
            pane.pane.set_edgecolor(COLORS["light"])
            pane._axinfo["grid"].update({"color": "#DDDDDD", "linewidth": 0.4})
        except Exception:
            pass
    ax.grid(not compact)


def halo(text, linewidth=2.0):
    text.set_path_effects([pe.withStroke(linewidth=linewidth, foreground="white")])
    return text


def draw_array(ax, sp_walls, half, *, show_cloud=False, show_region=False,
               show_capsule=False, mark_faces=False, lw_tank=0.9, patch_alpha=0.95,
               label_ports=True):
    # outer tank wireframe
    ax.add_collection3d(Line3DCollection(box_edges(half), colors=TANK_EDGE,
                                         linewidths=lw_tank, alpha=0.70))
    # top (+y) and floor (-y) faces -> the no-receiver faces
    if mark_faces:
        for sign, lab, dy in ((+1, "top (+y): no Rx", 0.0), (-1, "floor ($-y$): no Rx", 0.0)):
            ax.add_collection3d(Poly3DCollection([y_face(sign, half)],
                                facecolor=NO_RX_FACE, edgecolor=TANK_EDGE,
                                linewidths=0.5, alpha=0.18))
        tp = TP([0, half[1], 0]); fp = TP([0, -half[1], 0])
        halo(ax.text(tp[0], tp[1], tp[2] + 1.7, "top (+y): no receiver", ha="center",
                     fontsize=7.0, color=TANK_EDGE, weight="bold", zorder=30))
        halo(ax.text(fp[0], fp[1], fp[2] - 2.4, "floor (-y): no receiver", ha="center",
                     fontsize=7.0, color=TANK_EDGE, weight="bold", zorder=30))
    if show_region:
        ax.add_collection3d(Line3DCollection(box_edges(SWEEP / 2.0), colors=REGION,
                            linewidths=0.8, alpha=0.65, linestyles=LINESTYLES[1]))
    if show_cloud:
        uq = np.unique(POS, axis=0)
        if len(uq) > 400:
            uq = uq[np.random.default_rng(0).choice(len(uq), 400, replace=False)]
        q = TP(uq)
        ax.scatter(q[:, 0], q[:, 1], q[:, 2], s=3.0, c=CLOUD, alpha=0.35,
                   edgecolors="white", linewidths=0.25, depthshade=False)
    for i, (centre, wall, ysign) in enumerate(sp_walls, start=1):
        col = UPPER if ysign >= 0 else LOWER
        ax.add_collection3d(Poly3DCollection([receiver_patch(centre, wall)],
                            facecolor=col, edgecolor="#1a1a1a", linewidths=0.5,
                            alpha=patch_alpha))
        if label_ports:
            lp = TP([centre[0] * 1.16, centre[1] + (0.45 if ysign >= 0 else -0.45),
                     centre[2] * 1.16])
            halo(ax.text(lp[0], lp[1], lp[2], f"P{i}", fontsize=7.5, color="#111",
                         ha="center", va="center", weight="bold", zorder=40),
                 linewidth=2.2)
    if show_capsule:
        ax.add_collection3d(Line3DCollection(capsule_lines(axis="z"),
                            colors=CAPSULE, linewidths=1.0))
        c0 = TP([0, 0, 1.5]); cv = TP([0, 0, 3.0]) - TP([0, 0, 0])
        ax.quiver(c0[0], c0[1], c0[2], cv[0], cv[1], cv[2], color=CAPSULE, lw=1.4,
                  arrow_length_ratio=0.4)


V4 = [(SP[i].tolist(), wall_of(SP[i]), np.sign(SP[i, 1])) for i in range(4)]

# =============================================================== Figure 1 (3D)
fig = plt.figure(figsize=(W1, 3.45))
ax = fig.add_subplot(111, projection="3d")
draw_array(ax, V4, HALF, show_cloud=True, show_region=True, show_capsule=True,
           mark_faces=True)
style_axes(ax, HALF)
handles = [
    Patch(facecolor=UPPER, edgecolor="#1a1a1a", label="upper Rx, y=+6.75 cm"),
    Patch(facecolor=LOWER, edgecolor="#1a1a1a", label="lower Rx, y=-7.25 cm"),
    Patch(facecolor=NO_RX_FACE, edgecolor=TANK_EDGE, alpha=0.4, label="top/floor: no Rx"),
    Line2D([0], [0], color=REGION, ls="--", label="capsule-center volume"),
    Line2D([0], [0], marker="o", color="none", markerfacecolor=CLOUD,
           markeredgecolor="white", markeredgewidth=0.3,
           markersize=4, label="simulated centers"),
    Line2D([0], [0], color=CAPSULE, label="capsule pose"),
]
fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.015),
           frameon=False, fontsize=6.6, handlelength=1.4, labelspacing=0.28,
           columnspacing=0.75, ncol=2)
ax.set_position([0.02, 0.34, 0.96, 0.62])
save(fig, "fig_geometry.pdf")

# ===================================================== geometry ablation (grid)
SY_P, SY_N = 6.75, -7.25


def make_variant(kind):
    walls = [("-z", SP[0]), ("+z", SP[1]), ("+x", SP[2]), ("-x", SP[3])]
    out = []
    for wall, p in walls:
        c = p.copy()
        if kind == "symmetric":
            c[1] = 0.0
        elif kind == "common":
            c[1] = SY_P
        elif kind == "v4":
            c[1] = SY_P if wall in ("-z", "+x") else SY_N
        out.append((c.tolist(), wall, np.sign(c[1]) if c[1] != 0 else 1))
    return out


variants = [
    ("symmetric", "y=0\nmirror-symmetric"),
    ("common", "+y\ncommon-mode"),
    ("v4", "+/-y\nanti-symmetric"),
]
fig = plt.figure(figsize=(W2, 2.65))
for k, (kind, note) in enumerate(variants):
    ax = fig.add_subplot(1, 3, k + 1, projection="3d")
    layout = make_variant(kind)
    if kind == "symmetric":
        layout = [(c, w, 0.5) for (c, w, _s) in layout]
    draw_array(ax, layout, HALF, mark_faces=True, lw_tank=0.7, patch_alpha=0.95,
               label_ports=False)
    style_axes(ax, HALF, compact=True)
    panel_letter(ax, "abc"[k], x=0.03, y=0.96)
    ax.text2D(0.5, 0.02, note, transform=ax.transAxes, ha="center", va="top",
              fontsize=7.0, color=TANK_EDGE)
fig.subplots_adjust(left=0.01, right=0.995, top=0.98, bottom=0.06, wspace=0.01)
save(fig, "fig_geometry_ablation.pdf")
