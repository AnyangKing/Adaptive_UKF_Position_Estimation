import unittest
import numpy as np

from run_compare import smooth_directions


class SmoothingTests(unittest.TestCase):
    def test_unit_norm_and_causality(self):
        raw=np.array([[1.,0,0],[0,1.,0],[0,0,1.]])
        output=smooth_directions(raw,0.5)
        np.testing.assert_allclose(np.linalg.norm(output,axis=1),1.0)
        np.testing.assert_allclose(output[0],raw[0])
        changed=raw.copy(); changed[2]=[0,0,-1]
        output_changed=smooth_directions(changed,0.5)
        np.testing.assert_allclose(output_changed[:2],output[:2])


if __name__=="__main__": unittest.main(verbosity=2)
