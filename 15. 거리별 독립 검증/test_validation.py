import unittest
import numpy as np

from run_distance_validation import FIXED_SRP_BIAS_RAD,make_trajectory


class ValidationTests(unittest.TestCase):
    def test_fixed_bias_and_trajectory(self):
        self.assertEqual(FIXED_SRP_BIAS_RAD.shape,(2,))
        trajectory=make_trajectory(100,0)
        self.assertEqual(trajectory.shape,(12,3)); self.assertTrue(np.all(np.isfinite(trajectory)))
        self.assertTrue(np.all((trajectory[:,2]<0)&(trajectory[:,2]>-100)))


if __name__=="__main__": unittest.main(verbosity=2)
