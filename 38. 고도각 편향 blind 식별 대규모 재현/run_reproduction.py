"""38번 러너: 대규모 편향 feature 수집(무거움) 후 재현 통계를 산출한다.

편향 원자료는 bias_pool.json에, 재현 통계는 reproduction.json에 저장한다.
"""

from pathlib import Path
import json

from bias_features import (DISTANCES, GEOMETRIES_PER_DISTANCE, REPEATS,
                           SIGNAL_FEATURES, collect)
from reproduction import analyze, N_SPLITS, N_BOOTSTRAP


def run():
    records = collect()
    result = analyze(records)
    payload = {
        "config": {
            "distances_m": list(DISTANCES),
            "geometries_per_distance": GEOMETRIES_PER_DISTANCE,
            "repeats_per_geometry": REPEATS,
            "signal_features": list(SIGNAL_FEATURES),
            "n_splits": N_SPLITS,
            "n_bootstrap": N_BOOTSTRAP,
            "note": "37번 C(n=24)의 고도각 편향 blind 식별을 새 seed 대규모에서 재현 검정",
        },
        "reproduction": result,
        "raw": records,
    }
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    (out / "bias_pool.json").write_text(json.dumps({"config": payload["config"], "raw": records},
                                                   indent=2), encoding="utf-8")
    (out / "reproduction.json").write_text(json.dumps({"config": payload["config"],
                                                       "reproduction": result}, indent=2),
                                           encoding="utf-8")
    print(json.dumps({"config": payload["config"], "reproduction": result},
                     indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
