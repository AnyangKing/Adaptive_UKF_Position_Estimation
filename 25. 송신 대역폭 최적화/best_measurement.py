"""중복 full-SRP 계산 없이 현재 최선 10차원 관측을 추출한다."""

import numpy as np

from estimators import estimate_gcc_phat_doa,estimate_toa_matched_filter,pair_delays_to_reference_tdoa
from gated_srp import estimate_gated_srp


def _unit(az,el): return np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])


def extract_best_measurement(received,cfg,window_s=0.005):
    toas,peak_quality=estimate_toa_matched_filter(received,cfg)
    gcc_az,gcc_el,gcc_direction,pair_delays=estimate_gcc_phat_doa(received,cfg)
    srp_az,srp_el,srp_direction,score,_=estimate_gated_srp(received,cfg,window_s,toas=toas)
    tdoa=pair_delays_to_reference_tdoa(pair_delays)
    disagreement=float(np.degrees(np.arccos(np.clip(gcc_direction@srp_direction,-1,1))))
    z=np.r_[cfg.sound_speed_m_s*toas[0],cfg.sound_speed_m_s*tdoa,srp_az,srp_el]
    quality={"doa_disagreement_deg":disagreement,"minimum_peak_quality":float(np.min(peak_quality)),
             "reference_peak_quality":float(peak_quality[0]),"gated_srp_score":float(score),
             "gcc_azimuth_rad":float(gcc_az),"gcc_elevation_rad":float(gcc_el)}
    return z,quality
