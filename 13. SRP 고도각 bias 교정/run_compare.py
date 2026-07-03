"""validation 선택 SRP bias 보정을 독립 200 m test UKF에 적용."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from bias_model import predict,train_and_select
from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position, signal_measurement, wrap_angle
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
    for k in range(1,len(truth)):
        estimates[k]=wrapper.step(observations[k],qualities[k])[:3]
    errors=np.linalg.norm(estimates-truth,axis=1)
    return {"initial_error_m":float(errors[0]),"rmse_after_5_m":float(np.sqrt(np.mean(errors[5:]**2))),
        "max_error_m":float(np.max(errors)),"final_error_m":float(errors[-1])},estimates


def run():
    selected,model,scores,_,_=train_and_select(); cfg=ChannelConfig(); truth=trajectory()
    raw=[]; corrected=[]; qualities=[]
    for k,position in enumerate(truth):
        ping_cfg=replace(cfg,seed=93001+k,radial_velocity_m_s=0.6+0.2*np.sin(k/5))
        _,received,_=synthesize_received(position,ping_cfg); z,q=signal_measurement(received,ping_cfg)
        measured=np.array([[q["srp_azimuth_rad"],q["srp_elevation_rad"]]])
        correction=predict(selected,model,np.array([z[0]]),measured)[0]
        z_raw=z.copy(); z_raw[8:10]=measured[0]
        z_corrected=z_raw.copy(); z_corrected[8:10]=wrap_angle(measured[0]-correction)
        raw.append(z_raw); corrected.append(z_corrected); qualities.append(q)
    raw_metrics,raw_est=evaluate(np.asarray(raw),qualities,truth,cfg)
    corrected_metrics,corrected_est=evaluate(np.asarray(corrected),qualities,truth,cfg)
    result={"selection":{"selected":selected,"validation_doa_rmse_deg":scores,
        "model":np.asarray(model).tolist()},"raw":raw_metrics,"corrected":corrected_metrics,
        "improvement_after_5_percent":100*(raw_metrics["rmse_after_5_m"]-corrected_metrics["rmse_after_5_m"])/raw_metrics["rmse_after_5_m"]}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"srp_bias_correction.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    np.savez(output/"srp_bias_correction.npz",truth=truth,raw=raw_est,corrected=corrected_est)
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
