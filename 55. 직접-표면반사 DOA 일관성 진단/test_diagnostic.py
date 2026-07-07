"""55번 반사 DOA 일관성 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from reflected_doa import reflected_arrival_time, reflected_srp_doa
from run_consistency import geometry, measure


def test_reflected_after_direct():
    """반사 도착시각이 양수이고 직접파 이후다(가장 이른 도착보다 늦음)."""
    cfg = replace(ChannelConfig(), second_order_multipath=True, seed=3)
    _, received, _ = synthesize_received(np.array([300.0, 20.0, -40.0]), cfg)
    from path_identifiability import observed_peaks
    times, _ = observed_peaks(received[0], cfg, maximum=6)
    t_refl = reflected_arrival_time(received[0], cfg)
    assert t_refl >= float(np.min(times)) and t_refl > 0.0


def test_reflected_doa_runs():
    cfg = replace(ChannelConfig(), second_order_multipath=True, surface_roughness=0.3, seed=5)
    _, received, _ = synthesize_received(np.array([250.0, 10.0, -35.0]), cfg)
    az, el = reflected_srp_doa(received, cfg)
    assert np.isfinite(az) and np.isfinite(el)
    assert -np.pi <= az <= np.pi and -np.pi/2 <= el <= np.pi/2


def test_measure_row_fields():
    pos, env, depth = geometry(200, 0)
    row = measure(pos, env, 200, 0)
    for k in ("el_direct_deg", "el_reflected_deg", "el_true_deg", "el_bias_deg",
              "direct_reflected_gap_deg"):
        assert k in row and np.isfinite(row[k])


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
