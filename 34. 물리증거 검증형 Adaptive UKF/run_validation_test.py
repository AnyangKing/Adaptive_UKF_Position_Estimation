"""물리 evidence 검증형 Adaptive UKF를 validation 선택 후 독립 test한다."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance,initialize_position
from path_identifiability import observed_peaks
from peak_measurement import extract_measurement
from physics_verified import PhysicsVerifiedAdaptiveUKF
from ukf import SignalObservationUKF,acceleration_process_covariance

DISTANCES=(100,200,400,600); STEPS=10; COUNT=4


def trajectory(distance,split,index):
    root=341000 if split=='validation' else 342000; rng=np.random.default_rng(root+distance*20+index)
    az=rng.uniform(-np.pi,np.pi); depth=rng.uniform(12.,78.)
    start=np.array([distance*np.cos(az),distance*np.sin(az),-depth]); tangent=np.array([-np.sin(az),np.cos(az),0.])
    radial=np.array([np.cos(az),np.sin(az),0.]); t=np.arange(STEPS,dtype=float)
    truth=start+t[:,None]*(.72*tangent+rng.uniform(-.2,.2)*radial)
    meta={'snr_db':float(rng.choice([10.,20.,30.])), 'surface_reflection':float(-rng.uniform(.72,.97)),
          'bottom_reflection':float(rng.uniform(.32,.78)), 'radial_velocity_m_s':float(rng.uniform(-1.3,1.3))}
    return truth,meta


def collect(split):
    base=ChannelConfig(); data=[]; seedroot=343000 if split=='validation' else 344000
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


def evaluate(item,cfg,threshold,scale):
    _,_,truth,observations,qualities,peaks=item; initial=initialize_position(observations[0],cfg)
    wrapper=PhysicsVerifiedAdaptiveUKF(make_filter(initial,cfg),cfg,threshold,scale)
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)): estimate[k]=wrapper.step(observations[k],qualities[k],*peaks[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1); tail=error[3:]
    return {'rmse_m':float(np.sqrt(np.mean(tail**2))),'diverged':bool(np.any(tail>50.)),
            'retry_rate':float(np.mean([h['retried'] for h in wrapper.history])),
            'mean_evidence_change':float(np.mean([h['evidence_change'] for h in wrapper.history]))}


def aggregate(data,cfg,threshold,scale):
    records={}
    for d in DISTANCES:
        values=[evaluate(x,cfg,threshold,scale) for x in data if x[0]==d]; rms=np.array([x['rmse_m'] for x in values])
        records[str(d)]={'mean_rmse_m':float(np.mean(rms)),'p90_rmse_m':float(np.percentile(rms,90)),
            'max_rmse_m':float(np.max(rms)),'divergence_rate':float(np.mean([x['diverged'] for x in values])),
            'mean_retry_rate':float(np.mean([x['retry_rate'] for x in values])),
            'mean_evidence_change':float(np.mean([x['mean_evidence_change'] for x in values]))}
    means=[records[str(d)]['mean_rmse_m'] for d in DISTANCES]
    score=float(np.mean(means)+.25*np.max(means)+100*sum(records[str(d)]['divergence_rate'] for d in DISTANCES))
    return {'robust_score':score,'records':records}


def run():
    cfg,validation=collect('validation'); candidates={'baseline':(1e99,1.)}
    for threshold in (0.,1.,2.):
        for scale in (4.,16.): candidates[f'd{int(threshold)}_x{int(scale)}']=(threshold,scale)
    val={name:aggregate(validation,cfg,*args) for name,args in candidates.items()}
    selected=min(val,key=lambda x:val[x]['robust_score']); _,test=collect('test')
    result={'baseline':aggregate(test,cfg,*candidates['baseline']),
            'selected':aggregate(test,cfg,*candidates[selected])}
    payload={'selected_on_validation':selected,'candidates':candidates,'validation':val,'test':result}
    output=Path(__file__).resolve().parent/'results'; output.mkdir(exist_ok=True)
    (output/'physics_verified_policy.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps(payload,indent=2)); return payload


if __name__=='__main__': run()
