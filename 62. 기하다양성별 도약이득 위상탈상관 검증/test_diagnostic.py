"""62번 위상탈상관 스윕 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from run_motion_sweep import (CONDITIONS, DISTANCE, STEPS, geometry,
                              phase_swing_cycles, truth_trajectory)


def test_conditions_cover_design():
    names = [c[0] for c in CONDITIONS]
    assert "static" in names and "tangential_1.0" in names and "tang_1.0_vz" in names
    assert sum(1 for c in CONDITIONS if c[2] == "radial") == 3


def test_static_and_tangential_phase_near_zero():
    """핵심 예측: 정지·등거리 선회(vz=0)는 위상 스윙 ≈ 0."""
    pos, env, az, sign = geometry(0, 0)
    t_static = truth_trajectory(pos, az, sign, 0.0, "none", 0.0)
    t_tang = truth_trajectory(pos, az, sign, 1.0, "tangential", 0.0)
    assert phase_swing_cycles(t_static, env) < 0.02
    assert phase_swing_cycles(t_tang, env) < 0.15      # 곡률 없는 직선 접선이라 미세 변화만
    # 접선 궤적은 수평거리가 거의 불변
    r = np.hypot(t_tang[:, 0], t_tang[:, 1])
    assert np.max(np.abs(r - DISTANCE)) < 0.5


def test_vz_and_radial_rotate_phase():
    """vz·radial 운동은 위상을 여러 사이클 돌린다."""
    pos, env, az, sign = geometry(5, 0)
    t_vz = truth_trajectory(pos, az, sign, 1.0, "tangential", 0.08)
    t_rad = truth_trajectory(pos, az, sign, 1.0, "radial", 0.0)
    assert phase_swing_cycles(t_vz, env) > 1.0
    assert phase_swing_cycles(t_rad, env) > 1.0


def test_trajectory_shapes():
    pos, env, az, sign = geometry(2, 1)
    t = truth_trajectory(pos, az, sign, 0.2, "radial", 0.0)
    assert t.shape == (STEPS, 3)
    assert np.allclose(t[0], pos)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
