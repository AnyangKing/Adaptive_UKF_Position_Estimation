import unittest
import numpy as np

from measurement import ideal_measurement
from config import ChannelConfig


class SRPMeasurementTests(unittest.TestCase):
    def test_measurement_angle_slots(self):
        z=ideal_measurement(np.array([100.0,20.0,-20.0]),ChannelConfig())
        self.assertEqual(z.shape,(10,)); self.assertTrue(np.all(np.isfinite(z)))


if __name__=="__main__": unittest.main(verbosity=2)
