# Mechanism section draft

작성일: 2026-07-08  
상태: SCI 원고용 1차 영어 초안. Fig. 1, Fig. 2, 58번 결과와 연결.

## Section title candidate

Carrier-Sensitive Coherent Interference after Direct-Path Gating

## Draft text

The proposed frequency-agile strategy is motivated by the structure of the post-gating DOA error. In the adopted signal-processing chain, a direct-path gate is applied before SRP-based DOA extraction in order to suppress late multipath. This operation reduces gross reflection contamination, but it does not guarantee that the DOA estimate is purely determined by the direct arrival. At long range, the direct path and a surface-reflected path can arrive within a sufficiently small delay difference that both components remain inside the selected DOA processing window. The SRP peak is then formed from a coherent superposition of the direct component and the residual reflected leakage.

Let the complex baseband contribution of the direct path be approximated as

```text
s_d(t) = A_d exp(j 2*pi*f*t),
```

and let the in-gate reflected leakage be

```text
s_r(t) = A_r exp(j 2*pi*f*(t - delta) + j theta_r),
```

where `f` is the acoustic carrier frequency, `delta` is the direct-reflection delay difference, and `theta_r` includes reflection and propagation phase terms not explicitly modeled here. The relevant coherent phase relation is therefore

```text
phi(f, delta) = 2*pi*f*delta + theta_r.
```

For a fixed carrier frequency and a static target, `delta` is approximately constant across pings. The interference phase is therefore locked, and the resulting DOA bias appears as a temporally correlated deterministic error rather than zero-mean measurement noise. This explains why simply increasing the DOA covariance or adding a blind bias state was insufficient in earlier experiments: the filter sees a consistent geometric error and can absorb it into the state trajectory.

Carrier-frequency agility changes this temporal structure. If the transmit carrier is varied across pings, the same propagation geometry produces different interference phases:

```text
phi_k = 2*pi*f_k*delta + theta_r.
```

The receiver array and the UKF state model are unchanged, but the bias presented to the estimator is no longer locked to a single carrier phase. When the set of carrier frequencies spans enough phase diversity for the given `delta`, the coherent bias is converted into a less correlated residual sequence. This is the whitening mechanism illustrated in Fig. 1.

The mechanism is range-dependent because `delta` determines whether the reflected component falls inside the DOA gate and how sensitively the interference phase changes with carrier frequency. In the 58번 diagnostic experiment, short-range cases did not benefit from carrier hopping. At 100 m and 200 m, the frequency-agile average was ineffective or slightly adverse, consistent with a regime in which the dominant residual error is not the same in-gate coherent surface leakage. In contrast, at 400 m and 600 m, the frequency-agile average reduced the median absolute DOA bias by approximately 78% and 92%, respectively. This range selectivity is important: it supports the proposed physical mechanism and prevents interpreting frequency agility as a generic frequency-selection trick.

This interpretation also explains the difference between static and moving targets. For a static target, both the geometry and the carrier are fixed under conventional transmission, so the interference phase remains locked. Frequency agility becomes the main available source of phase diversity. For a moving target, however, `delta` varies naturally as the target geometry changes. Even under a fixed carrier, the phase `phi(f, delta(t))` can drift over time, producing motion-induced self-whitening. This is why moving-target experiments showed strong residual decorrelation under frequency agility but did not produce a reproducible pooled RMSE improvement.

The proposed method is therefore best viewed as a transmit-side observation design rather than a new filtering architecture. The UKF still fuses TOA, TDOA, and DOA measurements in the same state model. The carrier schedule changes the statistical structure of the DOA error before it reaches the filter. Under static or quasi-static long-range conditions, this removes a coherent bias component that the filter cannot safely reject by covariance tuning alone.

## Figure links

- Fig. 1: conceptual direct/reflected path and phase rotation diagram from 72번.
- Fig. 2: range-dependent carrier-agile bias reduction from 70번/58번.
- Fig. 3: static 600 m localization validation from 70번/61번.
- Fig. 4: moving-target boundary from 70번/63번.

## Key claims allowed by this mechanism section

- Carrier hopping changes the phase relation between direct and in-gate reflected components.
- Long-range static/quasi-static targets benefit because fixed-carrier bias is phase-locked.
- The method does not require changing the 8-sensor array or UKF state model.
- The method is not universally beneficial at all ranges or for all motion regimes.

## Key claims to avoid

- Do not claim that all multipath is removed.
- Do not claim that the reflected path is explicitly resolved.
- Do not claim that frequency agility improves moving-target RMSE in the current evidence.
- Do not claim that the mechanism is identical to radar glint; it is related by phase diversity but physically distinct.
