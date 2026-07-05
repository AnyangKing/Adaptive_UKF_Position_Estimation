"""GCC-SRP 불일치를 SRP가 아닌 GCC-TDOA 불확실성으로 라우팅."""

import numpy as np


class RoutedAdaptiveRUKF:
    def __init__(self,ukf):
        self.ukf=ukf; self.base_R=ukf.R.copy(); self.history=[]

    @staticmethod
    def _nis(residual,covariance,indices):
        value=residual[indices]; block=covariance[indices,indices]
        return float(value@np.linalg.solve(block,value))

    def step(self,observation,quality):
        self.ukf.predict(); R=self.base_R.copy()
        disagreement=quality["doa_disagreement_deg"]
        routing_scale=min(100.0,1.0+(disagreement/2.0)**2)
        # SRP가 Monte Carlo에서 꼬리오차가 작았으므로 불일치 원인을 GCC-TDOA에 배정한다.
        R[1:8,1:8]*=routing_scale
        _,_,predicted,_,S=self.ukf.measurement_statistics(R)
        residual=self.ukf._z_residual(np.asarray(observation).copy(),predicted)
        blocks={"toa":(slice(0,1),6.63),"tdoa":(slice(1,8),18.48),"doa":(slice(8,10),9.21)}
        diagnostics={"disagreement_deg":disagreement,"tdoa_routing_scale":routing_scale}
        for name,(indices,threshold) in blocks.items():
            nis=self._nis(residual,S,indices); scale=min(100.0,max(1.0,nis/threshold))
            R[indices,indices]*=scale; diagnostics[f"{name}_nis"]=nis; diagnostics[f"{name}_scale"]=scale
        self.ukf.update(observation,R); self.history.append(diagnostics)
        return self.ukf.x.copy()
