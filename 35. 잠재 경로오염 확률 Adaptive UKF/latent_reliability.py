"""물리 경로 residual을 2상태 잠재 오염확률로 시간 누적하는 Adaptive UKF."""

import numpy as np
from scipy.special import expit

from config import usb_array_global_m
from soft_path_update import _assignment_loglikes,_expected_relative


def physical_residual_score(position,peak_times,peak_strengths,cfg,timing_std_s=.001):
    position=np.asarray(position).copy(); position[2]=np.clip(position[2],-cfg.water_depth_m+.1,-.1)
    expected=_expected_relative(position,usb_array_global_m(cfg.receiver_depth_m)[0],cfg)
    likes=_assignment_loglikes(np.asarray(peak_times),np.asarray(peak_strengths),expected,timing_std_s,0.0)
    if not len(likes): return float('inf')
    return float(np.sqrt(max(0.,-2.*np.max(likes))))


class LatentPathReliabilityUKF:
    def __init__(self,ukf,cfg,score_threshold=1.,score_slope=.5,max_scale=1.,
                 enter_probability=.05,recover_probability=.20):
        self.ukf=ukf; self.cfg=cfg; self.base_R=ukf.R.copy()
        self.threshold=float(score_threshold); self.slope=max(float(score_slope),1e-6)
        self.max_scale=float(max_scale); self.enter=float(enter_probability); self.recover=float(recover_probability)
        self.contamination_probability=.05; self.history=[]

    @staticmethod
    def _nis(residual,covariance,indices):
        value=residual[indices]; block=covariance[indices,indices]
        return float(value@np.linalg.solve(block,value))

    def step(self,observation,quality,peak_times,peak_strengths):
        self.ukf.predict()
        score=physical_residual_score(self.ukf.x[:3],peak_times,peak_strengths,self.cfg)
        prior=(self.contamination_probability*(1.-self.recover)+
               (1.-self.contamination_probability)*self.enter)
        bad_likelihood=float(expit((score-self.threshold)/self.slope)) if np.isfinite(score) else 1.
        denominator=prior*bad_likelihood+(1.-prior)*(1.-bad_likelihood)
        posterior=prior*bad_likelihood/max(denominator,1e-12)
        self.contamination_probability=float(np.clip(posterior,1e-6,1.-1e-6))

        R=self.base_R.copy(); latent_scale=1.+self.contamination_probability*(self.max_scale-1.)
        R[1:10,1:10]*=latent_scale
        disagreement=quality['doa_disagreement_deg']; routing_scale=min(100.,1.+(disagreement/2.)**2)
        if disagreement>5.: R[1:8,1:8]*=routing_scale
        else: R[8:10,8:10]*=routing_scale
        _,_,predicted,_,S=self.ukf.measurement_statistics(R)
        residual=self.ukf._z_residual(np.asarray(observation).copy(),predicted)
        for indices,limit in ((slice(0,1),6.63),(slice(1,8),18.48),(slice(8,10),9.21)):
            R[indices,indices]*=min(100.,max(1.,self._nis(residual,S,indices)/limit))
        self.ukf.update(observation,R)
        self.history.append({'score':score,'contamination_probability':self.contamination_probability,
                             'latent_scale':latent_scale,'bad_likelihood':bad_likelihood})
        return self.ukf.x.copy()
