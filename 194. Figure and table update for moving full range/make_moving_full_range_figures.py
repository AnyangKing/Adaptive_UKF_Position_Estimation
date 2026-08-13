from __future__ import annotations

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(__file__).with_name("moving_full_range_source.csv")
FIG_DIR = ROOT / "paper" / "figures"


def load_rows():
    with SOURCE.open(newline="", encoding="utf-8") as f:
        return [
            {k: float(v) for k, v in row.items()}
            for row in csv.DictReader(f)
        ]


def save_rmse_plot(rows):
    x = [r["distance_m"] for r in rows]
    fixed = [r["fixed_rmse_m"] for r in rows]
    hop = [r["hop_rmse_m"] for r in rows]
    soft = [r["softR_rmse_m"] for r in rows]

    fig, ax = plt.subplots(figsize=(7.2, 4.1), dpi=220)
    ax.plot(x, fixed, marker="o", linewidth=2.1, label="Fixed 32 kHz")
    ax.plot(x, hop, marker="s", linewidth=2.1, label="Plain hop")
    ax.plot(x, soft, marker="^", linewidth=2.4, label="Transition-aware soft-R")
    ax.axvline(800, color="0.55", linestyle="--", linewidth=1.2)
    ax.annotate(
        "hop tail\nrecovered",
        xy=(800, 22.386),
        xytext=(705, 20.7),
        arrowprops={"arrowstyle": "->", "lw": 1.0, "color": "0.25"},
        fontsize=9,
    )
    ax.set_xlabel("Nominal range (m)")
    ax.set_ylabel("Settled RMSE (m)")
    ax.set_title("Moving full-range validation (528 paired cases)")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    out = FIG_DIR / "fig7_moving_full_range_rmse.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def save_gain_tail_plot(rows):
    x = [r["distance_m"] for r in rows]
    gain_fixed = [r["softR_gain_vs_fixed_m"] for r in rows]
    gain_hop = [r["softR_gain_vs_hop_m"] for r in rows]
    tail = [100 * r["softR_tail_worsened_vs_hop"] for r in rows]

    fig, ax1 = plt.subplots(figsize=(7.2, 4.1), dpi=220)
    ax1.axhline(0, color="0.55", linewidth=1.0)
    ax1.plot(x, gain_fixed, marker="o", linewidth=2.2, label="soft-R gain vs fixed")
    ax1.plot(x, gain_hop, marker="s", linewidth=2.2, label="soft-R gain vs hop")
    ax1.set_xlabel("Nominal range (m)")
    ax1.set_ylabel("RMSE gain (m)")
    ax1.grid(True, alpha=0.25)

    ax2 = ax1.twinx()
    ax2.bar(x, tail, width=42, alpha=0.18, color="tab:red", label="tail worsened vs hop")
    ax2.set_ylabel("Tail worsened vs hop (%)")
    ax2.set_ylim(0, max(tail) * 1.35 + 1)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, frameon=False, loc="upper left")
    ax1.set_title("Transition-aware gain and remaining tail risk")
    fig.tight_layout()
    out = FIG_DIR / "fig8_moving_full_range_gain_tail.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    outputs = [save_rmse_plot(rows), save_gain_tail_plot(rows)]
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()
