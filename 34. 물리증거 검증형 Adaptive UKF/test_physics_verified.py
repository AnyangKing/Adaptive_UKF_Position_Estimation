import unittest
import numpy as np
from config import ChannelConfig
from measurement import fixed_measurement_covariance
from physics_verified import PhysicsVerifiedAdaptiveUKF
from ukf import SignalObservationUKF,acceleration_process_covariance


class PhysicsVerifiedTest(unittest.TestCase):
    def test_wrapper_constructs(self):
        cfg=ChannelConfig(); ukf=SignalObservationUKF(np.zeros(6),np.eye(6),
            acceleration_process_covariance(1.,.2),fixed_measurement_covariance(),cfg)
        wrapper=PhysicsVerifiedAdaptiveUKF(ukf,cfg,1.,4.)
        self.assertEqual(wrapper.base_R.shape,(10,10))


if __name__=='__main__': unittest.main()
