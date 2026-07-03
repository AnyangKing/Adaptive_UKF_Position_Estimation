import unittest
import numpy as np

from calibration import estimate_calibration


class CalibrationTests(unittest.TestCase):
    def test_small_calibration_is_spd(self):
        bias,R,residuals=estimate_calibration(0.005,count=12)
        self.assertEqual(bias.shape,(10,)); self.assertEqual(R.shape,(10,10))
        self.assertEqual(residuals.shape,(12,10))
        self.assertTrue(np.all(np.linalg.eigvalsh(R)>0))
        np.testing.assert_allclose(R,R.T,atol=1e-12)


if __name__=="__main__": unittest.main(verbosity=2)
