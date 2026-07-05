import unittest
import numpy as np
from channel import synthesize_received
from config import ChannelConfig
from multipeak_measurement import extract_measurement


class MultiHypothesisTest(unittest.TestCase):
    def test_candidates_are_sorted_and_separated(self):
        cfg = ChannelConfig(seed=27001); _, received, _ = synthesize_received(np.array([100., 20., -30.]), cfg)
        z, q = extract_measurement(received, cfg)
        self.assertEqual(z.shape, (10,)); self.assertGreaterEqual(len(q["candidates"]), 3)
        self.assertAlmostEqual(q["candidates"][0]["score_ratio"], 1.0, places=5)
        for i, left in enumerate(q["candidates"]):
            self.assertTrue(np.all(np.isfinite(left["direction"])))
            for right in q["candidates"][i + 1:]:
                angle = np.degrees(np.arccos(np.clip(left["direction"] @ right["direction"], -1., 1.)))
                self.assertGreater(angle, 5.0)


if __name__ == "__main__": unittest.main()
