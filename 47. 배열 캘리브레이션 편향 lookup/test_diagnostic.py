"""47번 배열 캘리브레이션 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

import trajectory as tj
from calibration import ElevationBiasLookup, corrected_observations, MAX_CORRECTION_RAD
from config import ChannelConfig


def test_split_seeds_disjoint():
    v, _ = tj.scenario(200, 0, "validation")
    t, _ = tj.scenario(200, 0, "test")
    assert np.linalg.norm(v[0] - t[0]) > 1.0


def test_lookup_predicts_known_bias():
    """색인 근처에 같은 편향이 몰려 있으면 그 값을 회복한다."""
    az = np.linspace(-np.pi, np.pi, 50)
    el = np.zeros(50)
    bias = np.full(50, 0.02)  # 상수 편향
    lut = ElevationBiasLookup(az, el, bias, k=5)
    assert abs(lut.predict(0.3, 0.0) - 0.02) < 1e-6


def test_prediction_clipped():
    lut = ElevationBiasLookup([0.0], [0.0], [100.0], k=1)
    assert abs(lut.predict(0.0, 0.0)) <= MAX_CORRECTION_RAD + 1e-12


def test_fit_and_correct_shapes():
    cfg = ChannelConfig()
    val = [tj.collect_trajectory(200, 0, "validation")]
    lut = ElevationBiasLookup.fit(val, cfg, k=5)
    assert len(lut.bias) == tj.STEPS
    rec = tj.collect_trajectory(200, 1, "test")
    z = corrected_observations(rec, lut)
    assert np.allclose(z[:, :9], rec["observations"][:, :9])   # el 외 불변
    assert z.shape == rec["observations"].shape


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
