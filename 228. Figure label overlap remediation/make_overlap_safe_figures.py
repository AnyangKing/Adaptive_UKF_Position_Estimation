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
    "direct": "#111827",
    "surface": "#FF7F0E",
    "array": "#1F77B4",
    "target": "#D62728",
    "gate": "#7C3AED",
    "nls": "#17BECF",
}


def numbered(prefix: str) -> Path:
    matches = sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith(prefix))
    if not matches:
        raise FileNotFoundError(prefix)
    return matches[0]


def load_json(prefix: str, *parts: str) -> dict:
    return json.loads(numbered(prefix).joinpath(*parts).read_text(encoding="utf-8"))


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
            "lines.linewidth": 1.15,
            "lines.markersize": 3.1,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.dpi": 600,
            "figure.dpi": 160,
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(pad=0.35)
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=600, bbox_inches="tight")
    plt.close(fig)


def add_arrow(ax, start, end, color, lw=1.3, ls="-", ms=7.5, z=5):
    ax.add_patch(
        FancyArrowPatch(
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
    )


def label_box(ax, x, y, text, color="#111827", fontsize=6.9, ha="center"):
    ax.text(
        x,
        y,
        text,
        ha=ha,
        va="center",
        fontsize=fontsize,
        color=color,
        bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "none", "alpha": 0.88},
        zorder=8,
    )


def fig1_system_concept() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(7.05, 2.82))

    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.text(0.02, 0.98, "(a)", transform=ax.transAxes, ha="left", va="top", fontsize=8.5, fontweight="bold")
    ax.plot([0.55, 9.45], [4.45, 4.45], color="#4C78A8", lw=1.25)
    ax.plot([0.55, 9.45], [0.50, 0.50], color="#8D6E63", lw=1.25)
    ax.text(0.65, 4.62, "surface", fontsize=6.8, color="#4C78A8")
    ax.text(0.65, 0.18, "bottom", fontsize=6.8, color="#8D6E63")

    array = np.array([1.45, 2.15])
    target = np.array([8.30, 1.95])
    refl = np.array([5.05, 4.45])
    add_arrow(ax, array, target, COLORS["direct"], lw=1.35)
    ax.plot([array[0], refl[0]], [array[1], refl[1]], "--", color=COLORS["surface"], lw=1.25)
    add_arrow(ax, refl, target, COLORS["surface"], lw=1.25, ls="--")
    label_box(ax, 4.10, 2.35, "direct path", COLORS["direct"], fontsize=6.3)
    label_box(ax, 4.85, 3.82, "surface reflection", COLORS["surface"], fontsize=6.3)

    ax.scatter([array[0]], [array[1]], s=38, color=COLORS["array"], zorder=6)
    ax.scatter([target[0]], [target[1]], s=82, marker="*", color=COLORS["target"], zorder=7)
    ax.text(array[0] - 0.18, array[1] + 0.30, "8-sensor\nUSBL", ha="right", fontsize=6.8)
    ax.text(target[0] + 0.26, target[1] + 0.25, "beacon", ha="left", fontsize=6.8)

    gate = Rectangle(
        (6.05, 0.92),
        2.05,
        1.45,
        linewidth=1.0,
        edgecolor=COLORS["gate"],
        facecolor="#F3E8FF",
        linestyle=(0, (2, 2)),
        alpha=0.60,
        zorder=1,
    )
    ax.add_patch(gate)
    label_box(ax, 7.08, 2.58, "5 ms DOA gate", COLORS["gate"], fontsize=6.4)
    ax.text(7.08, 0.73, "coherent direct + leakage", ha="center", fontsize=6.5, color=COLORS["gate"])

    inset = np.array([1.28, 0.92])
    radius = 0.18
    for t in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        ax.scatter(inset[0] + radius * np.cos(t), inset[1] + 0.55 * radius * np.sin(t), s=7, color=COLORS["array"])
    ax.add_patch(Circle(inset, radius, fill=False, color=COLORS["array"], lw=0.75))
    ax.text(1.62, 0.86, "66 mm aperture", fontsize=6.5, color=COLORS["array"], va="center")

    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.text(0.02, 0.98, "(b)", transform=ax.transAxes, ha="left", va="top", fontsize=8.5, fontweight="bold")
    ax.text(0.25, 4.42, r"coherent phase: $\phi_k=2\pi f_k\delta_k+\theta_r$", fontsize=8.0)
    ax.text(0.25, 4.02, r"static: $\delta_k\approx\delta_0$", fontsize=6.6, color=COLORS["muted"])
    ax.text(5.10, 4.02, r"moving: $\delta_k=\delta(t_k)$ may self-whiten", fontsize=6.6, color=COLORS["muted"])

    for x0, label, color, angles in [
        (2.15, "fixed 32 kHz", COLORS["fixed"], [50, 58, 66]),
        (6.35, "30--34 kHz pings", COLORS["soft"], [20, 90, 160, 235, 305]),
    ]:
        ax.add_patch(FancyBboxPatch((x0 - 0.86, 3.15), 1.72, 0.30, boxstyle="round,pad=0.025", edgecolor=color, facecolor="white", lw=0.75))
        ax.text(x0, 3.30, label, ha="center", va="center", fontsize=6.5, color=color)
        c = np.array([x0, 2.30])
        ax.add_patch(Circle(c, 0.46, fill=False, color="#9CA3AF", lw=0.75))
        palette = [color] * len(angles) if x0 < 4 else ["#FF7F0E", "#2CA02C", "#9467BD", "#17BECF", "#D62728"]
        for a, cc in zip(angles, palette):
            rad = np.deg2rad(a)
            add_arrow(ax, c, c + 0.34 * np.array([np.cos(rad), np.sin(rad)]), cc, lw=1.15, ms=6.5)
        note = "phase locked\ncorrelated bias" if x0 < 4 else "phase rotates\nless persistence"
        ax.text(x0, 1.36, note, ha="center", fontsize=6.6, color=color)

    add_arrow(ax, (3.10, 2.30), (5.05, 2.30), "#111827", lw=1.0, ms=7)
    ax.text(4.08, 2.55, r"change $f_k$", ha="center", fontsize=6.8)
    ax.add_patch(FancyBboxPatch((7.86, 1.80), 1.38, 0.82, boxstyle="round,pad=0.05", edgecolor="#9CA3AF", facecolor="#F9FAFB", lw=0.75))
    ax.text(8.55, 2.34, "TOA/TDOA/DOA", ha="center", fontsize=6.1)
    ax.text(8.55, 2.04, r"Adaptive-$R$ UKF", ha="center", fontsize=6.1)
    add_arrow(ax, (7.03, 2.30), (7.86, 2.23), COLORS["soft"], lw=1.0, ms=7)
    save(fig, "fig1_system_concept")


def fig2_frequency_agile_bias() -> None:
    agility = load_json("58.", "results", "agility.json")
    distances = [100, 200, 400, 600]
    fixed = [agility["summary"][str(d)]["median_abs_bias_32k_deg"] for d in distances]
    hopped = [agility["summary"][str(d)]["median_abs_bias_hopavg_deg"] for d in distances]
    reductions = [agility["summary"][str(d)]["hop_reduction_pct"] for d in distances]
    x = np.arange(len(distances))
    width = 0.34
    fig, ax = plt.subplots(figsize=(3.35, 2.28))
    ax.bar(x - width / 2, fixed, width, label="fixed 32 kHz", color=COLORS["fixed"])
    ax.bar(x + width / 2, hopped, width, label="agile average", color=COLORS["hop"])
    ax.set_xticks(x, [str(d) for d in distances])
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Median |elev. bias| (deg)")
    ax.set_title("Carrier agility changes coherent bias")
    ymax = max(fixed + hopped) * 1.34
    ax.set_ylim(0, ymax)
    for i, pct in enumerate(reductions):
        y = max(fixed[i], hopped[i]) + ymax * 0.045
        ax.text(i, y, f"{pct:+.0f}%", ha="center", va="bottom", fontsize=6.7, color=COLORS["soft"] if pct >= 0 else COLORS["bad"])
    ax.legend(frameon=False, loc="upper right", ncol=1, borderaxespad=0.2)
    save(fig, "fig2_frequency_agile_bias")


def fig3_static_600m_paired_rmse() -> None:
    static = load_json("61.", "results", "static_hop_validation.json")
    trials = [t for t in static["trials"] if int(t["distance"]) == 600]
    fixed = [t["fixed_settled_rmse_m"] for t in trials]
    hop = [t["hop_settled_rmse_m"] for t in trials]
    summary = static["summary"]["600"]
    fig, ax = plt.subplots(figsize=(3.05, 2.35))
    for f, h in zip(fixed, hop):
        color = COLORS["soft"] if h < f else COLORS["bad"]
        ax.plot([0, 1], [f, h], color=color, alpha=0.30, lw=0.65)
        ax.scatter([0, 1], [f, h], color=color, s=7, alpha=0.55)
    ax.scatter([0, 1], [mean(fixed), mean(hop)], color="#111827", s=24, zorder=5, label="mean")
    ax.set_xticks([0, 1], ["Fixed\n32 kHz", "Agile\n30--34 kHz"])
    ax.set_ylabel("Settled RMSE (m)")
    ax.set_title("Static 600 m paired validation")
    ax.text(
        0.03,
        0.98,
        f"mean {summary['fixed_mean_rmse_m']:.2f} → {summary['hop_mean_rmse_m']:.2f} m\nΔ={summary['mean_improvement_m']:.2f} m, p={summary['wilcoxon_greater_p']:.4f}",
        transform=ax.transAxes,
        va="top",
        fontsize=6.4,
        bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "#D1D5DB", "alpha": 0.86},
    )
    ax.legend(frameon=False, loc="upper right", borderaxespad=0.2)
    save(fig, "fig3_static_600m_paired_rmse")


def fig4_moving_whitening_lag1() -> None:
    moving = load_json("63.", "results", "moving_validation.json")
    runs = moving["runs"]
    fixed = [r["lag1_fixed"] for r in runs]
    hop = [r["lag1_hop"] for r in runs]
    summary = moving["summary"]["M2_whitening"]
    pooled = moving["summary"]["M1_pooled_moving"]
    fig, ax = plt.subplots(figsize=(3.10, 2.42))
    for f, h in zip(fixed, hop):
        ax.plot([0, 1], [f, h], color=COLORS["soft"] if h < f else COLORS["bad"], alpha=0.18, lw=0.55, zorder=1)
    bp = ax.boxplot([fixed, hop], positions=[0, 1], widths=0.30, showfliers=False, patch_artist=True, zorder=3)
    for patch, color in zip(bp["boxes"], [COLORS["fixed"], COLORS["hop"]]):
        patch.set_facecolor(color)
        patch.set_alpha(0.18)
        patch.set_edgecolor(color)
    ax.scatter(np.zeros(len(fixed)) - 0.04, fixed, s=7, alpha=0.28, color=COLORS["fixed"], zorder=2)
    ax.scatter(np.ones(len(hop)) + 0.04, hop, s=7, alpha=0.28, color=COLORS["hop"], zorder=2)
    ax.axhline(0, color="#111827", lw=0.65, alpha=0.55)
    ax.set_xticks([0, 1], ["Fixed", "Agile"])
    ax.set_ylabel("Lag-1 residual correlation")
    ax.set_title("Moving residual decorrelation")
    ax.set_ylim(-1.04, 1.10)
    ax.text(0.03, 0.05, f"lag-1 {summary['mean_lag1_fixed']:.2f} → {summary['mean_lag1_hop']:.2f}", transform=ax.transAxes, fontsize=6.1, bbox={"boxstyle": "round,pad=0.15", "facecolor": "white", "edgecolor": "none", "alpha": 0.82})
    save(fig, "fig4_moving_whitening_lag1")


def parse_quasi_rows():
    text = numbered("82.").joinpath("result_summary.md").read_text(encoding="utf-8", errors="replace")
    rows = []
    for line in text.splitlines():
        m = re.match(r"\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([+-]?[0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([0-9.]+)\s*\|\s*([^|]+)\|", line)
        if m:
            rows.append({"speed": float(m.group(1)), "gain": float(m.group(4)), "decision": m.group(7).strip()})
    if not rows:
        raise RuntimeError("Could not parse quasi-static rows")
    return rows


def fig5_quasi_static_speed_boundary() -> None:
    rows = parse_quasi_rows()
    x = np.arange(len(rows))
    colors = [COLORS["soft"] if r["decision"] == "validated" else COLORS["bad"] for r in rows]
    fig, ax = plt.subplots(figsize=(3.25, 2.25))
    ax.axhline(0, color="#111827", lw=0.65, alpha=0.55)
    ax.bar(x, [r["gain"] for r in rows], color=colors, alpha=0.78, width=0.72)
    ax.set_xticks(x, [f"{r['speed']:.3f}".rstrip("0").rstrip(".") if r["speed"] else "0" for r in rows], rotation=25)
    ax.set_xlabel("Drift speed (m/s)")
    ax.set_ylabel("RMSE gain (m)")
    ax.set_title("Quasi-static boundary at 600 m")
    ymax = max(r["gain"] for r in rows)
    ymin = min(r["gain"] for r in rows)
    ax.set_ylim(min(-0.45, ymin - 0.25), ymax + 0.55)
    for i, r in enumerate(rows):
        marker = "✓" if r["decision"] == "validated" else "×"
        y = r["gain"] + (0.18 if r["gain"] >= 0 else -0.20)
        ax.text(i, y, marker, ha="center", va="bottom" if r["gain"] >= 0 else "top", fontsize=7.2)
    save(fig, "fig5_quasi_static_speed_boundary")


def fig6_crlb_floor() -> None:
    crlb = load_json("45.", "results", "crlb.json")
    distances = [100, 200, 400, 600]
    empirical = [crlb["summary"][str(d)]["crlb_empirical_m"] for d in distances]
    routing = [crlb["summary"][str(d)]["routing_rmse_m"] for d in distances]
    nls = [crlb["summary"][str(d)]["nls_rmse_m"] for d in distances]
    floor = [crlb["summary"][str(d)]["routing_bias_floor_vs_emp_m"] for d in distances]
    fig, ax = plt.subplots(figsize=(3.20, 2.25))
    ax.plot(distances, empirical, marker="o", color=COLORS["fixed"], label="empirical CRLB")
    ax.plot(distances, nls, marker="s", color=COLORS["nls"], label="NLS")
    ax.plot(distances, routing, marker="^", color=COLORS["hop"], label="routed UKF")
    ax.fill_between(distances, empirical, routing, color=COLORS["hop"], alpha=0.09)
    ax.set_xlabel("Range (m)")
    ax.set_ylabel("Position scale (m)")
    ax.set_title("Compact-aperture range floor")
    ax.text(0.52, 0.10, f"600 m excess ≈ {floor[-1]:.2f} m", transform=ax.transAxes, fontsize=6.3, bbox={"boxstyle": "round,pad=0.16", "facecolor": "white", "edgecolor": "#D1D5DB", "alpha": 0.86})
    ax.legend(frameon=False, loc="upper left", borderaxespad=0.15)
    save(fig, "fig6_crlb_floor")


def fig7_fig8_moving_full_range() -> None:
    source = numbered("194.").joinpath("moving_full_range_source.csv")
    with source.open(newline="", encoding="utf-8") as f:
        rows = [{k: float(v) for k, v in row.items()} for row in csv.DictReader(f)]
    x = [r["distance_m"] for r in rows]
    fixed = [r["fixed_rmse_m"] for r in rows]
    hop = [r["hop_rmse_m"] for r in rows]
    soft = [r["softR_rmse_m"] for r in rows]

    fig, ax = plt.subplots(figsize=(3.35, 2.35))
    ax.plot(x, fixed, marker="o", color=COLORS["fixed"], label="fixed 32 kHz")
    ax.plot(x, hop, marker="s", color=COLORS["hop"], label="plain hop")
    ax.plot(x, soft, marker="^", color=COLORS["soft"], lw=1.35, label=r"transition-aware soft-$R$")
    ax.axvline(800, color="#6B7280", ls="--", lw=0.75)
    ax.annotate("hop tail", xy=(800, 22.386), xytext=(655, 21.3), arrowprops={"arrowstyle": "->", "lw": 0.65, "color": "#374151"}, fontsize=6.5)
    ax.set_xlabel("Nominal range (m)")
    ax.set_ylabel("Settled RMSE (m)")
    ax.set_title("Moving validation over 0--1000 m")
    ax.legend(frameon=False, loc="upper left", borderaxespad=0.15, handlelength=1.6)
    save(fig, "fig7_moving_full_range_rmse")

    gain_fixed = [r["softR_gain_vs_fixed_m"] for r in rows]
    gain_hop = [r["softR_gain_vs_hop_m"] for r in rows]
    tail = [100 * r["softR_tail_worsened_vs_hop"] for r in rows]
    fig, ax1 = plt.subplots(figsize=(3.35, 2.35))
    ax1.axhline(0, color="#111827", lw=0.65, alpha=0.55)
    ax1.plot(x, gain_fixed, marker="o", color=COLORS["fixed"], label="gain vs fixed")
    ax1.plot(x, gain_hop, marker="s", color=COLORS["soft"], label="gain vs hop")
    ax1.set_xlabel("Nominal range (m)")
    ax1.set_ylabel("RMSE gain (m)")
    ax2 = ax1.twinx()
    ax2.bar(x, tail, width=42, color=COLORS["bad"], alpha=0.14, label="tail worsened")
    ax2.set_ylabel("Tail worsened (%)")
    ax2.set_ylim(0, max(tail) * 1.35 + 1)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, frameon=False, loc="upper left", borderaxespad=0.15)
    ax1.set_title(r"Soft-$R$ gain and remaining tail risk")
    save(fig, "fig8_moving_full_range_gain_tail")


def fig_tworay_fit() -> None:
    agility = load_json("58.", "results", "agility.json")
    carriers = np.array(agility["config"]["carriers_khz"])
    f_hz = carriers * 1000.0
    geoms = {(g["distance"], g["index"]): g for g in agility["geometries"]}
    picks = [(400, 1), (600, 5)]
    fig, axes = plt.subplots(2, 1, figsize=(3.30, 3.05), sharex=True)
    handles = labels = None
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
        l1 = ax.plot(fd / 1000, Ad @ coef, color=COLORS["hop"], lw=1.05, label="two-ray fit")
        l2 = ax.plot(carriers, y, "o", color=COLORS["fixed"], ms=2.6, label="signal-estimated bias")
        ax.axhline(np.mean(y), color="#6B7280", lw=0.55, ls="--")
        ax.set_ylabel("Elev. bias (deg)")
        ax.set_title(f"{key[0]} m, delay {g['delta_us']/1000:.2f} ms, $R^2$={r2:.2f}", fontsize=7.0, pad=2.0)
        handles, labels = ax.get_legend_handles_labels()
    axes[-1].set_xlabel("Carrier frequency (kHz)")
    if handles and labels:
        fig.legend(handles, labels, frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.52, 1.02), fontsize=6.5)
    fig.subplots_adjust(top=0.88, hspace=0.42)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "fig_tworay_fit.pdf", bbox_inches="tight")
    fig.savefig(OUT / "fig_tworay_fit.png", dpi=600, bbox_inches="tight")
    plt.close(fig)


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
    print(json.dumps({"updated": sorted(p.name for p in OUT.glob("fig*.pdf"))}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
