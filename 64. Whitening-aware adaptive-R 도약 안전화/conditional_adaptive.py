"""작은 불일치는 DOA, 큰 불일치는 TDOA에 배정하는 조건부 adaptive R."""

import numpy as np


class ConditionalAdaptiveRUKF:
    def __init__(self,ukf,threshold_deg):
        self.ukf=ukf; self.base_R=ukf.R.copy(); self.threshold=float(threshold_deg); self.history=[]

    @staticmethod
    def _nis(residual,covariance,indices):
        value=residual[indices]; block=covariance[indices,indices]
        return float(value@np.linalg.solve(block,value))

    def step(self,observation,quality):
        self.ukf.predict(); R=self.base_R.copy(); disagreement=quality["doa_disagreement_deg"]
        scale=min(100.,1.+(disagreement/2.)**2); routed=disagreement>self.threshold
        if routed: R[1:8,1:8]*=scale
        else: R[8:10,8:10]*=scale
        _,_,predicted,_,S=self.ukf.measurement_statistics(R)
        residual=self.ukf._z_residual(np.asarray(observation).copy(),predicted)
        for indices,limit in ((slice(0,1),6.63),(slice(1,8),18.48),(slice(8,10),9.21)):
            nis=self._nis(residual,S,indices); R[indices,indices]*=min(100.,max(1.,nis/limit))
        total_nis=float(residual@np.linalg.solve(S,residual))
        self.ukf.update(observation,R)
        self.history.append({"disagreement_deg":disagreement,"routed":routed,
                             "innovation":residual,"S":S,"nis":total_nis})
        return self.ukf.x.copy()
