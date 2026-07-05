"""Trust-region 경로 주변화 반경을 validation에서 선택하고 독립 test한다."""

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

DISTANCES=(100,200,400,600); STEPS=10; COUNT=4
BASE_POLICY={'timing_std_s':.001,'temperature':1.,'covariance_retention':0.,'strength_weight':.5}


def trajectory(distance,split,index):
    root=331000 if split=='validation' else 332000; rng=np.random.default_rng(root+distance*20+index)
    az=rng.uniform(-np.pi,np.pi); depth=rng.uniform(12.,78.)
    start=np.array([distance*np.cos(az),distance*np.sin(az),-depth]); tangent=np.array([-np.sin(az),np.cos(az),0.])
    radial=np.array([np.cos(az),np.sin(az),0.]); t=np.arange(STEPS,dtype=float)
    truth=start+t[:,None]*(.72*tangent+rng.uniform(-.2,.2)*radial)
    meta={'snr_db':float(rng.choice([10.,20.,30.])), 'surface_reflection':float(-rng.uniform(.72,.97)),
          'bottom_reflection':float(rng.uniform(.32,.78)), 'radial_velocity_m_s':float(rng.uniform(-1.3,1.3))}
    return truth,meta


def collect(split):
    base=ChannelConfig(); data=[]; seedroot=333000 if split=='validation' else 334000
    for distance in DISTANCES:
        for index in range(COUNT):
            truth,meta=trajectory(distance,split,index); observations=[]; qualities=[]; peaks=[]
            for k,position in enumerate(truth):
                cfg=replace(base,seed=seedroot+distance*100+index*20+k,**meta)
                _,received,_=synthesize_received(position,cfg); z,q=extract_measurement(received,cfg)
                times,strengths=observed_peaks(received[0],cfg,maximum=6)
                observations.append(z); qualities.append(q); peaks.append((times,strengths))
            data.append((distance,index,truth,np.asarray(observations),qualities,peaks))
    return base,data


def make_filter(initial,cfg):
    return SignalObservationUKF(np.r_[initial,np.zeros(3)],np.diag([8.**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.,.20),fixed_measurement_covariance(),cfg)


def evaluate(item,cfg,radius):
    _,_,truth,observations,qualities,peaks=item; initial=initialize_position(observations[0],cfg)
    wrapper=PeakMarginAdaptiveRUKF(make_filter(initial,cfg)); marginalizer=None
    if radius!='baseline': marginalizer=CubaturePathMarginalizer(cfg,**BASE_POLICY,trust_radius=radius)
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)):
        wrapper.step(observations[k],qualities[k])
        if marginalizer is not None: marginalizer.update(wrapper.ukf,*peaks[k])
        estimate[k]=wrapper.ukf.x[:3]
    error=np.linalg.norm(estimate-truth,axis=1); tail=error[3:]
    result={'rmse_m':float(np.sqrt(np.mean(tail**2))),'diverged':bool(np.any(tail>50.))}
    if marginalizer is not None:
        h=[x for x in marginalizer.history if x['applied']]
        result['limited_rate']=float(np.mean([x['blend']<.999999 for x in h])); result['mean_blend']=float(np.mean([x['blend'] for x in h]))
    return result


def aggregate(data,cfg,radius):
    records={}
    for d in DISTANCES:
        values=[evaluate(x,cfg,radius) for x in data if x[0]==d]; rms=np.array([x['rmse_m'] for x in values])
        records[str(d)]={'mean_rmse_m':float(np.mean(rms)),'p90_rmse_m':float(np.percentile(rms,90)),
                         'max_rmse_m':float(np.max(rms)),'divergence_rate':float(np.mean([x['diverged'] for x in values])),
                         'mean_limited_rate':None if radius=='baseline' else float(np.mean([x['limited_rate'] for x in values]))}
    means=[records[str(d)]['mean_rmse_m'] for d in DISTANCES]
    score=float(np.mean(means)+.25*np.max(means)+100*sum(records[str(d)]['divergence_rate'] for d in DISTANCES))
    return {'robust_score':score,'records':records}


def run():
    cfg,validation=collect('validation'); candidates={'baseline':'baseline','unbounded':None,'r0.25':.25,'r0.5':.5,'r1':1.,'r2':2.}
    val={name:aggregate(validation,cfg,radius) for name,radius in candidates.items()}
    selected=min(val,key=lambda x:val[x]['robust_score']); _,test=collect('test')
    # 선택 결과 외 후보는 최초 test 실패 후 원인 진단용이며 후속 확인 test의 성능 근거로 사용하지 않는다.
    test_result={name:aggregate(test,cfg,radius) for name,radius in candidates.items()}
    payload={'selected_on_validation':selected,'candidates':candidates,'validation':val,'test':test_result}
    output=Path(__file__).resolve().parent/'results'; output.mkdir(exist_ok=True)
    (output/'trust_region_policy.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps(payload,indent=2)); return payload


if __name__=='__main__': run()
