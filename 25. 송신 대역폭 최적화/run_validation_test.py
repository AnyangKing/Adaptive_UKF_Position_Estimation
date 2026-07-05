"""LFM bandwidth 8/12/20/30 kHz의 gated-SRP validation과 UKF test."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from best_measurement import extract_best_measurement
from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig,usb_array_global_m
from measurement import fixed_measurement_covariance,initialize_position
from ukf import SignalObservationUKF,acceleration_process_covariance


DISTANCES=(100,200,400,600); BANDWIDTHS=(8000.,12000.,20000.,30000.)


def scenario(distance,split,steps):
    seed=(251000 if split=="validation" else 252000)+distance; rng=np.random.default_rng(seed)
    az=rng.uniform(-np.pi,np.pi); depth=rng.uniform(12,78); start=np.array([distance*np.cos(az),distance*np.sin(az),-depth])
    tangent=np.array([-np.sin(az),np.cos(az),0.]); radial=np.array([np.cos(az),np.sin(az),0.])
    t=np.arange(steps,dtype=float); truth=start+t[:,None]*(0.7*tangent+0.12*radial)
    meta={"snr_db":float(rng.choice([10.,20.,30.])),"surface_reflection":float(-rng.uniform(0.72,0.96)),
          "bottom_reflection":float(rng.uniform(0.32,0.78)),"radial_velocity_m_s":float(rng.uniform(-1.2,1.2))}
    return truth,meta


def collect(distance,bandwidth,split,steps):
    base=replace(ChannelConfig(),chirp_bandwidth_hz=bandwidth); truth,meta=scenario(distance,split,steps)
    center=usb_array_global_m(base.receiver_depth_m).mean(axis=0); observations=[]; qualities=[]; angular=[]
    seed_root=253000 if split=="validation" else 254000
    for k,position in enumerate(truth):
        cfg=replace(base,seed=seed_root+int(bandwidth/1000)*10000+distance*10+k,**meta)
        _,received,_=synthesize_received(position,cfg); z,q=extract_best_measurement(received,cfg)
        observations.append(z); qualities.append(q)
        estimate=np.array([np.cos(z[9])*np.cos(z[8]),np.cos(z[9])*np.sin(z[8]),np.sin(z[9])])
        actual=position-center; actual/=np.linalg.norm(actual)
        angular.append(np.degrees(np.arccos(np.clip(estimate@actual,-1,1))))
    return base,truth,np.asarray(observations),qualities,np.asarray(angular)


def validate():
    scores={}
    for bandwidth in BANDWIDTHS:
        per={}
        for distance in DISTANCES:
            *_,angular=collect(distance,bandwidth,"validation",5)
            per[str(distance)]=float(np.sqrt(np.mean(angular**2)))
        values=list(per.values()); overall=float(np.sqrt(np.mean(np.square(values))))
        scores[str(int(bandwidth))]={"overall_doa_rmse_deg":overall,"worst_distance_rmse_deg":max(values),
            "robust_score":overall+0.25*max(values),"per_distance":per}
    selected=min(BANDWIDTHS,key=lambda b:scores[str(int(b))]["robust_score"])
    return selected,scores


def evaluate(cfg,truth,observations,qualities):
    initial=initialize_position(observations[0],cfg)
    wrapper=ConditionalAdaptiveRUKF(SignalObservationUKF(np.r_[initial,np.zeros(3)],
        np.diag([8.**2]*3+[1.5**2]*3),acceleration_process_covariance(1.,0.20),
        fixed_measurement_covariance(),cfg),5.)
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)): estimate[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1)
    return {"rmse_after_3_m":float(np.sqrt(np.mean(error[3:]**2))),"max_error_m":float(np.max(error)),
            "final_error_m":float(error[-1]),"diverged_over_50m":bool(np.any(error>50))}


def run():
    selected,scores=validate(); test={}
    for distance in DISTANCES:
        cfg12,truth12,z12,q12,_=collect(distance,12000.,"test",10)
        if selected==12000.: cfgs,truths,zs,qs=cfg12,truth12,z12,q12
        else: cfgs,truths,zs,qs,_=collect(distance,selected,"test",10)
        test[str(distance)]={"baseline_12khz":evaluate(cfg12,truth12,z12,q12),
                             "selected":evaluate(cfgs,truths,zs,qs)}
    payload={"selection":{"selected_bandwidth_hz":selected,"validation":scores},"test":test}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"bandwidth_comparison.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2)); return payload


if __name__=="__main__": run()
