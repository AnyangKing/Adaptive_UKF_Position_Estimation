"""52번 프로파일 관측가능성 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from run_observability import scene, observables, repeated_r2, FEATURES, GRAD_MIN, GRAD_MAX


def test_scene_independent_gradient():
    """gradient가 지정 범위 안이고 위치와 별개로 뽑힌다."""
    _, g0, _ = scene(0); _, g1, _ = scene(1)
    assert GRAD_MIN <= g0 <= GRAD_MAX and GRAD_MIN <= g1 <= GRAD_MAX
    assert g0 != g1


def test_observables_shape():
    g, f = observables(0)
    assert GRAD_MIN <= g <= GRAD_MAX
    assert set(f) == set(FEATURES)
    assert all(np.isfinite(v) for v in f.values())


def test_r2_recovers_synthetic_signal():
    """feature가 gradient와 선형관계면 R²가 양수로 나온다(회귀 파이프라인 정상)."""
    rng = np.random.default_rng(0)
    rows = []
    for _ in range(120):
        g = rng.uniform(GRAD_MIN, GRAD_MAX)
        feats = {f: 0.0 for f in FEATURES}
        feats["toa_range_m"] = 10.0*g + rng.normal(0, 0.05)   # gradient에 선형 의존
        for f in FEATURES:
            if f != "toa_range_m":
                feats[f] = rng.normal()
        rows.append({"gradient": g, "feats": feats})
    res = repeated_r2(rows)
    assert res["median_r2"] > 0.3


def test_r2_null_when_no_signal():
    """feature가 gradient와 무관하면 out-of-sample R² 중앙값이 0 근처(또는 음수)."""
    rng = np.random.default_rng(1)
    rows = [{"gradient": rng.uniform(GRAD_MIN, GRAD_MAX),
             "feats": {f: rng.normal() for f in FEATURES}} for _ in range(120)]
    res = repeated_r2(rows)
    assert res["median_r2"] < 0.15


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
