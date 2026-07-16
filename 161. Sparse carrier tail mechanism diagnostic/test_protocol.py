"""Fast protocol checks for the post-validation diagnostic."""

from run_tail_diagnostic import (
    DIAGNOSTIC_GEOMETRIES,
    GEOM_ROOT,
    PING_ROOT,
    SCHEDULES,
    geometry,
)


def test_exact_replay_contract():
    assert DIAGNOSTIC_GEOMETRIES == (2, 5, 19)
    assert GEOM_ROOT == 1_600_000 and PING_ROOT == 1_603_000
    assert set(SCHEDULES) == {"fixed32", "linear20_30_34", "four_carrier_cycle"}


def test_replayed_geometry_environment():
    position, environment = geometry(2)
    assert abs(position[2] - -35.97884664510978) < 1.0e-9
    assert environment["snr_db"] == 20.0
    assert environment["radial_velocity_m_s"] == 0.0


if __name__ == "__main__":
    for name, function in sorted(globals().items()):
        if name.startswith("test_") and callable(function):
            function()
            print(f"PASS {name}")
    print("all tests passed")
