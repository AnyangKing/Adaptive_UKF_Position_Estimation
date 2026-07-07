"""50번 (③ 새 feature 탐색): 현실채널 멀티패스 구조 feature가 계통 고도각 편향을 예측하는가.

각 기하에서 현실채널(2차반사+거친표면)로 noise 평균한 el_bias와, 도착구조 blind feature들을
계산해 Spearman 상관을 본다. 기존 peak_margin(49번 realistic ρ≈-0.22)을 넘는 feature가 있으면
"물리 경로 일관성" novelty의 새 근거가 되고(→③ 진행), 없으면 ③를 접는 근거가 된다. GT는 편향
label에만.
"""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from scipy.stats import spearmanr

from channel import synthesize_received
from config import ChannelConfig
from measurement import ideal_measurement
from newfeatures import FEATURE_NAMES, structure_features
from peak_measurement import extract_measurement

DISTANCES = (100, 200, 400, 600)
GEOMS = 20
REPEATS = 4
GEOM_ROOT = 500000
NOISE_ROOT = 503000
ROUGHNESS = 0.3


def geometry(distance, index):
    rng = np.random.default_rng(GEOM_ROOT + distance * 50 + index)
    az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(12.0, 78.0)
    pos = np.array([distance*np.cos(az), distance*np.sin(az), -depth])
    env = dict(snr_db=float(rng.choice([10.0, 20.0, 30.0])),
               surface_reflection=float(-rng.uniform(0.72, 0.97)),
               bottom_reflection=float(rng.uniform(0.32, 0.78)),
               radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)))
    return pos, env


def measure(pos, env, distance, index):
    """현실채널에서 noise 평균 el_bias와 blind 구조 feature(+peak_margin)."""
    el_bias, feats, margins = [], {n: [] for n in FEATURE_NAMES}, []
    for r in range(REPEATS):
        cfg = replace(ChannelConfig(), seed=NOISE_ROOT + distance*1000 + index*20 + r,
                      second_order_multipath=True, surface_roughness=ROUGHNESS, **env)
        _, received, _ = synthesize_received(pos, cfg)
        z, q = extract_measurement(received, cfg)
        truth = ideal_measurement(pos, cfg)
        el_bias.append(np.degrees(z[9] - truth[9]))
        margins.append(float(q["peak_margin"]))
        f = structure_features(received[0], cfg)
        for n in FEATURE_NAMES:
            feats[n].append(f[n])
    row = {"distance": distance, "el_bias_deg": float(np.mean(el_bias)),
           "peak_margin": float(np.mean(margins))}
    for n in FEATURE_NAMES:
        row[n] = float(np.mean(feats[n]))
    return row


def run():
    rows = [measure(*geometry(d, i), d, i) for d in DISTANCES for i in range(GEOMS)]
    el = np.array([r["el_bias_deg"] for r in rows])
    correlations = {}
    for name in FEATURE_NAMES + ("peak_margin",):
        vals = np.array([r[name] for r in rows])
        rho, p = spearmanr(vals, el)
        correlations[name] = {"spearman_rho": float(rho), "p": float(p)}
    payload = {"config": {"distances_m": list(DISTANCES), "geoms_per_distance": GEOMS,
                          "repeats": REPEATS, "surface_roughness": ROUGHNESS, "n": len(rows),
                          "note": "현실채널 멀티패스 구조 feature vs 고도각 편향 Spearman (blind)"},
               "feature_vs_elbias": correlations}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "newfeatures.json").write_text(json.dumps({**payload, "raw": rows}, indent=2,
                                                     ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
