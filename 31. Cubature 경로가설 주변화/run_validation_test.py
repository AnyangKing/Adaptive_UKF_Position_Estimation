"""경로배정-상태 cubature 주변화 정책을 validation 선택 후 독립 test한다."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position
from path_identifiability import observed_peaks
from peak_adaptive import PeakMarginAdaptiveRUKF
from peak_measurement import extract_measurement
from soft_path_update import CubaturePathMarginalizer
from ukf import SignalObservationUKF, acceleration_process_covariance

DISTANCES=(100,200,400,600); STEPS=10


def trajectory(distance,split,index):
    root=311000 if split=='validation' else 312000; rng=np.random.default_rng(root+distance*20+index)
    az=rng.uniform(-np.pi,np.pi); depth=rng.uniform(12.,78.)
    start=np.array([distance*np.cos(az),distance*np.sin(az),-depth]); tangent=np.array([-np.sin(az),np.cos(az),0.])
    radial=np.array([np.cos(az),np.sin(az),0.]); t=np.arange(STEPS,dtype=float)
    truth=start+t[:,None]*(.72*tangent+rng.uniform(-.2,.2)*radial)
    meta={'snr_db':float(rng.choice([10.,20.,30.])), 'surface_reflection':float(-rng.uniform(.72,.97)),
          'bottom_reflection':float(rng.uniform(.32,.78)), 'radial_velocity_m_s':float(rng.uniform(-1.3,1.3))}
    return truth,meta


def collect(split,count=4):
    base=ChannelConfig(); data=[]; seedroot=313000 if split=='validation' else 314000
    for distance in DISTANCES:
        for index in range(count):
            truth,meta=trajectory(distance,split,index); observations=[]; qualities=[]; peaks=[]
            for k,position in enumerate(truth):
                cfg=replace(base,seed=seedroot+distance*100+index*20+k,**meta)
                _,received,_=synthesize_received(position,cfg); z,q=extract_measurement(received,cfg)
                times,strengths=observed_peaks(received[0],cfg,maximum=6)
                observations.append(z); qualities.append(q); peaks.append((times,strengths))
            data.append((distance,truth,np.asarray(observations),qualities,peaks))
    return base,data


def make_filter(initial,cfg):
    return SignalObservationUKF(np.r_[initial,np.zeros(3)],np.diag([8.**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.,.20),fixed_measurement_covariance(),cfg)


def evaluate(item,cfg,policy=None):
    _,truth,observations,qualities,peaks=item; initial=initialize_position(observations[0],cfg)
    wrapper=PeakMarginAdaptiveRUKF(make_filter(initial,cfg)); marginalizer=None
    if policy is not None: marginalizer=CubaturePathMarginalizer(cfg,**policy)
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)):
        wrapper.step(observations[k],qualities[k])
        if marginalizer is not None: marginalizer.update(wrapper.ukf,*peaks[k])
        estimate[k]=wrapper.ukf.x[:3]
    error=np.linalg.norm(estimate-truth,axis=1)
    result={'rmse_after_3_m':float(np.sqrt(np.mean(error[3:]**2))), 'max_error_m':float(np.max(error)),
            'diverged_over_50m':bool(np.any(error>50.))}
    if marginalizer is not None:
        applied=[h for h in marginalizer.history if h['applied']]
        result['mean_effective_points']=float(np.mean([h['effective_points'] for h in applied]))
        result['mean_max_weight']=float(np.mean([h['max_weight'] for h in applied]))
    return result


def aggregate(data,cfg,policy):
    records={}
    for d in DISTANCES:
        values=[evaluate(item,cfg,policy) for item in data if item[0]==d]
        records[str(d)]={'mean_rmse_m':float(np.mean([x['rmse_after_3_m'] for x in values])),
                         'p90_rmse_m':float(np.percentile([x['rmse_after_3_m'] for x in values],90)),
                         'max_rmse_m':float(np.max([x['rmse_after_3_m'] for x in values])),
                         'divergence_rate':float(np.mean([x['diverged_over_50m'] for x in values])),
                         'mean_effective_points':None if policy is None else float(np.mean([x['mean_effective_points'] for x in values]))}
    means=[records[str(d)]['mean_rmse_m'] for d in DISTANCES]
    score=float(np.mean(means)+.25*np.max(means)+100*sum(records[str(d)]['divergence_rate'] for d in DISTANCES))
    return {'robust_score':score,'records':records}


def run():
    cfg,validation=collect('validation'); policies={'baseline':None}
    for sigma_ms in (.25,.5,1.0):
        for temperature in (1.,2.):
            policies[f's{sigma_ms:g}_t{temperature:g}']={'timing_std_s':sigma_ms/1000.,'temperature':temperature,
                                                          'covariance_retention':0.0,'strength_weight':.5}
    validation_results={name:aggregate(validation,cfg,policy) for name,policy in policies.items()}
    selected=min(validation_results,key=lambda key:validation_results[key]['robust_score'])
    _,test=collect('test'); test_results={'baseline':aggregate(test,cfg,None),
                                         'selected':aggregate(test,cfg,policies[selected])}
    payload={'selected_on_validation':selected,'policies':policies,'validation':validation_results,'test':test_results}
    output=Path(__file__).resolve().parent/'results'; output.mkdir(exist_ok=True)
    (output/'cubature_path_marginalization.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps(payload,indent=2)); return payload


if __name__=='__main__': run()
