import unittest
import numpy as np

from run_waveform_sweep import run


class WaveformSweepTests(unittest.TestCase):
    def test_sweep(self):
        result=run()
        self.assertEqual(set(result),{"1ms","2ms","5ms","10ms"})
        for metrics in result.values():
            self.assertTrue(np.all(np.isfinite(list(metrics.values()))))
        self.assertLessEqual(result["1ms"]["mean_direct_surface_overlap_fraction"],
                             result["10ms"]["mean_direct_surface_overlap_fraction"])


if __name__=="__main__": unittest.main(verbosity=2)
