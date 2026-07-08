"""Generate a first-pass conceptual Fig. 1 for the manuscript.

The figure is intentionally schematic. It explains the mechanism behind the
frequency-agile result rather than reporting a new experiment:

- compact 8-sensor USBL array receives a direct path and an in-gate surface
  reflection;
- gated SRP/DOA processing cannot fully remove coherent leakage;
- fixed carrier locks the interference phase;
- carrier hopping rotates the phase phi = 2*pi*f*delta across pings.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


OUT = Path(__file__).resolve().parent / "figures"


def setup() -> None:
    plt.rcParams.update(
        {
            "figure.figsize": (9.0, 4.6),
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.bottom": False,
            "axes.spines.left": False,
            "xtick.bottom": False,
            "ytick.left": False,
            "xtick.labelbottom": False,
            "ytick.labelleft": False,
        }
    )


def draw_geometry(ax) -> None:
    ax.set_title("(a) Shallow-water USBL geometry and in-gate leakage")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    # Water boundaries
    ax.plot([0, 10], [5.45, 5.45], color="#4C78A8", linewidth=2)
    ax.text(0.2, 5.6, "sea surface", color="#4C78A8")
    ax.plot([0, 10], [0.45, 0.45], color="#8D6E63", linewidth=2)
    ax.text(0.2, 0.12, "seafloor", color="#8D6E63")

    # Receiver and beacon
    rx = (1.45, 2.65)
    tx = (8.45, 2.05)
    surface_reflect = (5.1, 5.45)
    ax.scatter(*rx, s=90, color="#1F77B4", zorder=5)
    ax.text(rx[0] - 0.45, rx[1] + 0.35, "8-sensor\nUSBL array", ha="center")
    ax.scatter(*tx, s=90, color="#D62728", marker="*", zorder=5)
    ax.text(tx[0] + 0.25, tx[1] + 0.15, "beacon / target", va="center")

    # Direct and reflected paths
    ax.add_patch(FancyArrowPatch(rx, tx, arrowstyle="->", mutation_scale=13, color="#222222", linewidth=2))
    ax.text(4.8, 2.15, "direct path", color="#222222", rotation=-5)
    ax.plot([rx[0], surface_reflect[0], tx[0]], [rx[1], surface_reflect[1], tx[1]], "--", color="#F58518", linewidth=2)
    ax.add_patch(FancyArrowPatch(surface_reflect, tx, arrowstyle="->", mutation_scale=13, color="#F58518", linewidth=0))
    ax.text(4.15, 4.95, "surface-reflected path", color="#F58518")

    # Gate window callout
    gate = Rectangle((6.15, 1.25), 2.25, 1.65, fill=False, linestyle=":", linewidth=1.6, color="#9467BD")
    ax.add_patch(gate)
    ax.text(6.35, 2.85, "5 ms DOA gate", color="#9467BD")
    ax.text(6.3, 1.05, "direct + leakage\nprocessed coherently", color="#9467BD")

    # Array inset
    inset_center = (1.45, 1.35)
    ax.add_patch(Circle(inset_center, 0.42, fill=False, color="#1F77B4", linewidth=1.2))
    for k in range(8):
        a = 2 * math.pi * k / 8
        ax.add_patch(Circle((inset_center[0] + 0.42 * math.cos(a), inset_center[1] + 0.42 * math.sin(a)), 0.045, color="#1F77B4"))
    ax.text(inset_center[0], 0.72, "compact aperture", ha="center", color="#1F77B4")


def draw_phase(ax) -> None:
    ax.set_title("(b) Carrier hopping rotates the coherent bias phase")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)

    ax.text(0.3, 5.35, r"interference phase:  $\phi = 2\pi f\delta$", fontsize=11)
    ax.text(0.3, 4.88, r"$\delta$: direct--reflection delay difference", color="#555555")

    # Fixed carrier column
    ax.text(1.7, 4.25, "fixed carrier", ha="center", weight="bold")
    fixed_center = (1.7, 2.75)
    ax.add_patch(Circle(fixed_center, 0.9, fill=False, color="#999999", linewidth=1.2))
    angle = math.radians(35)
    end = (fixed_center[0] + 0.78 * math.cos(angle), fixed_center[1] + 0.78 * math.sin(angle))
    for _ in range(5):
        ax.add_patch(FancyArrowPatch(fixed_center, end, arrowstyle="->", mutation_scale=12, color="#4C78A8", linewidth=1.6, alpha=0.7))
    ax.text(fixed_center[0], 1.25, "same phase\n→ correlated bias", ha="center", color="#4C78A8")

    # Frequency-agile column
    ax.text(6.35, 4.25, "frequency-agile pinging", ha="center", weight="bold")
    hop_center = (6.35, 2.75)
    ax.add_patch(Circle(hop_center, 0.9, fill=False, color="#999999", linewidth=1.2))
    colors = ["#F58518", "#54A24B", "#E45756", "#72B7B2", "#B279A2"]
    for i, deg in enumerate([20, 95, 170, 245, 315]):
        a = math.radians(deg)
        end = (hop_center[0] + 0.78 * math.cos(a), hop_center[1] + 0.78 * math.sin(a))
        ax.add_patch(FancyArrowPatch(hop_center, end, arrowstyle="->", mutation_scale=12, color=colors[i], linewidth=1.6, alpha=0.85))
        ax.text(end[0] * 0.98 + hop_center[0] * 0.02, end[1] * 0.98 + hop_center[1] * 0.02, f"f{i+1}", color=colors[i], fontsize=8)
    ax.text(hop_center[0], 1.25, "rotating phase\n→ whitened bias", ha="center", color="#2F7D32")

    # Arrow linking columns
    ax.add_patch(FancyArrowPatch((3.0, 2.75), (5.0, 2.75), arrowstyle="->", mutation_scale=15, color="#333333", linewidth=1.4))
    ax.text(4.0, 3.05, "change f,\nnot the array", ha="center", fontsize=8)

    # UKF output note
    box = Rectangle((8.05, 0.26), 1.68, 0.88, fill=True, facecolor="#F4F4F4", edgecolor="#BBBBBB")
    ax.add_patch(box)
    ax.text(8.89, 0.70, "TOA/TDOA/DOA\n→ UKF position", ha="center", va="center", fontsize=8.5)


def main() -> None:
    setup()
    fig, axes = plt.subplots(1, 2)
    draw_geometry(axes[0])
    draw_phase(axes[1])
    fig.suptitle("Frequency-agile USBL positioning: coherent multipath bias whitening", fontsize=12, y=0.98)
    plt.tight_layout(pad=0.7, rect=[0, 0, 1, 0.94])

    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(OUT / f"fig1_system_concept.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
