"""Fast protocol tests for folder 159."""

import numpy as np

from run_reduced_schedule_pilot import (
    GEOMS,
    SETTLE_START,
    STEPS,
    SCHEDULES,
    geometry,
    lag1,
)


def test_schedule_contract():
    assert GEOMS == 4
    assert 0 < SETTLE_START < STEPS == 20
    assert set(SCHEDULES) == {
        "fixed32",
        "linear20_30_34",
        "random20_30_34_seeded",
        "four_carrier_cycle",
    }
    assert all(len(values) == STEPS for values in SCHEDULES.values())
    assert np.array_equal(
        np.sort(SCHEDULES["linear20_30_34"]),
        np.sort(SCHEDULES["random20_30_34_seeded"]),
    )
    assert not np.array_equal(
        SCHEDULES["linear20_30_34"],
        SCHEDULES["random20_30_34_seeded"],
    )


def test_geometries_are_static_and_at_600_m():
    for index in range(GEOMS):
        position, environment = geometry(index)
        assert abs(np.hypot(position[0], position[1]) - 600.0) < 1.0e-9
        assert environment["radial_velocity_m_s"] == 0.0


def test_lag1_contract():
    assert lag1([1.0, 1.0, 1.0]) is None
    assert lag1([1.0, 2.0, 3.0, 4.0]) > 0.99


if __name__ == "__main__":
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
            print(f"PASS {name}")
    print("all tests passed")
