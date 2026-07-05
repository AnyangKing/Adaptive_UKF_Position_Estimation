import unittest
import numpy as np
from soft_path_update import _cubature_points, _assignment_loglikes


class SoftPathUpdateTest(unittest.TestCase):
    def test_positive_cubature_reproduces_moments(self):
        mean=np.arange(6,dtype=float); covariance=np.diag(np.arange(1,7,dtype=float))
        points=_cubature_points(mean,covariance); weights=np.full(12,1/12)
        self.assertTrue(np.allclose(weights@points,mean))
        difference=points-mean
        self.assertTrue(np.allclose(np.einsum('i,ij,ik->jk',weights,difference,difference),covariance))

    def test_assignment_likelihood_is_finite(self):
        values=_assignment_loglikes(np.array([1.,1.002,1.006]),np.ones(3),np.array([0.,.002,.006]),5e-4,.5)
        self.assertTrue(np.any(np.isfinite(values)))

    def test_uniform_weights_do_not_inflate_covariance(self):
        mean=np.zeros(6); covariance=np.diag([2.,3.,4.,5.,6.,7.])
        points=_cubature_points(mean,covariance); weights=np.full(12,1/12)
        posterior=weights@points; difference=points-posterior
        recovered=np.einsum('i,ij,ik->jk',weights,difference,difference)
        self.assertTrue(np.allclose(recovered,covariance))

    def test_mixture_covariance_is_positive(self):
        prior=np.eye(2); raw=np.diag([.5,2.]); delta=np.array([2.,-1.]); blend=.25
        mixed=(1-blend)*prior+blend*raw+blend*(1-blend)*np.outer(delta,delta)
        self.assertGreater(np.min(np.linalg.eigvalsh(mixed)),0.)


if __name__=='__main__': unittest.main()
