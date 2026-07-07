"""53번 joint UKF 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from config import ChannelConfig
from joint_ukf import JointPositionGradientUKF, REFRACTION_K
from measurement import fixed_measurement_covariance, ideal_measurement
from run_joint import trajectory, observe, run_baseline, run_joint
from ukf import acceleration_process_covariance


def _make(cfg, g0=0.0):
    Q = np.zeros((7, 7)); Q[:6, :6] = acceleration_process_covariance(1.0, 0.20); Q[6, 6] = 0.005**2
    P0 = np.diag([8.0**2]*3 + [1.5**2]*3 + [0.1**2])
    return JointPositionGradientUKF(np.r_[300.0, 20.0, -35.0, 0, 0, 0, g0], P0, Q,
                                    fixed_measurement_covariance(), cfg)


def test_measure_adds_gradient_term():
    """gradient≠0이면 h의 고도각이 K·g·range 만큼 이동한다."""
    cfg = ChannelConfig()
    f0 = _make(cfg, 0.0); fg = _make(cfg, 0.05)
    pt0 = f0.x.copy(); ptg = fg.x.copy()
    z0 = f0._measure(pt0); zg = fg._measure(ptg)
    rng = np.hypot(pt0[0]-f0.center[0], pt0[1]-f0.center[1])
    assert abs((zg[9]-z0[9]) - REFRACTION_K*0.05*rng) < 1e-9
    assert np.allclose(z0[:9], zg[:9])   # gradient는 고도각에만 영향


def test_step_runs_and_state_dim():
    cfg = ChannelConfig()
    ukf = _make(cfg)
    truth = np.array([300.0, 20.0, -35.0])
    z = ukf._measure(np.r_[truth, 0, 0, 0, 0.0])
    x = ukf.step(z)
    assert x.shape == (7,) and np.all(np.isfinite(x))


def test_trajectory_and_observe_shapes():
    truth, g, env = trajectory(0)
    assert truth.shape[1] == 3 and -0.1 <= g <= 0.1
    obs = observe(truth, g, env, 0)
    assert obs.shape[0] == truth.shape[0] and obs.shape[1] == 10


def test_baseline_and_joint_run():
    cfg = ChannelConfig()
    truth, g, env = trajectory(1)
    obs = observe(truth, g, env, 1)
    base = run_baseline(obs, truth, cfg)
    joint, g_est = run_joint(obs, truth, cfg)
    assert base.shape == joint.shape
    assert np.isfinite(g_est)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
