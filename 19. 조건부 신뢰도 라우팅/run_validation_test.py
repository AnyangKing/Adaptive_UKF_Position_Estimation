"""조건부 routing 문턱을 validation에서 선택하고 별도 test에서 평가."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from conditional_adaptive import ConditionalAdaptiveRUKF
from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance,initialize_position,signal_measurement
from ukf import SignalObservationUKF,acceleration_process_covariance


DISTANCES=(100,200,400,600)


def trajectory(distance,split,steps=10):
    az=-0.45 if split=="validation" else 2.45; depth=22. if split=="validation" else 58.
    start=np.array([distance*np.cos(az),distance*np.sin(az),-depth])
    tangent=np.array([-np.sin(az),np.cos(az),0.]); radial=np.array([np.cos(az),np.sin(az),0.])
    t=np.arange(steps,dtype=float); velocity=(0.65*tangent+0.18*radial) if split=="validation" else (0.72*tangent-0.12*radial)
    return start+t[:,None]*velocity+np.column_stack((np.zeros(steps),np.zeros(steps),0.4*np.sin(t/3)))


def collect(split):
    cfg=ChannelConfig(); datasets={}; seed_root=191000 if split=="validation" else 192000
    for distance in DISTANCES:
        truth=trajectory(distance,split); observations=[]; qualities=[]
        for k,position in enumerate(truth):
            if split=="validation":
                snr=(10.,15.,20.)[k%3]; surface=-0.96; bottom=0.72
            else: snr=20.; surface=-0.90; bottom=0.60
            ping_cfg=replace(cfg,seed=seed_root+distance*10+k,snr_db=snr,
                surface_reflection=surface,bottom_reflection=bottom,
                radial_velocity_m_s=0.65+0.15*np.sin(k/3))
            _,received,_=synthesize_received(position,ping_cfg); z,q=signal_measurement(received,ping_cfg)
            z[8]=q["srp_azimuth_rad"]; z[9]=q["srp_elevation_rad"]
            observations.append(z); qualities.append(q)
        datasets[distance]=(truth,np.asarray(observations),qualities)
    return cfg,datasets


def make_core(initial,cfg):
    return SignalObservationUKF(np.r_[initial,np.zeros(3)],np.diag([8.**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.,0.20),fixed_measurement_covariance(),cfg)


def evaluate(dataset,cfg,policy):
    truth,observations,qualities=dataset; initial=initialize_position(observations[0],cfg)
    wrapper=AdaptiveRUKF(make_core(initial,cfg)) if policy=="old" else ConditionalAdaptiveRUKF(make_core(initial,cfg),policy)
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)): estimate[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1)
    activation=0.0 if policy=="old" else float(np.mean([h["routed"] for h in wrapper.history]))
    return {"rmse_after_3_m":float(np.sqrt(np.mean(error[3:]**2))),"max_error_m":float(np.max(error)),
        "final_error_m":float(error[-1]),"diverged_over_50m":bool(np.any(error>50)),
        "routing_activation_rate":activation}


def validate():
    cfg,data=collect("validation"); candidates=["old",5.,10.,15.,20.]; scores={}
    for candidate in candidates:
        records={str(d):evaluate(data[d],cfg,candidate) for d in DISTANCES}
        rmses=[r["rmse_after_3_m"] for r in records.values()]; divergence=sum(r["diverged_over_50m"] for r in records.values())
        robust=float(np.mean(rmses)+0.25*np.max(rmses)+100*divergence)
        scores[str(candidate)]={"robust_score":robust,"mean_rmse_m":float(np.mean(rmses)),
            "worst_rmse_m":float(np.max(rmses)),"records":records}
    selected=min(candidates,key=lambda c:scores[str(c)]["robust_score"])
    return selected,scores


def run():
    selected,scores=validate(); cfg,test_data=collect("test")
    test={str(d):{"old":evaluate(test_data[d],cfg,"old"),
                  "selected":evaluate(test_data[d],cfg,selected)} for d in DISTANCES}
    payload={"selection":{"selected":selected,"validation":scores},"test":test}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"conditional_routing.json").write_text(json.dumps(payload,indent=2),encoding="utf-8")
    print(json.dumps(payload,indent=2)); return payload


if __name__=="__main__": run()
