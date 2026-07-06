"""46번 대규모 MC 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

import trajectory as tj
from config import ChannelConfig
from run_montecarlo import _run, _bootstrap_ci, TRIALS


def test_trials_scaled_up():
    assert TRIALS >= 40


def test_run_both_modes():
    cfg = ChannelConfig()
    rec = tj.collect_trajectory(200, 0, "test")
    p_rmse, p_div, p_c = _run(rec, cfg, routing=False)
    r_rmse, r_div, r_c = _run(rec, cfg, routing=True)
    assert np.isfinite(p_rmse) and np.isfinite(r_rmse)
    assert "mean_nees" in p_c and "mean_nees" in r_c


def test_bootstrap_ci_orders():
    diffs = np.array([0.5, 1.0, -0.2, 2.0, 0.3, 1.5, 0.8, -0.1])
    lo, hi = _bootstrap_ci(diffs)
    assert lo <= np.mean(diffs) <= hi


def test_high_trial_seeds_distinct():
    """40 trial까지 궤적 시작점이 서로 다르다(seed 충돌 없음)."""
    starts = [tj.scenario(400, t, "test")[0] for t in range(40)]
    starts = np.array(starts)
    # 모든 쌍이 최소 몇 m 이상 떨어져 있다(방위·깊이 랜덤).
    assert len(np.unique(np.round(starts, 3), axis=0)) == 40


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
