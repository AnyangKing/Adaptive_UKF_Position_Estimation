"""외부 테스트 프레임워크 없이 실행 가능한 기본 검증."""

import unittest
import numpy as np

from config import Config, sensor_positions_m
from run_smoke import run
from simulator import (
    generate_observations,
    generate_trajectory,
    initialize_position_from_observation,
    observation_from_position,
    wrap_angle,
)


class ObservationTests(unittest.TestCase):
    def test_sensor_geometry(self):
        sensors = sensor_positions_m()
        self.assertEqual(sensors.shape, (8, 3))
        np.testing.assert_allclose(np.linalg.norm(sensors[:, :2], axis=1), 0.033)
        np.testing.assert_allclose(sensors[::2, 2], 0.0)
        np.testing.assert_allclose(sensors[1::2, 2], -0.079)

    def test_known_axis_observation(self):
        sensors = sensor_positions_m()
        position = sensors[0] + np.array([10.0, 0.0, 0.0])
        z = observation_from_position(position, sensors)
        self.assertAlmostEqual(z[0], 10.0, places=12)
        self.assertAlmostEqual(z[8], 0.0, places=12)
        self.assertAlmostEqual(z[16], 0.0, places=12)

    def test_measurement_only_initialization(self):
        position = np.array([60.0, -40.0, 30.0])
        z = observation_from_position(position)
        np.testing.assert_allclose(initialize_position_from_observation(z), position, atol=1e-10)

    def test_noiseless_observations_match_trajectory(self):
        cfg = Config(num_steps=5)
        trajectory = generate_trajectory(cfg)
        observations = generate_observations(trajectory)
        expected = np.vstack([observation_from_position(p) for p in trajectory])
        np.testing.assert_allclose(observations, expected)

    def test_angle_wrap_interval(self):
        wrapped = wrap_angle(np.array([-3 * np.pi, np.pi, 3 * np.pi]))
        self.assertTrue(np.all(wrapped >= -np.pi))
        self.assertTrue(np.all(wrapped < np.pi))


class SmokeTests(unittest.TestCase):
    def test_noiseless_ukf(self):
        metrics = run()
        self.assertLess(metrics["rmse_m"], 0.05)
        self.assertLess(metrics["max_error_m"], 0.15)


if __name__ == "__main__":
    unittest.main(verbosity=2)

