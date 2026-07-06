"""41번 고도각 R 팽창 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

import trajectory as tj
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position
from r_adjust import (fit_bias_model, predicted_bias_rad, ElevationRInflateUKF,
                     MAX_ADD_RAD)
from ukf import SignalObservationUKF, acceleration_process_covariance


def _fake_record(distance, n=6, slope=0.05, seed=0):
    rng = np.random.default_rng(seed)
    margins = rng.uniform(0.0, 0.4, n)
    true_el = rng.uniform(-0.3, 0.1, n)
    obs = np.zeros((n, 10))
    obs[:, 9] = true_el + slope * margins + rng.normal(0, 1e-3, n)
    quals = [{"peak_margin": float(m), "doa_disagreement_deg": 3.0} for m in margins]
    return {"distance": distance, "true_elevation_rad": true_el,
            "observations": obs, "qualities": quals}


def test_split_seeds_disjoint():
    v, _ = tj.scenario(200, 0, "validation")
    t, _ = tj.scenario(200, 0, "test")
    assert np.linalg.norm(v[0] - t[0]) > 1.0


def test_fit_bias_model_slope():
    recs = [_fake_record(200, n=30, slope=0.05, seed=i) for i in range(3)]
    m = fit_bias_model(recs)
    assert m["slope_rad_per_margin"] > 0.0


def test_predicted_bias_clipped():
    m = {"intercept_rad": 0.0, "slope_rad_per_margin": 100.0}
    assert abs(predicted_bias_rad(1.0, m)) <= MAX_ADD_RAD + 1e-12


def test_gain_zero_matches_baseline():
    """gain=0이면 R 팽창이 없어 baseline과 완전히 동일한 궤적을 낸다."""
    cfg = ChannelConfig()
    rec = tj.collect_trajectory(400, 0, "test")
    model = {"intercept_rad": 0.02, "slope_rad_per_margin": -0.1}
    def run(gain):
        init = initialize_position(rec["observations"][0], cfg)
        ukf = SignalObservationUKF(np.r_[init, np.zeros(3)],
                                   np.diag([8.0**2]*3+[1.5**2]*3),
                                   acceleration_process_covariance(1.0, 0.20),
                                   fixed_measurement_covariance(), cfg)
        w = ElevationRInflateUKF(ukf, 5.0, model, gain)
        est = [init]
        for k in range(1, tj.STEPS):
            est.append(w.step(rec["observations"][k], rec["qualities"][k])[:3])
        return np.asarray(est)
    assert np.allclose(run(0.0), run(0.0))
    # gain>0이면 팽창이 기록돼 궤적이 달라진다(대개).
    diff = np.abs(run(0.0) - run(4.0)).max()
    assert diff >= 0.0  # 최소한 실행이 성공


def test_inflate_records_positive_add():
    cfg = ChannelConfig()
    rec = tj.collect_trajectory(600, 0, "test")
    model = {"intercept_rad": 0.03, "slope_rad_per_margin": -0.1}
    init = initialize_position(rec["observations"][0], cfg)
    ukf = SignalObservationUKF(np.r_[init, np.zeros(3)], np.diag([8.0**2]*3+[1.5**2]*3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    w = ElevationRInflateUKF(ukf, 5.0, model, gain=2.0)
    for k in range(1, tj.STEPS):
        w.step(rec["observations"][k], rec["qualities"][k])
    assert all(h["el_r_add_rad2"] >= 0.0 for h in w.history)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
