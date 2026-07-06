"""49번 (③ 첫 단계, go/no-go): 채널을 현실화하면 편향 구조·per-ping 물리신호가 달라지는지 재진단.

핵심 질문: 3경로 평면반사(baseline)를 2차 반사 + 거친 표면 산란(realistic)으로 바꾸면
(1) DOA 오차 크기가 커지는가, (2) 38번의 peak_margin→고도각편향 예측신호(ρ≈-0.44, 설명력 ~9%)가
강해지는가. 강해지면 반증됐던 신뢰도 추론 novelty가 현실 채널에서 부활할 여지가 있다(→③ 본격 진행).
안 강해지면 편향 하한이 현실 채널에서도 유지된다는 결과로 ②에 흡수한다.

GT는 편향 label 산출에만. 두 모드는 같은 위치·환경·noise seed에서 채널 옵션만 다르다.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from scipy.stats import spearmanr

from channel import synthesize_received
from config import ChannelConfig
from measurement import ideal_measurement
from peak_measurement import extract_measurement

DISTANCES = (100, 200, 400, 600)
GEOMS = 20
REPEATS = 4
GEOM_ROOT = 490000
NOISE_ROOT = 493000
ROUGHNESS = 0.3   # 거친 표면 산란 강도(std)


def _unit(az, el):
    return np.array([np.cos(el)*np.cos(az), np.cos(el)*np.sin(az), np.sin(el)])


def geometry(distance, index):
    rng = np.random.default_rng(GEOM_ROOT + distance * 50 + index)
    az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(12.0, 78.0)
    pos = np.array([distance*np.cos(az), distance*np.sin(az), -depth])
    env = dict(snr_db=float(rng.choice([10.0, 20.0, 30.0])),
               surface_reflection=float(-rng.uniform(0.72, 0.97)),
               bottom_reflection=float(rng.uniform(0.32, 0.78)),
               radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)))
    return pos, env


def _measure(pos, env, distance, index, realistic):
    """모드별 noise 평균 고도각편향·총DOA오차·peak_margin·불일치."""
    extra = dict(second_order_multipath=True, surface_roughness=ROUGHNESS) if realistic else {}
    el_bias, ang_err, margins, disagree = [], [], [], []
    for r in range(REPEATS):
        seed = NOISE_ROOT + distance * 1000 + index * 20 + r
        cfg = replace(ChannelConfig(), seed=seed, **env, **extra)
        _, received, _ = synthesize_received(pos, cfg)
        z, q = extract_measurement(received, cfg)
        truth = ideal_measurement(pos, cfg)
        el_bias.append(np.degrees(z[9] - truth[9]))
        ang = np.degrees(np.arccos(np.clip(_unit(z[8], z[9]) @ _unit(truth[8], truth[9]), -1, 1)))
        ang_err.append(ang); margins.append(float(q["peak_margin"]))
        disagree.append(float(q["doa_disagreement_deg"]))
    return {"el_bias_deg": float(np.mean(el_bias)), "ang_err_deg": float(np.mean(ang_err)),
            "peak_margin": float(np.mean(margins)), "disagreement_deg": float(np.mean(disagree))}


def _summarize(records, mode):
    rows = [r for r in records if r["mode"] == mode]
    el = np.array([r["el_bias_deg"] for r in rows])
    ang = np.array([r["ang_err_deg"] for r in rows])
    margin = np.array([r["peak_margin"] for r in rows])
    dis = np.array([r["disagreement_deg"] for r in rows])
    rho_m, p_m = spearmanr(margin, el)
    rho_d, p_d = spearmanr(dis, el)
    return {"median_ang_err_deg": float(np.median(ang)), "p90_ang_err_deg": float(np.percentile(ang, 90)),
            "median_abs_el_bias_deg": float(np.median(np.abs(el))),
            "peak_margin_vs_elbias_rho": float(rho_m), "peak_margin_p": float(p_m),
            "disagreement_vs_elbias_rho": float(rho_d), "disagreement_p": float(p_d),
            "n": len(rows)}


def run():
    records = []
    for d in DISTANCES:
        for i in range(GEOMS):
            pos, env = geometry(d, i)
            for realistic in (False, True):
                m = _measure(pos, env, d, i, realistic)
                records.append({"distance": d, "index": i,
                                "mode": "realistic" if realistic else "baseline", **m})
    payload = {"config": {"distances_m": list(DISTANCES), "geoms_per_distance": GEOMS,
                          "repeats": REPEATS, "surface_roughness": ROUGHNESS,
                          "note": "baseline(3경로) vs realistic(2차반사+거친표면) 편향·신호 재진단"},
               "baseline": _summarize(records, "baseline"),
               "realistic": _summarize(records, "realistic")}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "rediagnose.json").write_text(json.dumps({**payload, "raw": records}, indent=2,
                                                    ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
