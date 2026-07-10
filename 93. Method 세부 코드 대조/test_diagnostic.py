"""93번 method-facts 추출기의 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

from extract_method_facts import extract

FACTS = extract()


def test_channel_and_array():
    c = FACTS["channel"]; a = FACTS["array"]
    assert c["sample_rate_hz"] == 192000.0 and c["carrier_hz_default"] == 32000.0
    assert c["chirp_bandwidth_hz"] == 12000.0 and c["pulse_duration_s"] == 0.01
    assert c["realism_flags_present"] is False        # 61은 canonical 채널
    assert a["ring_radius_m"] == 0.033 and a["ring_vertical_offset_m"] == 0.079


def test_gate_and_filter():
    assert FACTS["gating"]["direct_gate_window_s"] == 0.005
    assert FACTS["ukf"]["alpha"] == 0.3 and FACTS["ukf"]["beta"] == 2.0
    assert FACTS["filter_init"]["accel_process_std_m_s2"] == 0.2
    assert FACTS["fixed_R"]["doa_std_deg"] == 2.0


def test_adaptive_R_rule():
    ar = FACTS["adaptive_R_actual"]
    assert ar["threshold_deg"] == 5.0
    assert ar["nis_limits_chi2_99"] == [6.63, 18.48, 9.21]


def test_protocols():
    p61 = FACTS["protocol_61_static"]
    assert p61["geoms_per_distance"] == 20 and p61["steps"] == 20 and p61["settle_start"] == 10
    p63 = FACTS["protocol_63_moving"]
    assert p63["total_trials"] == 64 and p63["distance_m"] == 600.0
    p82 = FACTS["protocol_82_quasistatic"]
    assert p82["total_paired_trials"] == 132
    assert len(p82["speeds_m_s"]) == 6 and p82["motion_modes"] == ["radial", "tangential"]


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
