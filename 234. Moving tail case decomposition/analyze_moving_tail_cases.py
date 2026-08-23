from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "191. Moving full range transition aware independent validation" / "moving_full_range_independent_validation.json"
TAIL_THRESHOLD_M = -1.0


def load_rows() -> list[dict[str, Any]]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    return payload["trials"]


def index_by_policy(rows: list[dict[str, Any]]) -> dict[str, dict[tuple[float, str, int], dict[str, Any]]]:
    out: dict[str, dict[tuple[float, str, int], dict[str, Any]]] = defaultdict(dict)
    for row in rows:
        key = (float(row["distance_m"]), str(row["condition"]), int(row["index"]))
        out[str(row["policy"])][key] = row
    return dict(out)


def case_table(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_policy = index_by_policy(rows)
    fixed = by_policy["fixed_baseline"]
    hop = by_policy["hop_baseline"]
    soft = by_policy["hop_transition_softR"]
    keys = sorted(fixed)
    table = []
    for key in keys:
        f = fixed[key]
        h = hop[key]
        s = soft[key]
        distance, condition, index = key
        table.append(
            {
                "distance_m": distance,
                "condition": condition,
                "index": index,
                "fixed_rmse_m": f["settled_rmse_m"],
                "hop_rmse_m": h["settled_rmse_m"],
                "softR_rmse_m": s["settled_rmse_m"],
                "hop_gain_vs_fixed_m": f["settled_rmse_m"] - h["settled_rmse_m"],
                "softR_gain_vs_fixed_m": f["settled_rmse_m"] - s["settled_rmse_m"],
                "softR_gain_vs_hop_m": h["settled_rmse_m"] - s["settled_rmse_m"],
                "softR_tail_vs_fixed": (f["settled_rmse_m"] - s["settled_rmse_m"]) < TAIL_THRESHOLD_M,
                "softR_tail_vs_hop": (h["settled_rmse_m"] - s["settled_rmse_m"]) < TAIL_THRESHOLD_M,
                "hop_tail_vs_fixed": (f["settled_rmse_m"] - h["settled_rmse_m"]) < TAIL_THRESHOLD_M,
                "softR_transition_risk_count": s.get("transition_risk_count", 0),
                "softR_mean_transition_scale": s.get("mean_transition_scale", 1.0),
            }
        )
    return table


def group_summary(cases: list[dict[str, Any]], keys: list[str]) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for case in cases:
        groups[tuple(case[k] for k in keys)].append(case)
    rows = []
    for gkey, subset in sorted(groups.items()):
        row = {k: v for k, v in zip(keys, gkey)}
        row.update(
            {
                "n": len(subset),
                "fixed_mean_rmse_m": mean(c["fixed_rmse_m"] for c in subset),
                "hop_mean_rmse_m": mean(c["hop_rmse_m"] for c in subset),
                "softR_mean_rmse_m": mean(c["softR_rmse_m"] for c in subset),
                "hop_gain_vs_fixed_m": mean(c["hop_gain_vs_fixed_m"] for c in subset),
                "softR_gain_vs_fixed_m": mean(c["softR_gain_vs_fixed_m"] for c in subset),
                "softR_gain_vs_hop_m": mean(c["softR_gain_vs_hop_m"] for c in subset),
                "hop_tail_vs_fixed_fraction": mean(c["hop_tail_vs_fixed"] for c in subset),
                "softR_tail_vs_fixed_fraction": mean(c["softR_tail_vs_fixed"] for c in subset),
                "softR_tail_vs_hop_fraction": mean(c["softR_tail_vs_hop"] for c in subset),
                "softR_transition_risks": sum(c["softR_transition_risk_count"] for c in subset),
            }
        )
        rows.append(row)
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    out = ["| " + " | ".join(columns) + " |", "|" + "|".join("---:" if c.endswith("_m") or c.endswith("fraction") or c == "n" else "---" for c in columns) + "|"]
    for row in rows:
        cells = []
        for c in columns:
            v = row[c]
            if isinstance(v, float):
                cells.append(f"{v:.3f}")
            else:
                cells.append(str(v))
        out.append("| " + " | ".join(cells) + " |")
    return out


def make_report(payload: dict[str, Any]) -> str:
    overall = payload["overall"]
    lines = [
        "# Moving tail case decomposition",
        "",
        "This analysis decomposes the 191 full-range moving validation tails without rerunning the simulator.",
        f"Tail is defined as paired gain < {TAIL_THRESHOLD_M:.1f} m, i.e. the target policy is more than 1 m worse than the reference.",
        "",
        "## Overall",
        "",
        f"- Cases: {overall['n']}",
        f"- softR vs fixed mean gain: {overall['softR_gain_vs_fixed_m']:.3f} m",
        f"- softR vs fixed tail worsened fraction: {overall['softR_tail_vs_fixed_fraction']:.3f}",
        f"- softR vs hop mean gain: {overall['softR_gain_vs_hop_m']:.3f} m",
        f"- softR vs hop tail worsened fraction: {overall['softR_tail_vs_hop_fraction']:.3f}",
        f"- hop vs fixed tail worsened fraction: {overall['hop_tail_vs_fixed_fraction']:.3f}",
        "",
        "## Distance decomposition",
        "",
    ]
    lines.extend(
        markdown_table(
            payload["by_distance"],
            [
                "distance_m",
                "n",
                "softR_gain_vs_fixed_m",
                "softR_tail_vs_fixed_fraction",
                "softR_gain_vs_hop_m",
                "softR_tail_vs_hop_fraction",
                "hop_tail_vs_fixed_fraction",
            ],
        )
    )
    lines.extend(["", "## Motion-condition decomposition", ""])
    lines.extend(
        markdown_table(
            payload["by_condition"],
            [
                "condition",
                "n",
                "softR_gain_vs_fixed_m",
                "softR_tail_vs_fixed_fraction",
                "softR_gain_vs_hop_m",
                "softR_tail_vs_hop_fraction",
                "hop_tail_vs_fixed_fraction",
            ],
        )
    )
    lines.extend(["", "## Highest softR-vs-fixed tail cells", ""])
    lines.extend(
        markdown_table(
            payload["worst_cells_softR_vs_fixed"][:12],
            [
                "distance_m",
                "condition",
                "n",
                "softR_gain_vs_fixed_m",
                "softR_tail_vs_fixed_fraction",
                "softR_gain_vs_hop_m",
                "softR_tail_vs_hop_fraction",
            ],
        )
    )
    lines.extend(["", "## Worst individual softR-vs-fixed cases", ""])
    lines.extend(
        markdown_table(
            payload["worst_cases_softR_vs_fixed"][:15],
            [
                "distance_m",
                "condition",
                "index",
                "fixed_rmse_m",
                "hop_rmse_m",
                "softR_rmse_m",
                "softR_gain_vs_fixed_m",
                "softR_gain_vs_hop_m",
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The remaining 13.1% softR-vs-fixed tail is not uniformly distributed.",
            "- Most distance-averaged gains remain positive, but tail risk concentrates in a few distance/motion cells.",
            "- The moving-target claim should therefore keep both statements: mean/P90 improvement is strong, but residual tail cases remain and motivate future risk-aware scheduling or additional guards.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    rows = load_rows()
    cases = case_table(rows)
    by_distance = group_summary(cases, ["distance_m"])
    by_condition = group_summary(cases, ["condition"])
    by_cell = group_summary(cases, ["distance_m", "condition"])
    overall = group_summary(cases, [])[0]
    worst_cells = sorted(by_cell, key=lambda r: (-r["softR_tail_vs_fixed_fraction"], r["softR_gain_vs_fixed_m"]))
    worst_cases = sorted(cases, key=lambda r: r["softR_gain_vs_fixed_m"])
    payload = {
        "source": str(SOURCE.relative_to(ROOT)),
        "tail_threshold_m": TAIL_THRESHOLD_M,
        "overall": overall,
        "by_distance": by_distance,
        "by_condition": by_condition,
        "by_distance_condition": by_cell,
        "worst_cells_softR_vs_fixed": worst_cells,
        "worst_cases_softR_vs_fixed": worst_cases,
    }
    (HERE / "moving_tail_decomposition.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (HERE / "result_summary.md").write_text(make_report(payload), encoding="utf-8")
    print(json.dumps(payload["overall"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

