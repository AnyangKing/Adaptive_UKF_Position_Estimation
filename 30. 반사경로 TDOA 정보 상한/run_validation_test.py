"""Oracle 경로연관으로 반사경로 TDOA가 줄 수 있는 위치정보 상한을 측정한다."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from augmented_ukf import AugmentedUKF, ConditionalWrapper, augmented_measurement, acceleration_process_covariance
from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position
from path_identifiability import observed_peaks
from peak_measurement import extract_measurement

DISTANCES=(100,200,400,600); STEPS=10


def trajectory(distance,split,index):
    root=301000 if split=='validation' else 302000; rng=np.random.default_rng(root+distance*20+index)
    az=rng.uniform(-np.pi,np.pi); depth=rng.uniform(12.,78.)
    start=np.array([distance*np.cos(az),distance*np.sin(az),-depth]); tangent=np.array([-np.sin(az),np.cos(az),0.])
    radial=np.array([np.cos(az),np.sin(az),0.]); t=np.arange(STEPS,dtype=float)
    truth=start+t[:,None]*(0.72*tangent+rng.uniform(-.2,.2)*radial)
    meta={'snr_db':float(rng.choice([10.,20.,30.])), 'surface_reflection':float(-rng.uniform(.72,.97)),
          'bottom_reflection':float(rng.uniform(.32,.78)), 'radial_velocity_m_s':float(rng.uniform(-1.3,1.3))}
    return truth,meta


def oracle_path_observation(received,all_paths,cfg):
    values=[]
    for signal,paths in zip(received,all_paths):
        times,_=observed_peaks(signal,cfg,maximum=8); selected=[]
        for path in paths: selected.append(times[int(np.argmin(np.abs(times-path.delay_s)))])
        values.extend((cfg.sound_speed_m_s*(selected[1]-selected[0]),
                       cfg.sound_speed_m_s*(selected[2]-selected[0])))
    return np.asarray(values)


def collect(split,count=4):
    base=ChannelConfig(); data=[]; seedroot=303000 if split=='validation' else 304000
    for distance in DISTANCES:
        for index in range(count):
            truth,meta=trajectory(distance,split,index); obs=[]; qualities=[]
            for k,position in enumerate(truth):
                cfg=replace(base,seed=seedroot+distance*100+index*20+k,**meta)
                _,received,paths=synthesize_received(position,cfg); z,q=extract_measurement(received,cfg)
                obs.append(np.r_[z,oracle_path_observation(received,paths,cfg)]); qualities.append(q)
            data.append((distance,truth,np.asarray(obs),qualities))
    return base,data


def calibrate(cfg,data):
    residuals=[]
    for _,truth,obs,_ in data:
        residuals.extend([row[10:]-augmented_measurement(position,cfg,'all')[10:] for position,row in zip(truth,obs)])
    residuals=np.asarray(residuals); std=np.maximum(np.std(residuals,axis=0,ddof=1),0.03)
    return std


def evaluate(item,cfg,path_std,path_mode):
    _,truth,obs,qualities=item; initial=initialize_position(obs[0,:10],cfg)
    R=fixed_measurement_covariance()
    selected_std=path_std[:2] if path_mode=='reference' else path_std
    if path_mode!='none': R=np.diag(np.r_[np.diag(R),selected_std**2])
    ukf=AugmentedUKF(np.r_[initial,np.zeros(3)],np.diag([8.**2]*3+[1.5**2]*3),
                     acceleration_process_covariance(1.,.20),R,cfg,path_mode)
    wrapper=ConditionalWrapper(ukf); estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)):
        z=obs[k,:10] if path_mode=='none' else (obs[k,:12] if path_mode=='reference' else obs[k])
        estimate[k]=wrapper.step(z,qualities[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1)
    return float(np.sqrt(np.mean(error[3:]**2)))


def aggregate(data,cfg,path_std,path_mode):
    return {str(d): {'mean_rmse_m':float(np.mean(values)),'p90_rmse_m':float(np.percentile(values,90)),
                     'max_rmse_m':float(np.max(values))}
            for d in DISTANCES for values in [[evaluate(x,cfg,path_std,path_mode) for x in data if x[0]==d]]}


def run():
    cfg,validation=collect('validation'); path_std=calibrate(cfg,validation)
    modes=('none','reference','all')
    val={mode:aggregate(validation,cfg,path_std,mode) for mode in modes}
    def robust_score(records):
        values=[records[str(d)]['mean_rmse_m'] for d in DISTANCES]
        return float(np.mean(values)+.25*np.max(values))
    selected=min(modes,key=lambda mode:robust_score(val[mode]))
    _,test=collect('test'); result={mode:aggregate(test,cfg,path_std,mode) for mode in ('none',selected)}
    payload={'calibrated_path_std_m':path_std.tolist(),'selected_on_validation':selected,
             'validation_scores':{m:robust_score(val[m]) for m in modes},'validation':val,'test':result}
    output=Path(__file__).resolve().parent/'results'; output.mkdir(exist_ok=True)
    (output/'multipath_information_upper_bound.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps(payload,indent=2)); return payload


if __name__=='__main__': run()
