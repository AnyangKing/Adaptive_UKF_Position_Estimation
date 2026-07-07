"""SRP-PHAT DOA를 0.2° 격자 argmax에서 sub-grid 포물선 보간으로 개선한다.

지금까지 모든 폴더가 "편향은 gated SRP 격자(0.2°)로 하한 추정"이라 적었듯, 0.2° 격자가 각 정밀도를
깎는다. 여기서는 fine 격자 score 표면에서 peak 주변 3점을 az·el 각각 포물선 보간해 sub-grid
방향을 얻는다(양자화 성분 저감). 채택 관측(직접파 창 gated SRP)과 동일한 창·격자를 쓰되 argmax를
보간으로 대체한다. novelty가 아니라 순수 성능 심화다.
"""

from __future__ import annotations

import numpy as np

from estimators import (_direction_grid, _srp_scores, estimate_gcc_phat_doa,
                        estimate_toa_matched_filter, pair_delays_to_reference_tdoa)
from peak_measurement import crop_direct


def _parab_offset(y1, y2, y3):
    """3점 포물선 정점의 격자 offset ∈ [-0.5, 0.5] (y2가 중앙 peak)."""
    denom = y1 - 2.0*y2 + y3
    if abs(denom) < 1e-12:
        return 0.0
    return float(np.clip(0.5*(y1 - y3)/denom, -0.5, 0.5))


def gated_srp_subgrid(received, cfg, toas, window_s=0.005, fine_step=0.2):
    """직접파 창 gated SRP를 coarse→fine→sub-grid 보간해 (az, el) 반환."""
    cropped = crop_direct(received, cfg, toas)
    coarse_dirs, caz, cel = _direction_grid(np.arange(-180.0, 180.0, 2.0),
                                            np.arange(-80.0, 82.0, 2.0))
    cscores = _srp_scores(cropped, coarse_dirs, cfg)
    best = int(np.argmax(cscores))
    center_az = np.degrees(caz[best]); center_el = np.degrees(cel[best])
    az_axis = np.arange(center_az - 2.0, center_az + 2.0 + 1e-9, fine_step)
    el_axis = np.arange(max(-89.0, center_el - 2.0), min(89.0, center_el + 2.0) + 1e-9, fine_step)
    fine_dirs, _, _ = _direction_grid(az_axis, el_axis)
    scores = _srp_scores(cropped, fine_dirs, cfg).reshape(len(el_axis), len(az_axis))
    ei, ai = np.unravel_index(int(np.argmax(scores)), scores.shape)
    daz = _parab_offset(scores[ei, ai-1], scores[ei, ai], scores[ei, ai+1]) if 0 < ai < len(az_axis)-1 else 0.0
    dele = _parab_offset(scores[ei-1, ai], scores[ei, ai], scores[ei+1, ai]) if 0 < ei < len(el_axis)-1 else 0.0
    az = np.radians(az_axis[ai] + daz*fine_step)
    el = np.radians(el_axis[ei] + dele*fine_step)
    return float(az), float(el)


def extract_measurement_subgrid(received, cfg):
    """extract_measurement과 동일 관측이되 DOA만 sub-grid 보간으로 정밀화."""
    toas, peak_quality = estimate_toa_matched_filter(received, cfg)
    gcc_az, gcc_el, gcc_direction, pair_delays = estimate_gcc_phat_doa(received, cfg)
    srp_az, srp_el = gated_srp_subgrid(received, cfg, toas)
    tdoa = pair_delays_to_reference_tdoa(pair_delays)
    srp_dir = np.array([np.cos(srp_el)*np.cos(srp_az), np.cos(srp_el)*np.sin(srp_az), np.sin(srp_el)])
    disagreement = float(np.degrees(np.arccos(np.clip(gcc_direction @ srp_dir, -1, 1))))
    z = np.r_[cfg.sound_speed_m_s*toas[0], cfg.sound_speed_m_s*tdoa, srp_az, srp_el]
    quality = {"doa_disagreement_deg": disagreement, "minimum_peak_quality": float(np.min(peak_quality))}
    return z, quality
