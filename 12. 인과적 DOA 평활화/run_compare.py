"""SRP 단위방향의 causal EMA가 UKF 위치오차에 미치는 영향 비교."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from channel import synthesize_received
from config import ChannelConfig, usb_array_global_m
from measurement import fixed_measurement_covariance, initialize_position, signal_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


def trajectory(steps=30):
    t=np.arange(steps,dtype=float)
    return np.column_stack((200+0.8*t,30+0.4*t,-25-0.12*t+0.5*np.sin(t/7)))


def angles_to_direction(az,el):
    return np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])


def direction_to_angles(direction):
    direction=direction/np.linalg.norm(direction)
    return np.arctan2(direction[1],direction[0]),np.arctan2(direction[2],np.hypot(direction[0],direction[1]))


def smooth_directions(raw,alpha):
    output=np.zeros_like(raw); output[0]=raw[0]
    for k in range(1,len(raw)):
        output[k]=alpha*output[k-1]+(1-alpha)*raw[k]
        output[k]/=np.linalg.norm(output[k])
    return output


def evaluate(observations,qualities,truth,cfg):
    initial=initialize_position(observations[0],cfg)
    wrapper=AdaptiveRUKF(SignalObservationUKF(
        np.r_[initial,np.zeros(3)],np.diag([8.0**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.0,0.20),fixed_measurement_covariance(),cfg))
    estimates=np.zeros_like(truth); estimates[0]=initial
    for k in range(1,len(truth)):
        estimates[k]=wrapper.step(observations[k],qualities[k])[:3]
    norm=np.linalg.norm(estimates-truth,axis=1)
    return {"rmse_after_5_m":float(np.sqrt(np.mean(norm[5:]**2))),
            "max_error_m":float(np.max(norm)),"final_error_m":float(norm[-1])},estimates


def run():
    cfg=ChannelConfig(); truth=trajectory(); base_observations=[]; qualities=[]; raw=[]
    for k,position in enumerate(truth):
        ping_cfg=replace(cfg,seed=93001+k,radial_velocity_m_s=0.6+0.2*np.sin(k/5))
        _,received,_=synthesize_received(position,ping_cfg); z,q=signal_measurement(received,ping_cfg)
        z[8]=q["srp_azimuth_rad"]; z[9]=q["srp_elevation_rad"]
        base_observations.append(z); qualities.append(q)
        raw.append(angles_to_direction(z[8],z[9]))
    base_observations=np.asarray(base_observations); raw=np.asarray(raw)
    truth_direction=truth-usb_array_global_m(cfg.receiver_depth_m).mean(axis=0)
    truth_direction/=np.linalg.norm(truth_direction,axis=1,keepdims=True)
    result={}; arrays={"truth":truth,"raw_direction":raw}
    for alpha in (0.0,0.5,0.8):
        directions=raw if alpha==0 else smooth_directions(raw,alpha)
        observations=base_observations.copy()
        for k,direction in enumerate(directions):
            observations[k,8],observations[k,9]=direction_to_angles(direction)
        metrics,estimates=evaluate(observations,qualities,truth,cfg)
        angular=np.degrees(np.arccos(np.clip(np.sum(directions*truth_direction,axis=1),-1,1)))
        metrics["doa_rmse_deg"]=float(np.sqrt(np.mean(angular**2)))
        metrics["doa_mean_deg"]=float(np.mean(angular))
        key="raw" if alpha==0 else f"ema_{alpha:g}"
        result[key]=metrics; arrays[key]=estimates; arrays[f"{key}_direction"]=directions
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"doa_smoothing_comparison.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    np.savez(output/"doa_smoothing_comparison.npz",**arrays)
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
