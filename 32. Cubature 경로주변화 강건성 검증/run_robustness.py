"""31번에서 고정한 soft path policy를 더 많은 완전 신규 궤적에서 paired 검증한다."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np
from scipy.stats import wilcoxon

from channel import synthesize_received
from config import ChannelConfig
from measurement import fixed_measurement_covariance, initialize_position
from path_identifiability import observed_peaks
from peak_adaptive import PeakMarginAdaptiveRUKF
from peak_measurement import extract_measurement
from soft_path_update import CubaturePathMarginalizer
from ukf import SignalObservationUKF, acceleration_process_covariance

DISTANCES=(100,200,400,600); TRAJECTORIES=8; STEPS=10
FIXED_POLICY={'timing_std_s':.001,'temperature':1.0,'covariance_retention':0.0,'strength_weight':.5}


def trajectory(distance,index):
    rng=np.random.default_rng(321000+distance*20+index); az=rng.uniform(-np.pi,np.pi); depth=rng.uniform(12.,78.)
    start=np.array([distance*np.cos(az),distance*np.sin(az),-depth]); tangent=np.array([-np.sin(az),np.cos(az),0.])
    radial=np.array([np.cos(az),np.sin(az),0.]); t=np.arange(STEPS,dtype=float)
    truth=start+t[:,None]*(.72*tangent+rng.uniform(-.2,.2)*radial)
    meta={'snr_db':float(rng.choice([10.,20.,30.])), 'surface_reflection':float(-rng.uniform(.72,.97)),
          'bottom_reflection':float(rng.uniform(.32,.78)), 'radial_velocity_m_s':float(rng.uniform(-1.3,1.3))}
    return truth,meta


def collect():
    base=ChannelConfig(); data=[]
    for distance in DISTANCES:
        for index in range(TRAJECTORIES):
            truth,meta=trajectory(distance,index); observations=[]; qualities=[]; peaks=[]
            for k,position in enumerate(truth):
                cfg=replace(base,seed=323000+distance*100+index*20+k,**meta)
                _,received,_=synthesize_received(position,cfg); z,q=extract_measurement(received,cfg)
                times,strengths=observed_peaks(received[0],cfg,maximum=6)
                observations.append(z); qualities.append(q); peaks.append((times,strengths))
            data.append((distance,index,truth,np.asarray(observations),qualities,peaks))
    return base,data


def make_filter(initial,cfg):
    return SignalObservationUKF(np.r_[initial,np.zeros(3)],np.diag([8.**2]*3+[1.5**2]*3),
        acceleration_process_covariance(1.,.20),fixed_measurement_covariance(),cfg)


def evaluate(item,cfg,use_soft):
    distance,index,truth,observations,qualities,peaks=item; initial=initialize_position(observations[0],cfg)
    wrapper=PeakMarginAdaptiveRUKF(make_filter(initial,cfg)); marginalizer=CubaturePathMarginalizer(cfg,**FIXED_POLICY)
    estimate=np.zeros_like(truth); estimate[0]=initial
    for k in range(1,len(truth)):
        wrapper.step(observations[k],qualities[k])
        if use_soft: marginalizer.update(wrapper.ukf,*peaks[k])
        estimate[k]=wrapper.ukf.x[:3]
    error=np.linalg.norm(estimate-truth,axis=1); tail=error[3:]
    result={'distance_m':distance,'index':index,'rmse_m':float(np.sqrt(np.mean(tail**2))),
            'max_after_3_m':float(np.max(tail)),'diverged_after_3':bool(np.any(tail>50.))}
    if use_soft:
        history=[h for h in marginalizer.history if h['applied']]
        result.update({'mean_effective_points':float(np.mean([h['effective_points'] for h in history])),
                       'mean_max_weight':float(np.mean([h['max_weight'] for h in history])),
                       'mean_evidence_span':float(np.mean([h['evidence_span'] for h in history]))})
    return result


def bootstrap_ci(values,seed=326000,repeats=20000):
    values=np.asarray(values); rng=np.random.default_rng(seed)
    means=np.mean(rng.choice(values,size=(repeats,len(values)),replace=True),axis=1)
    return [float(np.percentile(means,2.5)),float(np.percentile(means,97.5))]


def summarize(baseline,soft):
    result={}
    for distance in DISTANCES:
        b=np.array([x['rmse_m'] for x in baseline if x['distance_m']==distance])
        s=np.array([x['rmse_m'] for x in soft if x['distance_m']==distance]); delta=b-s
        result[str(distance)]={'baseline_mean_rmse_m':float(np.mean(b)),'soft_mean_rmse_m':float(np.mean(s)),
            'relative_change_percent':float(100*(np.mean(s)/np.mean(b)-1)),
            'improvement_rate':float(np.mean(delta>0)),'mean_improvement_m':float(np.mean(delta)),
            'improvement_ci95_m':bootstrap_ci(delta,326000+distance),
            'baseline_divergence_rate':float(np.mean([x['diverged_after_3'] for x in baseline if x['distance_m']==distance])),
            'soft_divergence_rate':float(np.mean([x['diverged_after_3'] for x in soft if x['distance_m']==distance]))}
    all_b=np.array([x['rmse_m'] for x in baseline]); all_s=np.array([x['rmse_m'] for x in soft]); delta=all_b-all_s
    statistic,pvalue=wilcoxon(all_b,all_s,alternative='greater')
    result['overall']={'baseline_mean_rmse_m':float(np.mean(all_b)),'soft_mean_rmse_m':float(np.mean(all_s)),
        'relative_change_percent':float(100*(np.mean(all_s)/np.mean(all_b)-1)),
        'improvement_rate':float(np.mean(delta>0)),'mean_improvement_m':float(np.mean(delta)),
        'improvement_ci95_m':bootstrap_ci(delta),'wilcoxon_one_sided_statistic':float(statistic),
        'wilcoxon_one_sided_pvalue':float(pvalue)}
    return result


def run():
    cfg,data=collect(); baseline=[evaluate(item,cfg,False) for item in data]; soft=[evaluate(item,cfg,True) for item in data]
    payload={'fixed_policy':FIXED_POLICY,'trajectory_count':len(data),'summary':summarize(baseline,soft),
             'paired_records':[{'distance_m':b['distance_m'],'index':b['index'],'baseline_rmse_m':b['rmse_m'],
                                'soft_rmse_m':s['rmse_m'],'improvement_m':b['rmse_m']-s['rmse_m'],
                                'mean_effective_points':s['mean_effective_points'],
                                'mean_max_weight':s['mean_max_weight'],
                                'mean_evidence_span':s['mean_evidence_span']}
                               for b,s in zip(baseline,soft)]}
    output=Path(__file__).resolve().parent/'results'; output.mkdir(exist_ok=True)
    (output/'fixed_policy_robustness.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    print(json.dumps(payload,indent=2)); return payload


if __name__=='__main__': run()
