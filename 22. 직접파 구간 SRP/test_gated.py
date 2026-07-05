import unittest
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from gated_srp import crop_direct_arrival


class GatedTests(unittest.TestCase):
    def test_crop_is_shorter(self):
        cfg=ChannelConfig(seed=1); _,received,_=synthesize_received(np.array([100.,20.,-30.]),cfg)
        cropped,toas=crop_direct_arrival(received,cfg,0.002)
        self.assertEqual(cropped.shape[0],8); self.assertLess(cropped.shape[1],received.shape[1]); self.assertEqual(toas.shape,(8,))


if __name__=="__main__": unittest.main(verbosity=2)
