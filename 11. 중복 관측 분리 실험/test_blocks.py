import unittest
import numpy as np

from run_compare import covariance_for


class BlockTests(unittest.TestCase):
    def test_disabled_blocks_remain_spd(self):
        for args in [(False,True,True),(True,False,True),(True,True,False)]:
            R=covariance_for(*args)
            self.assertTrue(np.all(np.linalg.eigvalsh(R)>0))
            np.testing.assert_allclose(R,R.T,atol=1e-12)


if __name__=="__main__": unittest.main(verbosity=2)
