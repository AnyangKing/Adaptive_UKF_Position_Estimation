"""full/1/2/5 ms gated SRP validation 선택과 독립 UKF test."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig,usb_array_global_m
from gated_srp import estimate_gated_srp
from measurement import fixed_measurement_covariance,initialize_position,signal_measurement
from ukf import SignalObservationUKF,acceleration_process_covariance


DISTANCES=(100,200,400,600); CANDIDATES=("full",0.001,0.002,0.005)


def trajectory(distance,split,steps=10):
    az=0.15 if split=="validation" else -1.05; depth=62. if split=="validation" else 26.
    start=np.array([distance*np.cos(az),distance*np.sin(az),-depth])
    tangent=np.array([-np.sin(az),np.cos(az),0.]); radial=np.array([np.cos(az),np.sin(az),0.])
    t=np.arange(steps,dtype=float); velocity=(0.68*tangent+0.15*radial) if split=="validation" else (0.72*tangent-0.10*radial)
    return start+t[:,None]*velocity+np.column_stack((np.zeros(steps),np.zeros(steps),0.35*np.sin(t/3)))


def unit(az,el): return np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])
def angle_deg(a,b): return float(np.degrees(np.arccos(np.clip(a@b,-1,1))))


def collect(split):
    cfg=ChannelConfig(); seed_root=221000 if split=="validation" else 222000; center=usb_array_global_m().mean(axis=0); data={}
    for distance in DISTANCES:
        truth=trajectory(distance,split); variants={str(c):[] for c in CANDIDATES}; qualities={str(c):[] for c in CANDIDATES}; angular={str(c):[] for c in CANDIDATES}
        for k,position in enumerate(truth):
            ping_cfg=replace(cfg,seed=seed_root+distance*10+k,snr_db=20.,surface_reflection=-0.90,
                bottom_reflection=0.60,radial_velocity_m_s=0.6+0.1*np.sin(k/3))
            _,received,_=synthesize_received(position,ping_cfg); z,q=signal_measurement(received,ping_cfg)
            gcc=unit(z[8],z[9]); full=unit(q["srp_azimuth_rad"],q["srp_elevation_rad"])
            actual=position-center; actual/=np.linalg.norm(actual)
            zf=z.copy(); zf[8]=q["srp_azimuth_rad"]; zf[9]=q["srp_elevation_rad"]
            variants["full"].append(zf); qualities["full"].append(q.copy()); angular["full"].append(angle_deg(full,actual))
            for window in CANDIDATES[1:]:
                az,el,direction,_,_=estimate_gated_srp(received,ping_cfg,window)
                zg=z.copy(); zg[8]=az; zg[9]=el
                qg=q.copy(); qg["doa_disagreement_deg"]=angle_deg(gcc,direction)
                key=str(window); variants[key].append(zg); qualities[key].append(qg); angular[key].append(angle_deg(direction,actual))
        data[distance]=(truth,{k:np.asarray(v) for k,v in variants.items()},qualities,angular)
    return cfg,data


def evaluate_ukf(truth,observations,qualities,cfg):
    initial=initialize_position(observations[0],cfg)
    wrapper=ConditionalAdaptiveRUKF(SignalObservationUKF(np.r_[initial,np.zeros(3)],
        np.diag([8.**2]*3+[1.5**2]*3),acceleration_process_covariance(1.,0.20),
        fixed_measurement_covariance(),cfg),5.)
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)): estimate[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1)
    return {"rmse_after_3_m":float(np.sqrt(np.mean(error[3:]**2))),"max_error_m":float(np.max(error)),
            "final_error_m":float(error[-1]),"diverged_over_50m":bool(np.any(error>50))}


def validate():
    _,data=collect("validation"); scores={}
    for candidate in CANDIDATES:
        key=str(candidate); per={str(d):float(np.sqrt(np.mean(np.square(data[d][3][key])))) for d in DISTANCES}
        values=list(per.values()); scores[key]={"overall_doa_rmse_deg":float(np.sqrt(np.mean(np.square(values)))),
            "worst_distance_rmse_deg":max(values),"robust_score":float(np.sqrt(np.mean(np.square(values)))+0.25*max(values)),"per_distance":per}
    selected=min(CANDIDATES,key=lambda c:scores[str(c)]["robust_score"])
    return selected,scores


def run():
    selected,scores=validate(); cfg,data=collect("test"); key=str(selected); test={}
    for distance in DISTANCES:
        truth,variants,qualities,_=data[distance]
        test[str(distance)]={"full":evaluate_ukf(truth,variants["full"],qualities["full"],cfg),
            "selected":evaluate_ukf(truth,variants[key],qualities[key],cfg)}
    payload={"selection":{"selected":selected,"validation":scores},"test":test}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"gated_srp.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2)); return payload


if __name__=="__main__": run()
