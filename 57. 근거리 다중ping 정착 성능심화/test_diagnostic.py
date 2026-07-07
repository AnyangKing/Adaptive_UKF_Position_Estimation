"""57번 다중 ping 정착 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from config import ChannelConfig
from run_settling import trajectory, run_trajectory, STEPS, WINDOWS


def test_trajectory_length():
    truth, meta = trajectory(100, 0)
    assert truth.shape == (STEPS, 3) and STEPS >= 30
    assert np.hypot(truth[0, 0], truth[0, 1]) > 50.0


def test_windows_defined():
    assert WINDOWS["after3"] == 3 and WINDOWS["steady_last5"] == STEPS-5


def test_run_trajectory_returns_windows():
    r = run_trajectory(100, 0, ChannelConfig())
    for name in WINDOWS:
        assert name in r and np.isfinite(r[name]) and r[name] >= 0.0


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
