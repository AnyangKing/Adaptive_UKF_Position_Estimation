"""기준 TOA+GCC-TDOA와 센서별 absolute TOA 8개 융합 비교."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from absolute_adaptive import AbsoluteRangeAdaptiveUKF
from absolute_measurement import initialize_position as initialize_absolute,measurement_covariance
from absolute_ukf import SignalObservationUKF as AbsoluteUKF
from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from estimators import estimate_toa_matched_filter,estimate_toa_tracked
from measurement import fixed_measurement_covariance,initialize_position,signal_measurement
from ukf import SignalObservationUKF,acceleration_process_covariance


def trajectory(distance,steps=12):
    az=-1.72; depth=46.; start=np.array([distance*np.cos(az),distance*np.sin(az),-depth])
    tangent=np.array([-np.sin(az),np.cos(az),0.]); radial=np.array([np.cos(az),np.sin(az),0.])
    t=np.arange(steps,dtype=float)
    return start+t[:,None]*(0.68*tangent+0.08*radial)+np.column_stack((np.zeros(steps),np.zeros(steps),0.35*np.sin(t/3)))


def evaluate_baseline(observations,qualities,truth,cfg):
    initial=initialize_position(observations[0],cfg)
    wrapper=ConditionalAdaptiveRUKF(SignalObservationUKF(np.r_[initial,np.zeros(3)],
        np.diag([8.**2]*3+[1.5**2]*3),acceleration_process_covariance(1.,0.20),
        fixed_measurement_covariance(),cfg),5.)
    return _run(wrapper,initial,observations,qualities,truth)


def evaluate_absolute(observations,qualities,truth,cfg):
    initial=initialize_absolute(observations[0],cfg)
    wrapper=AbsoluteRangeAdaptiveUKF(AbsoluteUKF(np.r_[initial,np.zeros(3)],
        np.diag([8.**2]*3+[1.5**2]*3),acceleration_process_covariance(1.,0.20),
        measurement_covariance(),cfg))
    return _run(wrapper,initial,observations,qualities,truth)


def _run(wrapper,initial,observations,qualities,truth):
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)): estimate[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1)
    return {"initial_error_m":float(error[0]),"rmse_after_3_m":float(np.sqrt(np.mean(error[3:]**2))),
        "max_error_m":float(np.max(error)),"final_error_m":float(error[-1]),
        "diverged_over_50m":bool(np.any(error>50))}


def run():
    cfg=ChannelConfig(); result={}
    for distance in (100,200,400,600):
        truth=trajectory(distance); baseline=[]; strongest=[]; tracked=[]; qualities=[]; previous=None
        for k,position in enumerate(truth):
            ping_cfg=replace(cfg,seed=200000+distance*10+k,radial_velocity_m_s=0.6+0.12*np.sin(k/3),
                snr_db=20.,surface_reflection=-0.90,bottom_reflection=0.60)
            _,received,_=synthesize_received(position,ping_cfg); z,q=signal_measurement(received,ping_cfg)
            z[8]=q["srp_azimuth_rad"]; z[9]=q["srp_elevation_rad"]
            strongest_toas,_=estimate_toa_matched_filter(received,ping_cfg)
            tracked_toas,_,_=estimate_toa_tracked(received,ping_cfg,previous); previous=tracked_toas
            baseline.append(z); strongest.append(np.r_[ping_cfg.sound_speed_m_s*strongest_toas,z[8:10]])
            tracked.append(np.r_[ping_cfg.sound_speed_m_s*tracked_toas,z[8:10]]); qualities.append(q)
        result[str(distance)]={
            "baseline_conditional_tdoa":evaluate_baseline(np.asarray(baseline),qualities,truth,cfg),
            "absolute_strongest":evaluate_absolute(np.asarray(strongest),qualities,truth,cfg),
            "absolute_tracked":evaluate_absolute(np.asarray(tracked),qualities,truth,cfg)}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"absolute_toa_comparison.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
