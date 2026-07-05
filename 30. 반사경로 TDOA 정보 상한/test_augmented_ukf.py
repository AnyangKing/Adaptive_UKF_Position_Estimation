import unittest
import numpy as np
from augmented_ukf import augmented_measurement
from config import ChannelConfig


class AugmentedMeasurementTest(unittest.TestCase):
    def test_shape_and_direct_limit(self):
        z=augmented_measurement(np.array([100.,20.,-45.]),ChannelConfig(),'all')
        self.assertEqual(z.shape,(26,)); self.assertTrue(np.all(z[10:]>0))


if __name__=='__main__': unittest.main()
