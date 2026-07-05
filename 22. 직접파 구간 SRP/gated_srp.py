"""matched-filter 도착시각 주변의 초기 구간만 사용하는 SRP-PHAT."""

import numpy as np

from estimators import estimate_srp_phat_doa,estimate_toa_matched_filter


def crop_direct_arrival(received,cfg,window_s,pre_s=0.0001):
    toas,_=estimate_toa_matched_filter(received,cfg); reference=float(np.min(toas))
    start=max(0,int(np.floor((reference-pre_s)*cfg.sample_rate_hz)))
    end=min(received.shape[1],int(np.ceil((reference+window_s)*cfg.sample_rate_hz)))
    if end-start<32: raise ValueError("direct-arrival window is too short")
    return received[:,start:end],toas


def estimate_gated_srp(received,cfg,window_s):
    cropped,toas=crop_direct_arrival(received,cfg,window_s)
    az,el,direction,score=estimate_srp_phat_doa(cropped,cfg)
    return az,el,direction,score,toas
