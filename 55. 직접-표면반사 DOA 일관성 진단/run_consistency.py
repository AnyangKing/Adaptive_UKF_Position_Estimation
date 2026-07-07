"""55번 (③ 물리 경로 일관성 재조준): 직접-표면반사 DOA 일관성이 (a) 소스 깊이를 독립 구속하는가,
(b) 직접-반사 고도각 gap이 계통 편향을 blind로 예측하는가.

원래 novelty("물리 경로 일관성")를 직접-반사 DOA 중복으로 검사한다. 반사파는 직접파와 다른 고도각
에서 도착하므로 소스 깊이를 독립 구속할 수 있고, 둘의 불일치는 array-intrinsic 편향(고도각 의존)이
직접·반사에 다르게 작용한 흔적일 수 있다. GT는 label로만.
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
from reflected_doa import reflected_srp_doa

DISTANCES = (100, 200, 400, 600)
GEOMS = 8
REPEATS = 4
GEOM_ROOT = 550000
NOISE_ROOT = 553000


def geometry(distance, index):
    rng = np.random.default_rng(GEOM_ROOT + distance*50 + index)
    az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(12.0, 78.0)
    pos = np.array([distance*np.cos(az), distance*np.sin(az), -depth])
    env = dict(snr_db=float(rng.choice([10.0, 20.0, 30.0])),
               surface_reflection=float(-rng.uniform(0.72, 0.97)),
               bottom_reflection=float(rng.uniform(0.32, 0.78)),
               radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)))
    return pos, env, float(depth)


def measure(pos, env, distance, index):
    el_d, el_r, el_true_l = [], [], []
    for r in range(REPEATS):
        cfg = replace(ChannelConfig(), seed=NOISE_ROOT + distance*1000 + index*20 + r,
                      second_order_multipath=True, surface_roughness=0.3, **env)
        _, received, _ = synthesize_received(pos, cfg)
        z, _ = extract_measurement(received, cfg)          # 직접파 DOA
        _, elr = reflected_srp_doa(received, cfg)           # 반사파 DOA
        truth = ideal_measurement(pos, cfg)
        el_d.append(float(z[9])); el_r.append(float(elr)); el_true_l.append(float(truth[9]))
    el_d = float(np.mean(el_d)); el_r = float(np.mean(el_r)); el_true = float(np.mean(el_true_l))
    return {"distance": distance, "el_direct_deg": np.degrees(el_d),
            "el_reflected_deg": np.degrees(el_r), "el_true_deg": np.degrees(el_true),
            "el_bias_deg": np.degrees(el_d - el_true),
            "direct_reflected_gap_deg": np.degrees(el_d - el_r)}


def run():
    rows = [measure(*geometry(d, i)[:2], d, i) for d in DISTANCES for i in range(GEOMS)]
    el_true = np.array([r["el_true_deg"] for r in rows])
    el_d = np.array([r["el_direct_deg"] for r in rows])
    el_r = np.array([r["el_reflected_deg"] for r in rows])
    bias = np.array([r["el_bias_deg"] for r in rows])
    gap = np.array([r["direct_reflected_gap_deg"] for r in rows])

    # (a) 반사 DOA가 참 고도각을 직접 DOA와 독립으로 구속하는가: 회귀 R² 비교
    def r2(features):
        X = np.column_stack([np.ones(len(rows))] + features)
        beta, *_ = np.linalg.lstsq(X, el_true, rcond=None)
        res = el_true - X @ beta
        return float(1 - np.sum(res**2)/np.sum((el_true - el_true.mean())**2))
    r2_direct = r2([el_d])
    r2_direct_reflected = r2([el_d, el_r])

    payload = {"config": {"distances_m": list(DISTANCES), "geoms_per_distance": GEOMS,
                          "repeats": REPEATS, "n": len(rows),
                          "note": "직접-표면반사 DOA 일관성: 깊이 독립구속 + gap의 편향 예측력"},
               "depth_constraint": {
                   "true_el_from_direct_only_R2": r2_direct,
                   "true_el_from_direct_plus_reflected_R2": r2_direct_reflected,
                   "reflected_el_vs_true_el_rho": float(spearmanr(el_r, el_true)[0])},
               "bias_signal": {
                   "gap_vs_elbias_rho": float(spearmanr(gap, bias)[0]),
                   "gap_vs_elbias_p": float(spearmanr(gap, bias)[1]),
                   "reflected_el_vs_elbias_rho": float(spearmanr(el_r, bias)[0])}}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "consistency.json").write_text(json.dumps({**payload, "raw": rows}, indent=2,
                                                     ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
