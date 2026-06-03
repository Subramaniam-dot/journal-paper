#!/usr/bin/env python3
"""fig_phase_sensitivity.pdf: SDR phase-drift survivability curve.

Plots the cheap test-perturbation-only calibration-mismatch protocol:
train on clean features, perturb held-out receiver-link phase, and evaluate
S3/S5 tree models without retraining.  All values are CST simulation and are
framed as a portable coherent SDR-array requirement, not a VNA measurement.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from paperstyle import COLORS, LINESTYLES, MARKERS, W1, save


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DATA = REPO / "experiments" / "feature_ablation" / "phase_noise_sensitivity_latest.json"


def levels(payload: dict, subset: str, model: str):
    rows = payload["summary"]["drift"]["subsets"][subset]["models"][model]["levels"]
    x = [float(r["level_deg"]) for r in rows]
    y = [float(r["mean_cm"]) for r in rows]
    e = [float(r["std_cm"]) for r in rows]
    return x, y, e


def main() -> int:
    payload = json.load(open(DATA))
    floor = payload["s1_magnitude_floor_cm"]

    fig, ax = plt.subplots(figsize=(W1, 2.25))
    ax.axvspan(2, 10, color=COLORS["good"], alpha=0.12, lw=0)
    ax.text(3.0, 1.92, "calibrated SDR", color=COLORS["good"], fontsize=7, va="center")

    style = {
        ("histgb", "S3_mics_magphase"): (COLORS["cfm"], LINESTYLES[0], MARKERS[0], "HistGB S3 MICS"),
        ("histgb", "S5_full_rich"): (COLORS["cfm"], LINESTYLES[1], MARKERS[1], "HistGB S5 full"),
        ("extratrees", "S3_mics_magphase"): (COLORS["det"], LINESTYLES[0], MARKERS[2], "ExtraTrees S3"),
        ("extratrees", "S5_full_rich"): (COLORS["det"], LINESTYLES[1], MARKERS[3], "ExtraTrees S5"),
    }

    for (model, subset), (color, ls, marker, label) in style.items():
        x, y, e = levels(payload, subset, model)
        ax.errorbar(
            x,
            y,
            yerr=e,
            color=color,
            linestyle=ls,
            marker=marker,
            markersize=3.4,
            linewidth=0.95,
            elinewidth=0.55,
            capsize=1.5,
            label=label,
        )

    floor_mean = floor.get("histgb", 1.5)
    ax.axhline(floor_mean, color=COLORS["dark"], linestyle="--", linewidth=0.9)
    ax.text(31, floor_mean + 0.045, "S1 magnitude floor", color=COLORS["dark"], fontsize=7)

    ax.set_xlabel("inter-receiver phase drift $\\sigma$ (deg)")
    ax.set_ylabel("3D MAE (cm)")
    ax.set_xlim(-1, 61)
    ax.set_ylim(0.85, 2.05)
    ax.set_xticks([0, 5, 10, 15, 30, 45, 60])
    ax.grid(True, axis="y")

    handles, labels = ax.get_legend_handles_labels()
    band = Line2D([0], [0], color=COLORS["good"], lw=5, alpha=0.18, label="2-10 deg SDR band")
    handles.append(band)
    labels.append("2-10 deg SDR band")
    ax.legend(handles, labels, loc="lower right", ncol=1, frameon=False, handlelength=2.0)
    fig.subplots_adjust(left=0.12, right=0.985, bottom=0.19, top=0.985)
    save(fig, "fig_phase_sensitivity.pdf")
    print(os.path.join(HERE, "figures", "fig_phase_sensitivity.pdf"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
