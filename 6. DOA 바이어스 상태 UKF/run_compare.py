"""6차원 adaptive UKF와 8차원 DOA-bias adaptive UKF 비교."""

from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from bias_ukf import DOABiasUKF, bias_process_covariance
from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, ideal_measurement, initialize_position, signal_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


def trajectory(steps=30):
    t=np.arange(steps,dtype=float)
    return np.column_stack((100+0.75*t,20+0.35*t,-20-0.10*t+0.4*np.sin(t/8)))


def position_metrics(estimates, truth):
    errors=np.linalg.norm(estimates-truth,axis=1)
    return {"rmse_all_m":float(np.sqrt(np.mean(errors**2))),
            "rmse_after_5_m":float(np.sqrt(np.mean(errors[5:]**2))),
            "max_error_m":float(np.max(errors)),"final_error_m":float(errors[-1])}, errors


def run():
    cfg=ChannelConfig(); truth=trajectory(); observations=[]; qualities=[]; true_observation_bias=[]
    for position in truth:
        _, received, _=synthesize_received(position,cfg)
        z,q=signal_measurement(received,cfg); observations.append(z); qualities.append(q)
        delta=z-ideal_measurement(position,cfg)
        delta[8:]=(delta[8:]+np.pi)%(2*np.pi)-np.pi
        true_observation_bias.append(delta[8:])
    observations=np.asarray(observations); true_observation_bias=np.asarray(true_observation_bias)
    initial=initialize_position(observations[0],cfg); base_R=fixed_measurement_covariance()
    base=AdaptiveRUKF(SignalObservationUKF(
        np.r_[initial,np.zeros(3)],np.diag([5.0**2]*3+[1.0**2]*3),
        acceleration_process_covariance(1.0,0.20),base_R,cfg))
    bias=AdaptiveRUKF(DOABiasUKF(
        np.r_[initial,np.zeros(3),0.0,0.0],
        np.diag([5.0**2]*3+[1.0**2]*3+[np.radians(5.0)**2]*2),
        bias_process_covariance(),base_R,cfg))
    base_est=np.zeros_like(truth); bias_est=np.zeros_like(truth)
    bias_state=np.zeros((len(truth),2)); base_est[0]=bias_est[0]=initial
    for k in range(1,len(truth)):
        base_est[k]=base.step(observations[k],qualities[k])[:3]
        state=bias.step(observations[k],qualities[k]); bias_est[k]=state[:3]; bias_state[k]=state[6:8]
    base_metrics,base_errors=position_metrics(base_est,truth)
    bias_metrics,bias_errors=position_metrics(bias_est,truth)
    result={"six_state_adaptive":base_metrics,"eight_state_bias":bias_metrics,
        "improvement_after_5_percent":100*(base_metrics["rmse_after_5_m"]-bias_metrics["rmse_after_5_m"])/base_metrics["rmse_after_5_m"],
        "final_estimated_az_bias_deg":float(np.degrees(bias_state[-1,0])),
        "final_estimated_el_bias_deg":float(np.degrees(bias_state[-1,1])),
        "mean_observed_az_error_deg":float(np.degrees(np.mean(true_observation_bias[:,0]))),
        "mean_observed_el_error_deg":float(np.degrees(np.mean(true_observation_bias[:,1])))}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"bias_comparison.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    np.savez(output/"bias_comparison.npz",truth=truth,base=base_est,bias=bias_est,
             bias_state=bias_state,observed_angle_error=true_observation_bias,
             base_errors=base_errors,bias_errors=bias_errors)
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
