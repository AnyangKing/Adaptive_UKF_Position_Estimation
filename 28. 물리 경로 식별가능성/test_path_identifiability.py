import unittest
import numpy as np
from config import ChannelConfig
from path_identifiability import evaluate_scene


class PathIdentifiabilityTest(unittest.TestCase):
    def test_direct_path_is_detected_in_clean_scene(self):
        records = evaluate_scene(np.array([100.0, 20.0, -45.0]), ChannelConfig(seed=28001, snr_db=30.0))
        self.assertEqual(len(records), 8)
        self.assertGreaterEqual(sum(r["matched"]["direct"]["found"] for r in records), 7)


if __name__ == "__main__": unittest.main()
