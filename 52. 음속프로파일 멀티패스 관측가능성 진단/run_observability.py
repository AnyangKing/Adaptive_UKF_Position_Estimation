"""52번 (방향 A 첫 진단): 음속 프로파일(gradient)이 멀티패스 관측으로 식별 가능한가.

원래 "물리 경로 일관성" 아이디어를, 반증된 per-ping 신뢰도 추론이 아니라 '환경(음속 프로파일)을
멀티패스로 추정'하는 쪽으로 재조준한다. 그 전제인 관측가능성을 먼저 진단한다: 소스 위치와 음속
gradient를 서로 독립으로 랜덤 생성하면, 관측 가능한 양(TOA 거리·DOA·멀티패스 도착구조·불일치)만으로
gradient를 복원할 수 있는가?

gradient와 위치를 독립 표본으로 뽑으므로, 관측→gradient 예측력이 있으면 그것은 위치 교락이 아니라
gradient 자체의 관측 signature다. out-of-sample 회귀 R²와 feature별 Spearman으로 판정한다.
gradient가 복원되면 위치+프로파일 joint 추정(방향 A)이 성립할 여지가 있다. Ground Truth(gradient)는
label로만.
"""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from scipy.stats import spearmanr

from channel import synthesize_received
from config import ChannelConfig
from path_identifiability import observed_peaks
from peak_measurement import extract_measurement

N_SCENES = 240
GEOM_ROOT = 520000
GRAD_MIN, GRAD_MAX = -0.12, 0.12
N_SPLITS = 200
RIDGE = 1e-2


def scene(index):
    rng = np.random.default_rng(GEOM_ROOT + index)
    distance = float(rng.uniform(100.0, 600.0))
    az = rng.uniform(-np.pi, np.pi); depth = rng.uniform(12.0, 78.0)
    pos = np.array([distance*np.cos(az), distance*np.sin(az), -depth])
    gradient = float(rng.uniform(GRAD_MIN, GRAD_MAX))   # 위치와 독립으로 뽑음
    env = dict(snr_db=float(rng.choice([10.0, 20.0, 30.0])),
               surface_reflection=float(-rng.uniform(0.72, 0.97)),
               bottom_reflection=float(rng.uniform(0.32, 0.78)),
               radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)))
    return pos, gradient, env


def observables(index):
    pos, gradient, env = scene(index)
    cfg = replace(ChannelConfig(), seed=523000 + index, second_order_multipath=True,
                  surface_roughness=0.3, sound_speed_gradient=gradient, **env)
    _, received, _ = synthesize_received(pos, cfg)
    z, q = extract_measurement(received, cfg)
    times, strengths = observed_peaks(received[0], cfg, maximum=6)
    t = np.sort(times)
    refl1 = float((t[1] - t[0]) * 1e6) if len(t) >= 2 else 0.0
    refl2 = float((t[2] - t[0]) * 1e6) if len(t) >= 3 else 0.0
    spread = float((t[-1] - t[0]) * 1e6)
    # blind 관측 벡터(위치 GT 미사용). 절대 TOA 거리, DOA 고도, 멀티패스 지연구조, 불일치, margin.
    feats = {"toa_range_m": float(z[0]), "doa_elevation_rad": float(z[9]),
             "first_reflection_delay_us": refl1, "second_reflection_delay_us": refl2,
             "peak_spread_us": spread, "doa_disagreement_deg": float(q["doa_disagreement_deg"]),
             "peak_margin": float(q["peak_margin"])}
    return gradient, feats


FEATURES = ("toa_range_m", "doa_elevation_rad", "first_reflection_delay_us",
            "second_reflection_delay_us", "peak_spread_us", "doa_disagreement_deg", "peak_margin")


def _design(rows):
    return np.array([[1.0] + [r["feats"][f] for f in FEATURES] for r in rows])


def _standardize(train, test):
    mean = train.mean(0); std = train.std(0); mean[0] = 0; std[0] = 1; std[std < 1e-12] = 1
    return (train - mean)/std, (test - mean)/std


def repeated_r2(rows, seed=520):
    rng = np.random.default_rng(seed)
    X = _design(rows); y = np.array([r["gradient"] for r in rows])
    n = len(rows); n_test = n // 2; r2s = []
    for _ in range(N_SPLITS):
        p = rng.permutation(n); te, tr = p[:n_test], p[n_test:]
        xtr, xte = _standardize(X[tr], X[te]); ytr, yte = y[tr], y[te]
        beta = np.linalg.solve(xtr.T@xtr + RIDGE*np.eye(xtr.shape[1]), xtr.T@ytr)
        pred = xte@beta
        ss_res = np.sum((yte-pred)**2); ss_tot = np.sum((yte-yte.mean())**2)
        r2s.append(1 - ss_res/ss_tot if ss_tot > 1e-12 else 0.0)
    r2s = np.asarray(r2s)
    return {"median_r2": float(np.median(r2s)),
            "r2_ci90": [float(np.percentile(r2s, 5)), float(np.percentile(r2s, 95))],
            "prob_r2_positive": float(np.mean(r2s > 0))}


def run():
    rows = []
    for i in range(N_SCENES):
        g, f = observables(i)
        rows.append({"gradient": g, "feats": f})
    y = np.array([r["gradient"] for r in rows])
    corr = {f: {"rho": float(spearmanr([r["feats"][f] for r in rows], y)[0]),
                "p": float(spearmanr([r["feats"][f] for r in rows], y)[1])} for f in FEATURES}
    payload = {"config": {"n_scenes": N_SCENES, "gradient_range": [GRAD_MIN, GRAD_MAX],
                          "n_splits": N_SPLITS,
                          "note": "위치·gradient 독립표본. 관측→gradient 복원 R²로 프로파일 관측가능성 진단"},
               "gradient_recovery": repeated_r2(rows),
               "feature_vs_gradient_spearman": corr}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "observability.json").write_text(json.dumps({**payload, "raw": rows}, indent=2,
                                                       ensure_ascii=False), encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
