"""잠재 오염확률 정책을 validation에서 선택하고 독립 test에 고정 적용한다."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from config import ChannelConfig
from latent_reliability import LatentPathReliabilityUKF
from measurement import fixed_measurement_covariance,initialize_position
from path_identifiability import observed_peaks
from peak_measurement import extract_measurement
from ukf import SignalObservationUKF,acceleration_process_covariance

DISTANCES=(100,200,400,600); STEPS=10; COUNT=4


def trajectory(distance,split,index):
    root=351000 if split=='validation' else 352000; rng=np.random.default_rng(root+distance*20+index)
    az=rng.uniform(-np.pi,np.pi); depth=rng.uniform(12.,78.)
    start=np.array([distance*np.cos(az),distance*np.sin(az),-depth]); tangent=np.array([-np.sin(az),np.cos(az),0.])
    radial=np.array([np.cos(az),np.sin(az),0.]); t=np.arange(STEPS,dtype=float)
    truth=start+t[:,None]*(.72*tangent+rng.uniform(-.2,.2)*radial)
    meta={'snr_db':float(rng.choice([10.,20.,30.])), 'surface_reflection':float(-rng.uniform(.72,.97)),
          'bottom_reflection':float(rng.uniform(.32,.78)), 'radial_velocity_m_s':float(rng.uniform(-1.3,1.3))}
    return truth,meta


def collect(split):
    base=ChannelConfig(); data=[]; seedroot=353000 if split=='validation' else 354000
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


def evaluate(item,cfg,threshold,slope,max_scale):
    _,_,truth,observations,qualities,peaks=item; initial=initialize_position(observations[0],cfg)
    wrapper=LatentPathReliabilityUKF(make_filter(initial,cfg),cfg,threshold,slope,max_scale)
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)): estimate[k]=wrapper.step(observations[k],qualities[k],*peaks[k])[:3]
    error=np.linalg.norm(estimate-truth,axis=1); tail=error[3:]
    return {'rmse_m':float(np.sqrt(np.mean(tail**2))),'diverged':bool(np.any(tail>50.)),
            'scores':[h['score'] for h in wrapper.history],
            'mean_probability':float(np.mean([h['contamination_probability'] for h in wrapper.history]))}


def aggregate(data,cfg,threshold,slope,max_scale):
    records={}
    for d in DISTANCES:
        values=[evaluate(x,cfg,threshold,slope,max_scale) for x in data if x[0]==d]; rms=np.array([x['rmse_m'] for x in values])
        records[str(d)]={'mean_rmse_m':float(np.mean(rms)),'p90_rmse_m':float(np.percentile(rms,90)),
            'max_rmse_m':float(np.max(rms)),'divergence_rate':float(np.mean([x['diverged'] for x in values])),
            'mean_contamination_probability':float(np.mean([x['mean_probability'] for x in values]))}
    means=[records[str(d)]['mean_rmse_m'] for d in DISTANCES]
    score=float(np.mean(means)+.25*np.max(means)+100*sum(records[str(d)]['divergence_rate'] for d in DISTANCES))
    return {'robust_score':score,'records':records}


def run():
    cfg,validation=collect('validation')
    diagnostic=[evaluate(x,cfg,1.,1.,1.) for x in validation]
    scores=np.array([s for record in diagnostic for s in record['scores'] if np.isfinite(s)])
    q50=float(np.percentile(scores,50)); q75=float(np.percentile(scores,75)); slope=max(.2,float((q75-q50)/2))
    candidates={'baseline':(q50,slope,1.)}
    for label,threshold in (('q50',q50),('q75',q75)):
        for scale in (4.,16.): candidates[f'{label}_x{int(scale)}']=(threshold,slope,scale)
    val={name:aggregate(validation,cfg,*args) for name,args in candidates.items()}
    selected=min(val,key=lambda x:val[x]['robust_score']); _,test=collect('test')
    result={'baseline':aggregate(test,cfg,*candidates['baseline']),
            'selected':aggregate(test,cfg,*candidates[selected])}
    payload={'score_calibration':{'q50':q50,'q75':q75,'slope':slope},'selected_on_validation':selected,
             'candidates':candidates,'validation':val,'test':result}
    output=Path(__file__).resolve().parent/'results'; output.mkdir(exist_ok=True)
    (output/'latent_path_reliability.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps(payload,indent=2)); return payload


if __name__=='__main__': run()
