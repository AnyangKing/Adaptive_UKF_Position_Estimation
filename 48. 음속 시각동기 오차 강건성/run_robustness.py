"""48번: 음속 불일치와 클럭 오프셋 스윕에서 라우팅 UKF의 위치 RMSE 열화를 측정한다.

(A) 음속 스윕: 실제 음속 c_true ∈ {1470,1485,1500,1515,1530}, 가정 1500. 신호 재합성 필요.
(B) 클럭 스윕: c_true=1500 기준 신호에 절대 TOA 오프셋 ∈ {0, 0.5, 1.0} ms (재합성 불필요).
거리별·전체 평균 RMSE와 발산율을 baseline(음속 일치·오프셋 0) 대비 보고한다.
"""

from pathlib import Path
import json
import numpy as np

from robustness import DISTANCES, collect_mismatched, run_routing_rmse

TRIALS = 10
SOUND_SPEEDS = (1470.0, 1485.0, 1500.0, 1515.0, 1530.0)
CLOCK_OFFSETS_S = (0.0, 0.0005, 0.001)


def _sweep(get_record):
    rows = []
    for d in DISTANCES:
        for t in range(TRIALS):
            rmse, div = run_routing_rmse(get_record(d, t))
            rows.append({"distance": d, "rmse_m": rmse, "div": div})
    out = {}
    for d in list(DISTANCES) + ["overall"]:
        sub = rows if d == "overall" else [r for r in rows if r["distance"] == d]
        out[str(d)] = {"mean_rmse_m": float(np.mean([r["rmse_m"] for r in sub])),
                       "div50_rate": float(np.mean([r["div"] for r in sub]))}
    return out


def run():
    sound_speed = {}
    for c in SOUND_SPEEDS:
        sound_speed[str(int(c))] = _sweep(
            lambda d, t, c=c: collect_mismatched(d, t, "test", c_true=c))
    clock = {}
    for off in CLOCK_OFFSETS_S:
        clock[f"{off*1000:.1f}ms"] = _sweep(
            lambda d, t, off=off: collect_mismatched(d, t, "test", c_true=1500.0,
                                                     clock_offset_s=off))
    payload = {"config": {"distances_m": list(DISTANCES), "trials_per_distance": TRIALS,
                          "assumed_sound_speed_m_s": 1500.0,
                          "sound_speeds_m_s": list(SOUND_SPEEDS),
                          "clock_offsets_ms": [o*1000 for o in CLOCK_OFFSETS_S],
                          "note": "라우팅 UKF 강건성: 음속 불일치·클럭 오프셋 vs baseline(1500·0)"},
               "sound_speed_sweep": sound_speed, "clock_offset_sweep": clock}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "robustness.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                         encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
