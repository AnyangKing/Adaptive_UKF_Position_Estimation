"""Build a failure-mode map from existing validation JSON files.

No new simulations are run here.  The script reads the adopted/boundary results
from folders 63--67 and 160--162, then writes a provenance-backed map for the
next moving-target experiments.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent


def folder(prefix: int) -> Path:
    matches = [p for p in ROOT.iterdir() if p.is_dir() and p.name.startswith(f"{prefix}.")]
    if not matches:
        raise FileNotFoundError(prefix)
    return matches[0]


def load(prefix: int, name: str) -> dict[str, Any]:
    path = folder(prefix) / "results" / name
    return json.loads(path.read_text(encoding="utf-8"))


def maybe_load(prefix: int, name: str) -> dict[str, Any] | None:
    path = folder(prefix) / "results" / name
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def fmt(value: float | None, digits: int = 3) -> str:
    if value is None:
        return "-"
    return f"{value:.{digits}f}"


def build() -> dict[str, Any]:
    r63 = load(63, "moving_validation.json")
    r64 = load(64, "whitening_guard.json")
    r65 = load(65, "anchor_hop_schedule.json")
    r66 = load(66, "anchor_hop_midscale.json")
    r67 = load(67, "motion_aware_schedule.json")
    r160 = load(160, "four_carrier_independent_validation.json")
    r162 = load(162, "transition_toa_guard_pilot.json")

    policies64 = r64["summary"]["policies"]
    policies65 = r65["summary"]["policies"]
    policies66 = r66["summary"]["policies"]
    policies67 = r67["summary"]["policies"]

    failure_modes = [
        {
            "mode": "motion_self_whitening",
            "evidence_folder": folder(63).name,
            "observable_runtime_indicators": [
                "short-window DOA innovation variance",
                "GCC-SRP disagreement",
                "NIS tail",
            ],
            "offline_only_indicators": [
                "true elevation residual lag-1",
                "fixed-vs-hop paired RMSE gain",
                "ground-truth motion class",
            ],
            "evidence": {
                "pooled_mean_gain_m": r63["summary"]["M1_pooled_moving"]["mean_gain_m"],
                "pooled_wilcoxon_p": r63["summary"]["M1_pooled_moving"]["wilcoxon_greater_p"],
                "lag1_fixed": r63["summary"]["M2_whitening"]["mean_lag1_fixed"],
                "lag1_hop": r63["summary"]["M2_whitening"]["mean_lag1_hop"],
                "lag1_p": r63["summary"]["M2_whitening"]["wilcoxon_fixed_gt_hop_p"],
            },
            "interpretation": (
                "Carrier agility changes residual correlation, but target motion already changes "
                "the multipath phase under fixed carrier; whitening alone is not enough to claim RMSE gain."
            ),
            "next_action": "Do not use lag-1 reduction as a moving-target performance claim.",
        },
        {
            "mode": "schedule_safety_evaporation",
            "evidence_folder": f"{folder(64).name}; {folder(65).name}; {folder(66).name}; {folder(67).name}",
            "observable_runtime_indicators": [
                "carrier schedule",
                "GCC-SRP disagreement",
                "NIS",
                "observed TOA/TDOA jumps",
            ],
            "offline_only_indicators": ["oracle condition label", "paired RMSE gain"],
            "evidence": {
                "64_hop_always_gain_vs_fixed_m": policies64["hop_always"]["mean_gain_vs_fixed_m"],
                "65_hop_always_gain_vs_fixed_m": policies65["hop_always"]["mean_gain_vs_fixed_m"],
                "66_hop_always_gain_vs_fixed_m": policies66["hop_always"]["mean_gain_vs_fixed_m"],
                "67_condition_aware_gain_vs_fixed_m": policies67["condition_aware"]["mean_gain_vs_fixed_m"],
                "67_condition_aware_p": policies67["condition_aware"]["wilcoxon_gain_gt0_p"],
            },
            "interpretation": (
                "More clever carrier schedules did not reliably beat fixed carrier on independent moving seeds. "
                "Even an oracle condition-aware rule failed to reproduce a meaningful gain."
            ),
            "next_action": "Deprioritize schedule-only motion-aware methods.",
        },
        {
            "mode": "carrier_transition_toa_branch_switching",
            "evidence_folder": f"{folder(160).name}; {folder(161).name}; {folder(162).name}",
            "observable_runtime_indicators": [
                "reference TOA adjacent range jump",
                "carrier change flag",
                "TOA block NIS",
                "matched-filter peak quality",
            ],
            "offline_only_indicators": ["post-validation selected tail geometry"],
            "evidence": {
                "160_four_carrier_mean_rmse_m": r160["summary"]["four_carrier_cycle"]["mean_settled_rmse_m"],
                "160_four_carrier_divergence_rate": r160["summary"]["four_carrier_cycle"]["divergence_rate"],
                "162_stage": r162["config"]["stage"],
                "162_decision": r162["decision"],
                "162_four_baseline_mean_rmse_m": r162["summary"]["four_carrier_cycle"]["baseline_adaptive_r"]["mean_settled_rmse_m"],
                "162_four_guard_mean_rmse_m": r162["summary"]["four_carrier_cycle"]["transition_toa_guard"]["mean_settled_rmse_m"],
            },
            "interpretation": (
                "TOA branch switching is an observed-signal failure mechanism, not a truth-derived oracle feature. "
                "The existing guard is only post-hoc/static, so it must be validated independently."
            ),
            "next_action": "Run 179 independent validation before using the guard as a method component.",
        },
    ]

    candidate_ranking = [
        {
            "candidate": "TOA branch switching independent validation",
            "priority": 1,
            "reason": "Uses observable TOA jump + carrier transition and already passed a post-hoc pilot.",
            "next_folder": 179,
            "claim_status": "validation_candidate_not_claimed",
        },
        {
            "candidate": "carrier-transition-aware Adaptive-R",
            "priority": 2,
            "reason": "Generalizes TOA guard from static tail control into an observed-risk covariance routing rule.",
            "next_folder": 180,
            "claim_status": "development_candidate",
        },
        {
            "candidate": "motion-aware adaptive transmission schedule",
            "priority": 3,
            "reason": "Oracle condition-aware schedule failed on independent seed; runtime risk detection has a low ceiling.",
            "next_folder": None,
            "claim_status": "future_work_only",
        },
    ]

    return {
        "stage": "failure_map_no_new_simulation",
        "source_folders": [folder(i).name for i in (63, 64, 65, 66, 67, 160, 161, 162)],
        "failure_modes": failure_modes,
        "candidate_ranking": candidate_ranking,
        "claim_boundary": [
            "Moving-target pooled RMSE improvement is not established.",
            "Residual lag-1 reduction is mechanism evidence only.",
            "Post-hoc/oracle results cannot be promoted to method performance without independent validation.",
            "Future moving-target methods must use only observed TOA/TDOA/DOA/quality/NIS features.",
        ],
    }


def write_markdown(payload: dict[str, Any]) -> None:
    lines = [
        "# Moving target failure mode map",
        "",
        "이 문서는 기존 결과 JSON만 읽어 만든 실패 지도다. 새 실험이나 새 성능 claim은 없다.",
        "",
        "## Failure modes",
        "",
        "| failure mode | key evidence | runtime-observable signals | offline-only signals | next action |",
        "|---|---|---|---|---|",
    ]
    for item in payload["failure_modes"]:
        ev = item["evidence"]
        if item["mode"] == "motion_self_whitening":
            key = (
                f"mean gain {fmt(ev['pooled_mean_gain_m'])} m, "
                f"p={fmt(ev['pooled_wilcoxon_p'])}; "
                f"lag-1 {fmt(ev['lag1_fixed'])}→{fmt(ev['lag1_hop'])}"
            )
        elif item["mode"] == "schedule_safety_evaporation":
            key = (
                f"64 hop gain {fmt(ev['64_hop_always_gain_vs_fixed_m'])} m; "
                f"66 hop gain {fmt(ev['66_hop_always_gain_vs_fixed_m'])} m; "
                f"67 oracle gain {fmt(ev['67_condition_aware_gain_vs_fixed_m'])} m"
            )
        else:
            key = (
                f"160 four-carrier RMSE {fmt(ev['160_four_carrier_mean_rmse_m'])} m, "
                f"div {fmt(ev['160_four_carrier_divergence_rate'])}; "
                f"162 pilot {fmt(ev['162_four_baseline_mean_rmse_m'])}→{fmt(ev['162_four_guard_mean_rmse_m'])} m"
            )
        lines.append(
            "| {mode} | {key} | {obs} | {off} | {next} |".format(
                mode=item["mode"],
                key=key,
                obs=", ".join(item["observable_runtime_indicators"]),
                off=", ".join(item["offline_only_indicators"]),
                next=item["next_action"],
            )
        )

    lines.extend([
        "",
        "## Candidate ranking",
        "",
        "| priority | candidate | reason | status |",
        "|---:|---|---|---|",
    ])
    for c in payload["candidate_ranking"]:
        lines.append(f"| {c['priority']} | {c['candidate']} | {c['reason']} | {c['claim_status']} |")

    lines.extend([
        "",
        "## Claim boundary",
        "",
    ])
    lines.extend([f"- {line}" for line in payload["claim_boundary"]])
    (HERE / "failure_mode_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_decision(payload: dict[str, Any]) -> None:
    text = """# Next experiment decision

## 결정

다음 실험은 schedule-only moving method가 아니라 carrier transition이 만든 관측 위험을 다룬다.

1. 179번: 162번 TOA branch switching guard를 독립 seed에서 검증한다.
2. 180번: guard 개념을 carrier-transition-aware Adaptive-R 후보로 일반화해 moving target 개발 조건에서 찔러본다.

## 이유

- 63번은 carrier agility가 residual lag-1을 낮춘다는 기전은 보였지만 moving pooled RMSE gain은 보이지 않았다.
- 64--67번은 schedule을 바꾸거나 oracle condition rule을 써도 독립 seed에서 이득이 안정적으로 재현되지 않았다.
- 162번의 TOA branch switching은 ground truth 없이도 reference TOA jump와 carrier transition으로 감지할 수 있다.

## 금지

- 179 또는 180이 독립검증 전이면 논문 성능 claim으로 쓰지 않는다.
- moving target RMSE 개선을 lag-1 whitening만으로 주장하지 않는다.
- oracle condition label 또는 post-hoc geometry 선택을 제안법 입력으로 쓰지 않는다.
"""
    (HERE / "next_experiment_decision.md").write_text(text, encoding="utf-8")


def main() -> None:
    payload = build()
    (HERE / "failure_mode_map.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_markdown(payload)
    write_decision(payload)
    print(json.dumps({"failure_modes": len(payload["failure_modes"]), "candidates": len(payload["candidate_ranking"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
