"""38번 재현 파이프라인의 계약을 최소로 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

import bias_features as bf
from reproduction import (repeated_split_reduction, bootstrap_spearman,
                          feature_correlations, TARGETS)


def _fake(n, seed=0):
    """el_bias가 feature와 상관되도록 만든 합성 기록."""
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        q = rng.uniform(-3e4, -1e4)
        el = 0.2 + 1e-5 * q + rng.normal(0, 0.1)   # neg_min_peak_quality와 상관
        out.append({
            "distance": int(rng.choice(bf.DISTANCES)),
            "el_bias_deg": float(el), "az_bias_deg": float(rng.normal(0, 0.3)),
            "bias_angle_deg": float(abs(rng.normal(0.6, 0.2))),
            "features": {"doa_disagreement_deg": rng.uniform(1, 8),
                         "peak_margin": rng.uniform(0, 0.3),
                         "neg_min_peak_quality": q},
        })
    return out


def test_geometry_seeds_differ_from_37():
    """38번 GEOMETRY_ROOT는 37번(370000)과 다른 계열이어야 한다."""
    assert bf.GEOMETRY_ROOT >= 380000


def test_geometry_distance_matches():
    pos, _ = bf.geometry(400, 3)
    assert abs(np.hypot(pos[0], pos[1]) - 400.0) < 1e-6


def test_decompose_cheap():
    original = bf.REPEATS
    bf.REPEATS = 2
    try:
        r = bf.decompose_geometry(200, 0)
    finally:
        bf.REPEATS = original
    assert np.isfinite(r["el_bias_deg"]) and np.isfinite(r["bias_angle_deg"])
    assert set(r["features"]) == set(bf.SIGNAL_FEATURES)


def test_reduction_detects_real_signal():
    """feature와 상관된 합성 el_bias에서 잔차감소 중앙값이 양수여야 한다."""
    records = _fake(120, seed=1)
    res = repeated_split_reduction(records, "el_bias_deg")
    assert res["median_reduction"] > 0.0
    assert 0.0 <= res["prob_reduction_positive"] <= 1.0


def test_bootstrap_spearman_shape():
    records = _fake(80, seed=2)
    corr = feature_correlations(records, "el_bias_deg")
    for name in bf.SIGNAL_FEATURES:
        assert "rho" in corr[name] and len(corr[name]["ci95"]) == 2


def test_targets_present():
    assert TARGETS[0] == "el_bias_deg"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
