import unittest
import numpy as np

from absolute_measurement import ideal_measurement,measurement_covariance
from config import ChannelConfig


class AbsoluteTests(unittest.TestCase):
    def test_dimensions_and_spd(self):
        cfg=ChannelConfig(); z=ideal_measurement(np.array([100.,20.,-40.]),cfg); R=measurement_covariance()
        self.assertEqual(z.shape,(10,)); self.assertEqual(R.shape,(10,10))
        self.assertTrue(np.all(np.linalg.eigvalsh(R)>0))


if __name__=="__main__": unittest.main(verbosity=2)
