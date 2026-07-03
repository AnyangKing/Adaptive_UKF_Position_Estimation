import unittest
import numpy as np

from config import ChannelConfig
from measurement import fixed_measurement_covariance, ideal_measurement, initialize_position
from estimators import pair_delays_to_reference_tdoa
from run_smoke import run


class SignalUKFTests(unittest.TestCase):
    def test_pair_delay_reconstruction(self):
        q = np.array([0.0, 1, 2, -1, 3, -2, 4, -3], dtype=float) * 1e-6
        pairs = np.array([q[i] - q[j] for i in range(8) for j in range(i+1, 8)])
        np.testing.assert_allclose(pair_delays_to_reference_tdoa(pairs), q[1:], atol=1e-15)

    def test_full_tdoa_covariance(self):
        covariance = fixed_measurement_covariance()
        self.assertEqual(covariance.shape, (10, 10))
        self.assertGreater(covariance[1, 2], 0.0)
        self.assertTrue(np.all(np.linalg.eigvalsh(covariance) > 0.0))

    def test_ideal_initialization(self):
        cfg = ChannelConfig()
        position = np.array([100.0, 20.0, -20.0])
        z = ideal_measurement(position, cfg)
        np.testing.assert_allclose(initialize_position(z, cfg), position, atol=1e-9)

    def test_end_to_end_smoke(self):
        metrics = run()
        self.assertTrue(all(np.isfinite(v) for v in metrics.values()))
        self.assertLess(metrics["rmse_after_5_m"], 10.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
