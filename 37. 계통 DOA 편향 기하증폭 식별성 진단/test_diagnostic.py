"""37번 진단 파이프라인의 계약을 최소로 검증한다 (무거운 전체 실행 없이).

이 환경에는 pytest가 없으므로 순수 Python assert로 작성하고 직접 실행한다.
"""

import numpy as np

import bias_decomposition as bd
from identifiability import diagnose_B, diagnose_C, _standardize


def test_geometry_is_split_disjoint():
    v_pos, _ = bd.geometry(200, 0, "validation")
    t_pos, _ = bd.geometry(200, 0, "test")
    assert np.linalg.norm(v_pos - t_pos) > 1.0


def test_geometry_distance_matches():
    pos, _ = bd.geometry(400, 2, "test")
    assert abs(np.hypot(pos[0], pos[1]) - 400.0) < 1e-6


def test_decompose_reduces_repeats_cheaply():
    original = bd.REPEATS
    bd.REPEATS = 3
    try:
        pos, env = bd.geometry(200, 0, "test")
        r = bd.decompose_geometry(pos, env, 200, 0, "test")
    finally:
        bd.REPEATS = original
    assert np.isfinite(r["bias_angle_deg"]) and r["bias_angle_deg"] >= 0.0
    assert np.isfinite(r["random_angle_deg"]) and r["random_angle_deg"] >= 0.0
    assert r["pos_bias_m"] >= 0.0
    assert {"doa_disagreement_deg", "gated_full_gap_deg"}.issubset(r["features"])


def test_standardize_keeps_intercept():
    train = np.array([[1.0, 2.0], [1.0, 4.0], [1.0, 6.0]])
    test = np.array([[1.0, 4.0]])
    tr, te = _standardize(train, test)
    assert np.allclose(tr[:, 0], 1.0)
    assert abs(tr[:, 1].mean()) < 1e-9
    assert abs(te[0, 1]) < 1e-9


def test_diagnose_bc_shapes():
    rng = np.random.default_rng(0)
    def fake(n):
        out = []
        for _ in range(n):
            out.append({
                "distance": 200, "true_azimuth_deg": rng.uniform(-180, 180),
                "true_elevation_deg": rng.uniform(-40, 10),
                "bias_angle_deg": abs(rng.normal(0.5, 0.2)),
                "az_bias_deg": rng.normal(0, 0.3), "el_bias_deg": rng.normal(0.1, 0.2),
                "features": {"doa_disagreement_deg": rng.uniform(1, 8),
                             "gated_full_gap_deg": rng.uniform(0, 2),
                             "peak_margin": rng.uniform(0, 0.3),
                             "neg_min_peak_quality": rng.uniform(-3e4, -1e4)},
            })
        return out
    v, t = fake(12), fake(12)
    b, c = diagnose_B(v, t), diagnose_C(v, t)
    for target in ("bias_angle_deg", "az_bias_deg", "el_bias_deg"):
        assert "residual_reduction" in b[target]
        assert "residual_reduction" in c[target]
    assert "feature_correlations" in c


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
