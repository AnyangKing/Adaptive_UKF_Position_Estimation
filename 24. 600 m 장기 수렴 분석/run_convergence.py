"""현재 최선 구성의 600 m 30-ping 장기 수렴 분석."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from best_measurement import extract_best_measurement
from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from measurement import fixed_measurement_covariance,initialize_position
from ukf import SignalObservationUKF,acceleration_process_covariance


DISTANCE=600; STEPS=30; TRIALS=4


def scenario(trial):
    rng=np.random.default_rng(241001+trial); az=rng.uniform(-np.pi,np.pi); depth=rng.uniform(12,75)
    start=np.array([DISTANCE*np.cos(az),DISTANCE*np.sin(az),-depth])
    tangent=np.array([-np.sin(az),np.cos(az),0.]); radial=np.array([np.cos(az),np.sin(az),0.])
    speed=rng.uniform(0.5,1.1); heading=rng.uniform(-0.35,0.35); horizontal=speed*(np.cos(heading)*tangent+np.sin(heading)*radial)
    vz=rng.uniform(-0.04,0.04); t=np.arange(STEPS,dtype=float); truth=start+t[:,None]*np.r_[horizontal[:2],vz]
    meta={"azimuth_rad":float(az),"depth_m":float(depth),"speed_m_s":float(speed),
        "snr_db":float(rng.choice([10.,20.,30.])),"surface_reflection":float(-rng.uniform(0.70,0.98)),
        "bottom_reflection":float(rng.uniform(0.30,0.80)),"radial_velocity_m_s":float(rng.uniform(-1.5,1.5))}
    return truth,meta


def sustained_below(errors,threshold=5.0,run_length=5):
    for k in range(len(errors)-run_length+1):
        if np.all(errors[k:k+run_length]<threshold): return k
    return None


def run_trial(trial):
    cfg=ChannelConfig(); truth,meta=scenario(trial); observations=[]; qualities=[]
    for k,position in enumerate(truth):
        ping_cfg=replace(cfg,seed=242000+trial*STEPS+k,snr_db=meta["snr_db"],
            surface_reflection=meta["surface_reflection"],bottom_reflection=meta["bottom_reflection"],
            radial_velocity_m_s=meta["radial_velocity_m_s"])
        _,received,_=synthesize_received(position,ping_cfg); z,q=extract_best_measurement(received,ping_cfg)
        observations.append(z); qualities.append(q)
    observations=np.asarray(observations); initial=initialize_position(observations[0],cfg)
    wrapper=ConditionalAdaptiveRUKF(SignalObservationUKF(np.r_[initial,np.zeros(3)],
        np.diag([8.**2]*3+[1.5**2]*3),acceleration_process_covariance(1.,0.20),
        fixed_measurement_covariance(),cfg),5.)
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,STEPS): estimate[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1); convergence=sustained_below(error)
    metrics={**meta,"initial_error_m":float(error[0]),
        "rmse_after_3_m":float(np.sqrt(np.mean(error[3:]**2))),
        "rmse_after_10_m":float(np.sqrt(np.mean(error[10:]**2))),
        "rmse_after_20_m":float(np.sqrt(np.mean(error[20:]**2))),
        "mean_last_5_m":float(np.mean(error[-5:])),"final_error_m":float(error[-1]),
        "minimum_error_m":float(np.min(error)),"maximum_error_m":float(np.max(error)),
        "first_sustained_5m_step":convergence,
        "routing_activation_rate":float(np.mean([h["routed"] for h in wrapper.history]))}
    return metrics,error


def run():
    records=[]; errors=[]
    for trial in range(TRIALS):
        record,error=run_trial(trial); records.append(record); errors.append(error)
    summary={key:float(np.mean([r[key] for r in records])) for key in
        ("initial_error_m","rmse_after_3_m","rmse_after_10_m","rmse_after_20_m","mean_last_5_m","final_error_m")}
    summary["converged_below_5m_rate"]=float(np.mean([r["first_sustained_5m_step"] is not None for r in records]))
    payload={"configuration":{"distance_m":DISTANCE,"trials":TRIALS,"steps":STEPS},"summary":summary,"trials":records}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"convergence_600m.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    np.savez(output/"convergence_600m.npz",errors=np.asarray(errors))
    print(json.dumps(payload,indent=2)); return payload


if __name__=="__main__": run()
