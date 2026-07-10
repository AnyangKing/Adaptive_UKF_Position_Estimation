from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "82. 준정지 속도 경계 검증 실행" / "results" / "quasi_static_boundary.json"
OUT = Path(__file__).resolve().parent / "figures"


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    by_speed = data["summary"]["by_speed"]

    speeds = sorted(float(k) for k in by_speed.keys())
    labels = [f"{s:.3f}" for s in speeds]
    x = list(range(len(speeds)))
    gains = [by_speed[f"{s:.3f}"]["mean_gain_m"] for s in speeds]
    lag_reductions = [by_speed[f"{s:.3f}"]["mean_lag1_reduction"] for s in speeds]
    decisions = [by_speed[f"{s:.3f}"]["decision"] for s in speeds]

    OUT.mkdir(parents=True, exist_ok=True)

    fig, ax1 = plt.subplots(figsize=(7.6, 4.2), dpi=220)
    ax2 = ax1.twinx()

    ax1.axhline(0.0, color="#fecaca", linestyle="--", linewidth=1.0, zorder=0)
    ax1.plot(x, gains, marker="o", color="#2563eb", linewidth=2.2, label="RMSE gain")
    ax2.plot(
        x,
        lag_reductions,
        marker="s",
        color="#dc2626",
        linewidth=2.0,
        label="lag-1 reduction",
    )

    for xi, y, decision in zip(x, gains, decisions):
        if decision == "validated":
            ax1.scatter([xi], [y], s=70, facecolors="none", edgecolors="#16a34a", linewidths=1.8)
        else:
            ax1.scatter([xi], [y], s=70, marker="x", color="#111827", linewidths=1.8)

    ax1.axvspan(-0.25, 1.25, color="#dcfce7", alpha=0.35, label="continuous validated region")
    ax1.text(
        0.55,
        max(gains) * 0.92,
        "continuous\nboundary\n0.005 m/s",
        ha="center",
        va="top",
        fontsize=8,
        color="#166534",
    )

    ax1.set_title("Quasi-static speed boundary at 600 m")
    ax1.set_xlabel("speed (m/s)")
    ax1.set_ylabel("mean RMSE gain, fixed - hop (m)", color="#2563eb")
    ax2.set_ylabel("elevation residual lag-1 reduction", color="#dc2626")
    ax1.tick_params(axis="y", labelcolor="#2563eb")
    ax2.tick_params(axis="y", labelcolor="#dc2626")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, rotation=0)
    ax1.set_xlim(-0.35, len(x) - 0.65)
    ax1.grid(True, axis="y", linestyle=":", color="#cbd5e1")

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="lower right", fontsize=8)

    fig.tight_layout()
    fig.savefig(OUT / "fig5_quasi_static_speed_boundary.png")
    fig.savefig(OUT / "fig5_quasi_static_speed_boundary.svg")


if __name__ == "__main__":
    main()
