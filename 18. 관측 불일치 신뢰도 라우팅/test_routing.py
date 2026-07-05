import unittest
import numpy as np

from routed_adaptive import RoutedAdaptiveRUKF


class RoutingTests(unittest.TestCase):
    def test_scale_formula_bounds(self):
        for disagreement in (0.,2.,20.,100.):
            scale=min(100.,1.+(disagreement/2.)**2)
            self.assertGreaterEqual(scale,1.); self.assertLessEqual(scale,100.)


if __name__=="__main__": unittest.main(verbosity=2)
