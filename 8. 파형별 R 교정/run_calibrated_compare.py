"""독립 calibration과 test split에서 파형별 R 교정 효과를 평가한다."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from calibration import estimate_calibration
from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position, signal_measurement, wrap_angle
from ukf import SignalObservationUKF, acceleration_process_covariance


def test_trajectory(steps=30):
    t=np.arange(steps,dtype=float)
    return np.column_stack((200+0.8*t,30+0.4*t,-25-0.12*t+0.5*np.sin(t/7)))


def collect_test_observations(duration_s,truth):
    observations=[]; qualities=[]
    base=replace(ChannelConfig(),pulse_duration_s=duration_s)
    for k,position in enumerate(truth):
        # calibration seed(81001~)와 겹치지 않고 매 ping마다 독립 잡음을 사용한다.
        cfg=replace(base,seed=92001+k,radial_velocity_m_s=0.6+0.2*np.sin(k/5))
        _,received,_=synthesize_received(position,cfg)
        z,q=signal_measurement(received,cfg); observations.append(z); qualities.append(q)
    return base,np.asarray(observations),qualities


def run_filter(cfg,observations,qualities,truth,R,bias):
    corrected=observations-np.asarray(bias)
    corrected[:,8:]=wrap_angle(corrected[:,8:])
    initial=initialize_position(corrected[0],cfg)
    wrapper=AdaptiveRUKF(SignalObservationUKF(
        np.r_[initial,np.zeros(3)],np.diag([8.0**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.0,0.20),R,cfg))
    estimates=np.zeros_like(truth); estimates[0]=initial
    for k in range(1,len(truth)):
        estimates[k]=wrapper.step(corrected[k],qualities[k])[:3]
    errors=np.linalg.norm(estimates-truth,axis=1)
    return {"initial_error_m":float(errors[0]),"rmse_all_m":float(np.sqrt(np.mean(errors**2))),
        "rmse_after_5_m":float(np.sqrt(np.mean(errors[5:]**2))),
        "max_error_m":float(np.max(errors)),"final_error_m":float(errors[-1])},estimates,errors


def run():
    truth=test_trajectory(); result={}; arrays={"truth":truth}; calibration_info={}
    for duration_ms in (5,10):
        duration_s=duration_ms/1000.0
        bias,R,residuals=estimate_calibration(duration_s)
        cfg,observations,qualities=collect_test_observations(duration_s,truth)
        default,default_est,default_err=run_filter(
            cfg,observations,qualities,truth,fixed_measurement_covariance(),np.zeros(10))
        calibrated,cal_est,cal_err=run_filter(cfg,observations,qualities,truth,R,bias)
        key=f"{duration_ms}ms"
        result[key]={"default":default,"calibrated":calibrated,
            "improvement_after_5_percent":100*(default["rmse_after_5_m"]-calibrated["rmse_after_5_m"])/default["rmse_after_5_m"]}
        calibration_info[key]={"bias":bias.tolist(),"std":np.sqrt(np.diag(R)).tolist(),
            "min_eigenvalue":float(np.min(np.linalg.eigvalsh(R)))}
        arrays.update({f"{key}_default":default_est,f"{key}_calibrated":cal_est,
                       f"{key}_default_errors":default_err,f"{key}_calibrated_errors":cal_err,
                       f"{key}_calibration_residuals":residuals})
    payload={"split":{"calibration_seed":81001,"test_seed_start":92001,
        "calibration_samples_per_waveform":30,"test_steps":30},
        "results":result,"calibration":calibration_info}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"calibrated_comparison.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    np.savez(output/"calibrated_comparison.npz",**arrays)
    print(json.dumps(payload,indent=2)); return payload


if __name__=="__main__": run()
