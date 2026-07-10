from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, FancyBboxPatch
import numpy as np


OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(exist_ok=True)


COLORS = {
    "water": "#4C78A8",
    "seafloor": "#8D6E63",
    "direct": "#222222",
    "surface": "#F58518",
    "gate": "#8E63C7",
    "array": "#1F77B4",
    "target": "#D62728",
    "agile": "#2E8B57",
    "fixed": "#4C78A8",
    "muted": "#6B7280",
}


def add_arrow(ax, start, end, color, lw=2.8, ls="-", ms=14, z=4):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=ms,
        linewidth=lw,
        linestyle=ls,
        color=color,
        shrinkA=0,
        shrinkB=0,
        zorder=z,
    )
    ax.add_patch(arrow)
    return arrow


def add_label_box(ax, xy, text, color, width=1.8, height=0.48, fontsize=9.5):
    x, y = xy
    box = FancyBboxPatch(
        (x - width / 2, y - height / 2),
        width,
        height,
        boxstyle="round,pad=0.04,rounding_size=0.06",
        linewidth=1.0,
        edgecolor=color,
        facecolor="white",
        alpha=0.96,
        zorder=7,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize, color=color, zorder=8)


def draw_geometry(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("(a) In-gate coherent multipath in compact shallow-water USBL", loc="left", fontsize=13, pad=8)

    # water boundaries
    ax.plot([0.45, 9.55], [5.35, 5.35], color=COLORS["water"], lw=2.5)
    ax.plot([0.45, 9.55], [0.55, 0.55], color=COLORS["seafloor"], lw=2.5)
    ax.text(0.55, 5.55, "sea surface", color=COLORS["water"], fontsize=10, va="bottom")
    ax.text(0.55, 0.28, "seafloor", color=COLORS["seafloor"], fontsize=10, va="top")

    array = np.array([1.8, 2.7])
    target = np.array([8.25, 2.15])
    refl = np.array([5.15, 5.35])

    # paths
    add_arrow(ax, array, target, COLORS["direct"], lw=3.0, ms=16)
    ax.text(4.3, 2.22, "direct path", color=COLORS["direct"], fontsize=10, rotation=-5, va="center")

    ax.plot([array[0], refl[0]], [array[1], refl[1]], color=COLORS["surface"], lw=3.0, ls="--")
    add_arrow(ax, refl, target, COLORS["surface"], lw=3.0, ls="--", ms=16)
    ax.text(4.05, 4.28, "surface-reflected path", color=COLORS["surface"], fontsize=10, rotation=23)

    # sensors and target
    ax.scatter([array[0]], [array[1]], s=180, color=COLORS["array"], zorder=6)
    ax.scatter([target[0]], [target[1]], s=230, marker="*", color=COLORS["target"], zorder=7)
    ax.text(array[0] - 0.4, array[1] + 0.32, "8-sensor\nUSBL array", ha="right", fontsize=10)
    ax.text(target[0] + 0.24, target[1] + 0.05, "beacon / target", ha="left", fontsize=10)

    # DOA gate as time/coherence concept
    gate = Rectangle(
        (6.25, 1.42),
        2.15,
        1.55,
        linewidth=2.0,
        edgecolor=COLORS["gate"],
        facecolor="#F3ECFF",
        linestyle=(0, (1.5, 2.0)),
        alpha=0.9,
        zorder=2,
    )
    ax.add_patch(gate)
    ax.text(7.2, 3.08, "5 ms DOA gate", color=COLORS["gate"], fontsize=10.5, ha="center", va="bottom")
    ax.text(
        7.2,
        1.2,
        "direct + leakage\nprocessed coherently",
        color=COLORS["gate"],
        fontsize=9.5,
        ha="center",
        va="top",
    )

    # compact aperture inset
    center = np.array([1.7, 1.15])
    r = 0.34
    for t in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        ax.scatter(center[0] + r * np.cos(t), center[1] + 0.55 * r * np.sin(t), s=28, color=COLORS["array"], zorder=6)
    ax.add_patch(Circle(center, r, fill=False, color=COLORS["array"], lw=1.3, alpha=0.85))
    ax.text(center[0] + 0.68, 0.98, "compact aperture\n66 mm", color=COLORS["array"], fontsize=9.5, ha="left", va="center")

    # mechanism note
    ax.text(
        5.05,
        5.82,
        r"$\delta$: direct--reflection delay difference inside the gate",
        fontsize=9.5,
        ha="center",
        color=COLORS["muted"],
    )


def draw_phase_panel(ax):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("(b) Carrier agility changes residual statistics before UKF fusion", loc="left", fontsize=13, pad=8)

    ax.text(0.55, 5.35, r"coherent phase:  $\phi_k = 2\pi f_k\delta_k + \theta_r$", fontsize=13)
    ax.text(0.55, 4.92, r"static target:  $\delta_k \approx \delta_0$", fontsize=10.5, color=COLORS["muted"])
    ax.text(5.55, 4.92, r"moving target:  $\delta_k=\delta(t_k)$ can self-whiten", fontsize=10.5, color=COLORS["muted"])

    # fixed carrier box
    add_label_box(ax, (2.1, 4.05), "fixed 32 kHz", COLORS["fixed"], width=1.75, height=0.45, fontsize=10)
    fixed_center = np.array([2.1, 2.8])
    ax.add_patch(Circle(fixed_center, 0.82, fill=False, color="#9CA3AF", lw=1.8))
    for a in [58, 61, 59]:
        rad = np.deg2rad(a)
        add_arrow(ax, fixed_center, fixed_center + 0.55 * np.array([np.cos(rad), np.sin(rad)]), COLORS["fixed"], lw=2.2, ms=12)
    ax.text(2.1, 1.55, "phase nearly locked\ncorrelated DOA bias", color=COLORS["fixed"], fontsize=10.5, ha="center")

    # agile carrier box
    add_label_box(ax, (6.1, 4.05), "30--34 kHz agile pings", COLORS["agile"], width=2.55, height=0.45, fontsize=10)
    agile_center = np.array([6.1, 2.8])
    ax.add_patch(Circle(agile_center, 0.82, fill=False, color="#9CA3AF", lw=1.8))
    angles = [18, 92, 164, 240, 304]
    freq_labels = ["f1", "f2", "f3", "f4", "f5"]
    freq_colors = ["#F58518", "#54A24B", "#E45756", "#72B7B2", "#B279A2"]
    for a, lab, c in zip(angles, freq_labels, freq_colors):
        rad = np.deg2rad(a)
        end = agile_center + 0.60 * np.array([np.cos(rad), np.sin(rad)])
        add_arrow(ax, agile_center, end, c, lw=2.2, ms=12)
        ax.text(end[0] + 0.10 * np.cos(rad), end[1] + 0.10 * np.sin(rad), lab, color=c, fontsize=9.5, ha="center", va="center")
    ax.text(6.1, 1.55, "phase rotates\nwhitened residual", color=COLORS["agile"], fontsize=10.5, ha="center")

    # arrow from fixed to agile
    add_arrow(ax, (3.45, 2.8), (4.75, 2.8), "#111827", lw=2.2, ms=14)
    ax.text(4.1, 3.08, "change $f_k$\nnot the array", ha="center", fontsize=10)

    # UKF fusion box
    ax.add_patch(
        FancyBboxPatch(
            (7.75, 2.05),
            1.65,
            1.25,
            boxstyle="round,pad=0.08,rounding_size=0.08",
            edgecolor="#9CA3AF",
            facecolor="#F9FAFB",
            lw=1.5,
        )
    )
    ax.text(8.58, 2.84, "same receiver", fontsize=9.5, ha="center", color=COLORS["muted"])
    ax.text(8.58, 2.48, "TOA/TDOA/DOA", fontsize=10.5, ha="center")
    ax.text(8.58, 2.18, r"$\rightarrow$ adaptive-R UKF", fontsize=10.5, ha="center")
    add_arrow(ax, (6.95, 2.8), (7.75, 2.8), COLORS["agile"], lw=2.2, ms=12)

    # bottom takeaway
    ax.text(
        5.0,
        0.62,
        "Novelty claim: not frequency hopping itself, but post-gating coherent DOA-bias whitening and its tracking boundary.",
        fontsize=10,
        ha="center",
        color="#111827",
    )


def main():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 13,
            "figure.dpi": 160,
            "savefig.dpi": 300,
            "svg.fonttype": "none",
        }
    )

    fig, axes = plt.subplots(1, 2, figsize=(15.2, 6.8), constrained_layout=False)
    fig.suptitle(
        "Carrier-agile whitening of post-gating coherent multipath DOA bias",
        fontsize=16,
        y=0.98,
    )
    draw_geometry(axes[0])
    draw_phase_panel(axes[1])
    fig.subplots_adjust(left=0.035, right=0.985, bottom=0.08, top=0.86, wspace=0.10)

    for ext in ["png", "svg"]:
        fig.savefig(OUT / f"fig1_system_concept_polished.{ext}", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
