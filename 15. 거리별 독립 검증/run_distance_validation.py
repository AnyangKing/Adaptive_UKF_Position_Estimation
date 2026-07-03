"""고정된 10 ms SRP constant correction의 거리별 독립 검증."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position, signal_measurement, wrap_angle
from ukf import SignalObservationUKF, acceleration_process_covariance


# 13번 train/validation에서 선택되고 test 전에 고정된 signed residual.
FIXED_SRP_BIAS_RAD=np.array([0.00026560684880701696,0.01606807603660994])


def make_trajectory(distance_m,replicate,steps=12):
    azimuth=(0.35,-1.15)[replicate]; depth=(20.0,55.0)[replicate]
    start=np.array([distance_m*np.cos(azimuth),distance_m*np.sin(azimuth),-depth])
    tangent=np.array([-np.sin(azimuth),np.cos(azimuth),0.0])
    radial=np.array([np.cos(azimuth),np.sin(azimuth),0.0])
    t=np.arange(steps,dtype=float)
    return start+t[:,None]*(0.75*tangent+0.25*radial)+np.column_stack(
        (np.zeros(steps),np.zeros(steps),0.3*np.sin(t/4)))


def make_filter(initial,cfg):
    return AdaptiveRUKF(SignalObservationUKF(
        np.r_[initial,np.zeros(3)],np.diag([8.0**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.0,0.20),fixed_measurement_covariance(),cfg))


def evaluate(observations,qualities,truth,cfg):
    initial=initialize_position(observations[0],cfg); wrapper=make_filter(initial,cfg)
    estimates=np.zeros_like(truth); estimates[0]=initial
    for k in range(1,len(truth)):
        estimates[k]=wrapper.step(observations[k],qualities[k])[:3]
    errors=np.linalg.norm(estimates-truth,axis=1)
    return {"initial_error_m":float(errors[0]),"rmse_after_3_m":float(np.sqrt(np.mean(errors[3:]**2))),
        "max_error_m":float(np.max(errors)),"final_error_m":float(errors[-1]),
        "diverged_over_50m":bool(np.any(errors>50.0))}


def run_single(distance,replicate):
    cfg=ChannelConfig(); truth=make_trajectory(distance,replicate); raw=[]; corrected=[]; qualities=[]
    seed_base=150000+int(distance)*10+replicate*100
    for k,position in enumerate(truth):
        ping_cfg=replace(cfg,seed=seed_base+k,radial_velocity_m_s=0.7+0.15*np.sin(k/3),
            snr_db=20.0,surface_reflection=-0.90,bottom_reflection=0.60)
        _,received,_=synthesize_received(position,ping_cfg); z,q=signal_measurement(received,ping_cfg)
        z[8]=q["srp_azimuth_rad"]; z[9]=q["srp_elevation_rad"]
        zc=z.copy(); zc[8:10]=wrap_angle(zc[8:10]-FIXED_SRP_BIAS_RAD)
        raw.append(z); corrected.append(zc); qualities.append(q)
    return evaluate(np.asarray(raw),qualities,truth,cfg),evaluate(np.asarray(corrected),qualities,truth,cfg)


def aggregate(records):
    return {"mean_rmse_after_3_m":float(np.mean([r["rmse_after_3_m"] for r in records])),
        "std_rmse_after_3_m":float(np.std([r["rmse_after_3_m"] for r in records],ddof=1)),
        "mean_initial_error_m":float(np.mean([r["initial_error_m"] for r in records])),
        "worst_max_error_m":float(np.max([r["max_error_m"] for r in records])),
        "divergence_rate":float(np.mean([r["diverged_over_50m"] for r in records]))}


def run():
    result={"fixed_bias_rad":FIXED_SRP_BIAS_RAD.tolist(),"distances":{}}
    for distance in (100,200,400,600):
        raw_records=[]; corrected_records=[]
        for replicate in range(2):
            raw,corrected=run_single(distance,replicate)
            raw_records.append(raw); corrected_records.append(corrected)
        result["distances"][str(distance)]={"raw_runs":raw_records,"corrected_runs":corrected_records,
            "raw":aggregate(raw_records),"corrected":aggregate(corrected_records)}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"distance_validation.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
