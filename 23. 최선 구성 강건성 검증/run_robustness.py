"""고정된 최선 구성의 거리별 소규모 Monte Carlo 강건성 평가."""

from dataclasses import replace
from pathlib import Path
from time import perf_counter
import json
import numpy as np

from best_measurement import extract_best_measurement
from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from measurement import fixed_measurement_covariance,initialize_position
from ukf import SignalObservationUKF,acceleration_process_covariance


DISTANCES=(100,200,400,600); TRIALS=4; STEPS=10


def scenario(distance,trial):
    rng=np.random.default_rng(230001+distance*100+trial); az=rng.uniform(-np.pi,np.pi); depth=rng.uniform(10,80)
    start=np.array([distance*np.cos(az),distance*np.sin(az),-depth])
    tangent=np.array([-np.sin(az),np.cos(az),0.]); radial=np.array([np.cos(az),np.sin(az),0.])
    speed=rng.uniform(0.4,1.2); heading=rng.uniform(-0.5,0.5)
    horizontal=speed*(np.cos(heading)*tangent+np.sin(heading)*radial); vz=rng.uniform(-0.08,0.08)
    t=np.arange(STEPS,dtype=float); truth=start+t[:,None]*np.r_[horizontal[:2],vz]
    metadata={"azimuth_rad":float(az),"start_depth_m":float(depth),"speed_m_s":float(speed),
        "snr_db":float(rng.choice([10.,20.,30.])),"surface_reflection":float(-rng.uniform(0.70,0.98)),
        "bottom_reflection":float(rng.uniform(0.30,0.80)),"radial_velocity_m_s":float(rng.uniform(-1.5,1.5))}
    return truth,metadata


def run_trial(distance,trial):
    cfg=ChannelConfig(); truth,meta=scenario(distance,trial); observations=[]; qualities=[]; times=[]
    for k,position in enumerate(truth):
        ping_cfg=replace(cfg,seed=240000+distance*100+trial*STEPS+k,snr_db=meta["snr_db"],
            surface_reflection=meta["surface_reflection"],bottom_reflection=meta["bottom_reflection"],
            radial_velocity_m_s=meta["radial_velocity_m_s"])
        _,received,_=synthesize_received(position,ping_cfg); start=perf_counter()
        z,q=extract_best_measurement(received,ping_cfg); times.append((perf_counter()-start)*1000)
        observations.append(z); qualities.append(q)
    observations=np.asarray(observations); initial=initialize_position(observations[0],cfg)
    wrapper=ConditionalAdaptiveRUKF(SignalObservationUKF(np.r_[initial,np.zeros(3)],
        np.diag([8.**2]*3+[1.5**2]*3),acceleration_process_covariance(1.,0.20),
        fixed_measurement_covariance(),cfg),5.)
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,STEPS): estimate[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1); routed=np.mean([h["routed"] for h in wrapper.history])
    return {**meta,"initial_error_m":float(error[0]),"rmse_after_3_m":float(np.sqrt(np.mean(error[3:]**2))),
        "max_error_m":float(np.max(error)),"final_error_m":float(error[-1]),
        "diverged_over_50m":bool(np.any(error>50)),"routing_activation_rate":float(routed),
        "measurement_time_ms_per_ping":float(np.mean(times))}


def summarize(records):
    values=np.array([r["rmse_after_3_m"] for r in records])
    return {"mean_rmse_m":float(np.mean(values)),"std_rmse_m":float(np.std(values,ddof=1)),
        "median_rmse_m":float(np.median(values)),"p90_rmse_m":float(np.percentile(values,90)),
        "max_rmse_m":float(np.max(values)),"divergence_rate":float(np.mean([r["diverged_over_50m"] for r in records])),
        "mean_routing_activation_rate":float(np.mean([r["routing_activation_rate"] for r in records])),
        "mean_measurement_time_ms":float(np.mean([r["measurement_time_ms_per_ping"] for r in records]))}


def run():
    result={"configuration":{"distances":DISTANCES,"trials_per_distance":TRIALS,"steps":STEPS,
        "gated_srp_window_ms":5.0,"conditional_routing_threshold_deg":5.0},"distances":{}}
    for distance in DISTANCES:
        records=[run_trial(distance,trial) for trial in range(TRIALS)]
        result["distances"][str(distance)]={"summary":summarize(records),"trials":records}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"robustness_results.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
