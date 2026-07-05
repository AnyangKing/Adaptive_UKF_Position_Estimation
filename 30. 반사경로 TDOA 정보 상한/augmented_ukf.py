"""기존 TOA/TDOA/DOA에 반사경로 상대 TDOA를 결합하는 UKF."""

import numpy as np
from config import usb_array_global_m
from measurement import ideal_measurement, wrap_angle


def multipath_range_differences(position, cfg):
    source = np.asarray(position); surface = source.copy(); surface[2] = -source[2]
    bottom = source.copy(); bottom[2] = -2.0 * cfg.water_depth_m - source[2]
    sensors = usb_array_global_m(cfg.receiver_depth_m); values = []
    for sensor in sensors:
        direct = np.linalg.norm(source - sensor)
        values.extend((np.linalg.norm(surface - sensor) - direct,
                       np.linalg.norm(bottom - sensor) - direct))
    return np.asarray(values)


def augmented_measurement(position, cfg, path_mode="all"):
    base = ideal_measurement(position, cfg)
    if path_mode == "none": return base
    paths = multipath_range_differences(position, cfg)
    return np.r_[base, paths[:2] if path_mode == "reference" else paths]


def acceleration_process_covariance(dt_s, std_m_s2):
    block = std_m_s2**2 * np.array([[dt_s**4/4, dt_s**3/2], [dt_s**3/2, dt_s**2]])
    result = np.zeros((6, 6))
    for axis in range(3): result[np.ix_([axis, axis+3], [axis, axis+3])] = block
    return result


class AugmentedUKF:
    def __init__(self, state, covariance, Q, R, cfg, path_mode="all", dt=1.0,
                 alpha=0.3, beta=2.0, kappa=0.0):
        self.x=np.asarray(state,dtype=float).copy(); self.P=np.asarray(covariance,dtype=float).copy()
        self.Q=np.asarray(Q,dtype=float); self.R=np.asarray(R,dtype=float); self.cfg=cfg
        self.path_mode=path_mode; self.dt=dt; self.n=6
        self.lam=alpha**2*(self.n+kappa)-self.n
        self.wm=np.full(13,1/(2*(self.n+self.lam))); self.wc=self.wm.copy()
        self.wm[0]=self.lam/(self.n+self.lam); self.wc[0]=self.wm[0]+1-alpha**2+beta

    @staticmethod
    def _sym(a): return 0.5*(a+a.T)
    @staticmethod
    def _residual(a,b):
        result=a-b; result[8:10]=wrap_angle(result[8:10]); return result
    def _sigma(self):
        jitter=0.0
        for _ in range(8):
            try: root=np.linalg.cholesky((self.n+self.lam)*(self._sym(self.P)+jitter*np.eye(6))); break
            except np.linalg.LinAlgError: jitter=1e-12 if jitter==0 else jitter*10
        points=np.empty((13,6)); points[0]=self.x
        for i in range(6): points[i+1]=self.x+root[:,i]; points[i+7]=self.x-root[:,i]
        return points
    def predict(self):
        sigma=self._sigma(); sigma[:,:3]+=self.dt*sigma[:,3:]; self.x=self.wm@sigma
        dx=sigma-self.x; self.P=self._sym(self.Q+np.einsum('i,ij,ik->jk',self.wc,dx,dx))
    def statistics(self,R=None):
        sigma=self._sigma(); z=np.vstack([augmented_measurement(x[:3],self.cfg,self.path_mode) for x in sigma])
        mean=self.wm@z
        for j in (8,9): mean[j]=np.arctan2(self.wm@np.sin(z[:,j]),self.wm@np.cos(z[:,j]))
        dz=np.vstack([self._residual(row.copy(),mean) for row in z])
        S=self._sym((self.R if R is None else R)+np.einsum('i,ij,ik->jk',self.wc,dz,dz))
        return sigma,mean,dz,S
    def update(self,observation,R=None):
        sigma,mean,dz,S=self.statistics(R); cross=np.einsum('i,ij,ik->jk',self.wc,sigma-self.x,dz)
        K=np.linalg.solve(S,cross.T).T; innovation=self._residual(np.asarray(observation).copy(),mean)
        self.x+=K@innovation; self.P=self._sym(self.P-K@S@K.T)


class ConditionalWrapper:
    def __init__(self,ukf): self.ukf=ukf; self.base_R=ukf.R.copy()
    def step(self,z,quality):
        self.ukf.predict(); R=self.base_R.copy(); disagreement=quality['doa_disagreement_deg']
        scale=min(100.,1+(disagreement/2.)**2)
        if disagreement>5: R[1:8,1:8]*=scale
        else: R[8:10,8:10]*=scale
        if len(z)>10:
            _,mean,_,S=self.ukf.statistics(R); residual=self.ukf._residual(np.asarray(z).copy(),mean)
            value=residual[10:]; block=S[10:,10:]
            nis=float(value@np.linalg.solve(block,value)); limit=9.21 if len(value)==2 else 32.0
            R[10:,10:]*=min(100.,max(1.,nis/limit))
        self.ukf.update(z,R); return self.ukf.x.copy()
