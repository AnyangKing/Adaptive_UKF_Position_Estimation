"""10 ms 기준과 sweep에서 선택한 5 ms 파형의 adaptive UKF 비교."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position, signal_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


def trajectory(steps=30):
    t=np.arange(steps,dtype=float)
    return np.column_stack((100+0.75*t,20+0.35*t,-20-0.10*t+0.4*np.sin(t/8)))


def run_filter(duration_s,truth):
    cfg=replace(ChannelConfig(),pulse_duration_s=duration_s)
    observations=[]; qualities=[]
    for position in truth:
        _,received,_=synthesize_received(position,cfg)
        z,q=signal_measurement(received,cfg); observations.append(z); qualities.append(q)
    observations=np.asarray(observations); initial=initialize_position(observations[0],cfg)
    wrapper=AdaptiveRUKF(SignalObservationUKF(
        np.r_[initial,np.zeros(3)],np.diag([5.0**2]*3+[1.0**2]*3),
        acceleration_process_covariance(1.0,0.20),fixed_measurement_covariance(),cfg))
    estimates=np.zeros_like(truth); estimates[0]=initial
    for k in range(1,len(truth)):
        estimates[k]=wrapper.step(observations[k],qualities[k])[:3]
    errors=np.linalg.norm(estimates-truth,axis=1)
    metrics={"initial_error_m":float(errors[0]),"rmse_all_m":float(np.sqrt(np.mean(errors**2))),
        "rmse_after_5_m":float(np.sqrt(np.mean(errors[5:]**2))),
        "max_error_m":float(np.max(errors)),"final_error_m":float(errors[-1]),
        "mean_doa_disagreement_deg":float(np.mean([q["doa_disagreement_deg"] for q in qualities]))}
    return metrics,estimates,errors


def run():
    truth=trajectory(); ten,ten_est,ten_err=run_filter(0.010,truth)
    five,five_est,five_err=run_filter(0.005,truth)
    result={"10ms":ten,"5ms":five,
        "rmse_after_5_improvement_percent":100*(ten["rmse_after_5_m"]-five["rmse_after_5_m"])/ten["rmse_after_5_m"]}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"waveform_ukf_comparison.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    np.savez(output/"waveform_ukf_comparison.npz",truth=truth,ten_ms=ten_est,five_ms=five_est,
             ten_ms_errors=ten_err,five_ms_errors=five_err)
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
