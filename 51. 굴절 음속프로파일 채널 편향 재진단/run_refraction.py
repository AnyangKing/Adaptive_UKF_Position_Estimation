"""51번 (③ 굴절 채널): 거리·깊이 의존 음속(굴절)이 편향 구조·per-ping 신호를 바꾸는지 재진단.

Bellhop이 현재 모델보다 더하는 핵심 물리는 굴절(휜 경로)이다. 여기서는 선형 음속 gradient로
직접파 도착 고도각을 휘게 하고, baseline(g=0, 2차반사+거친표면)과 굴절(g=-0.05) 채널을 같은
기하·seed에서 비교한다. 질문: (1) DOA 오차·편향이 커지는가, (2) 기존 peak_margin 예측신호가
강해지는가, (3) 굴절 편향이 관측 거리(z[0])로 예측되는가(=프로파일 알면 보정 가능하나 blind는 아님).

GT는 편향 label에만. 굴절은 순수 물리(음속 프로파일)로만 결정된다.
"""

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
GRADIENT = -0.05          # 굴절 음속 gradient [s^-1] (하향 굴절)
GEOM_ROOT = 510000
NOISE_ROOT = 513000


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


def measure(pos, env, distance, index, gradient):
    common = dict(second_order_multipath=True, surface_roughness=0.3, sound_speed_gradient=gradient)
    el_bias, ang, margins, obs_range = [], [], [], []
    for r in range(REPEATS):
        cfg = replace(ChannelConfig(), seed=NOISE_ROOT + distance*1000 + index*20 + r, **env, **common)
        _, received, _ = synthesize_received(pos, cfg)
        z, q = extract_measurement(received, cfg)
        truth = ideal_measurement(pos, cfg)
        el_bias.append(np.degrees(z[9] - truth[9]))
        ang.append(np.degrees(np.arccos(np.clip(_unit(z[8], z[9]) @ _unit(truth[8], truth[9]), -1, 1))))
        margins.append(float(q["peak_margin"])); obs_range.append(float(z[0]))
    return {"distance": distance, "el_bias_deg": float(np.mean(el_bias)),
            "ang_err_deg": float(np.mean(ang)), "peak_margin": float(np.mean(margins)),
            "obs_range_m": float(np.mean(obs_range))}


def _summ(rows):
    el = np.array([r["el_bias_deg"] for r in rows])
    ang = np.array([r["ang_err_deg"] for r in rows])
    margin = np.array([r["peak_margin"] for r in rows])
    rng = np.array([r["obs_range_m"] for r in rows])
    return {"median_ang_err_deg": float(np.median(ang)), "p90_ang_err_deg": float(np.percentile(ang, 90)),
            "median_abs_el_bias_deg": float(np.median(np.abs(el))),
            "peak_margin_vs_elbias_rho": float(spearmanr(margin, el)[0]),
            "obs_range_vs_elbias_rho": float(spearmanr(rng, el)[0]),
            "obs_range_vs_elbias_p": float(spearmanr(rng, el)[1]), "n": len(rows)}


def run():
    base, refr = [], []
    for d in DISTANCES:
        for i in range(GEOMS):
            pos, env = geometry(d, i)
            base.append(measure(pos, env, d, i, 0.0))
            refr.append(measure(pos, env, d, i, GRADIENT))
    payload = {"config": {"distances_m": list(DISTANCES), "geoms_per_distance": GEOMS,
                          "repeats": REPEATS, "gradient_s^-1": GRADIENT,
                          "note": "baseline(g=0) vs 굴절(g=-0.05) 채널 편향·신호 재진단, 둘 다 2차반사+거친표면"},
               "baseline": _summ(base), "refracted": _summ(refr)}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "refraction.json").write_text(json.dumps({**payload, "raw_baseline": base,
                                                     "raw_refracted": refr}, indent=2,
                                                    ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
