import unittest
import numpy as np

from run_compare import run


class AdaptiveTests(unittest.TestCase):
    def test_fixed_and_adaptive_pipeline(self):
        result = run()
        values = list(result["fixed"].values()) + list(result["adaptive"].values())
        self.assertTrue(np.all(np.isfinite(values)))
        self.assertGreaterEqual(result["doa_gate_activation_rate"], 0.0)
        self.assertLessEqual(result["doa_gate_activation_rate"], 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
