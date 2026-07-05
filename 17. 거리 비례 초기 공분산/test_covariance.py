import unittest
import numpy as np

from config import ChannelConfig
from run_compare import geometry_position_covariance


class CovarianceTests(unittest.TestCase):
    def test_spd_and_distance_scaling(self):
        cfg=ChannelConfig(); near=geometry_position_covariance(np.array([100.,0.,-30.]),cfg)
        far=geometry_position_covariance(np.array([600.,0.,-30.]),cfg)
        self.assertTrue(np.all(np.linalg.eigvalsh(near)>0)); self.assertTrue(np.all(np.linalg.eigvalsh(far)>0))
        self.assertGreater(np.trace(far),np.trace(near))
        self.assertAlmostEqual(float(near[0,0]),9.0,places=6)


if __name__=="__main__": unittest.main(verbosity=2)
