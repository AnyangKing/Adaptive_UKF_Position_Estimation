import unittest
import numpy as np

from run_validation_test import averaged_initial_observation


class InitializationTests(unittest.TestCase):
    def test_wrap_safe_direction_average(self):
        z=np.zeros((2,10)); z[:,0]=100.; z[0,8]=np.radians(179); z[1,8]=np.radians(-179)
        result=averaged_initial_observation(z,2)
        self.assertGreater(abs(np.degrees(result[8])),170.)


if __name__=="__main__": unittest.main(verbosity=2)
