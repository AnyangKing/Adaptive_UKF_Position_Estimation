"""8 absolute ranges와 SRP DOA용 block-NIS adaptive wrapper."""

import numpy as np


class AbsoluteRangeAdaptiveUKF:
    def __init__(self,ukf):
        self.ukf=ukf; self.base_R=ukf.R.copy(); self.history=[]
    @staticmethod
    def _nis(residual,covariance,indices):
        value=residual[indices]; block=covariance[indices,indices]
        return float(value@np.linalg.solve(block,value))
    def step(self,observation,quality):
        self.ukf.predict(); R=self.base_R.copy()
        _,_,predicted,_,S=self.ukf.measurement_statistics(R)
        residual=self.ukf._z_residual(np.asarray(observation).copy(),predicted)
        range_nis=self._nis(residual,S,slice(0,8)); doa_nis=self._nis(residual,S,slice(8,10))
        R[0:8,0:8]*=min(100.,max(1.,range_nis/20.09))
        R[8:10,8:10]*=min(100.,max(1.,doa_nis/9.21))
        self.ukf.update(observation,R)
        self.history.append({"range_nis":range_nis,"doa_nis":doa_nis})
        return self.ukf.x.copy()
