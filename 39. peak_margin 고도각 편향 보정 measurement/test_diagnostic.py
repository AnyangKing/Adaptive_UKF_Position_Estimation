"""39번 ablation 파이프라인 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

import trajectory as tj
from elevation_correction import (fit_correction, predicted_bias_rad,
                                  corrected_observations, MAX_CORRECTION_RAD)


def _fake_record(distance, n=4, slope=0.02, seed=0):
    rng = np.random.default_rng(seed)
    margins = rng.uniform(0.0, 0.4, n)
    true_el = rng.uniform(-0.3, 0.1, n)
    obs = np.zeros((n, 10))
    # el_bias = slope*margin (+잡음)이 되도록 관측 고도각 구성
    obs[:, 9] = true_el + slope * margins + rng.normal(0, 1e-3, n)
    quals = [{"peak_margin": float(m)} for m in margins]
    return {"distance": distance, "true_elevation_rad": true_el,
            "observations": obs, "qualities": quals}


def test_split_seeds_disjoint():
    v, _ = tj.scenario(200, 0, "validation")
    t, _ = tj.scenario(200, 0, "test")
    assert np.linalg.norm(v[0] - t[0]) > 1.0


def test_fit_recovers_positive_slope():
    recs = [_fake_record(200, n=30, slope=0.05, seed=i) for i in range(4)]
    fit = fit_correction(recs)
    assert fit["slope_rad_per_margin"] > 0.0
    assert fit["n_pings"] == 120


def test_correction_clipped():
    corr = {"intercept_rad": 0.0, "slope_rad_per_margin": 100.0}
    assert abs(predicted_bias_rad(1.0, corr)) <= MAX_CORRECTION_RAD + 1e-12


def test_corrected_only_changes_elevation():
    rec = _fake_record(400, n=5, seed=3)
    corr = {"intercept_rad": 0.01, "slope_rad_per_margin": 0.02}
    z = corrected_observations(rec, corr)
    assert np.allclose(z[:, :9], rec["observations"][:, :9])   # el 외 열 불변
    assert not np.allclose(z[:, 9], rec["observations"][:, 9]) # el은 변함


def test_corrected_reduces_bias_on_synthetic():
    """참편향과 같은 방향 계수면 보정 후 고도각 오차가 준다."""
    rec = _fake_record(600, n=40, slope=0.05, seed=7)
    fit = fit_correction([rec])
    z = corrected_observations(rec, fit)
    before = np.std(rec["observations"][:, 9] - rec["true_elevation_rad"])
    after = np.std(z[:, 9] - rec["true_elevation_rad"])
    assert after <= before


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
