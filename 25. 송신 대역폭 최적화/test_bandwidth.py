import unittest

from dataclasses import replace
from channel import make_probe
from config import ChannelConfig


class BandwidthTests(unittest.TestCase):
    def test_probe_lengths_equal(self):
        lengths=[len(make_probe(replace(ChannelConfig(),chirp_bandwidth_hz=b))) for b in (8000.,12000.,20000.,30000.)]
        self.assertEqual(len(set(lengths)),1)


if __name__=="__main__": unittest.main(verbosity=2)
