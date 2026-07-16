"""Diagnostic tests for preregistered schedule definitions."""

import numpy as np

from run_stage0_schedule_prescreen import SCHEDULES, STEPS


def main() -> None:
    assert len(SCHEDULES) == 8
    assert all(values.shape == (STEPS,) for values in SCHEDULES.values())
    assert np.all(SCHEDULES["fixed32"] == 32.0)
    assert np.isclose(SCHEDULES["linear20_30_34"].min(), 30.0)
    assert np.isclose(SCHEDULES["linear20_30_34"].max(), 34.0)
    assert np.isclose(SCHEDULES["narrow_linear20_31_33"].min(), 31.0)
    assert np.isclose(SCHEDULES["narrow_linear20_31_33"].max(), 33.0)
    assert np.isclose(SCHEDULES["wide_linear20_28_36"].min(), 28.0)
    assert np.isclose(SCHEDULES["wide_linear20_28_36"].max(), 36.0)
    assert set(np.unique(SCHEDULES["two_extreme_alternating"])) == {30.0, 34.0}
    assert np.sum(SCHEDULES["fixed3_hop1_static"] != 32.0) == 5
    assert np.allclose(
        np.sort(SCHEDULES["random20_30_34_seeded"]),
        np.sort(SCHEDULES["linear20_30_34"]),
    )
    print("ok")


if __name__ == "__main__":
    main()
