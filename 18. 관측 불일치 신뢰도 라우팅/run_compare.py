"""기존 DOA 감쇠와 신규 TDOA 감쇠 adaptive routing의 거리별 비교."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from adaptive import AdaptiveRUKF
from routed_adaptive import RoutedAdaptiveRUKF
from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance,initialize_position,signal_measurement
from ukf import SignalObservationUKF,acceleration_process_covariance


def trajectory(distance,steps=15):
    az=0.90; depth=42.; start=np.array([distance*np.cos(az),distance*np.sin(az),-depth])
    tangent=np.array([-np.sin(az),np.cos(az),0.]); radial=np.array([np.cos(az),np.sin(az),0.])
    t=np.arange(steps,dtype=float)
    return start+t[:,None]*(0.70*tangent+0.10*radial)+np.column_stack((np.zeros(steps),np.zeros(steps),0.45*np.sin(t/4)))


def make_core(initial,cfg):
    return SignalObservationUKF(np.r_[initial,np.zeros(3)],np.diag([8.**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.,0.20),fixed_measurement_covariance(),cfg)


def evaluate(observations,qualities,truth,cfg,mode):
    initial=initialize_position(observations[0],cfg)
    wrapper=AdaptiveRUKF(make_core(initial,cfg)) if mode=="old" else RoutedAdaptiveRUKF(make_core(initial,cfg))
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)): estimate[k]=wrapper.step(observations[k],qualities[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1)
    return {"initial_error_m":float(error[0]),"rmse_after_5_m":float(np.sqrt(np.mean(error[5:]**2))),
        "max_error_m":float(np.max(error)),"final_error_m":float(error[-1]),
        "diverged_over_50m":bool(np.any(error>50)),
        "mean_disagreement_deg":float(np.mean([q["doa_disagreement_deg"] for q in qualities]))},estimate


def run():
    cfg=ChannelConfig(); result={}; arrays={}
    for distance in (100,200,400,600):
        truth=trajectory(distance); observations=[]; qualities=[]
        for k,position in enumerate(truth):
            ping_cfg=replace(cfg,seed=180000+distance*10+k,radial_velocity_m_s=0.6+0.15*np.sin(k/4),
                snr_db=20.,surface_reflection=-0.90,bottom_reflection=0.60)
            _,received,_=synthesize_received(position,ping_cfg); z,q=signal_measurement(received,ping_cfg)
            z[8]=q["srp_azimuth_rad"]; z[9]=q["srp_elevation_rad"]
            observations.append(z); qualities.append(q)
        observations=np.asarray(observations); old,old_est=evaluate(observations,qualities,truth,cfg,"old")
        routed,routed_est=evaluate(observations,qualities,truth,cfg,"routed")
        result[str(distance)]={"old_doa_downweight":old,"routed_tdoa_downweight":routed,
            "improvement_percent":100*(old["rmse_after_5_m"]-routed["rmse_after_5_m"])/old["rmse_after_5_m"]}
        arrays.update({f"truth_{distance}":truth,f"old_{distance}":old_est,f"routed_{distance}":routed_est})
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"routing_comparison.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    np.savez(output/"routing_comparison.npz",**arrays)
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
