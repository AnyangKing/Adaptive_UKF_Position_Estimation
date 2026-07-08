import numpy as np

from config import ChannelConfig
from run_motion_aware_schedule import (
    CONDITION_AWARE_RULE,
    CONDITIONS,
    DISTANCE,
    FIXED_CARRIER_HZ,
    GEOMS,
    HOP_BANK_HZ,
    POLICIES,
    SETTLE_START,
    STEPS,
    schedule_for,
)


def test_frozen_experiment_design():
    assert DISTANCE == 600.0
    assert GEOMS == 8
    assert STEPS == 16
    assert SETTLE_START == 8
    assert [c[0] for c in CONDITIONS] == [
        "radial_0.05",
        "radial_1.0",
        "tangential_1.0",
        "tang_1.0_vz",
    ]
    assert set(POLICIES) == {"fixed", "hop_always", "fixed3_hop1", "fixed4_hop1", "condition_aware"}


def test_condition_aware_rule_is_66_oracle():
    assert CONDITION_AWARE_RULE == {
        "radial_0.05": "fixed",
        "radial_1.0": "hop_always",
        "tangential_1.0": "fixed4_hop1",
        "tang_1.0_vz": "fixed3_hop1",
    }
    for condition, base in CONDITION_AWARE_RULE.items():
        assert np.allclose(schedule_for("condition_aware", condition), schedule_for(base, condition))


def test_carriers_are_in_band():
    cfg = ChannelConfig()
    half_bw = cfg.chirp_bandwidth_hz / 2.0
    assert FIXED_CARRIER_HZ == 32000.0
    assert HOP_BANK_HZ.min() - half_bw > 0.0
    assert HOP_BANK_HZ.max() + half_bw < cfg.sample_rate_hz / 2.0
    for condition, *_ in CONDITIONS:
        for policy in POLICIES:
            carriers = schedule_for(policy, condition)
            assert carriers.shape == (STEPS,)
            assert carriers.min() - half_bw > 0.0
            assert carriers.max() + half_bw < cfg.sample_rate_hz / 2.0


if __name__ == "__main__":
    test_frozen_experiment_design()
    test_condition_aware_rule_is_66_oracle()
    test_carriers_are_in_band()
    print("diagnostic tests passed")
