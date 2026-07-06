"""44번 라우팅 ablation 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

import trajectory as tj
from config import ChannelConfig
from conditional_adaptive import ConditionalAdaptiveRUKF
from measurement import fixed_measurement_covariance, initialize_position
from run_routing_ablation import _run_plain, _run_routing, _rmse_after
from ukf import SignalObservationUKF, acceleration_process_covariance


def test_split_seeds_disjoint():
    v, _ = tj.scenario(200, 0, "validation")
    t, _ = tj.scenario(200, 0, "test")
    assert np.linalg.norm(v[0] - t[0]) > 1.0


def test_routing_history_records_nis():
    cfg = ChannelConfig()
    rec = tj.collect_trajectory(400, 0, "test")
    init = initialize_position(rec["observations"][0], cfg)
    ukf = SignalObservationUKF(np.r_[init, np.zeros(3)], np.diag([8.0**2]*3+[1.5**2]*3),
                               acceleration_process_covariance(1.0, 0.20),
                               fixed_measurement_covariance(), cfg)
    w = ConditionalAdaptiveRUKF(ukf, 5.0)
    w.step(rec["observations"][1], rec["qualities"][1])
    h = w.history[-1]
    assert "nis" in h and np.isfinite(h["nis"]) and "routed" in h


def test_both_variants_run():
    cfg = ChannelConfig()
    rec = tj.collect_trajectory(200, 0, "test")
    p_est, p_nv, p_iv, p_div = _run_plain(rec, cfg)
    r_est, r_nv, r_iv, r_div, routed = _run_routing(rec, cfg)
    assert p_est.shape == r_est.shape == (tj.STEPS, 3)
    assert 0.0 <= routed <= 1.0
    assert np.isfinite(_rmse_after(p_est, rec["truth"])[0])
    assert np.isfinite(_rmse_after(r_est, rec["truth"])[0])


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
