"""Generate first-pass manuscript figures from validated experiment JSON files.

This folder is intentionally a paper-assembly step, not a new estimator experiment.
It converts the strongest validated results into reproducible PNG/SVG figures:

1. frequency-agile carrier hopping reduces coherent DOA bias in static geometry;
2. the same mechanism improves static 600 m localization RMSE;
3. moving targets show whitening but not reliable RMSE gain;
4. earlier CRLB analysis explains why sub-meter performance is not expected at 600 m.
"""

from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "figures"


def numbered_folder(prefix: str) -> Path:
    matches = sorted(p for p in ROOT.glob(prefix + "*") if p.is_dir())
    if not matches:
        raise FileNotFoundError(f"Cannot find numbered folder: {prefix}*")
    return matches[0]


def load_json(prefix: str, *parts: str) -> dict:
    path = numbered_folder(prefix).joinpath(*parts)
    return json.loads(path.read_text(encoding="utf-8"))


def savefig(name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.tight_layout(pad=0.6)
    for ext in ("png", "svg"):
        plt.savefig(OUT / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close()


def style() -> None:
    plt.rcParams.update(
        {
            "figure.figsize": (6.6, 3.8),
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.unicode_minus": False,
        }
    )


def fig2_frequency_agile_bias(agility: dict) -> dict:
    distances = [100, 200, 400, 600]
    fixed = [agility["summary"][str(d)]["median_abs_bias_32k_deg"] for d in distances]
    hopped = [agility["summary"][str(d)]["median_abs_bias_hopavg_deg"] for d in distances]
    reductions = [agility["summary"][str(d)]["hop_reduction_pct"] for d in distances]

    x = list(range(len(distances)))
    width = 0.36

    plt.figure()
    plt.bar([i - width / 2 for i in x], fixed, width, label="Fixed 32 kHz", color="#4C78A8")
    plt.bar([i + width / 2 for i in x], hopped, width, label="Frequency-agile average", color="#F58518")
    ytop = max(max(fixed), max(hopped)) * 1.24
    plt.ylim(0, ytop)
    for i, pct in enumerate(reductions):
        ymax = max(fixed[i], hopped[i])
        label = f"−{pct:.0f}%" if pct >= 0 else f"+{abs(pct):.0f}%"
        color = "#2F7D32" if pct >= 0 else "#B00020"
        plt.text(i, ymax + ytop * 0.025, label, ha="center", va="bottom", fontsize=9, color=color)

    plt.xticks(x, [f"{d} m" for d in distances])
    plt.ylabel("Median absolute DOA bias (deg)")
    plt.xlabel("Target range")
    plt.title("Frequency agility suppresses long-range coherent DOA bias")
    plt.legend(frameon=False, loc="upper right")
    savefig("fig2_frequency_agile_bias")

    return {
        "distances_m": distances,
        "fixed_32k_median_abs_bias_deg": fixed,
        "hop_average_median_abs_bias_deg": hopped,
        "reduction_pct": reductions,
    }


def fig3_static_600m_paired(static: dict) -> dict:
    trials_600 = [t for t in static["trials"] if int(t["distance"]) == 600]
    fixed = [t["fixed_settled_rmse_m"] for t in trials_600]
    hopped = [t["hop_settled_rmse_m"] for t in trials_600]
    improvement = [t["improvement_m"] for t in trials_600]
    summary = static["summary"]["600"]

    plt.figure()
    for i, (f, h) in enumerate(zip(fixed, hopped)):
        color = "#54A24B" if h < f else "#E45756"
        plt.plot([0, 1], [f, h], color=color, alpha=0.45, linewidth=1.2)
        plt.scatter([0, 1], [f, h], color=color, s=20, alpha=0.8)

    plt.scatter([0, 1], [mean(fixed), mean(hopped)], color="black", s=85, zorder=5, label="Mean")
    plt.xticks([0, 1], ["Fixed 32 kHz", "Frequency-agile"])
    plt.ylabel("Settled RMSE (m)")
    plt.title("Static 600 m localization improves under frequency agility")
    plt.text(
        0.02,
        0.96,
        f"mean: {summary['fixed_mean_rmse_m']:.2f} → {summary['hop_mean_rmse_m']:.2f} m\n"
        f"Δ={summary['mean_improvement_m']:.2f} m, p={summary['wilcoxon_greater_p']:.4f}",
        transform=plt.gca().transAxes,
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#CCCCCC", alpha=0.9),
    )
    plt.legend(frameon=False, loc="upper right")
    savefig("fig3_static_600m_paired_rmse")

    return {
        "n": len(trials_600),
        "fixed_mean_rmse_m": mean(fixed),
        "hop_mean_rmse_m": mean(hopped),
        "mean_improvement_m": mean(improvement),
        "improved_fraction": sum(1 for v in improvement if v > 0) / len(improvement),
        "wilcoxon_greater_p": summary["wilcoxon_greater_p"],
    }


def fig4_moving_whitening_lag1(moving: dict) -> dict:
    runs = moving["runs"]
    fixed = [r["lag1_fixed"] for r in runs]
    hopped = [r["lag1_hop"] for r in runs]
    summary = moving["summary"]["M2_whitening"]
    pooled = moving["summary"]["M1_pooled_moving"]

    plt.figure()
    for f, h in zip(fixed, hopped):
        color = "#54A24B" if h < f else "#E45756"
        plt.plot([0, 1], [f, h], color=color, alpha=0.3, linewidth=1.0)
    plt.boxplot([fixed, hopped], positions=[0, 1], widths=0.42, showfliers=False)
    plt.scatter([0] * len(fixed), fixed, s=14, alpha=0.45, color="#4C78A8", label="Runs")
    plt.scatter([1] * len(hopped), hopped, s=14, alpha=0.45, color="#F58518")
    plt.axhline(0.0, color="black", linewidth=0.9, alpha=0.6)
    plt.xticks([0, 1], ["Fixed", "Frequency-agile"])
    plt.ylabel("Lag-1 correlation of DOA residual")
    plt.title("Moving targets: whitening without reliable RMSE gain")
    plt.text(
        0.02,
        0.96,
        f"lag-1: {summary['mean_lag1_fixed']:.2f} → {summary['mean_lag1_hop']:.2f}, "
        f"p={summary['wilcoxon_fixed_gt_hop_p']:.1e}\n"
        f"pooled RMSE gain={pooled['mean_gain_m']:.2f} m, p={pooled['wilcoxon_greater_p']:.3f}",
        transform=plt.gca().transAxes,
        va="top",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#CCCCCC", alpha=0.9),
    )
    savefig("fig4_moving_whitening_lag1")

    return {
        "n": len(runs),
        "mean_lag1_fixed": mean(fixed),
        "mean_lag1_hop": mean(hopped),
        "whitening_p": summary["wilcoxon_fixed_gt_hop_p"],
        "pooled_moving_mean_gain_m": pooled["mean_gain_m"],
        "pooled_moving_p": pooled["wilcoxon_greater_p"],
    }


def fig7_crlb_floor(crlb: dict) -> dict:
    distances = [100, 200, 400, 600]
    empirical = [crlb["summary"][str(d)]["crlb_empirical_m"] for d in distances]
    routing = [crlb["summary"][str(d)]["routing_rmse_m"] for d in distances]
    nls = [crlb["summary"][str(d)]["nls_rmse_m"] for d in distances]
    floor = [crlb["summary"][str(d)]["routing_bias_floor_vs_emp_m"] for d in distances]

    plt.figure()
    plt.plot(distances, empirical, marker="o", label="Empirical CRLB", color="#4C78A8")
    plt.plot(distances, nls, marker="s", label="NLS RMSE", color="#72B7B2")
    plt.plot(distances, routing, marker="^", label="Routed UKF RMSE", color="#F58518")
    plt.fill_between(distances, empirical, routing, where=[r >= e for r, e in zip(routing, empirical)], color="#F58518", alpha=0.12)
    plt.xlabel("Target range (m)")
    plt.ylabel("Position error / lower bound (m)")
    plt.title("Aperture-limited floor explains long-range RMSE")
    plt.text(
        0.56,
        0.12,
        f"600 m residual bias floor ≈ {floor[-1]:.2f} m",
        transform=plt.gca().transAxes,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="#CCCCCC", alpha=0.9),
    )
    plt.legend(frameon=False)
    savefig("fig7_crlb_floor")

    return {
        "distances_m": distances,
        "empirical_crlb_m": empirical,
        "nls_rmse_m": nls,
        "routing_rmse_m": routing,
        "routing_bias_floor_vs_emp_m": floor,
    }


def main() -> None:
    style()
    agility = load_json("58.", "results", "agility.json")
    static = load_json("61.", "results", "static_hop_validation.json")
    moving = load_json("63.", "results", "moving_validation.json")
    crlb = load_json("45.", "results", "crlb.json")

    summary = {
        "fig2_frequency_agile_bias": fig2_frequency_agile_bias(agility),
        "fig3_static_600m_paired_rmse": fig3_static_600m_paired(static),
        "fig4_moving_whitening_lag1": fig4_moving_whitening_lag1(moving),
        "fig7_crlb_floor": fig7_crlb_floor(crlb),
        "interpretation": {
            "paper_axis": "TOA/TDOA/DOA fused by UKF, with frequency-agile transmission used to whiten coherent multipath DOA bias.",
            "positive_domain": "static/quasi-static long-range targets, especially 600 m in the current validation.",
            "boundary": "moving targets show residual whitening but not reproducible RMSE improvement.",
            "performance_floor": "sub-meter 600 m performance is not supported by the aperture/CRLB analysis under the current array and realistic noise assumptions.",
        },
    }
    (OUT / "summary_numbers.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output_dir": str(OUT), "figures": sorted(p.name for p in OUT.glob("*"))}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
