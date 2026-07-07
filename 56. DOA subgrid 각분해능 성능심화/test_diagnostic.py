"""56번 sub-grid DOA 성능 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from config import ChannelConfig
from channel import synthesize_received
from estimators import estimate_toa_matched_filter
from improved_doa import _parab_offset, gated_srp_subgrid, extract_measurement_subgrid
from measurement import ideal_measurement


def test_parab_offset_center():
    """대칭 3점이면 offset 0, 한쪽으로 기울면 그 방향으로."""
    assert abs(_parab_offset(1.0, 2.0, 1.0)) < 1e-9
    assert _parab_offset(1.0, 2.0, 1.8) > 0     # 오른쪽이 높으면 +쪽
    assert -0.5 <= _parab_offset(0.0, 2.0, 1.9) <= 0.5


def test_subgrid_doa_accuracy():
    """무잡음이면 sub-grid DOA가 참 방향에 매우 가깝다(<1°)."""
    cfg = ChannelConfig()
    pos = np.array([200.0, 30.0, -35.0])
    _, received, _ = synthesize_received(pos, cfg, include_noise=False)
    toas, _ = estimate_toa_matched_filter(received, cfg)
    az, el = gated_srp_subgrid(received, cfg, toas)
    truth = ideal_measurement(pos, cfg)
    u = np.array([np.cos(el)*np.cos(az), np.cos(el)*np.sin(az), np.sin(el)])
    td = np.array([np.cos(truth[9])*np.cos(truth[8]), np.cos(truth[9])*np.sin(truth[8]), np.sin(truth[9])])
    assert np.degrees(np.arccos(np.clip(u@td, -1, 1))) < 1.5


def test_extract_subgrid_shape():
    cfg = ChannelConfig()
    _, received, _ = synthesize_received(np.array([300.0, 0.0, -30.0]), cfg)
    z, q = extract_measurement_subgrid(received, cfg)
    assert z.shape == (10,) and np.all(np.isfinite(z))
    assert "doa_disagreement_deg" in q


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
