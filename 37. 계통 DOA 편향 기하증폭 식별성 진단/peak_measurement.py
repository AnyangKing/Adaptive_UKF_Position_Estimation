"""5 ms gated SRP의 분리된 1·2위 peak margin을 포함한 최선 관측 추출."""

import numpy as np

from estimators import (
    _direction_grid,
    _srp_scores,
    estimate_gcc_phat_doa,
    estimate_toa_matched_filter,
    pair_delays_to_reference_tdoa,
)


def crop_direct(received, cfg, toas, window_s=0.005, pre_s=0.0001):
    reference = float(np.min(toas))
    start = max(0, int(np.floor((reference - pre_s) * cfg.sample_rate_hz)))
    end = min(received.shape[1], int(np.ceil((reference + window_s) * cfg.sample_rate_hz)))
    return received[:, start:end]


def gated_srp_with_margin(received, cfg, toas, exclusion_deg=10.0):
    cropped = crop_direct(received, cfg, toas)
    directions, azimuth, elevation = _direction_grid(
        np.arange(-180.0, 180.0, 2.0), np.arange(-80.0, 82.0, 2.0)
    )
    scores = _srp_scores(cropped, directions, cfg)
    best = int(np.argmax(scores)); best_direction = directions[best]
    separated = (directions @ best_direction) < np.cos(np.radians(exclusion_deg))
    second_score = float(np.max(scores[separated])) if np.any(separated) else float(scores[best])
    best_score = float(scores[best])
    margin = max(0.0, (best_score - second_score) / (abs(best_score) + 1.0e-12))

    center_az = np.degrees(azimuth[best]); center_el = np.degrees(elevation[best])
    fine_directions, fine_az, fine_el = _direction_grid(
        np.arange(center_az - 2.0, center_az + 2.01, 0.2),
        np.arange(max(-89.0, center_el - 2.0), min(89.0, center_el + 2.0) + 0.01, 0.2),
    )
    fine_scores = _srp_scores(cropped, fine_directions, cfg); fine_best = int(np.argmax(fine_scores))
    return float(fine_az[fine_best]), float(fine_el[fine_best]), fine_directions[fine_best], {
        "peak_margin": float(margin), "best_score": best_score, "second_score": second_score
    }


def extract_measurement(received, cfg):
    toas, peak_quality = estimate_toa_matched_filter(received, cfg)
    gcc_az, gcc_el, gcc_direction, pair_delays = estimate_gcc_phat_doa(received, cfg)
    srp_az, srp_el, srp_direction, peak = gated_srp_with_margin(received, cfg, toas)
    tdoa = pair_delays_to_reference_tdoa(pair_delays)
    disagreement = float(np.degrees(np.arccos(np.clip(gcc_direction @ srp_direction, -1.0, 1.0))))
    z = np.r_[cfg.sound_speed_m_s * toas[0], cfg.sound_speed_m_s * tdoa, srp_az, srp_el]
    quality = {
        **peak,
        "doa_disagreement_deg": disagreement,
        "minimum_peak_quality": float(np.min(peak_quality)),
        "gcc_azimuth_rad": float(gcc_az),
        "gcc_elevation_rad": float(gcc_el),
    }
    return z, quality
