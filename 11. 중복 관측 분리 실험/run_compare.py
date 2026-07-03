"""상관된 TOA/TDOA/SRP-DOA block을 선택적으로 비활성화해 중복정보 영향을 평가."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from channel import synthesize_received
from config import ChannelConfig
from estimators import estimate_toa_tracked
from measurement import fixed_measurement_covariance, initialize_position, signal_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


def trajectory(steps=30):
    t=np.arange(steps,dtype=float)
    return np.column_stack((200+0.8*t,30+0.4*t,-25-0.12*t+0.5*np.sin(t/7)))


def covariance_for(use_toa=True,use_tdoa=True,use_doa=True):
    R=fixed_measurement_covariance(); disabled_variance=1.0e8
    if not use_toa:
        R[0,:]=0; R[:,0]=0; R[0,0]=disabled_variance
    if not use_tdoa:
        R[1:8,:]=0; R[:,1:8]=0; R[1:8,1:8]=np.eye(7)*disabled_variance
    if not use_doa:
        R[8:10,:]=0; R[:,8:10]=0; R[8:10,8:10]=np.eye(2)*disabled_variance
    return R


def evaluate(observations,qualities,truth,cfg,R):
    initial=initialize_position(observations[0],cfg)
    wrapper=AdaptiveRUKF(SignalObservationUKF(
        np.r_[initial,np.zeros(3)],np.diag([8.0**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.0,0.20),R,cfg))
    estimates=np.zeros_like(truth); estimates[0]=initial
    for k in range(1,len(truth)):
        estimates[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=estimates-truth; norm=np.linalg.norm(error,axis=1)
    center=np.array([0.,0.,-cfg.receiver_depth_m]); radial=truth-center
    radial/=np.linalg.norm(radial,axis=1,keepdims=True)
    er=np.sum(error*radial,axis=1); et=np.linalg.norm(error-er[:,None]*radial,axis=1)
    return {"rmse_after_5_m":float(np.sqrt(np.mean(norm[5:]**2))),
        "radial_rmse_after_5_m":float(np.sqrt(np.mean(er[5:]**2))),
        "tangential_rmse_after_5_m":float(np.sqrt(np.mean(et[5:]**2))),
        "max_error_m":float(np.max(norm)),"final_error_m":float(norm[-1])},estimates


def run():
    cfg=ChannelConfig(); truth=trajectory(); srp_strong=[]; srp_tracked=[]; qualities=[]; previous=None
    for k,position in enumerate(truth):
        ping_cfg=replace(cfg,seed=93001+k,radial_velocity_m_s=0.6+0.2*np.sin(k/5))
        _,received,_=synthesize_received(position,ping_cfg)
        z,q=signal_measurement(received,ping_cfg)
        tracked,_,_=estimate_toa_tracked(received,ping_cfg,previous); previous=tracked
        z[8]=q["srp_azimuth_rad"]; z[9]=q["srp_elevation_rad"]
        zt=z.copy(); zt[0]=ping_cfg.sound_speed_m_s*tracked[0]
        srp_strong.append(z); srp_tracked.append(zt); qualities.append(q)
    srp_strong=np.asarray(srp_strong); srp_tracked=np.asarray(srp_tracked)
    specifications={
        "full_srp_strongest":(srp_strong,covariance_for()),
        "toa_srp_strongest":(srp_strong,covariance_for(use_tdoa=False)),
        "tdoa_srp":(srp_strong,covariance_for(use_toa=False)),
        "toa_srp_tracked":(srp_tracked,covariance_for(use_tdoa=False)),
        "toa_tdoa_no_doa":(srp_strong,covariance_for(use_doa=False)),
    }
    result={}; arrays={"truth":truth}
    for name,(observations,R) in specifications.items():
        result[name],arrays[name]=evaluate(observations,qualities,truth,cfg,R)
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"observation_ablation.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    np.savez(output/"observation_ablation.npz",**arrays)
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
