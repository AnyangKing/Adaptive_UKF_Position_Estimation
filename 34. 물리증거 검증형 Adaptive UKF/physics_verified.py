"""Multipath evidence가 나빠지는 TOA/TDOA/DOA update를 R-inflation으로 재수행한다."""

import numpy as np
from soft_path_update import CubaturePathMarginalizer


class PhysicsVerifiedAdaptiveUKF:
    def __init__(self,ukf,cfg,evidence_drop_threshold=0.0,retry_scale=4.0):
        self.ukf=ukf; self.base_R=ukf.R.copy(); self.threshold=float(evidence_drop_threshold)
        self.retry_scale=float(retry_scale)
        self.evidence=CubaturePathMarginalizer(cfg,timing_std_s=.001,temperature=1.,
                                               covariance_retention=0.,strength_weight=.5)
        self.history=[]

    @staticmethod
    def _nis(residual,covariance,indices):
        value=residual[indices]; block=covariance[indices,indices]
        return float(value@np.linalg.solve(block,value))

    def _adaptive_R(self,observation,quality):
        R=self.base_R.copy(); disagreement=quality['doa_disagreement_deg']
        scale=min(100.,1.+(disagreement/2.)**2)
        if disagreement>5.: R[1:8,1:8]*=scale
        else: R[8:10,8:10]*=scale
        _,_,predicted,_,S=self.ukf.measurement_statistics(R)
        residual=self.ukf._z_residual(np.asarray(observation).copy(),predicted)
        for indices,limit in ((slice(0,1),6.63),(slice(1,8),18.48),(slice(8,10),9.21)):
            R[indices,indices]*=min(100.,max(1.,self._nis(residual,S,indices)/limit))
        return R

    def step(self,observation,quality,peak_times,peak_strengths):
        self.ukf.predict(); predicted_x=self.ukf.x.copy(); predicted_P=self.ukf.P.copy()
        before=self.evidence.evidence_score(predicted_x,predicted_P,peak_times,peak_strengths)
        R=self._adaptive_R(observation,quality); self.ukf.update(observation,R)
        proposed_x=self.ukf.x.copy(); proposed_P=self.ukf.P.copy()
        after=self.evidence.evidence_score(proposed_x,proposed_P,peak_times,peak_strengths)
        retried=bool(np.isfinite(before) and after<before-self.threshold)
        if retried:
            self.ukf.x=predicted_x; self.ukf.P=predicted_P
            self.ukf.update(observation,R*self.retry_scale)
            final=self.evidence.evidence_score(self.ukf.x,self.ukf.P,peak_times,peak_strengths)
        else: final=after
        self.history.append({'retried':retried,'before':before,'proposed':after,'final':final,
                             'evidence_change':after-before})
        return self.ukf.x.copy()
