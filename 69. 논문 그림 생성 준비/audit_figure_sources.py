"""논문 그림 후보별 원천 결과 파일 가용성 감사.

이 스크립트는 그림을 직접 그리기 전 단계에서, 각 그림 후보가 어떤 번호 폴더의
어떤 JSON/README 수치에 의존하는지 고정한다. 결과는 figure_source_manifest.json에
저장한다.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative: str):
    path = ROOT / relative
    return json.loads(path.read_text(encoding="utf-8"))


def exists(relative: str) -> bool:
    return (ROOT / relative).exists()


SOURCES = {
    "fig1_system_concept": {
        "kind": "conceptual",
        "source": "논문_초고_구조.md + system/channel model code",
        "status": "manual_drawing_needed",
        "note": "시스템+게이트-내 표면반사 누설 개념도. 정량 JSON보다 원고 도식이 필요.",
    },
    "fig2_bias_vs_carrier": {
        "kind": "quantitative",
        "source": "58. 반송파 미세도약 코히어런트 편향 진단/results/agility.json",
        "status": "available",
    },
    "fig3_static_600m_paired_rmse": {
        "kind": "quantitative",
        "source": "61. 정지표적 도약 대규모 독립검증/results/static_hop_validation.json",
        "status": "available",
    },
    "fig4_lag1_whitening": {
        "kind": "quantitative",
        "source": "63. 이동표적 도약 대규모검증 백색화 확인/results/moving_validation.json",
        "status": "available",
    },
    "fig5_static_moving_2x2_summary": {
        "kind": "quantitative_summary",
        "source": "59/61/63 README and JSON summaries",
        "status": "partly_available",
        "note": "61/63 JSON은 있음. 59는 README 수치 또는 재실행 결과 확인 필요.",
    },
    "fig6_array_rotation_bias_correlation": {
        "kind": "quantitative",
        "source": "42. 다중 ping 기하 다양화 편향 식별성/results/geometry_diversity.json",
        "status": "available",
    },
    "fig7_crlb_vs_rmse_floor": {
        "kind": "quantitative",
        "source": "45. CRLB 이론하한 대비 효율/results/crlb.json",
        "status": "available",
    },
}


def extract_key_numbers():
    agility = load_json("58. 반송파 미세도약 코히어런트 편향 진단/results/agility.json")
    static = load_json("61. 정지표적 도약 대규모 독립검증/results/static_hop_validation.json")
    moving = load_json("63. 이동표적 도약 대규모검증 백색화 확인/results/moving_validation.json")
    crlb = load_json("45. CRLB 이론하한 대비 효율/results/crlb.json")
    geometry = load_json("42. 다중 ping 기하 다양화 편향 식별성/results/geometry_diversity.json")

    return {
        "58_bias_carrier": {
            "400m_hop_reduction_pct": agility["summary"]["400"]["hop_reduction_pct"],
            "600m_hop_reduction_pct": agility["summary"]["600"]["hop_reduction_pct"],
            "600m_bias_32k_deg": agility["summary"]["600"]["median_abs_bias_32k_deg"],
            "600m_bias_hopavg_deg": agility["summary"]["600"]["median_abs_bias_hopavg_deg"],
        },
        "61_static_validation": {
            "600m_fixed_mean_rmse_m": static["summary"]["600"]["fixed_mean_rmse_m"],
            "600m_hop_mean_rmse_m": static["summary"]["600"]["hop_mean_rmse_m"],
            "600m_mean_improvement_m": static["summary"]["600"]["mean_improvement_m"],
            "600m_wilcoxon_p": static["summary"]["600"]["wilcoxon_greater_p"],
            "600m_fixed_median_rmse_m": static["summary"]["600"]["fixed_median_rmse_m"],
            "600m_hop_median_rmse_m": static["summary"]["600"]["hop_median_rmse_m"],
        },
        "63_moving_boundary": {
            "pooled_mean_gain_m": moving["summary"]["M1_pooled_moving"]["mean_gain_m"],
            "pooled_p": moving["summary"]["M1_pooled_moving"]["wilcoxon_greater_p"],
            "lag1_fixed_mean": moving["summary"]["M2_whitening"]["mean_lag1_fixed"],
            "lag1_hop_mean": moving["summary"]["M2_whitening"]["mean_lag1_hop"],
            "lag1_p": moving["summary"]["M2_whitening"]["wilcoxon_fixed_gt_hop_p"],
        },
        "45_crlb_floor": {
            "600m_crlb_empirical_m": crlb["summary"]["600"]["crlb_empirical_m"],
            "600m_routing_rmse_m": crlb["summary"]["600"]["routing_rmse_m"],
            "600m_bias_floor_m": crlb["summary"]["600"]["routing_bias_floor_vs_emp_m"],
        },
        "42_geometry_bias": {
            "source_keys": list(geometry.keys()),
            "note": "세부 구조가 그림 설계에 필요. README와 JSON을 함께 확인할 것.",
        },
    }


def main():
    manifest = {
        "purpose": "논문 그림 7종 생성 전 원천 데이터 감사",
        "figure_sources": SOURCES,
        "source_file_checks": {
            name: exists(info["source"]) if info["source"].endswith(".json") else None
            for name, info in SOURCES.items()
        },
        "key_numbers": extract_key_numbers(),
        "next_step": "70번에서 matplotlib 기반 실제 그림 생성 스크립트 작성 권장",
    }
    output = Path(__file__).resolve().parent / "figure_source_manifest.json"
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(manifest["source_file_checks"], indent=2, ensure_ascii=False))
    return manifest


if __name__ == "__main__":
    main()
