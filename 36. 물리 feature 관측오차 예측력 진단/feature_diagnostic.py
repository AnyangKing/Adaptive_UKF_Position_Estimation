"""물리 경로 feature가 실제 DOA/TOA 관측오차를 예측하는지 GT를 label로만 써서 진단한다.

필터를 더 복잡하게 만들기 전에, contamination likelihood에 넣을 feature가 실제 관측오차와
예측관계를 갖는지 먼저 확인한다. Ground Truth는 오차 label 산출에만 쓰고 feature 계산에는
쓰지 않는다.
"""

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from latent_reliability import physical_residual_score
from measurement import ideal_measurement
from path_identifiability import observed_peaks
from peak_measurement import extract_measurement
from soft_path_update import CubaturePathMarginalizer


# feature 이름과 방향: 모든 feature는 "값이 클수록 관측이 나쁘다"로 정렬한다.
FEATURE_NAMES = (
    "path_residual_score",    # 신규: 경로배정 정규화 residual (클수록 물리 불일치)
    "neg_path_evidence",      # 신규: cubature 경로 주변화 log evidence의 음수
    "doa_disagreement_deg",   # 기존: GCC-SRP 방향 불일치 (라우팅에 이미 사용)
    "peak_margin",            # 기존: gated SRP 1·2위 margin (26번은 오차와 양의 상관)
    "neg_min_peak_quality",   # 기존: 최소 peak 품질의 음수
)


def _unit(azimuth, elevation):
    return np.array([
        np.cos(elevation) * np.cos(azimuth),
        np.cos(elevation) * np.sin(azimuth),
        np.sin(elevation),
    ])


def doa_error_deg(measured, truth):
    direction = _unit(measured[8], measured[9])
    reference = _unit(truth[8], truth[9])
    return float(np.degrees(np.arccos(np.clip(direction @ reference, -1.0, 1.0))))


def scene(distance, index, split):
    """단일 정지 장면과 채널 설정을 독립 seed로 만든다."""
    root = 361000 if split == "validation" else 362000
    rng = np.random.default_rng(root + distance * 20 + index)
    azimuth = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    position = np.array([distance * np.cos(azimuth), distance * np.sin(azimuth), -depth])
    meta = dict(
        snr_db=float(rng.choice([10.0, 20.0, 30.0])),
        surface_reflection=float(-rng.uniform(0.72, 0.97)),
        bottom_reflection=float(rng.uniform(0.32, 0.78)),
        radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)),
    )
    cfg = replace(ChannelConfig(), seed=root + 50000 + distance * 100 + index, **meta)
    return position, cfg


def _finite(value, sentinel=1.0e3):
    """비유한 feature는 최악값(sentinel)으로 눌러 순위 계산을 깨지 않게 한다."""
    return float(value) if np.isfinite(value) else float(sentinel)


def measure_scene(distance, index, split, prior_stds):
    """한 장면을 한 번만 합성하고, 여러 prior 오차에서 feature와 실제 오차를 계산한다.

    반환: prior_std -> {"features": {...}, "errors": {...}}
    """
    position, cfg = scene(distance, index, split)
    _, received, _ = synthesize_received(position, cfg)

    measured, quality = extract_measurement(received, cfg)
    truth = ideal_measurement(position, cfg)
    times, strengths = observed_peaks(received[0], cfg, maximum=6)

    errors = {
        "doa_error_deg": doa_error_deg(measured, truth),
        "toa_error_m": float(abs(measured[0] - truth[0])),
        "tdoa_error_m": float(np.linalg.norm(measured[1:8] - truth[1:8])),
    }
    # prior에 무관한 기존 feature는 한 번만 계산한다.
    disagreement = float(quality["doa_disagreement_deg"])
    peak_margin = float(quality["peak_margin"])
    neg_min_quality = float(-quality["minimum_peak_quality"])

    marginalizer = CubaturePathMarginalizer(cfg, timing_std_s=1.0e-3, temperature=1.0)
    prior_covariance = np.diag([8.0**2, 8.0**2, 8.0**2])
    prior_rng = np.random.default_rng((361000 if split == "validation" else 362000)
                                      + 70000 + distance * 100 + index)

    result = {}
    for std in prior_stds:
        prior = position + prior_rng.normal(0.0, std, 3)
        prior[2] = np.clip(prior[2], -cfg.water_depth_m + 1.0, -1.0)
        score = physical_residual_score(prior, times, strengths, cfg)
        evidence = marginalizer.evidence_score(prior, prior_covariance, times, strengths)
        features = {
            "path_residual_score": _finite(score),
            "neg_path_evidence": _finite(-evidence),
            "doa_disagreement_deg": disagreement,
            "peak_margin": peak_margin,
            "neg_min_peak_quality": neg_min_quality,
        }
        result[std] = {"features": features, "errors": dict(errors)}
    return result
