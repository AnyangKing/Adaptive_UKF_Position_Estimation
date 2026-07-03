import unittest
import numpy as np

from distance_bias import DISTANCES,predict


class DistanceBiasTests(unittest.TestCase):
    def test_piecewise_interpolation(self):
        model=np.column_stack((DISTANCES/1000,DISTANCES/2000))
        value=predict("piecewise",model,np.array([150.]))
        np.testing.assert_allclose(value,[[0.15,0.075]])
    def test_raw_zero(self):
        np.testing.assert_allclose(predict("raw",None,np.array([100.,200.])),0.)


if __name__=="__main__": unittest.main(verbosity=2)
