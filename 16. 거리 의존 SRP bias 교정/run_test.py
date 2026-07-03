"""validation 선택 거리의존 correction을 신규 거리별 동적 test에 적용."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from channel import synthesize_received
from config import ChannelConfig
from distance_bias import DISTANCES,predict,select_model
from measurement import fixed_measurement_covariance,initialize_position,signal_measurement,wrap_angle
from ukf import SignalObservationUKF,acceleration_process_covariance


def trajectory(distance,steps=12):
    az=2.05; depth=38.; start=np.array([distance*np.cos(az),distance*np.sin(az),-depth])
    tangent=np.array([-np.sin(az),np.cos(az),0.]); radial=np.array([np.cos(az),np.sin(az),0.])
    t=np.arange(steps,dtype=float)
    return start+t[:,None]*(0.70*tangent-0.20*radial)+np.column_stack((np.zeros(steps),np.zeros(steps),0.4*np.sin(t/3)))


def evaluate(observations,qualities,truth,cfg):
    initial=initialize_position(observations[0],cfg)
    wrapper=AdaptiveRUKF(SignalObservationUKF(np.r_[initial,np.zeros(3)],
        np.diag([8.**2]*3+[1.5**2]*3),acceleration_process_covariance(1.,0.20),
        fixed_measurement_covariance(),cfg))
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)): estimate[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1)
    return {"initial_error_m":float(error[0]),"rmse_after_3_m":float(np.sqrt(np.mean(error[3:]**2))),
            "max_error_m":float(np.max(error)),"final_error_m":float(error[-1]),
            "diverged_over_50m":bool(np.any(error>50))}


def run():
    selected,model,scores,_,_=select_model(); cfg=ChannelConfig(); results={}
    for distance in DISTANCES:
        truth=trajectory(distance); raw=[]; corrected=[]; qualities=[]
        for k,position in enumerate(truth):
            ping_cfg=replace(cfg,seed=163000+int(distance)*10+k,radial_velocity_m_s=0.65+0.1*np.sin(k/3),
                snr_db=20.,surface_reflection=-0.90,bottom_reflection=0.60)
            _,received,_=synthesize_received(position,ping_cfg); z,q=signal_measurement(received,ping_cfg)
            z[8]=q["srp_azimuth_rad"]; z[9]=q["srp_elevation_rad"]
            correction=predict(selected,model,np.array([z[0]]))[0]
            zc=z.copy(); zc[8:10]=wrap_angle(zc[8:10]-correction)
            raw.append(z); corrected.append(zc); qualities.append(q)
        results[str(int(distance))]={"raw":evaluate(np.asarray(raw),qualities,truth,cfg),
                                     "corrected":evaluate(np.asarray(corrected),qualities,truth,cfg)}
    payload={"selection":{"selected":selected,"validation_scores":scores,
        "model":None if model is None else np.asarray(model).tolist()},"test":results}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"distance_bias_test.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2)); return payload


if __name__=="__main__": run()
