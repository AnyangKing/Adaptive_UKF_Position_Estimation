"""40번 거리적응 보정 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

import trajectory as tj
from correction_models import (fit_global, fit_gated, fit_interaction,
                               corrected_observations, _predict,
                               MAX_CORRECTION_RAD, GATE_RANGE_M)


def _fake_record(distance, n=6, slope=0.05, seed=0):
    rng = np.random.default_rng(seed)
    margins = rng.uniform(0.0, 0.4, n)
    true_el = rng.uniform(-0.3, 0.1, n)
    obs = np.zeros((n, 10))
    obs[:, 0] = distance + rng.normal(0, 1.0, n)     # 관측 TOA 거리 ≈ 실제 거리
    obs[:, 9] = true_el + slope * margins + rng.normal(0, 1e-3, n)
    quals = [{"peak_margin": float(m)} for m in margins]
    return {"distance": distance, "true_elevation_rad": true_el,
            "observations": obs, "qualities": quals}


def test_split_seeds_disjoint():
    v, _ = tj.scenario(200, 0, "validation")
    t, _ = tj.scenario(200, 0, "test")
    assert np.linalg.norm(v[0] - t[0]) > 1.0


def test_three_fitters_return_beta():
    recs = [_fake_record(d, n=20, seed=i) for i, d in enumerate((100, 200, 400, 600))]
    for fit in (fit_global, fit_gated, fit_interaction):
        c = fit(recs)
        assert "beta" in c and all(np.isfinite(c["beta"]))


def test_gated_off_below_gate():
    c = {"kind": "gated", "beta": [0.1, 0.2], "gate_m": GATE_RANGE_M}
    assert _predict(c, 0.3, GATE_RANGE_M - 50) == 0.0       # 근거리 보정 없음
    assert _predict(c, 0.3, GATE_RANGE_M + 50) != 0.0       # 장거리 보정 있음


def test_interaction_range_dependence():
    """interaction 모델은 같은 margin이라도 거리에 따라 다른 보정을 낸다."""
    c = fit_interaction([_fake_record(d, n=25, slope=0.02 + 0.03 * (d == 600), seed=d)
                         for d in (100, 200, 400, 600)])
    near = _predict(c, 0.3, 100.0)
    far = _predict(c, 0.3, 600.0)
    assert near != far


def test_correction_clipped():
    c = {"kind": "global", "beta": [0.0, 100.0]}
    assert abs(_predict(c, 1.0, 400.0)) <= MAX_CORRECTION_RAD + 1e-12


def test_corrected_only_changes_elevation():
    rec = _fake_record(400, n=5, seed=3)
    c = fit_global([rec])
    z = corrected_observations(rec, c)
    assert np.allclose(z[:, :9], rec["observations"][:, :9])
    assert not np.allclose(z[:, 9], rec["observations"][:, 9])


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
