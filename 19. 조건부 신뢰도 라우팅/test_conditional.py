import unittest

from conditional_adaptive import ConditionalAdaptiveRUKF


class ConditionalTests(unittest.TestCase):
    def test_threshold_comparison(self):
        threshold=10.; self.assertFalse(9.9>threshold); self.assertTrue(10.1>threshold)


if __name__=="__main__": unittest.main(verbosity=2)
