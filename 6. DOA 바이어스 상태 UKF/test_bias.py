import unittest
import numpy as np

from bias_ukf import bias_process_covariance
from run_compare import run


class BiasUKFTests(unittest.TestCase):
    def test_process_covariance(self):
        q=bias_process_covariance()
        self.assertEqual(q.shape,(8,8))
        self.assertTrue(np.all(np.linalg.eigvalsh(q)>=-1e-12))

    def test_comparison(self):
        result=run()
        values=list(result["six_state_adaptive"].values())+list(result["eight_state_bias"].values())
        self.assertTrue(np.all(np.isfinite(values)))


if __name__=="__main__": unittest.main(verbosity=2)
