import unittest
import numpy as np

from best_measurement import extract_best_measurement
from channel import synthesize_received
from config import ChannelConfig


class BestMeasurementTests(unittest.TestCase):
    def test_dimensions_and_finite(self):
        cfg=ChannelConfig(seed=1); _,received,_=synthesize_received(np.array([100.,20.,-30.]),cfg)
        z,q=extract_best_measurement(received,cfg)
        self.assertEqual(z.shape,(10,)); self.assertTrue(np.all(np.isfinite(z)))
        self.assertTrue(np.isfinite(q["doa_disagreement_deg"]))


if __name__=="__main__": unittest.main(verbosity=2)
