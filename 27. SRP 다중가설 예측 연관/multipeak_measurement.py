"""5 ms 직접파 창에서 분리된 SRP 방향 가설들을 추출한다."""

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


def separated_srp_candidates(received, cfg, toas, count=5, exclusion_deg=10.0):
    cropped = crop_direct(received, cfg, toas)
    directions, azimuth, elevation = _direction_grid(
        np.arange(-180.0, 180.0, 2.0), np.arange(-80.0, 82.0, 2.0)
    )
    scores = _srp_scores(cropped, directions, cfg)
    available = np.ones(len(scores), dtype=bool); coarse = []
    for _ in range(count):
        valid = np.flatnonzero(available)
        if not len(valid):
            break
        index = int(valid[np.argmax(scores[valid])]); coarse.append(index)
        available &= (directions @ directions[index]) < np.cos(np.radians(exclusion_deg))

    candidates = []
    for index in coarse:
        center_az = np.degrees(azimuth[index]); center_el = np.degrees(elevation[index])
        fine_directions, fine_az, fine_el = _direction_grid(
            np.arange(center_az - 2.0, center_az + 2.01, 0.2),
            np.arange(max(-89.0, center_el - 2.0), min(89.0, center_el + 2.0) + 0.01, 0.2),
        )
        fine_scores = _srp_scores(cropped, fine_directions, cfg)
        best = int(np.argmax(fine_scores)); score = float(fine_scores[best])
        candidates.append({
            "azimuth_rad": float(fine_az[best]), "elevation_rad": float(fine_el[best]),
            "direction": fine_directions[best], "score": score,
        })
    top_score = candidates[0]["score"]
    for candidate in candidates:
        candidate["score_ratio"] = float(candidate["score"] / (abs(top_score) + 1.0e-12))
    return candidates


def extract_measurement(received, cfg):
    toas, peak_quality = estimate_toa_matched_filter(received, cfg)
    gcc_az, gcc_el, gcc_direction, pair_delays = estimate_gcc_phat_doa(received, cfg)
    candidates = separated_srp_candidates(received, cfg, toas)
    first = candidates[0]; tdoa = pair_delays_to_reference_tdoa(pair_delays)
    disagreement = float(np.degrees(np.arccos(np.clip(gcc_direction @ first["direction"], -1.0, 1.0))))
    z = np.r_[cfg.sound_speed_m_s * toas[0], cfg.sound_speed_m_s * tdoa,
              first["azimuth_rad"], first["elevation_rad"]]
    quality = {"candidates": candidates, "doa_disagreement_deg": disagreement,
               "minimum_peak_quality": float(np.min(peak_quality)),
               "gcc_azimuth_rad": float(gcc_az), "gcc_elevation_rad": float(gcc_el)}
    return z, quality
