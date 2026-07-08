# Moving-target boundary section draft

작성일: 2026-07-08  
상태: SCI 원고용 1차 영어 초안. 63~67번 결과와 Fig. 4 중심.

## Section title candidate

Moving-Target Boundary: Whitening without Reproducible RMSE Gain

## Draft text

The static-target validation confirms that carrier-frequency agility can reduce a phase-locked coherent DOA bias when the propagation geometry remains nearly fixed. We next examined whether the same strategy generalizes to moving targets. This test is important because the original positioning problem involves dynamic tracking rather than only stationary beacons. However, moving trajectories also change the physical mechanism: the direct-reflection delay difference `delta` is no longer constant.

In the moving-target validation, frequency agility produced a clear change in the residual statistics. The mean lag-1 correlation of the DOA residual decreased from +0.470 under fixed-frequency transmission to −0.208 under frequency-agile transmission, with p = 5.6×10⁻¹⁰. This result confirms that carrier hopping decorrelates the coherent residual component even when the target moves. In that sense, the whitening mechanism is not restricted to static scenes.

The corresponding localization improvement, however, was not statistically reproduced. The pooled moving-target RMSE gain was −0.10 m, with p = 0.301. In other words, the residuals became less correlated, but the final position RMSE did not reliably improve. Some motion conditions benefited, whereas others introduced tail-risk behavior that offset the average gain. This disconnect between residual whitening and position RMSE is a key applicability boundary of the proposed method.

The most plausible explanation is motion-induced self-whitening. For a moving target, the delay difference `delta(t)` evolves as the target geometry changes. Even at a fixed carrier, the interference phase

```text
phi(t) = 2*pi*f*delta(t) + theta_r
```

can drift across pings. Thus, part of the phase diversity that carrier hopping provides for static targets is already supplied by the target motion itself. Additional carrier hopping still changes the residual statistics, but it no longer guarantees that the UKF receives more useful position information. Depending on the trajectory, it may also disturb a fixed-frequency dynamic anchor that the filter was implicitly using.

We tested several safety strategies to recover moving-target performance. These included whitening-aware measurement covariance inflation, DOA jump gating, NIS-based guards, fixed/hop anchor schedules, sparse hopping schedules, and condition-aware schedules. The pilot anchor-hop schedule showed promise, but the effect did not reproduce in larger independent validations. The condition-aware rule derived from an oracle-style analysis also failed to improve over the fixed-frequency baseline. Therefore, the present evidence does not support presenting carrier hopping as a general moving-target localization improvement.

This negative result is not a contradiction of the mechanism. Rather, it separates two claims that should remain distinct. Carrier hopping can whiten coherent DOA residuals. Static or quasi-static long-range targets can translate that whitening into a reproducible RMSE reduction. Moving targets, however, already provide geometric phase diversity and may require a more selective risk-aware transmission schedule before RMSE gains become reliable. We therefore treat moving-target scheduling as future work and keep the main validated contribution focused on static and quasi-static long-range USBL positioning.

## Numbers to preserve

| Quantity | Value |
|---|---|
| Moving lag-1 fixed | +0.470 |
| Moving lag-1 frequency-agile | −0.208 |
| Lag-1 whitening p | 5.6×10⁻¹⁰ |
| Moving pooled RMSE gain | −0.10 m |
| Moving pooled RMSE p | 0.301 |
| Failed safety attempts | 64 adaptive-R/gating, 66 sparse schedule midscale, 67 condition-aware schedule |

## Claims allowed

- Moving trajectories show strong residual whitening.
- Moving-target RMSE improvement was not statistically reproduced.
- Motion-induced self-whitening is a plausible boundary mechanism.
- Moving-target adaptive scheduling is future work.

## Claims to avoid

- Do not claim moving target performance improvement.
- Do not claim sparse anchor-hop is validated.
- Do not hide the schedule failures.
- Do not imply the static-target result is invalid because moving-target RMSE failed; they are different regimes.
