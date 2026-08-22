from __future__ import annotations

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figures"
SOURCE = ROOT / "82. 준정지 속도 경계 검증 실행" / "result_summary.md"


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.2,
            "axes.titlesize": 7.8,
            "axes.labelsize": 7.4,
            "xtick.labelsize": 6.9,
            "ytick.labelsize": 6.9,
            "legend.fontsize": 6.8,
            "axes.linewidth": 0.65,
            "axes.grid": True,
            "grid.alpha": 0.24,
            "grid.linewidth": 0.45,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.dpi": 600,
            "figure.dpi": 160,
        }
    )


def parse_rows() -> list[dict[str, float | str]]:
    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    rows = []
    for line in text.splitlines():
        m = re.match(
            r"\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([+-]?[0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([^|]+)\|",
            line,
        )
        if m:
            rows.append(
                {
                    "speed": float(m.group(1)),
                    "fixed": float(m.group(2)),
                    "agile": float(m.group(3)),
                    "gain": float(m.group(4)),
                    "p": float(m.group(5)),
                    "decision": m.group(7).strip(),
                }
            )
    if not rows:
        raise RuntimeError(f"No rows parsed from {SOURCE}")
    return rows


def main() -> None:
    setup_style()
    rows = parse_rows()
    x = np.arange(len(rows))
    colors = ["#2CA02C" if r["decision"] == "validated" else "#D62728" for r in rows]

    fig, ax = plt.subplots(figsize=(3.25, 2.25))
    ax.axhline(0, color="#111827", lw=0.65, alpha=0.55)
    ax.bar(x, [float(r["gain"]) for r in rows], color=colors, alpha=0.78, width=0.72)
    ax.set_xticks(
        x,
        [f"{float(r['speed']):.3f}".rstrip("0").rstrip(".") if r["speed"] else "0" for r in rows],
        rotation=25,
    )
    ax.set_xlabel("Drift speed (m/s)")
    ax.set_ylabel("RMSE gain (m)")
    ax.set_title("Quasi-static boundary at 600 m")

    ymax = max(float(r["gain"]) for r in rows)
    ymin = min(float(r["gain"]) for r in rows)
    ax.set_ylim(min(-0.60, ymin - 0.28), ymax + 0.70)

    for i, r in enumerate(rows):
        gain = float(r["gain"])
        label = "sig." if r["decision"] == "validated" else "n.s."
        y = gain + (0.20 if gain >= 0 else -0.22)
        ax.text(
            i,
            y,
            label,
            ha="center",
            va="bottom" if gain >= 0 else "top",
            fontsize=6.2,
            color="#111827",
            bbox={"boxstyle": "round,pad=0.12", "facecolor": "white", "edgecolor": "none", "alpha": 0.78},
        )

    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(pad=0.35)
    fig.savefig(OUT / "fig5_quasi_static_speed_boundary.pdf", bbox_inches="tight")
    fig.savefig(OUT / "fig5_quasi_static_speed_boundary.png", dpi=600, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
