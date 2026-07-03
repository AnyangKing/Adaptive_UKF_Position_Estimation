import unittest
import numpy as np

from bias_model import features,predict


class BiasModelTests(unittest.TestCase):
    def test_feature_and_prediction_shapes(self):
        ranges=np.array([100.,200.]); measured=np.array([[0.1,0.2],[0.2,-0.1]])
        self.assertEqual(features(ranges,measured).shape,(2,4))
        constant=predict("constant",np.array([0.01,-0.02]),ranges,measured)
        self.assertEqual(constant.shape,(2,2)); self.assertTrue(np.all(np.isfinite(constant)))


if __name__=="__main__": unittest.main(verbosity=2)
