"""48번 강건성 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from robustness import collect_mismatched, run_routing_rmse, ASSUMED_C
from trajectory import STEPS


def test_matched_case_runs():
    rec = collect_mismatched(200, 0, "test", c_true=ASSUMED_C)
    assert rec["observations"].shape == (STEPS, 10)
    rmse, div = run_routing_rmse(rec)
    assert np.isfinite(rmse) and rmse >= 0.0


def test_clock_offset_shifts_toa():
    """클럭 오프셋은 절대 TOA(z[0])만 c_assumed·offset 만큼 옮긴다."""
    base = collect_mismatched(200, 0, "test", c_true=ASSUMED_C, clock_offset_s=0.0)
    off = collect_mismatched(200, 0, "test", c_true=ASSUMED_C, clock_offset_s=0.001)
    d0 = off["observations"][:, 0] - base["observations"][:, 0]
    assert np.allclose(d0, ASSUMED_C * 0.001, atol=1e-6)
    # 나머지 관측 성분은 불변
    assert np.allclose(off["observations"][:, 1:], base["observations"][:, 1:])


def test_sound_speed_mismatch_changes_observations():
    base = collect_mismatched(400, 0, "test", c_true=1500.0)
    fast = collect_mismatched(400, 0, "test", c_true=1530.0)
    # 음속이 다르면 도달지연이 달라져 관측이 바뀐다.
    assert not np.allclose(base["observations"], fast["observations"])


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
