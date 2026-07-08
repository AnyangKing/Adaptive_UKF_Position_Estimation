import numpy as np

from config import ChannelConfig
from run_moving_validation import (
    CONDITIONS,
    DISTANCE,
    FIXED_CARRIER_HZ,
    GEOMS,
    HOP_CARRIERS_HZ,
    SETTLE_START,
    STEPS,
    geometry,
    lag1_autocorr,
    truth_trajectory,
)


def test_pre_registered_motion_conditions():
    names = [c[0] for c in CONDITIONS]
    assert names == ["radial_0.05", "radial_1.0", "tangential_1.0", "tang_1.0_vz"]
    assert GEOMS == 16
    assert STEPS == 20
    assert SETTLE_START == 10
    assert DISTANCE == 600.0


def test_hop_policy_is_frozen_from_61_62():
    cfg = ChannelConfig()
    nyquist = cfg.sample_rate_hz / 2.0
    half_bw = cfg.chirp_bandwidth_hz / 2.0
    assert FIXED_CARRIER_HZ == 32000.0
    assert len(HOP_CARRIERS_HZ) == STEPS
    assert np.isclose(HOP_CARRIERS_HZ[0], 30000.0)
    assert np.isclose(HOP_CARRIERS_HZ[-1], 34000.0)
    assert HOP_CARRIERS_HZ.min() - half_bw > 0.0
    assert HOP_CARRIERS_HZ.max() + half_bw < nyquist


def test_trajectory_modes_match_intended_geometry():
    pos, env, az, sign = geometry(0, 0)
    radial_truth = truth_trajectory(pos, az, sign, 1.0, "radial", 0.0)
    tangential_truth = truth_trajectory(pos, az, sign, 1.0, "tangential", 0.0)
    tang_vz_truth = truth_trajectory(pos, az, sign, 1.0, "tangential", 0.08)

    assert radial_truth.shape == (STEPS, 3)
    assert tangential_truth.shape == (STEPS, 3)
    assert tang_vz_truth.shape == (STEPS, 3)
    assert np.linalg.norm(radial_truth[-1, :2]) != np.linalg.norm(radial_truth[0, :2])
    assert abs(np.linalg.norm(tangential_truth[-1, :2]) - np.linalg.norm(tangential_truth[0, :2])) < 0.5
    assert abs(tang_vz_truth[-1, 2] - tang_vz_truth[0, 2]) > 1.0
    assert env["radial_velocity_m_s"] == 0.0


def test_lag1_autocorr_sanity():
    assert lag1_autocorr(np.ones(8)) == 0.0
    assert lag1_autocorr(np.arange(8.0)) > 0.8
    alternating = np.array([1.0, -1.0] * 5)
    assert lag1_autocorr(alternating) < -0.8


if __name__ == "__main__":
    test_pre_registered_motion_conditions()
    test_hop_policy_is_frozen_from_61_62()
    test_trajectory_modes_match_intended_geometry()
    test_lag1_autocorr_sanity()
    print("diagnostic tests passed")
