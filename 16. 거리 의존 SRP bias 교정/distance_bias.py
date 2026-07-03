"""거리균형 calibration/validation에서 SRP signed angle bias 모델 선택."""

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig,usb_array_global_m
from measurement import signal_measurement,wrap_angle

DISTANCES=np.array([100.,200.,400.,600.])


def collect(per_distance,seed):
    rng=np.random.default_rng(seed); center=usb_array_global_m().mean(axis=0)
    ranges=[]; measured=[]; residual=[]; labels=[]
    index=0
    for distance in DISTANCES:
        for _ in range(per_distance):
            az=rng.uniform(-np.pi,np.pi); depth=rng.uniform(8.,88.)
            source=np.array([distance*np.cos(az),distance*np.sin(az),-depth])
            cfg=replace(ChannelConfig(),seed=seed+index,snr_db=float(rng.uniform(10,30)),
                surface_reflection=float(-rng.uniform(0.70,0.98)),
                bottom_reflection=float(rng.uniform(0.30,0.80)),
                radial_velocity_m_s=float(rng.uniform(-1.5,1.5)))
            _,received,_=synthesize_received(source,cfg); z,q=signal_measurement(received,cfg)
            angle=np.array([q["srp_azimuth_rad"],q["srp_elevation_rad"]])
            delta=source-center; truth=np.array([np.arctan2(delta[1],delta[0]),
                np.arctan2(delta[2],np.hypot(delta[0],delta[1]))])
            ranges.append(z[0]); measured.append(angle); residual.append(wrap_angle(angle-truth))
            labels.append(distance); index+=1
    return {"range":np.asarray(ranges),"measured":np.asarray(measured),
            "residual":np.asarray(residual),"label":np.asarray(labels)}


def fit_models(train):
    constant=np.mean(train["residual"],axis=0)
    X=np.column_stack((np.ones(len(train["range"])),np.log(np.maximum(train["range"],1)/100)))
    linear=np.linalg.solve(X.T@X+np.diag([0.,1e-3]),X.T@train["residual"])
    piecewise=np.vstack([np.mean(train["residual"][train["label"]==d],axis=0) for d in DISTANCES])
    return {"raw":None,"constant":constant,"linear":linear,"piecewise":piecewise}


def predict(name,model,ranges):
    ranges=np.asarray(ranges)
    if name=="raw": return np.zeros((len(ranges),2))
    if name=="constant": return np.broadcast_to(model,(len(ranges),2)).copy()
    if name=="linear":
        X=np.column_stack((np.ones(len(ranges)),np.log(np.maximum(ranges,1)/100)))
        return X@model
    return np.column_stack((np.interp(ranges,DISTANCES,model[:,0]),
                            np.interp(ranges,DISTANCES,model[:,1])))


def angular_errors(corrected,truth_angles):
    az,el=corrected[:,0],corrected[:,1]
    u=np.column_stack((np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)))
    ta,te=truth_angles[:,0],truth_angles[:,1]
    v=np.column_stack((np.cos(te)*np.cos(ta),np.cos(te)*np.sin(ta),np.sin(te)))
    return np.degrees(np.arccos(np.clip(np.sum(u*v,axis=1),-1,1)))


def select_model():
    train=collect(6,161001); validation=collect(3,162001); models=fit_models(train)
    truth=wrap_angle(validation["measured"]-validation["residual"]); scores={}
    for name,model in models.items():
        corrected=wrap_angle(validation["measured"]-predict(name,model,validation["range"]))
        errors=angular_errors(corrected,truth)
        per_distance={str(int(d)):float(np.sqrt(np.mean(errors[validation["label"]==d]**2))) for d in DISTANCES}
        overall=float(np.sqrt(np.mean(errors**2))); worst=max(per_distance.values())
        scores[name]={"overall_rmse_deg":overall,"worst_distance_rmse_deg":worst,
                      "robust_score":overall+0.25*worst,"per_distance":per_distance}
    selected=min(scores,key=lambda name:scores[name]["robust_score"])
    return selected,models[selected],scores,train,validation
