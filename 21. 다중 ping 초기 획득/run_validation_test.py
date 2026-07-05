"""1/3/5 ping SRP 구면평균 초기화를 validation 선택 후 독립 test 평가."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from conditional_adaptive import ConditionalAdaptiveRUKF
from config import ChannelConfig
from measurement import fixed_measurement_covariance,initialize_position,signal_measurement
from ukf import SignalObservationUKF,acceleration_process_covariance


DISTANCES=(100,200,400,600); STEPS=12; EVAL_START=6


def trajectory(distance,split):
    az=1.55 if split=="validation" else -2.75; depth=34. if split=="validation" else 18.
    start=np.array([distance*np.cos(az),distance*np.sin(az),-depth])
    tangent=np.array([-np.sin(az),np.cos(az),0.]); radial=np.array([np.cos(az),np.sin(az),0.])
    t=np.arange(STEPS,dtype=float); velocity=(0.72*tangent+0.12*radial) if split=="validation" else (0.65*tangent-0.18*radial)
    return start+t[:,None]*velocity+np.column_stack((np.zeros(STEPS),np.zeros(STEPS),0.4*np.sin(t/3)))


def collect(split):
    cfg=ChannelConfig(); seed_root=211000 if split=="validation" else 212000; data={}
    for distance in DISTANCES:
        truth=trajectory(distance,split); observations=[]; qualities=[]
        for k,position in enumerate(truth):
            ping_cfg=replace(cfg,seed=seed_root+distance*10+k,snr_db=20.,surface_reflection=-0.90,
                bottom_reflection=0.60,radial_velocity_m_s=0.6+0.12*np.sin(k/3))
            _,received,_=synthesize_received(position,ping_cfg); z,q=signal_measurement(received,ping_cfg)
            z[8]=q["srp_azimuth_rad"]; z[9]=q["srp_elevation_rad"]
            observations.append(z); qualities.append(q)
        data[distance]=(truth,np.asarray(observations),qualities)
    return cfg,data


def averaged_initial_observation(observations,count):
    z=observations[count-1].copy(); az=observations[:count,8]; el=observations[:count,9]
    directions=np.column_stack((np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)))
    mean=np.mean(directions,axis=0); mean/=np.linalg.norm(mean)
    z[8]=np.arctan2(mean[1],mean[0]); z[9]=np.arctan2(mean[2],np.hypot(mean[0],mean[1]))
    # 현재 시점 거리관측을 유지하여 이동 중 과거 range 평균 bias를 피한다.
    return z


def evaluate(dataset,cfg,count):
    truth,observations,qualities=dataset; start=count-1
    initial_z=averaged_initial_observation(observations,count); initial=initialize_position(initial_z,cfg)
    wrapper=ConditionalAdaptiveRUKF(SignalObservationUKF(np.r_[initial,np.zeros(3)],
        np.diag([8.**2]*3+[1.5**2]*3),acceleration_process_covariance(1.,0.20),
        fixed_measurement_covariance(),cfg),5.)
    estimate=np.full_like(truth,np.nan); estimate[start]=initial
    for k in range(start+1,len(truth)): estimate[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=np.linalg.norm(estimate[EVAL_START:]-truth[EVAL_START:],axis=1)
    initial_error=float(np.linalg.norm(initial-truth[start]))
    return {"acquisition_delay_pings":start,"initial_error_m":initial_error,
        "rmse_from_common_step_m":float(np.sqrt(np.mean(error**2))),"max_error_m":float(np.max(error)),
        "final_error_m":float(error[-1]),"diverged_over_50m":bool(np.any(error>50))}


def validate():
    cfg,data=collect("validation"); scores={}
    for count in (1,3,5):
        records={str(d):evaluate(data[d],cfg,count) for d in DISTANCES}
        values=[r["rmse_from_common_step_m"] for r in records.values()]
        score=float(np.mean(values)+0.25*np.max(values)+100*sum(r["diverged_over_50m"] for r in records.values()))
        scores[str(count)]={"robust_score":score,"mean_rmse_m":float(np.mean(values)),
                            "worst_rmse_m":float(np.max(values)),"records":records}
    selected=min((1,3,5),key=lambda c:scores[str(c)]["robust_score"])
    return selected,scores


def run():
    selected,scores=validate(); cfg,data=collect("test")
    test={str(d):{"single_ping":evaluate(data[d],cfg,1),"selected":evaluate(data[d],cfg,selected)} for d in DISTANCES}
    payload={"selection":{"selected_ping_count":selected,"validation":scores,
        "common_evaluation_start_step":EVAL_START},"test":test}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"multiping_initialization.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2)); return payload


if __name__=="__main__": run()
