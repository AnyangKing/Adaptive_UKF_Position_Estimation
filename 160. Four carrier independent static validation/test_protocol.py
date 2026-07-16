"""Frozen protocol checks for folder 160; these do not run signal synthesis."""

import numpy as np

from run_independent_schedule_validation import (
    GEOMS,
    GEOM_ROOT,
    PING_ROOT,
    SETTLE_START,
    STEPS,
    SCHEDULES,
    geometry,
)


def test_independent_sample_contract():
    assert GEOMS == 20
    assert GEOM_ROOT == 1_600_000 and PING_ROOT == 1_603_000
    assert 0 < SETTLE_START < STEPS == 20
    assert set(SCHEDULES) == {"fixed32", "linear20_30_34", "four_carrier_cycle"}


def test_candidate_is_frozen_four_carrier_cycle():
    expected = np.resize(np.array([30_000.0, 31_333.333333, 32_666.666667, 34_000.0]), 20)
    assert np.allclose(SCHEDULES["four_carrier_cycle"], expected)
    assert np.allclose(SCHEDULES["linear20_30_34"], np.linspace(30_000.0, 34_000.0, 20))


def test_geometries_are_static_600_m():
    for index in range(GEOMS):
        position, environment = geometry(index)
        assert abs(np.hypot(position[0], position[1]) - 600.0) < 1.0e-9
        assert environment["radial_velocity_m_s"] == 0.0


if __name__ == "__main__":
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
            print(f"PASS {name}")
    print("all tests passed")
