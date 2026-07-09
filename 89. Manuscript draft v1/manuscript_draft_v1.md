# Carrier-Agile Whitening of Coherent Multipath DOA Bias in Static Shallow-Water USBL Tracking

## Abstract

Frequency diversity has long been used in radar and sonar, and frequency-hopped acoustic signals have also appeared in USBL-related literature. The question addressed here is narrower: can carrier agility reduce the post-gating coherent multipath direction-of-arrival (DOA) bias that limits compact shallow-water USBL localization? We answer this question in a TOA/TDOA/DOA-UKF tracking framework. First, we characterize a long-range elevation-bias floor that persists after direct-path gating and is amplified by the small aperture of an eight-sensor USBL array. We then show that the bias contains a carrier-locked component: under fixed-frequency transmission, the direct and in-gate surface-reflected paths keep a nearly constant interference phase, whereas ping-to-ping carrier agility rotates this phase and turns a deterministic bias into a whitened residual. With the carrier schedule fixed before validation, independent 600 m static experiments reduced settled RMSE from 13.01 m to 8.87 m (-32%, p = 0.0008). The same mechanism whitened moving-target residuals, but did not yield reliable pooled RMSE improvement, revealing an applicability boundary caused by motion-induced self-whitening and tail risk. A slow-drift validation supported continuous quasi-static use only up to 0.005 m/s. Thus, the novelty is not frequency hopping itself, but the mechanism, validation, and boundary of carrier-agile whitening for coherent multipath DOA bias in shallow-water USBL tracking.

## 1. Introduction

Underwater localization is a central function for autonomous underwater vehicles, moored instruments, docking systems, and compact surface or subsea platforms. Ultra-short baseline (USBL) systems are attractive because they can infer bearing from a compact hydrophone array while also using acoustic time-of-arrival information. However, compact aperture is also the source of a difficult accuracy limitation: at long range, small angular errors produce large position errors.

This work began from a conventional tracking question: can TOA, TDOA, and DOA measurements be fused with a Kalman-family estimator to improve 3-D underwater localization? A UKF-based tracker is indeed a useful backbone, particularly because the observation model is nonlinear and EKF linearization becomes fragile at longer range. Yet the dominant limitation observed in the present shallow-water signal simulations was not simply a filter problem. Even after direct-path time gating and adaptive measurement covariance routing, a systematic elevation component remained.

Multipath mitigation, USBL calibration, and frequency-diverse acoustic signaling are all mature topics. Radar literature has long used frequency agility to decorrelate glint-like angular errors [RADAR_FREQ_AGILITY_REF], and underwater positioning literature includes frequency-hopped acoustic modem USBL, Costas-based USBL design, acoustic frequency-comb approaches, and other frequency-diversity methods [FH_USBL_REF], [COSTAS_USBL_REF], [FREQ_COMB_REF]. Table 1 will distinguish these prior families from the present work. The contribution here is not the first use of frequency hopping. The gap is narrower: the post-gating DOA residual in a compact shallow-water USBL array can contain a carrier-locked coherent multipath component, and a transmit-side carrier schedule can whiten this residual before it is fused by a TOA/TDOA/DOA-UKF tracking loop.

We propose ping-to-ping carrier agility as an observation design rather than as a new receiver-side estimator. The receiver extracts the same observation vector: one absolute TOA-derived range, seven reference TDOA-derived range differences, and two DOA angles. The UKF fusion pipeline is kept fixed. What changes is the temporal structure of the residual entering the filter.

The paper makes four contributions. First, it characterizes a post-gating long-range DOA bias floor in compact shallow-water USBL tracking. Second, it identifies a carrier-sensitive coherent mechanism that explains why the residual changes with carrier frequency. Third, it validates a frozen 30--34 kHz ping-to-ping carrier schedule on independent 600 m static-target trials. Fourth, it quantifies the boundary: moving targets show strong residual whitening but not reliable pooled RMSE improvement, and a slow-drift sweep supports continuous quasi-static use only up to 0.005 m/s under the current protocol.

## 2. System and Signal Model

We consider a compact eight-sensor USBL array in a shallow-water acoustic environment. Let the source position at ping `k` be `p_k = [x_k,y_k,z_k]^T`, and let the `i`-th receiver element position be `s_i`, `i=0,...,7`. The array center is

```math
\bar{s}=\frac{1}{8}\sum_{i=0}^{7}s_i,
```

and the geometric source-to-sensor range is

```math
\rho_{i,k}=\|p_k-s_i\|_2.
```

The signal-derived observation vector is

```math
z_k =
\begin{bmatrix}
r_{0,k} &
\Delta r_{1,k} &
\cdots &
\Delta r_{7,k} &
\alpha_k &
\epsilon_k
\end{bmatrix}^{T},
```

where `r_{0,k}` is the reference-sensor TOA-derived range, `\Delta r_{i,k}` is the TDOA-derived range difference, and `\alpha_k`, `\epsilon_k` are azimuth and elevation. The ideal range and TDOA terms are

```math
r_{0,k}=\rho_{0,k},\quad
\Delta r_{i,k}=\rho_{i,k}-\rho_{0,k},\quad i=1,\ldots,7.
```

With `d_k=p_k-\bar{s}`, the ideal DOA components are

```math
\alpha_k=\operatorname{atan2}(d_{k,y},d_{k,x}),
```

```math
\epsilon_k=\operatorname{atan2}\left(d_{k,z},\sqrt{d_{k,x}^2+d_{k,y}^2}\right).
```

The UKF state is

```math
x_k=[p_k^T,u_k^T]^T
=
\begin{bmatrix}
x_k & y_k & z_k & v_{x,k} & v_{y,k} & v_{z,k}
\end{bmatrix}^T,
```

and a constant-velocity transition is used:

```math
x_{k+1}=Fx_k+w_k,\quad
F=
\begin{bmatrix}
I_3 & \Delta t I_3 \\
0_3 & I_3
\end{bmatrix}.
```

The measurement model is

```math
z_k=h(x_k)+v_k,
```

where `v_k` includes timing, TDOA, DOA, and coherent multipath residual components. A conditional adaptive-R wrapper changes the measurement covariance according to a signal-consistency indicator `g_k`, such as GCC/SRP DOA disagreement:

```math
R_k=
\begin{cases}
R_0, & g_k\le\tau,\\
R_{\mathrm{inflated}}, & g_k>\tau.
\end{cases}
```

This adaptive-R rule is used as the tracking backbone. The proposed contribution is not a new UKF variant; it is the transmit-side carrier schedule that changes the residual statistics entering this backbone. The array, propagation paths, and observation construction are summarized in Fig. 1.

## 3. Post-Gating DOA Bias Floor

The first phase of the study tested whether better filtering, adaptive covariance, calibration, feature routing, or higher-resolution DOA extraction could remove the long-range error. These attempts improved stability and reduced some outlier behavior, but they did not eliminate the dominant meter-scale floor. In particular, direct-path gated SRP and adaptive-R UKF fusion still produced long-range errors that were too large to be explained solely by zero-mean noise.

Estimator comparison and lower-bound analysis showed that the remaining error was not merely an inefficient filter implementation. At 600 m, the empirical CRLB-scale value was about 11.80 m, routed UKF performance was about 12.29 m, and NLS was about 13.38 m. The residual floor beyond the nominal bound was approximately 3.45 m. Fig. 6 will compare empirical performance with the CRLB-scale floor, showing why the remaining error after frequency agility is still meter-scale.

Further diagnostics showed that the error had a systematic elevation component tied to geometry. Array rotation tests, blind bias correction, lookup calibration, peak-margin correction, subgrid DOA refinement, and multi-ping averaging all failed to provide a general recovery path. This negative result is important: the problem is not simply that the filter needs more tuning. A persistent component remains in the measurement itself.

## 4. Carrier-Sensitive Coherent Interference Mechanism

The long-range residual becomes actionable when it is viewed as carrier-sensitive coherent interference. Suppose a direct component and an in-gate reflected component have an excess delay or path-difference term `\delta_k`. The carrier-dependent interference phase can be written as

```math
\phi_k(f_k,\delta_k)=2\pi f_k\delta_k+\theta_r,
```

where `f_k` is the transmit carrier frequency and `\theta_r` contains reflection-dependent phase terms. This expression is not used as a full reflected-path estimator. It is a mechanism-level model explaining why a coherent residual can remain temporally locked under fixed-carrier transmission.

For a static target and fixed carrier,

```math
f_k=f_0,\quad \delta_k\approx\delta_0,
```

so

```math
\phi_k\approx 2\pi f_0\delta_0+\theta_r.
```

The residual DOA bias can therefore persist with similar sign and magnitude across pings. In contrast, with carrier-agile pinging,

```math
f_k\in\{f_1,f_2,\ldots,f_K\},
```

so even if `\delta_k\approx\delta_0`,

```math
\phi_k\approx 2\pi f_k\delta_0+\theta_r
```

varies across pings. This rotates the coherent interference pattern and turns part of the deterministic DOA bias into a temporally whitened residual. Fig. 2 will show the carrier dependence of the residual elevation bias, while Fig. 1 illustrates the path geometry that motivates the phase model.

For moving targets, the path-difference term itself changes:

```math
\delta_k=\delta(t_k).
```

Thus, even fixed-carrier transmission can experience

```math
\phi_k\approx 2\pi f_0\delta(t_k)+\theta_r,
```

which explains the motion-induced self-whitening observed later in the moving-target experiments.

## 5. Frequency-Agile Whitening Method

The fixed-carrier baseline uses

```math
f_k=32\ \mathrm{kHz}.
```

The frequency-agile policy uses a frozen 20-ping linear sweep over

```math
f_k\in[30,34]\ \mathrm{kHz}.
```

All receiver-side processing is kept unchanged. The same TOA/TDOA/DOA observation vector is extracted, and the same adaptive-R UKF tracking backbone is used. Therefore, performance differences between fixed and frequency-agile transmission are attributed to the changed temporal structure of the measurement residual, not to a different estimator.

For static targets, the expected effect is reduced temporal correlation in the carrier-locked elevation residual. For moving targets, the expected effect is more limited because target motion already changes `\delta(t)` and can partially whiten the fixed-carrier residual. This distinction is important: the proposed schedule is expected to be strongest for static or very slow-drift long-range targets. Table 2 will summarize the fixed and frequency-agile policies together with the main validation metrics.

## 6. Static Validation

The primary validation uses independent static 600 m trials with the carrier schedule fixed before evaluation. Settled RMSE is computed over the post-transient ping set `K_s`:

```math
\mathrm{RMSE}_{\mathrm{settled}}
=
\sqrt{
\frac{1}{|K_s|}
\sum_{k\in K_s}
\|\hat{p}_k-p_k\|_2^2}.
```

With fixed 32 kHz transmission, mean settled RMSE was 13.01 m. With frequency-agile transmission, mean settled RMSE decreased to 8.87 m. This corresponds to a 32% reduction, with paired improvement of 4.14 m and p = 0.0008. The median error decreased from 13.97 m to 7.96 m. Fig. 3 will show the paired static 600 m validation result.

This is the paper's strongest performance result. It supports the claim that carrier-agile pinging can mitigate a carrier-locked coherent DOA residual in static long-range shallow-water USBL localization. It does not support a sub-meter long-range claim, nor does it imply that all multipath or aperture limitations have been removed.

## 7. Whitening Evidence and Applicability Boundary

To separate mechanism from localization performance, we examine the elevation residual sequence

```math
e_k=\epsilon^{\mathrm{meas}}_k-\epsilon^{\mathrm{ideal}}_k
```

and its lag-1 correlation:

```math
\operatorname{corr}_1(e)=
\frac{
\sum_{k=1}^{K-1}(e_k-\bar{e}_{1:K-1})(e_{k+1}-\bar{e}_{2:K})
}{
\sqrt{
\sum_{k=1}^{K-1}(e_k-\bar{e}_{1:K-1})^2
\sum_{k=2}^{K}(e_k-\bar{e}_{2:K})^2
}
}.
```

Moving-target experiments showed strong residual whitening: lag-1 correlation changed from +0.470 under fixed-carrier transmission to -0.208 under frequency-agile transmission, with p = 5.6e-10. However, pooled moving-target RMSE gain was not reliable (-0.10 m, p = 0.301). Fig. 4 will report this moving-target residual whitening result. The result establishes an applicability boundary: carrier agility can change the residual temporal structure without necessarily improving moving-target localization RMSE.

The quasi-static speed sweep further refines this boundary. Across all slow-drift trials, fixed transmission gave 11.98 m mean RMSE and frequency-agile transmission gave 10.49 m, with p = 8.00e-05. But speed-specific results were non-monotonic. Static and 0.005 m/s slow drift were validated, while 0.010 and 0.050 m/s were not supported. Positive results at 0.030 and 0.100 m/s are therefore treated as geometry-dependent recoveries rather than a monotonic speed threshold. Fig. 5 will summarize the slow-drift sweep and mark the continuous 0.005 m/s boundary.

The continuous validated quasi-static regime is consequently limited to 0.005 m/s under the present protocol. Table 2 will summarize the positive static result, the moving residual-whitening result, and the quasi-static boundary in one place to avoid overclaiming.

## 8. Discussion

The main lesson is that transmit-side observation design can change what the tracking filter sees. Frequency agility does not make a compact USBL array high-resolution, and it does not eliminate all multipath. It reduces one harmful component: the carrier-locked coherent DOA bias that survives direct-path gating. This is why the static result is strong but bounded.

The relationship to prior work should be stated carefully. Frequency agility is a classical idea in radar, and frequency-diverse acoustic signals have been used in underwater systems. The novelty here is the mechanism-driven application to post-gating coherent DOA bias in compact shallow-water USBL, evaluated inside a TOA/TDOA/DOA-UKF tracking loop with both positive static validation and negative/limited moving-boundary results. Table 1 will distinguish the present contribution from radar frequency agility, frequency-hopped USBL, Costas USBL, and acoustic frequency-comb positioning.

The deployment implication is also bounded. Static beacons, moored references, slow-drift assets, or calibration-like long-range localization scenarios are plausible beneficiaries. General AUV moving-target tracking requires additional logic. Future schedules may need to be motion- and geometry-aware, using innovation variance, NIS tails, estimated velocity direction, or hop/fixed residual disagreement to decide when carrier agility is helpful and when it increases tail risk.

Several limitations remain. The work is simulation-based and uses a specific compact array geometry and shallow-water channel model. Real-water and tank validation are required. The 30--34 kHz schedule is intentionally simple and not globally optimized. Exact citation audit is also required before submission, especially for radar frequency agility, frequency-hopped USBL, and Costas hopping USBL prior art.

## 9. Conclusion

This paper reframes a long-range compact USBL localization error as a post-gating coherent multipath DOA-bias problem rather than only as a filtering problem. A fixed carrier can lock the interference phase between direct and in-gate reflected components, leaving a persistent elevation bias. Ping-to-ping carrier agility rotates this phase and whitens the residual entering a TOA/TDOA/DOA-UKF tracking loop.

Independent static validation at 600 m reduced settled RMSE from 13.01 m to 8.87 m, a 32% improvement. Moving experiments confirmed residual whitening but not reliable pooled RMSE improvement, and slow-drift validation supported continuous quasi-static use only up to 0.005 m/s. The result is therefore a bounded observation-design method for static long-range shallow-water USBL localization, and a starting point for future motion- and geometry-aware carrier scheduling.
