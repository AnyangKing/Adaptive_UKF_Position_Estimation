from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figures"


COLORS = {
    "fixed": "#1F77B4",
    "hop": "#FF7F0E",
    "soft": "#2CA02C",
    "bad": "#D62728",
    "muted": "#6B7280",
    "grid": "#D1D5DB",
    "direct": "#111827",
    "surface": "#FF7F0E",
    "array": "#1F77B4",
    "target": "#D62728",
    "gate": "#7C3AED",
}


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.5,
            "axes.titlesize": 9.5,
            "axes.labelsize": 8.5,
            "xtick.labelsize": 7.8,
            "ytick.labelsize": 7.8,
            "legend.fontsize": 7.8,
            "axes.linewidth": 0.8,
            "axes.grid": True,
            "grid.alpha": 0.28,
            "grid.linewidth": 0.55,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "lines.linewidth": 1.55,
            "lines.markersize": 4.2,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.dpi": 600,
            "figure.dpi": 160,
        }
    )


def numbered(prefix: str) -> Path:
    matches = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith(prefix))
    if not matches:
        raise FileNotFoundError(prefix)
    return matches[0]


def load_json(prefix: str, *parts: str) -> dict:
    return json.loads(numbered(prefix).joinpath(*parts).read_text(encoding="utf-8"))


def save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(pad=0.45)
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=600, bbox_inches="tight")
    plt.close(fig)


def panel_label(ax, text: str) -> None:
    ax.text(
        0.0,
        1.02,
        text,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9.5,
        fontweight="bold",
    )


def add_arrow(ax, start, end, color, lw=1.9, ls="-", ms=10, z=5):
    patch = FancyArrowPatch(
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
    ax.add_patch(patch)


def fig1_system_concept() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.05))
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    panel_label(ax, "(a)")
    ax.plot([0.4, 9.6], [4.65, 4.65], color="#4C78A8", lw=1.8)
    ax.plot([0.4, 9.6], [0.45, 0.45], color="#8D6E63", lw=1.8)
    ax.text(0.45, 4.82, "surface", fontsize=7.8, color="#4C78A8")
    ax.text(0.45, 0.10, "bottom", fontsize=7.8, color="#8D6E63")

    array = np.array([1.45, 2.30])
    target = np.array([8.35, 2.05])
    refl = np.array([5.0, 4.65])
    add_arrow(ax, array, target, COLORS["direct"], lw=2.0)
    ax.plot([array[0], refl[0]], [array[1], refl[1]], "--", color=COLORS["surface"], lw=1.8)
    add_arrow(ax, refl, target, COLORS["surface"], lw=1.8, ls="--")
    ax.scatter([array[0]], [array[1]], s=70, color=COLORS["array"], zorder=6)
    ax.scatter([target[0]], [target[1]], s=120, marker="*", color=COLORS["target"], zorder=6)
    ax.text(array[0] - 0.15, array[1] + 0.35, "8-sensor\nUSBL", ha="right", fontsize=7.8)
    ax.text(target[0] + 0.18, target[1] + 0.05, "beacon", ha="left", fontsize=7.8)
    ax.text(4.1, 2.15, "direct", fontsize=7.6, color=COLORS["direct"])
    ax.text(4.05, 4.12, "surface reflection", fontsize=7.6, color=COLORS["surface"], rotation=20)
    gate = Rectangle((6.25, 1.25), 2.20, 1.45, linewidth=1.3, edgecolor=COLORS["gate"], facecolor="#F3E8FF", linestyle=(0, (2, 2)), alpha=0.75)
    ax.add_patch(gate)
    ax.text(7.35, 2.83, "5 ms DOA gate", ha="center", fontsize=7.8, color=COLORS["gate"])
    ax.text(7.35, 1.06, "coherent direct + leakage", ha="center", fontsize=7.4, color=COLORS["gate"])

    inset = np.array([1.4, 0.95])
    radius = 0.23
    for t in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        ax.scatter(inset[0] + radius * np.cos(t), inset[1] + 0.55 * radius * np.sin(t), s=12, color=COLORS["array"])
    ax.add_patch(Circle(inset, radius, fill=False, color=COLORS["array"], lw=0.9))
    ax.text(1.85, 0.85, "66 mm aperture", fontsize=7.5, color=COLORS["array"])

    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    panel_label(ax, "(b)")
    ax.text(0.15, 4.70, r"coherent phase  $\phi_k=2\pi f_k\delta_k+\theta_r$", fontsize=9.2)
    ax.text(0.15, 4.25, r"static: $\delta_k\approx\delta_0$", fontsize=7.8, color=COLORS["muted"])
    ax.text(5.05, 4.25, r"moving: $\delta_k=\delta(t_k)$ may self-whiten", fontsize=7.8, color=COLORS["muted"])
    for x0, label, color, angles in [
        (2.25, "fixed 32 kHz", COLORS["fixed"], [50, 56, 62]),
        (6.45, "30--34 kHz pings", COLORS["soft"], [15, 90, 165, 240, 310]),
    ]:
        ax.add_patch(FancyBboxPatch((x0 - 1.10, 3.35), 2.20, 0.34, boxstyle="round,pad=0.03", edgecolor=color, facecolor="white", lw=0.9))
        ax.text(x0, 3.52, label, ha="center", va="center", fontsize=7.8, color=color)
        c = np.array([x0, 2.45])
        ax.add_patch(Circle(c, 0.55, fill=False, color="#9CA3AF", lw=1.0))
        for i, a in enumerate(angles):
            rad = np.deg2rad(a)
            end = c + 0.42 * np.array([np.cos(rad), np.sin(rad)])
            add_arrow(ax, c, end, color if x0 < 4 else ["#FF7F0E", "#2CA02C", "#9467BD", "#17BECF", "#D62728"][i], lw=1.5, ms=8)
        note = "phase locked\ncorrelated bias" if x0 < 4 else "phase rotates\nless persistence"
        ax.text(x0, 1.35, note, ha="center", fontsize=7.8, color=color)
    add_arrow(ax, (3.35, 2.45), (5.25, 2.45), "#111827", lw=1.4)
    ax.text(4.30, 2.70, r"change $f_k$", ha="center", fontsize=7.8)
    ax.add_patch(FancyBboxPatch((7.85, 1.85), 1.65, 0.90, boxstyle="round,pad=0.06", edgecolor="#9CA3AF", facecolor="#F9FAFB", lw=0.9))
    ax.text(8.67, 2.48, "TOA/TDOA/DOA", ha="center", fontsize=7.8)
    ax.text(8.67, 2.12, r"Adaptive-$R$ UKF", ha="center", fontsize=7.8)
    add_arrow(ax, (7.05, 2.45), (7.85, 2.35), COLORS["soft"], lw=1.4)
    ax.text(5.0, 0.42, "Claim: observation design changes residual statistics before fusion.", ha="center", fontsize=8.0)
    save(fig, "fig1_system_concept")


def fig2_frequency_agile_bias() -> None:
    agility = load_json("58.", "results", "agility.json")
    distances = [100, 200, 400, 600]
    fixed = [agility["summary"][str(d)]["median_abs_bias_32k_deg"] for d in distances]
    hopped = [agility["summary"][str(d)]["median_abs_bias_hopavg_deg"] for d in distances]
    reductions = [agility["summary"][str(d)]["hop_reduction_pct"] for d in distances]
    x = np.arange(len(distances))
    width = 0.34
    fig, ax = plt.subplots(figsize=(3.45, 2.55))
    ax.bar(x - width / 2, fixed, width, label="fixed 32 kHz", color=COLORS["fixed"])
    ax.bar(x + width / 2, hopped, width, label="agile average", color=COLORS["hop"])
    ax.set_xticks(x, [f"{d}" for d in distances])
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Median |elevation bias| (deg)")
    ax.set_title("Carrier agility reduces coherent bias")
    ymax = max(fixed + hopped) * 1.24
    ax.set_ylim(0, ymax)
    for i, pct in enumerate(reductions):
        ax.text(i, max(fixed[i], hopped[i]) + ymax * 0.03, f"{pct:.0f}%", ha="center", va="bottom", fontsize=7.5, color=COLORS["soft"] if pct >= 0 else COLORS["bad"])
    ax.legend(frameon=False, loc="upper left")
    save(fig, "fig2_frequency_agile_bias")


def fig3_static_600m_paired_rmse() -> None:
    static = load_json("61.", "results", "static_hop_validation.json")
    trials = [t for t in static["trials"] if int(t["distance"]) == 600]
    fixed = [t["fixed_settled_rmse_m"] for t in trials]
    hop = [t["hop_settled_rmse_m"] for t in trials]
    summary = static["summary"]["600"]
    fig, ax = plt.subplots(figsize=(3.45, 2.7))
    for f, h in zip(fixed, hop):
        color = COLORS["soft"] if h < f else COLORS["bad"]
        ax.plot([0, 1], [f, h], color=color, alpha=0.38, lw=0.8)
        ax.scatter([0, 1], [f, h], color=color, s=10, alpha=0.70)
    ax.scatter([0, 1], [mean(fixed), mean(hop)], color="#111827", s=38, zorder=5, label="mean")
    ax.set_xticks([0, 1], ["Fixed\n32 kHz", "Agile\n30--34 kHz"])
    ax.set_ylabel("Settled RMSE (m)")
    ax.set_title("Static 600 m paired validation")
    ax.text(0.04, 0.96, f"{summary['fixed_mean_rmse_m']:.2f} → {summary['hop_mean_rmse_m']:.2f} m\nΔ={summary['mean_improvement_m']:.2f} m, p={summary['wilcoxon_greater_p']:.4f}", transform=ax.transAxes, va="top", fontsize=7.5, bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#D1D5DB", "alpha": 0.92})
    ax.legend(frameon=False, loc="upper right")
    save(fig, "fig3_static_600m_paired_rmse")


def fig4_moving_whitening_lag1() -> None:
    moving = load_json("63.", "results", "moving_validation.json")
    runs = moving["runs"]
    fixed = [r["lag1_fixed"] for r in runs]
    hop = [r["lag1_hop"] for r in runs]
    summary = moving["summary"]["M2_whitening"]
    pooled = moving["summary"]["M1_pooled_moving"]
    fig, ax = plt.subplots(figsize=(3.45, 2.65))
    for f, h in zip(fixed, hop):
        ax.plot([0, 1], [f, h], color=COLORS["soft"] if h < f else COLORS["bad"], alpha=0.25, lw=0.7)
    bp = ax.boxplot([fixed, hop], positions=[0, 1], widths=0.38, showfliers=False, patch_artist=True)
    for patch, color in zip(bp["boxes"], [COLORS["fixed"], COLORS["hop"]]):
        patch.set_facecolor(color)
        patch.set_alpha(0.22)
        patch.set_edgecolor(color)
    ax.scatter(np.zeros(len(fixed)) - 0.04, fixed, s=8, alpha=0.35, color=COLORS["fixed"])
    ax.scatter(np.ones(len(hop)) + 0.04, hop, s=8, alpha=0.35, color=COLORS["hop"])
    ax.axhline(0, color="#111827", lw=0.8, alpha=0.55)
    ax.set_xticks([0, 1], ["Fixed", "Agile"])
    ax.set_ylabel("Lag-1 residual correlation")
    ax.set_title("Moving: whitening but no pooled RMSE gain")
    ax.text(0.04, 0.96, f"lag-1 {summary['mean_lag1_fixed']:.2f} → {summary['mean_lag1_hop']:.2f}\np={summary['wilcoxon_fixed_gt_hop_p']:.1e}; RMSE gain={pooled['mean_gain_m']:.2f} m", transform=ax.transAxes, va="top", fontsize=7.3, bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#D1D5DB", "alpha": 0.92})
    save(fig, "fig4_moving_whitening_lag1")


def fig5_quasi_static_speed_boundary() -> None:
    text = numbered("82.").joinpath("result_summary.md").read_text(encoding="utf-8", errors="replace")
    rows = []
    for line in text.splitlines():
        m = re.match(r"\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([+-]?[0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([^|]+)\|", line)
        if m:
            rows.append(
                {
                    "speed": float(m.group(1)),
                    "fixed": float(m.group(2)),
                    "hop": float(m.group(3)),
                    "gain": float(m.group(4)),
                    "p": float(m.group(6)),
                    "decision": m.group(7).strip(),
                }
            )
    if not rows:
        raise RuntimeError("Could not parse 82 result_summary.md speed table")
    x = np.arange(len(rows))
    colors = [COLORS["soft"] if r["decision"] == "validated" else COLORS["bad"] for r in rows]
    fig, ax = plt.subplots(figsize=(3.55, 2.65))
    ax.axhline(0, color="#111827", lw=0.8, alpha=0.55)
    ax.bar(x, [r["gain"] for r in rows], color=colors, alpha=0.78)
    ax.set_xticks(x, [f"{r['speed']:.3f}".rstrip("0").rstrip(".") if r["speed"] else "0" for r in rows], rotation=25)
    ax.set_xlabel("Drift speed (m/s)")
    ax.set_ylabel("RMSE gain (m)")
    ax.set_title("Quasi-static boundary at 600 m")
    for i, r in enumerate(rows):
        ax.text(i, r["gain"] + (0.16 if r["gain"] >= 0 else -0.22), "✓" if r["decision"] == "validated" else "×", ha="center", va="bottom" if r["gain"] >= 0 else "top", fontsize=8.5)
    save(fig, "fig5_quasi_static_speed_boundary")


def fig6_crlb_floor() -> None:
    crlb = load_json("45.", "results", "crlb.json")
    distances = [100, 200, 400, 600]
    empirical = [crlb["summary"][str(d)]["crlb_empirical_m"] for d in distances]
    routing = [crlb["summary"][str(d)]["routing_rmse_m"] for d in distances]
    nls = [crlb["summary"][str(d)]["nls_rmse_m"] for d in distances]
    floor = [crlb["summary"][str(d)]["routing_bias_floor_vs_emp_m"] for d in distances]
    fig, ax = plt.subplots(figsize=(3.45, 2.55))
    ax.plot(distances, empirical, marker="o", color=COLORS["fixed"], label="empirical CRLB")
    ax.plot(distances, nls, marker="s", color="#17BECF", label="NLS")
    ax.plot(distances, routing, marker="^", color=COLORS["hop"], label="routed UKF")
    ax.fill_between(distances, empirical, routing, color=COLORS["hop"], alpha=0.10)
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Position scale (m)")
    ax.set_title("Compact-aperture range floor")
    ax.text(0.52, 0.14, f"600 m excess ≈ {floor[-1]:.2f} m", transform=ax.transAxes, fontsize=7.5, bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#D1D5DB", "alpha": 0.92})
    ax.legend(frameon=False, loc="upper left")
    save(fig, "fig6_crlb_floor")


def fig7_fig8_moving_full_range() -> None:
    source = numbered("194.").joinpath("moving_full_range_source.csv")
    with source.open(newline="", encoding="utf-8") as f:
        rows = [{k: float(v) for k, v in row.items()} for row in csv.DictReader(f)]
    x = [r["distance_m"] for r in rows]
    fixed = [r["fixed_rmse_m"] for r in rows]
    hop = [r["hop_rmse_m"] for r in rows]
    soft = [r["softR_rmse_m"] for r in rows]
    fig, ax = plt.subplots(figsize=(3.55, 2.65))
    ax.plot(x, fixed, marker="o", color=COLORS["fixed"], label="fixed 32 kHz")
    ax.plot(x, hop, marker="s", color=COLORS["hop"], label="plain hop")
    ax.plot(x, soft, marker="^", color=COLORS["soft"], lw=1.85, label=r"transition-aware soft-$R$")
    ax.axvline(800, color="#6B7280", ls="--", lw=0.8)
    ax.annotate("hop tail", xy=(800, 22.386), xytext=(640, 21.1), arrowprops={"arrowstyle": "->", "lw": 0.8, "color": "#374151"}, fontsize=7.5)
    ax.set_xlabel("Nominal range (m)")
    ax.set_ylabel("Settled RMSE (m)")
    ax.set_title("Moving validation over 0--1000 m")
    ax.legend(frameon=False, loc="upper left")
    save(fig, "fig7_moving_full_range_rmse")

    gain_fixed = [r["softR_gain_vs_fixed_m"] for r in rows]
    gain_hop = [r["softR_gain_vs_hop_m"] for r in rows]
    tail = [100 * r["softR_tail_worsened_vs_hop"] for r in rows]
    fig, ax1 = plt.subplots(figsize=(3.55, 2.65))
    ax1.axhline(0, color="#111827", lw=0.8, alpha=0.55)
    ax1.plot(x, gain_fixed, marker="o", color=COLORS["fixed"], label="gain vs fixed")
    ax1.plot(x, gain_hop, marker="s", color=COLORS["soft"], label="gain vs hop")
    ax1.set_xlabel("Nominal range (m)")
    ax1.set_ylabel("RMSE gain (m)")
    ax2 = ax1.twinx()
    ax2.bar(x, tail, width=44, color=COLORS["bad"], alpha=0.16, label="tail worsened")
    ax2.set_ylabel("Tail worsened (%)")
    ax2.set_ylim(0, max(tail) * 1.35 + 1)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, frameon=False, loc="upper left")
    ax1.set_title(r"Soft-$R$ gain and remaining tail risk")
    save(fig, "fig8_moving_full_range_gain_tail")


def fig_tworay_fit() -> None:
    agility = load_json("58.", "results", "agility.json")
    carriers = np.array(agility["config"]["carriers_khz"])
    f_hz = carriers * 1000.0
    geoms = {(g["distance"], g["index"]): g for g in agility["geometries"]}
    picks = [(400, 1), (600, 5)]
    fig, axes = plt.subplots(2, 1, figsize=(3.45, 3.25), sharex=True)
    for ax, key in zip(axes, picks):
        g = geoms[key]
        y = np.array(g["curve_deg"])
        delta = g["delta_us"] * 1e-6
        w = 2 * np.pi * delta
        A = np.column_stack([np.ones_like(f_hz), np.cos(w * f_hz), np.sin(w * f_hz)])
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        resid = y - A @ coef
        r2 = 1 - np.sum(resid**2) / np.sum((y - y.mean()) ** 2)
        fd = np.linspace(f_hz.min(), f_hz.max(), 400)
        Ad = np.column_stack([np.ones_like(fd), np.cos(w * fd), np.sin(w * fd)])
        ax.plot(fd / 1000, Ad @ coef, color=COLORS["hop"], lw=1.4, label="two-ray harmonic fit")
        ax.plot(carriers, y, "o", color=COLORS["fixed"], ms=3.2, label="signal-estimated bias")
        ax.axhline(np.mean(y), color="#6B7280", lw=0.7, ls="--")
        ax.set_ylabel("Elev. bias (deg)")
        ax.set_title(f"{key[0]} m, delay {g['delta_us']/1000:.2f} ms, $R^2$={r2:.2f}", fontsize=8.2)
    axes[0].legend(frameon=False, loc="lower left")
    axes[-1].set_xlabel("Carrier frequency (kHz)")
    save(fig, "fig_tworay_fit")


def main() -> None:
    setup_style()
    fig1_system_concept()
    fig2_frequency_agile_bias()
    fig3_static_600m_paired_rmse()
    fig4_moving_whitening_lag1()
    fig5_quasi_static_speed_boundary()
    fig6_crlb_floor()
    fig7_fig8_moving_full_range()
    fig_tworay_fit()
    outputs = sorted(p.name for p in OUT.glob("fig*.pdf"))
    report = {
        "output_dir": str(OUT),
        "pdf_count": len(outputs),
        "pdf_outputs": outputs,
        "png_dpi": 600,
        "claim_policy": "No new experiment, numeric claim, or conclusion was introduced.",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
