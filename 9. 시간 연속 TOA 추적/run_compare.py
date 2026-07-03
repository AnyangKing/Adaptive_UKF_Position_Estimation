"""독립 ping 잡음의 200 m 궤적에서 strongest와 tracked TOA 비교."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from channel import synthesize_received
from config import ChannelConfig
from estimators import estimate_toa_tracked
from measurement import fixed_measurement_covariance, ideal_measurement, initialize_position, signal_measurement
from ukf import SignalObservationUKF, acceleration_process_covariance


def trajectory(steps=30):
    t=np.arange(steps,dtype=float)
    return np.column_stack((200+0.8*t,30+0.4*t,-25-0.12*t+0.5*np.sin(t/7)))


def make_filter(initial,cfg):
    return AdaptiveRUKF(SignalObservationUKF(
        np.r_[initial,np.zeros(3)],np.diag([8.0**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.0,0.20),fixed_measurement_covariance(),cfg))


def evaluate(observations,qualities,truth,cfg):
    initial=initialize_position(observations[0],cfg); wrapper=make_filter(initial,cfg)
    estimates=np.zeros_like(truth); estimates[0]=initial
    for k in range(1,len(truth)):
        estimates[k]=wrapper.step(observations[k],qualities[k])[:3]
    errors=np.linalg.norm(estimates-truth,axis=1)
    return {"initial_error_m":float(errors[0]),"rmse_all_m":float(np.sqrt(np.mean(errors**2))),
        "rmse_after_5_m":float(np.sqrt(np.mean(errors[5:]**2))),
        "max_error_m":float(np.max(errors)),"final_error_m":float(errors[-1])},estimates,errors


def run():
    cfg=ChannelConfig(); truth=trajectory(); strongest=[]; tracked=[]; qualities=[]
    previous=None; fallback_count=0; toa_errors_strong=[]; toa_errors_track=[]
    for k,position in enumerate(truth):
        ping_cfg=replace(cfg,seed=93001+k,radial_velocity_m_s=0.6+0.2*np.sin(k/5))
        _,received,_=synthesize_received(position,ping_cfg)
        z,q=signal_measurement(received,ping_cfg)
        tracked_toas,_,fallback=estimate_toa_tracked(received,ping_cfg,previous)
        previous=tracked_toas; fallback_count+=int(np.sum(fallback))
        z_tracked=z.copy(); z_tracked[0]=ping_cfg.sound_speed_m_s*tracked_toas[0]
        strongest.append(z); tracked.append(z_tracked); qualities.append(q)
        ideal=ideal_measurement(position,ping_cfg)
        toa_errors_strong.append(z[0]-ideal[0]); toa_errors_track.append(z_tracked[0]-ideal[0])
    strongest=np.asarray(strongest); tracked=np.asarray(tracked)
    strong_metrics,strong_est,strong_err=evaluate(strongest,qualities,truth,cfg)
    track_metrics,track_est,track_err=evaluate(tracked,qualities,truth,cfg)
    result={"strongest_peak":strong_metrics,"tracked_peak":track_metrics,
        "improvement_after_5_percent":100*(strong_metrics["rmse_after_5_m"]-track_metrics["rmse_after_5_m"])/strong_metrics["rmse_after_5_m"],
        "strongest_toa_range_rmse_m":float(np.sqrt(np.mean(np.asarray(toa_errors_strong)**2))),
        "tracked_toa_range_rmse_m":float(np.sqrt(np.mean(np.asarray(toa_errors_track)**2))),
        "fallback_sensor_ping_rate":fallback_count/(8*len(truth))}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"tracked_toa_comparison.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    np.savez(output/"tracked_toa_comparison.npz",truth=truth,strongest=strong_est,tracked=track_est,
             strongest_errors=strong_err,tracked_errors=track_err,
             strongest_toa_errors=toa_errors_strong,tracked_toa_errors=toa_errors_track)
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
