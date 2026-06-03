"""Shared publication styling for paper figures.

The figures are authored at final IEEE print size and exported as vector PDF
with embedded TrueType fonts. Dense scatter layers should opt into
``rasterized=True`` locally; text and axes remain vector.
"""
from __future__ import annotations

import os

import matplotlib as mpl
from cycler import cycler

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "figures")

# IEEE Transactions column widths in inches.
W1 = 3.5
W2 = 7.16

# Okabe-Ito / Wong colorblind-safe cycle. CFM blue is intentionally first.
PALETTE = [
    "#0072B2",  # CFM
    "#D55E00",  # deterministic backbone / lower receivers
    "#009E73",
    "#CC79A7",
    "#E69F00",
    "#56B4E9",
    "#F0E442",
    "#000000",
]

COLORS = {
    "cfm": PALETTE[0],
    "det": PALETTE[1],
    "green": PALETTE[2],
    "purple": PALETTE[3],
    "orange": PALETTE[4],
    "sky": PALETTE[5],
    "yellow": PALETTE[6],
    "black": PALETTE[7],
    "dark": "#4D4D4D",
    "classical": "#999999",
    "light": "#CCCCCC",
    "grid": "#B0B0B0",
    "good": PALETTE[2],
    "warn": PALETTE[4],
    "mut": "#999999",
    "p1": PALETTE[5],
    "p2": PALETTE[3],
    "tank": "#F2F2F2",
}

LINESTYLES = ["-", "--", "-.", ":", (0, (3, 1, 1, 1))]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]
HATCHES = ["", "//", "..", "xx", "\\\\", "++", "--", "oo"]


def apply_style() -> None:
    """Apply the shared IEEE/Nature-compatible Matplotlib style."""
    mpl.rcParams.update(
        {
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
            "mathtext.fontset": "dejavusans",
            "font.size": 8,
            "axes.titlesize": 8,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "figure.titlesize": 8,
            "axes.linewidth": 0.5,
            "lines.linewidth": 0.9,
            "lines.markersize": 4,
            "lines.markeredgewidth": 0.5,
            "patch.linewidth": 0.5,
            "xtick.major.width": 0.5,
            "ytick.major.width": 0.5,
            "xtick.major.size": 2.5,
            "ytick.major.size": 2.5,
            "grid.linewidth": 0.4,
            "xtick.direction": "out",
            "ytick.direction": "out",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": "#333333",
            "axes.grid": False,
            "grid.color": COLORS["grid"],
            "grid.alpha": 0.3,
            "axes.axisbelow": True,
            "legend.frameon": False,
            "legend.handlelength": 1.8,
            "legend.borderpad": 0.4,
            "figure.dpi": 200,
            "savefig.dpi": 600,
            "savefig.bbox": None,
            "savefig.pad_inches": 0.0,
            "axes.titlepad": 3,
            "axes.labelpad": 2,
            "axes.prop_cycle": cycler(color=PALETTE),
        }
    )


def panel_letter(ax, letter: str, x: float = 0.015, y: float = 0.985):
    """Place a bold lowercase panel letter inside the top-left axes corner."""
    text_fn = ax.text2D if getattr(ax, "name", "") == "3d" and hasattr(ax, "text2D") else ax.text
    return text_fn(
        x,
        y,
        letter,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        fontweight="bold",
        color="#111111",
        zorder=100,
    )


def save(fig, name: str) -> None:
    """Save a fixed-size 600 dpi vector PDF with embedded metadata."""
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(
        os.path.join(OUT, name),
        dpi=600,
        bbox_inches=None,
        pad_inches=0.0,
        metadata={
            "Title": name,
            "Creator": "reports/paper/paperstyle.py",
            "Subject": "IEEE/Nature submission figure",
        },
    )
    # Import locally so this helper is safe before pyplot is initialized.
    import matplotlib.pyplot as plt

    plt.close(fig)
    print("wrote", name)


apply_style()
