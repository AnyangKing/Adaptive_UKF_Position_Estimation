import unittest
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from estimators import estimate_toa_tracked


class TrackingTests(unittest.TestCase):
    def test_first_ping_and_repeat(self):
        cfg=ChannelConfig(seed=1); source=np.array([200.0,30.0,-25.0])
        _,received,_=synthesize_received(source,cfg)
        first,_,fallback=estimate_toa_tracked(received,cfg,None)
        second,_,_=estimate_toa_tracked(received,cfg,first)
        self.assertEqual(first.shape,(8,)); self.assertFalse(np.any(fallback))
        np.testing.assert_allclose(second,first,atol=1e-12)


if __name__=="__main__": unittest.main(verbosity=2)
