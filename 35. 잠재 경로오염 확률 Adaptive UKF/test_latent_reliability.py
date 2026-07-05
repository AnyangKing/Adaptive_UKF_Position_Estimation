import unittest
import numpy as np
from config import ChannelConfig
from latent_reliability import physical_residual_score


class LatentReliabilityTest(unittest.TestCase):
    def test_matching_pattern_has_small_score(self):
        cfg=ChannelConfig(); position=np.array([100.,20.,-45.])
        from channel import paths_for_sensor
        from config import usb_array_global_m
        paths=paths_for_sensor(position,usb_array_global_m(cfg.receiver_depth_m)[0],cfg)
        times=np.array([p.delay_s for p in paths]); score=physical_residual_score(position,times,np.ones(3),cfg)
        self.assertLess(score,1e-8)


if __name__=='__main__': unittest.main()
