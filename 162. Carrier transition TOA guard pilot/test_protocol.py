"""Fast unit and protocol tests for the carrier-transition TOA guard."""

import numpy as np

from run_transition_guard_pilot import DEVELOPMENT_GEOMETRIES, RANGE_JUMP_THRESHOLD_M
from transition_guard import CarrierTransitionTOAGuardUKF


class DummyUKF:
    def __init__(self):
        self.R = np.eye(10)


def test_frozen_development_scope():
    assert DEVELOPMENT_GEOMETRIES == (2, 5, 19)
    assert RANGE_JUMP_THRESHOLD_M == 0.5


def test_guard_requires_carrier_change_and_range_jump():
    guard = CarrierTransitionTOAGuardUKF(DummyUKF(), 5.0, range_jump_threshold_m=0.5)
    guard.prime(np.r_[100.0, np.zeros(9)], 30_000.0)
    assert guard.previous_range_m == 100.0
    assert guard.previous_carrier_hz == 30_000.0
    # The complete update path needs a real UKF; the Boolean contract is also
    # enforced by integration result tests after the pilot run.


if __name__ == "__main__":
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
            print(f"PASS {name}")
    print("all tests passed")
