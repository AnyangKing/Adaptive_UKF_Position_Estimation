import numpy as np

from config import ChannelConfig
from run_anchor_hop_schedule import (
    CONDITIONS,
    DISTANCE,
    FIXED_CARRIER_HZ,
    GEOMS,
    HOP_BANK_HZ,
    POLICIES,
    SCHEDULES,
    SETTLE_START,
    STEPS,
    geometry,
    lag1_autocorr,
    truth_trajectory,
)
from ukf import SignalObservationUKF, acceleration_process_covariance
from measurement import fixed_measurement_covariance, ideal_measurement
from whitening_adaptive import WhiteningAwareAdaptiveRUKF


def test_pre_registered_conditions_and_policy_set():
    assert DISTANCE == 600.0
    assert GEOMS == 4
    assert STEPS == 16
    assert SETTLE_START == 8
    assert [c[0] for c in CONDITIONS] == [
        "radial_0.05",
        "radial_1.0",
        "tangential_1.0",
        "tang_1.0_vz",
    ]
    assert "fixed" in POLICIES
    assert "hop_always" in POLICIES
    assert "fixed3_hop1" in POLICIES
    assert "fixed4_hop1" in POLICIES


def test_hop_bank_and_schedules_are_in_band_and_frozen():
    cfg = ChannelConfig()
    assert FIXED_CARRIER_HZ == 32000.0
    assert np.isclose(HOP_BANK_HZ[0], 30000.0)
    assert np.isclose(HOP_BANK_HZ[-1], 34000.0)
    half_bw = cfg.chirp_bandwidth_hz / 2.0
    assert HOP_BANK_HZ.min() - half_bw > 0.0
    assert HOP_BANK_HZ.max() + half_bw < cfg.sample_rate_hz / 2.0
    for name, carriers in SCHEDULES.items():
        assert carriers.shape == (STEPS,)
        assert carriers[0] == FIXED_CARRIER_HZ or name == "hop_always"
        assert carriers.min() - half_bw > 0.0
        assert carriers.max() + half_bw < cfg.sample_rate_hz / 2.0
    assert np.mean(SCHEDULES["fixed3_hop1"] != FIXED_CARRIER_HZ) < np.mean(SCHEDULES["alternating_fh"] != FIXED_CARRIER_HZ)


def test_geometry_modes():
    pos, env, az, sign = geometry(0, 0)
    radial = truth_trajectory(pos, az, sign, 1.0, "radial", 0.0)
    tang = truth_trajectory(pos, az, sign, 1.0, "tangential", 0.0)
    tang_vz = truth_trajectory(pos, az, sign, 1.0, "tangential", 0.08)
    assert radial.shape == (STEPS, 3)
    assert abs(np.linalg.norm(tang[-1, :2]) - np.linalg.norm(tang[0, :2])) < 0.5
    assert abs(tang_vz[-1, 2] - tang_vz[0, 2]) > 1.0
    assert env["radial_velocity_m_s"] == 0.0


def test_lag1_autocorr_sanity():
    assert lag1_autocorr(np.ones(6)) == 0.0
    assert lag1_autocorr(np.arange(8.0)) > 0.8
    assert lag1_autocorr(np.array([1.0, -1.0] * 5)) < -0.8


def test_schedule_filter_wrapper_runs_without_jump_gate():
    cfg = ChannelConfig()
    state = np.array([600.0, 0.0, -30.0, 0.0, 0.0, 0.0])
    ukf = SignalObservationUKF(
        state,
        np.diag([8.0**2] * 3 + [1.5**2] * 3),
        acceleration_process_covariance(1.0, 0.20),
        fixed_measurement_covariance(),
        cfg,
    )
    wrapper = WhiteningAwareAdaptiveRUKF(ukf, base_doa_scale=1.0, jump_threshold_deg=None, jump_doa_scale=1.0)
    z0 = ideal_measurement(state[:3], cfg)
    z1 = z0.copy()
    z1[9] += np.radians(1.0)
    q = {"doa_disagreement_deg": 0.0}
    wrapper.step(z0, q)
    wrapper.step(z1, q)
    assert not wrapper.history[-1]["jump_gate"]
    assert wrapper.history[-1]["R_doa_scale"] >= 1.0


if __name__ == "__main__":
    test_pre_registered_conditions_and_policy_set()
    test_hop_bank_and_schedules_are_in_band_and_frozen()
    test_geometry_modes()
    test_lag1_autocorr_sanity()
    test_schedule_filter_wrapper_runs_without_jump_gate()
    print("diagnostic tests passed")
