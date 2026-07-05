import unittest
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from peak_measurement import extract_measurement


class PeakMarginTests(unittest.TestCase):
    def test_margin_is_finite_and_nonnegative(self):
        cfg = ChannelConfig(seed=1); _, received, _ = synthesize_received(np.array([100., 20., -30.]), cfg)
        z, q = extract_measurement(received, cfg)
        self.assertEqual(z.shape, (10,)); self.assertTrue(np.isfinite(q["peak_margin"]))
        self.assertGreaterEqual(q["peak_margin"], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
