"""SRP signed angle residual의 독립 calibration/validation 보정 모델."""

from dataclasses import replace
import numpy as np

from channel import synthesize_received
from config import ChannelConfig, usb_array_global_m
from measurement import signal_measurement, wrap_angle


def scenarios(count,seed):
    rng=np.random.default_rng(seed); result=[]
    for index in range(count):
        distance=rng.uniform(80.0,650.0); az=rng.uniform(-np.pi,np.pi)
        source=np.array([distance*np.cos(az),distance*np.sin(az),-rng.uniform(8.0,88.0)])
        cfg=replace(ChannelConfig(),pulse_duration_s=0.005,seed=seed+index,snr_db=float(rng.uniform(10,30)),
            surface_reflection=float(-rng.uniform(0.70,0.98)),
            bottom_reflection=float(rng.uniform(0.30,0.80)),
            radial_velocity_m_s=float(rng.uniform(-1.5,1.5)))
        result.append((source,cfg))
    return result


def collect(count,seed):
    rows=[]
    center=usb_array_global_m().mean(axis=0)
    for source,cfg in scenarios(count,seed):
        _,received,_=synthesize_received(source,cfg); z,q=signal_measurement(received,cfg)
        measured=np.array([q["srp_azimuth_rad"],q["srp_elevation_rad"]])
        delta=source-center
        truth=np.array([np.arctan2(delta[1],delta[0]),
            np.arctan2(delta[2],np.hypot(delta[0],delta[1]))])
        residual=wrap_angle(measured-truth)
        rows.append((z[0],measured,residual,truth))
    ranges=np.array([r[0] for r in rows]); measured=np.vstack([r[1] for r in rows])
    residual=np.vstack([r[2] for r in rows]); truth=np.vstack([r[3] for r in rows])
    return ranges,measured,residual,truth


def features(ranges,measured):
    log_range=np.log(np.maximum(ranges,1.0)/100.0)
    elevation=measured[:,1]
    return np.column_stack((np.ones(len(ranges)),log_range,elevation,elevation**2))


def fit_models(ranges,measured,residual):
    constant=np.mean(residual,axis=0)
    X=features(ranges,measured); penalty=np.diag([0.0,1e-3,1e-3,1e-3])
    ridge=np.linalg.solve(X.T@X+penalty,X.T@residual)
    return {"constant":constant,"ridge":ridge}


def predict(model_name,model,ranges,measured):
    if model_name=="constant":
        return np.broadcast_to(model,(len(ranges),2)).copy()
    return features(ranges,measured)@model


def angular_rmse(measured,truth):
    az,el=measured[:,0],measured[:,1]
    u=np.column_stack((np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)))
    ta,te=truth[:,0],truth[:,1]
    v=np.column_stack((np.cos(te)*np.cos(ta),np.cos(te)*np.sin(ta),np.sin(te)))
    error=np.degrees(np.arccos(np.clip(np.sum(u*v,axis=1),-1,1)))
    return float(np.sqrt(np.mean(error**2)))


def train_and_select():
    train=collect(30,131001); validation=collect(15,132001)
    models=fit_models(train[0],train[1],train[2]); scores={"raw":angular_rmse(validation[1],validation[3])}
    for name,model in models.items():
        corrected=wrap_angle(validation[1]-predict(name,model,validation[0],validation[1]))
        scores[name]=angular_rmse(corrected,validation[3])
    selected=min(("constant","ridge"),key=lambda name:scores[name])
    return selected,models[selected],scores,train,validation
