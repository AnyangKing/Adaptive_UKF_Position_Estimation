"""54번 (③ 새 레버): 송신 중심주파수가 계통 고도각 편향에 영향을 주는가.

배열 크기는 고정(반경 0.033 m)이라 중심주파수가 높을수록 파장 대비 개구가 커져 각 분해능이
좋아진다. 그럼 array-intrinsic 계통 편향(42번)이 주파수에 따라 줄어드는가?
- 주파수에 따라 편향이 줄면 → 다중주파수 융합/고주파 운용이 편향을 낮추는 새 레버(novelty 여지).
- 주파수에 무관하면 → 편향이 분해능이 아니라 순수 배열 기하에 고정임을 재확인(② 강화).
또 같은 기하에서 주파수 간 편향 상관도 본다(상관 낮으면 다중주파수가 평균으로 편향을 줄일 여지).

Ground Truth는 편향 label 산출에만. 채널은 3경로+2차반사+거친표면, 굴절은 끄고 주파수만 바꾼다.
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
GEOMS = 8
REPEATS = 4
CARRIERS_HZ = (16000.0, 24000.0, 32000.0, 48000.0, 64000.0)   # 192kHz 표본화 Nyquist 내
GEOM_ROOT = 540000
NOISE_ROOT = 543000


def _unit(az, el):
    return np.array([np.cos(el)*np.cos(az), np.cos(el)*np.sin(az), np.sin(el)])


def geometry(distance, index):
    rng = np.random.default_rng(GEOM_ROOT + distance*50 + index)
    az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(12.0, 78.0)
    pos = np.array([distance*np.cos(az), distance*np.sin(az), -depth])
    env = dict(snr_db=float(rng.choice([10.0, 20.0, 30.0])),
               surface_reflection=float(-rng.uniform(0.72, 0.97)),
               bottom_reflection=float(rng.uniform(0.32, 0.78)),
               radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)))
    return pos, env


def measure(pos, env, distance, index, carrier):
    el_bias, ang = [], []
    for r in range(REPEATS):
        cfg = replace(ChannelConfig(), seed=NOISE_ROOT + distance*1000 + index*20 + r,
                      second_order_multipath=True, surface_roughness=0.3,
                      carrier_hz=carrier, **env)
        _, received, _ = synthesize_received(pos, cfg)
        z, _ = extract_measurement(received, cfg)
        truth = ideal_measurement(pos, cfg)
        el_bias.append(np.degrees(z[9] - truth[9]))
        ang.append(np.degrees(np.arccos(np.clip(_unit(z[8], z[9]) @ _unit(truth[8], truth[9]), -1, 1))))
    return {"el_bias_deg": float(np.mean(el_bias)), "ang_err_deg": float(np.mean(ang))}


def run():
    # rows[carrier] = {(distance,index): measurement}
    per_carrier = {c: [] for c in CARRIERS_HZ}
    for d in DISTANCES:
        for i in range(GEOMS):
            pos, env = geometry(d, i)
            for c in CARRIERS_HZ:
                per_carrier[c].append(measure(pos, env, d, i, c))
    summary = {}
    for c in CARRIERS_HZ:
        el = np.array([m["el_bias_deg"] for m in per_carrier[c]])
        ang = np.array([m["ang_err_deg"] for m in per_carrier[c]])
        summary[f"{int(c/1000)}kHz"] = {
            "median_abs_el_bias_deg": float(np.median(np.abs(el))),
            "median_ang_err_deg": float(np.median(ang)),
            "p90_ang_err_deg": float(np.percentile(ang, 90))}
    # 주파수 간 편향 상관(같은 기하): 32kHz 기준 vs 다른 주파수
    ref = np.array([m["el_bias_deg"] for m in per_carrier[32000.0]])
    cross = {}
    for c in CARRIERS_HZ:
        vals = np.array([m["el_bias_deg"] for m in per_carrier[c]])
        cross[f"{int(c/1000)}kHz"] = float(spearmanr(ref, vals)[0]) if c != 32000.0 else 1.0
    payload = {"config": {"distances_m": list(DISTANCES), "geoms_per_distance": GEOMS,
                          "repeats": REPEATS, "carriers_hz": list(CARRIERS_HZ),
                          "note": "중심주파수 스윕 vs array-intrinsic 계통 편향. 배열 고정(반경0.033m)"},
               "by_frequency": summary,
               "elbias_cross_frequency_rho_vs_32kHz": cross}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "frequency.json").write_text(json.dumps({**payload, "raw": {f"{int(c/1000)}kHz": per_carrier[c]
                                                                       for c in CARRIERS_HZ}}, indent=2,
                                                   ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
