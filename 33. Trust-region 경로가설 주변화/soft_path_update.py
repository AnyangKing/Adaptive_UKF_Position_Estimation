"""양의 cubature 가중치로 상태와 multipath 경로배정을 동시에 주변화한다."""

from itertools import permutations
import numpy as np
from scipy.special import logsumexp

from channel import paths_for_sensor
from config import usb_array_global_m


def _cubature_points(mean, covariance):
    n = len(mean); jitter = 0.0
    for _ in range(8):
        try: root = np.linalg.cholesky(covariance + jitter * np.eye(n)); break
        except np.linalg.LinAlgError: jitter = 1e-12 if jitter == 0 else jitter * 10
    offsets = np.sqrt(n) * root
    return np.vstack([mean + offsets[:, i] for i in range(n)] +
                     [mean - offsets[:, i] for i in range(n)])


def _expected_relative(position, sensor, cfg):
    paths = paths_for_sensor(position, sensor, cfg)
    delays = np.array([path.delay_s for path in paths])
    return delays - delays[0]


def _assignment_loglikes(times, strengths, expected, timing_std_s, strength_weight):
    values = []
    for indices in permutations(range(len(times)), 3):
        # 반사 경로는 직접파보다 늦어야 한다. surface/bottom 순서는 강제하지 않는다.
        if times[indices[1]] <= times[indices[0]] or times[indices[2]] <= times[indices[0]]:
            continue
        observed = times[list(indices)] - times[indices[0]]
        residual = (observed[1:] - expected[1:]) / timing_std_s
        log_strength = np.sum(np.log(np.clip(strengths[list(indices)], 1e-8, 1.0)))
        values.append(-0.5 * float(residual @ residual) + strength_weight * float(log_strength))
    return np.asarray(values)


class CubaturePathMarginalizer:
    def __init__(self, cfg, timing_std_s=5e-4, temperature=1.0, covariance_retention=0.0,
                 strength_weight=0.5, trust_radius=None):
        self.cfg = cfg; self.timing_std_s = float(timing_std_s)
        self.temperature = float(temperature); self.covariance_retention = float(covariance_retention)
        self.strength_weight = float(strength_weight); self.sensor = usb_array_global_m(cfg.receiver_depth_m)[0]
        self.trust_radius = None if trust_radius is None else float(trust_radius)
        self.history = []

    def update(self, ukf, peak_times, peak_strengths):
        times = np.asarray(peak_times); strengths = np.asarray(peak_strengths)
        if len(times) < 3:
            self.history.append({"applied": False}); return ukf.x.copy()
        prior_mean = ukf.x.copy(); prior_cov = ukf.P.copy()
        points = _cubature_points(prior_mean, prior_cov); log_evidence = []
        for point in points:
            # 물 밖 sigma point는 경계에 투영해 image-source 모델의 정의역을 보존한다.
            position = point[:3].copy(); position[2] = np.clip(position[2], -self.cfg.water_depth_m + .1, -.1)
            expected = _expected_relative(position, self.sensor, self.cfg)
            likes = _assignment_loglikes(times, strengths, expected, self.timing_std_s, self.strength_weight)
            log_evidence.append(logsumexp(likes) if len(likes) else -1e12)
        logits = np.asarray(log_evidence) / self.temperature
        weights = np.exp(logits - logsumexp(logits))
        raw_mean = weights @ points; difference = points - raw_mean
        raw_cov = np.einsum('i,ij,ik->jk', weights, difference, difference)
        # 균일 likelihood에서 cubature moment가 원래 P를 정확히 재현해야 한다.
        # retention은 ablation용이며 기본값 0이다.
        raw_cov += self.covariance_retention * prior_cov
        delta = raw_mean - prior_mean
        mahalanobis = float(np.sqrt(max(0.0, delta @ np.linalg.solve(prior_cov, delta))))
        blend = 1.0
        if self.trust_radius is not None and mahalanobis > self.trust_radius:
            blend = self.trust_radius / (mahalanobis + 1e-15)
        # prior와 path posterior의 혼합 moment. 모드 사이 분산도 보존하므로 PSD를 유지한다.
        posterior_mean = prior_mean + blend * delta
        posterior_cov = ((1.0-blend)*prior_cov + blend*raw_cov +
                         blend*(1.0-blend)*np.outer(delta,delta) + 1e-10*np.eye(len(prior_mean)))
        ukf.x = posterior_mean; ukf.P = 0.5 * (posterior_cov + posterior_cov.T)
        ess = float(1.0 / np.sum(weights**2))
        self.history.append({"applied": True, "effective_points": ess,
                             "max_weight": float(np.max(weights)),
                             "evidence_span": float(np.max(log_evidence)-np.min(log_evidence)),
                             "raw_mahalanobis": mahalanobis, "blend": float(blend)})
        return ukf.x.copy()
