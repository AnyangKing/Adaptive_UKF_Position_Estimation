"""독립 시나리오에서 관측 bias와 full covariance R을 추정한다."""

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from estimators import (
    estimate_gcc_phat_doa,
    estimate_toa_matched_filter,
    pair_delays_to_reference_tdoa,
)
from measurement import ideal_measurement, wrap_angle


def _measurement_without_srp(received, cfg):
    toas, _ = estimate_toa_matched_filter(received, cfg)
    azimuth, elevation, _, pair_delays = estimate_gcc_phat_doa(received, cfg)
    tdoa = pair_delays_to_reference_tdoa(pair_delays)
    return np.r_[cfg.sound_speed_m_s*toas[0], cfg.sound_speed_m_s*tdoa,
                 azimuth, elevation]


def calibration_scenarios(count=30, seed=81001):
    rng=np.random.default_rng(seed); scenarios=[]
    for index in range(count):
        distance=rng.uniform(80.0,650.0); azimuth=rng.uniform(-np.pi,np.pi)
        source=np.array([distance*np.cos(azimuth),distance*np.sin(azimuth),
                         -rng.uniform(8.0,88.0)])
        scenarios.append((source,{"seed":seed+index,
            "snr_db":float(rng.uniform(10.0,30.0)),
            "surface_reflection":float(-rng.uniform(0.70,0.98)),
            "bottom_reflection":float(rng.uniform(0.30,0.80)),
            "radial_velocity_m_s":float(rng.uniform(-1.5,1.5))}))
    return scenarios


def estimate_calibration(duration_s, count=30, shrinkage=0.25):
    residuals=[]
    for source,parameters in calibration_scenarios(count):
        cfg=replace(ChannelConfig(),pulse_duration_s=duration_s,**parameters)
        _,received,_=synthesize_received(source,cfg)
        residual=_measurement_without_srp(received,cfg)-ideal_measurement(source,cfg)
        residual[8:]=wrap_angle(residual[8:])
        residuals.append(residual)
    residuals=np.asarray(residuals)
    bias=np.mean(residuals,axis=0)
    covariance=np.cov((residuals-bias).T,ddof=1)
    diagonal=np.diag(np.diag(covariance))
    covariance=(1.0-shrinkage)*covariance+shrinkage*diagonal
    floor=np.r_[np.full(8,1e-4**2),np.full(2,np.radians(0.02)**2)]
    covariance+=np.diag(floor)
    return bias,covariance,residuals
