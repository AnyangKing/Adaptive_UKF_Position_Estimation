"""진단 A 러너: 계통 DOA 편향의 실재와 위치 증폭을 거리별로 요약한다.

Ground Truth는 오차 계산에만 쓴다. validation/test 기하는 완전히 분리하며, 편향 실재
판정은 test 기하에서 본다. 원자료(거리·bias·random·feature)는 진단 B/C가 재사용하도록
bias_raw.json에 저장한다.
"""

from pathlib import Path
import json
import numpy as np

from bias_decomposition import DISTANCES, GEOMETRIES_PER_DISTANCE, REPEATS, collect


def summarize(records):
    summary = {}
    for distance in DISTANCES:
        rows = [r for r in records if r["distance"] == distance]
        bias = np.array([r["bias_angle_deg"] for r in rows])
        random = np.array([r["random_angle_deg"] for r in rows])
        summary[str(distance)] = {
            "median_bias_deg": float(np.median(bias)),
            "median_random_deg": float(np.median(random)),
            "median_bias_over_random": float(np.median(bias / np.maximum(random, 1e-9))),
            "median_el_bias_deg": float(np.median([r["el_bias_deg"] for r in rows])),
            "median_az_bias_deg": float(np.median([r["az_bias_deg"] for r in rows])),
            "median_el_random_deg": float(np.median([r["el_random_deg"] for r in rows])),
            "median_az_random_deg": float(np.median([r["az_random_deg"] for r in rows])),
            "median_pos_bias_m": float(np.median([r["pos_bias_m"] for r in rows])),
            "median_pos_random_m": float(np.median([r["pos_random_m"] for r in rows])),
            "geometry_count": len(rows),
        }
    return summary


def run():
    validation = collect("validation")
    test = collect("test")
    payload = {
        "config": {
            "distances_m": list(DISTANCES),
            "geometries_per_distance": GEOMETRIES_PER_DISTANCE,
            "repeats_per_geometry": REPEATS,
            "note": "bias=noise 평균 후 남는 계통 각도차, random=반복 산포. bias/random>1이면 다중 ping 무력",
        },
        "validation": summarize(validation),
        "test": summarize(test),
        "raw": {"validation": validation, "test": test},
    }
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(exist_ok=True)
    (output / "bias_raw.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    # 콘솔에는 요약만 출력한다.
    print(json.dumps({"config": payload["config"],
                      "validation": payload["validation"],
                      "test": payload["test"]}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
