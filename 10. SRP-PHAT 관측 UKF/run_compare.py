"""GCC/SRP DOA와 strongest/tracked TOA 조합을 동일 신호에서 비교."""

from dataclasses import replace
from pathlib import Path
from time import perf_counter
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


def evaluate(observations,qualities,truth,cfg):
    initial=initialize_position(observations[0],cfg)
    wrapper=AdaptiveRUKF(SignalObservationUKF(
        np.r_[initial,np.zeros(3)],np.diag([8.0**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.0,0.20),fixed_measurement_covariance(),cfg))
    estimates=np.zeros_like(truth); estimates[0]=initial
    start=perf_counter()
    for k in range(1,len(truth)):
        estimates[k]=wrapper.step(observations[k],qualities[k])[:3]
    filter_ms=(perf_counter()-start)*1000/(len(truth)-1)
    errors=estimates-truth; norms=np.linalg.norm(errors,axis=1)
    center=np.array([0.,0.,-cfg.receiver_depth_m]); radial=truth-center
    radial/=np.linalg.norm(radial,axis=1,keepdims=True)
    radial_error=np.sum(errors*radial,axis=1)
    tangential=np.linalg.norm(errors-radial_error[:,None]*radial,axis=1)
    return {"initial_error_m":float(norms[0]),
        "rmse_after_5_m":float(np.sqrt(np.mean(norms[5:]**2))),
        "radial_rmse_after_5_m":float(np.sqrt(np.mean(radial_error[5:]**2))),
        "tangential_rmse_after_5_m":float(np.sqrt(np.mean(tangential[5:]**2))),
        "max_error_m":float(np.max(norms)),"final_error_m":float(norms[-1]),
        "ukf_step_time_ms":filter_ms},estimates


def run():
    cfg=ChannelConfig(); truth=trajectory(); combinations={
        "gcc_strongest":[],"srp_strongest":[],"srp_tracked":[]}; qualities=[]
    previous=None; extraction_times=[]
    for k,position in enumerate(truth):
        ping_cfg=replace(cfg,seed=93001+k,radial_velocity_m_s=0.6+0.2*np.sin(k/5))
        _,received,_=synthesize_received(position,ping_cfg)
        start=perf_counter(); z,q=signal_measurement(received,ping_cfg)
        tracked,_,_=estimate_toa_tracked(received,ping_cfg,previous); previous=tracked
        extraction_times.append((perf_counter()-start)*1000)
        z_srp=z.copy(); z_srp[8]=q["srp_azimuth_rad"]; z_srp[9]=q["srp_elevation_rad"]
        z_srp_tracked=z_srp.copy(); z_srp_tracked[0]=ping_cfg.sound_speed_m_s*tracked[0]
        combinations["gcc_strongest"].append(z)
        combinations["srp_strongest"].append(z_srp)
        combinations["srp_tracked"].append(z_srp_tracked); qualities.append(q)
    result={}; arrays={"truth":truth}
    for name,observations in combinations.items():
        metrics,estimates=evaluate(np.asarray(observations),qualities,truth,cfg)
        result[name]=metrics; arrays[name]=estimates
    result["measurement_extraction_time_ms_per_ping"]=float(np.mean(extraction_times))
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"srp_ukf_comparison.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    np.savez(output/"srp_ukf_comparison.npz",**arrays)
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
