import unittest
import numpy as np

from run_convergence import sustained_below


class ConvergenceTests(unittest.TestCase):
    def test_sustained_detector(self):
        self.assertEqual(sustained_below(np.array([9,4,4,4,4,4,8.])),1)
        self.assertIsNone(sustained_below(np.array([4,4,8,4,4,4,4.])))


if __name__=="__main__": unittest.main(verbosity=2)
