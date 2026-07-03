import unittest
import numpy as np

from channel import synthesize_received
from config import ChannelConfig, usb_array_global_m
from estimators import estimate_gcc_phat_doa, estimate_srp_phat_doa
from run_compare import run


class ImprovedEstimatorTests(unittest.TestCase):
    def setUp(self):
        self.cfg = ChannelConfig()
        self.source = np.array([100.0, 20.0, -20.0])

    def test_gcc_and_srp_return_unit_vectors(self):
        _, received, _ = synthesize_received(self.source, self.cfg)
        _, _, gcc, delays = estimate_gcc_phat_doa(received, self.cfg)
        _, _, srp, score = estimate_srp_phat_doa(received, self.cfg)
        self.assertAlmostEqual(float(np.linalg.norm(gcc)), 1.0, places=10)
        self.assertAlmostEqual(float(np.linalg.norm(srp)), 1.0, places=10)
        self.assertEqual(delays.shape, (28,))
        self.assertTrue(np.isfinite(score))

    def test_noiseless_direct_srp(self):
        cfg = ChannelConfig(snr_db=80.0, radial_velocity_m_s=0.0)
        _, received, _ = synthesize_received(
            self.source, cfg, include_multipath=False, include_noise=False
        )
        _, _, direction, _ = estimate_srp_phat_doa(received, cfg)
        truth = self.source - usb_array_global_m(cfg.receiver_depth_m).mean(axis=0)
        truth /= np.linalg.norm(truth)
        error = np.degrees(np.arccos(np.clip(direction @ truth, -1, 1)))
        self.assertLess(error, 3.0)

    def test_comparison_pipeline(self):
        metrics = run()
        self.assertTrue(all(np.isfinite(value) for value in metrics.values()))
        self.assertLess(metrics["srp_phat_doa_error_deg"], 25.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
