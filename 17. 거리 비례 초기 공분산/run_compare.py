"""고정 등방성 P0와 거리비례 이방성 P0를 신규 거리별 궤적에서 비교."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from channel import synthesize_received
from config import ChannelConfig,usb_array_global_m
from measurement import fixed_measurement_covariance,initialize_position,signal_measurement
from ukf import SignalObservationUKF,acceleration_process_covariance


def geometry_position_covariance(initial_position,cfg,range_std_m=3.0,angle_std_deg=5.0):
    center=usb_array_global_m(cfg.receiver_depth_m).mean(axis=0)
    delta=np.asarray(initial_position)-center; distance=np.linalg.norm(delta); direction=delta/distance
    radial=np.outer(direction,direction); tangent=np.eye(3)-radial
    tangential_std=max(1.0,distance*np.radians(angle_std_deg))
    return range_std_m**2*radial+tangential_std**2*tangent


def initial_covariance(initial,cfg,mode):
    P=np.zeros((6,6)); P[3:,3:]=np.eye(3)*1.5**2
    P[:3,:3]=np.eye(3)*8.0**2 if mode=="fixed" else geometry_position_covariance(initial,cfg)
    return P


def trajectory(distance,steps=15):
    az=-2.30; depth=28.; start=np.array([distance*np.cos(az),distance*np.sin(az),-depth])
    tangent=np.array([-np.sin(az),np.cos(az),0.]); radial=np.array([np.cos(az),np.sin(az),0.])
    t=np.arange(steps,dtype=float)
    return start+t[:,None]*(0.65*tangent+0.15*radial)+np.column_stack((np.zeros(steps),np.zeros(steps),0.35*np.sin(t/4)))


def evaluate(observations,qualities,truth,cfg,mode):
    initial=initialize_position(observations[0],cfg)
    wrapper=AdaptiveRUKF(SignalObservationUKF(np.r_[initial,np.zeros(3)],
        initial_covariance(initial,cfg,mode),acceleration_process_covariance(1.,0.20),
        fixed_measurement_covariance(),cfg))
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)): estimate[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1)
    return {"initial_error_m":float(error[0]),"rmse_after_5_m":float(np.sqrt(np.mean(error[5:]**2))),
        "max_error_m":float(np.max(error)),"final_error_m":float(error[-1]),
        "diverged_over_50m":bool(np.any(error>50))},estimate


def run():
    cfg=ChannelConfig(); result={}; arrays={}
    for distance in (100,200,400,600):
        truth=trajectory(distance); observations=[]; qualities=[]
        for k,position in enumerate(truth):
            ping_cfg=replace(cfg,seed=170000+distance*10+k,radial_velocity_m_s=0.55+0.2*np.sin(k/4),
                snr_db=20.,surface_reflection=-0.90,bottom_reflection=0.60)
            _,received,_=synthesize_received(position,ping_cfg); z,q=signal_measurement(received,ping_cfg)
            z[8]=q["srp_azimuth_rad"]; z[9]=q["srp_elevation_rad"]
            observations.append(z); qualities.append(q)
        observations=np.asarray(observations); fixed,fixed_est=evaluate(observations,qualities,truth,cfg,"fixed")
        geometry,geometry_est=evaluate(observations,qualities,truth,cfg,"geometry")
        result[str(distance)]={"fixed":fixed,"geometry":geometry,
            "improvement_percent":100*(fixed["rmse_after_5_m"]-geometry["rmse_after_5_m"])/fixed["rmse_after_5_m"]}
        arrays.update({f"truth_{distance}":truth,f"fixed_{distance}":fixed_est,f"geometry_{distance}":geometry_est})
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"initial_covariance_comparison.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    np.savez(output/"initial_covariance_comparison.npz",**arrays)
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
