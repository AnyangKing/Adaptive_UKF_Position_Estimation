# Carrier-Agile Whitening of Coherent Multipath DOA Bias in Static Shallow-Water USBL Tracking

> Draft v4-ref (2026-07-10). Starts from manuscript v3 (folder 94) and replaces the main
> citation keys and reference entries using the metadata-closed references from folder 96.

> Sensors free-format dry-run candidate (folder 103). This is not a final submission
> file. It marks the manuscript-level sections that must be completed before
> target-journal submission.

## Abstract

Frequency diversity has long been used in radar and sonar, and frequency-hopped acoustic signals have also appeared in USBL-related literature. The question addressed here is narrower: can carrier agility reduce the post-gating coherent multipath direction-of-arrival (DOA) bias that limits compact shallow-water USBL localization? We answer this question in a TOA/TDOA/DOA-UKF tracking framework. First, we characterize a long-range elevation-bias floor that persists after direct-path gating and is amplified by the small aperture of an eight-sensor USBL array. We then show that the bias contains a carrier-locked component: under fixed-frequency transmission, the direct and in-gate surface-reflected paths keep a nearly constant interference phase, whereas ping-to-ping carrier agility rotates this phase and turns a deterministic bias into a whitened residual. With the carrier schedule fixed before validation, independent 600 m static experiments reduced settled RMSE from 13.01 m to 8.87 m (-32%, p = 0.0008). The same mechanism whitened moving-target residuals, but did not yield reliable pooled RMSE improvement, revealing an applicability boundary caused by motion-induced self-whitening and tail risk. A slow-drift validation supported continuous quasi-static use only up to 0.005 m/s. Thus, the novelty is not frequency hopping itself, but the mechanism, validation, and boundary of carrier-agile whitening for coherent multipath DOA bias in shallow-water USBL tracking.

## Keywords

USBL localization; underwater acoustic positioning; carrier agility; coherent multipath; direction-of-arrival bias; TOA/TDOA/DOA fusion; unscented Kalman filter; shallow water; frequency diversity; sensor fusion

## 1. Introduction

Underwater localization is a central function for autonomous underwater vehicles, moored instruments, docking systems, and compact surface or subsea platforms. Ultra-short baseline (USBL) systems are attractive because they can infer bearing from a compact hydrophone array while also using acoustic time-of-arrival information. However, compact aperture is also the source of a difficult accuracy limitation: at long range, small angular errors produce large position errors.

This work began from a conventional tracking question: can TOA, TDOA, and DOA measurements be fused with a Kalman-family estimator to improve 3-D underwater localization? A UKF-based tracker is indeed a useful backbone, particularly because the observation model is nonlinear and EKF linearization becomes fragile at longer range. Yet the dominant limitation observed in the present shallow-water signal simulations was not simply a filter problem. Even after direct-path time gating and adaptive measurement covariance routing, a systematic elevation component remained.

Multipath mitigation, USBL calibration, and frequency-diverse acoustic signaling are all mature topics. Radar literature has long used frequency agility to decorrelate glint-like angular errors [Loomis1974FrequencyAgilityGlint], and underwater positioning literature includes frequency-hopped acoustic modem USBL, Costas-based USBL design, acoustic frequency-comb approaches, and other frequency-diversity methods [Beaujean2007FrequencyHoppedUSBL], [Nhat2022CostasUSBL], [Qian2025FrequencyCombIUSBL]. Table 1 distinguishes these prior families from the present work. The contribution here is not the first use of frequency hopping. The gap is narrower: the post-gating DOA residual in a compact shallow-water USBL array can contain a carrier-locked coherent multipath component, and a transmit-side carrier schedule can whiten this residual before it is fused by a TOA/TDOA/DOA-UKF tracking loop.

**Table 1.** Positioning of the present work relative to related frequency-diverse and USBL localization literature. The distinction claimed here is not the first use of frequency hopping in USBL, but the identification and validation of carrier-agile whitening for post-gating coherent multipath DOA bias in a TOA/TDOA/DOA-UKF tracking loop. *(Draft status: principal citation metadata closed in folder 96; final journal style remains pending.)*

| Literature family | Frequency diversity used? | USBL positioning? | Main purpose in prior work | Post-gating coherent DOA-bias whitening? | TOA/TDOA/DOA-UKF tracking boundary quantified? | How this paper differs |
|---|---:|---:|---|---:|---:|---|
| Radar frequency agility / glint reduction [Loomis1974FrequencyAgilityGlint] | Yes | No | Decorrelate radar angular/glint tracking errors | Partly analogous, but not underwater USBL multipath | No | We cite this as the closest physical analogy, then narrow the claim to shallow-water USBL and surface-reflection-induced coherent DOA residuals. |
| Frequency-hopped acoustic modem USBL [Beaujean2007FrequencyHoppedUSBL] | Yes | Yes | Use frequency-hopped acoustic modem sequences for positioning | Not established as the target mechanism | No | Prior existence prevents a "first FH USBL" claim; our contribution is the residual-whitening mechanism and validation boundary. |
| Costas / hopped USBL shallow-water designs [Nhat2022CostasUSBL] | Yes | Yes | Improve correlation, time-delay, or navigation precision | Not the stated mechanism | No | Related waveform diversity exists, but does not isolate carrier-locked post-gating DOA bias entering a UKF tracker. |
| Acoustic frequency-comb / iUSBL approaches [Qian2025FrequencyCombIUSBL] | Yes | Often iUSBL or related positioning | Use comb/frequency-diverse signals for positioning or processing | Not the stated mechanism | No | Frequency diversity is used, but the system role and residual mechanism differ. |
| USBL calibration / installation-error correction | Usually no | Yes | Estimate mounting, alignment, or calibration errors | No | No | Calibration removes static system errors; here the residual remains tied to carrier-sensitive propagation/interference after gating. |
| **Present work** | Yes, ping-to-ping carrier agility | Yes, compact 8-sensor USBL | Change the temporal structure of the residual entering TOA/TDOA/DOA-UKF fusion | **Yes** | **Yes** | Static 600 m improvement is validated; moving/quasi-static boundary is explicitly reported, including negative results. |

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

where `v_k` includes timing, TDOA, DOA, and coherent multipath residual components. A conditional adaptive-R wrapper changes the measurement covariance according to a signal-consistency indicator `g_k`, defined as the GCC/SRP DOA disagreement in degrees. The wrapper operates in two stages. First, a graded scale is computed as

```math
s_k=\min\!\left(100,\;1+\left(\frac{g_k}{2}\right)^2\right).
```

The scale is applied to the DOA block of `R_k` when `g_k\le\tau`, and to the TDOA block when `g_k>\tau`, with `\tau=5^{\circ}`. This routes uncertainty toward the observation block that is less consistent with the current signal evidence. Second, each measurement block is independently checked by a normalized innovation squared (NIS) test:

```math
R_k^{(b)}
\leftarrow
R_k^{(b)}\cdot
\min\!\left(100,\;\max\!\left(1,\;\frac{\mathrm{NIS}_k^{(b)}}{\chi^2_{0.99}(d_b)}\right)\right),
```

where `b` denotes the TOA-range, TDOA, and DOA blocks with degrees of freedom `d_b=1,7,2`, respectively. The corresponding `\chi^2_{0.99}` thresholds are 6.63, 18.48, and 9.21. This adaptive-R rule is used as the tracking backbone. The proposed contribution is not a new UKF variant; it is the transmit-side carrier schedule that changes the residual statistics entering this backbone. The array, propagation paths, and observation construction are summarized in Fig. 1.

### 2.1 Implementation parameters

All experiments use the following fixed implementation. The array has eight elements on two rings of radius 33 mm, with four elements at `z=0` and four at `z=-79` mm rotated by 45 degrees. This gives a horizontal aperture of roughly 66 mm, about 1.4 wavelengths at 32 kHz. The receiver is at 30 m depth in a 100 m-deep waveguide with sound speed 1500 m/s. The probe is a 10 ms linear-FM chirp with 12 kHz bandwidth, Tukey windowing, and 192 kHz sampling. The channel model contains the direct path and first-order surface and bottom image-source reflections with Thorp absorption, Doppler, and colored ambient noise.

TOA is taken from the strongest matched-filter peak of the reference sensor. TDOA uses band-limited GCC-PHAT over all 28 sensor pairs and is reduced to seven reference differences by least squares. DOA uses SRP-PHAT on the 5 ms direct-path gate with a 2 degree global grid refined to 0.2 degree. The UKF uses `\alpha=0.3`, `\beta=2`, `\kappa=0`, `\Delta t=1` s, constant-velocity dynamics with white-acceleration process noise of standard deviation 0.20 m/s^2, initial covariance `diag(8^2 m^2 I_3, 1.5^2 (m/s)^2 I_3)`, and a fixed base measurement covariance built from 0.03 m TOA-range, 0.025 m per-sensor TDOA, and 2.0 degree DOA standard deviations.

## 3. Post-Gating DOA Bias Floor

The first phase of the study tested whether better filtering, adaptive covariance, calibration, feature routing, or higher-resolution DOA extraction could remove the long-range error. These attempts improved stability and reduced some outlier behavior, but they did not eliminate the dominant meter-scale floor. In particular, direct-path gated SRP and adaptive-R UKF fusion still produced long-range errors that were too large to be explained solely by zero-mean noise.

Estimator comparison and lower-bound analysis showed that the remaining error was not merely an inefficient filter implementation. At 600 m, the empirical CRLB-scale value was about 11.80 m, routed UKF performance was about 12.29 m, and NLS was about 13.38 m. The residual floor beyond the nominal bound was approximately 3.45 m. Fig. 6 compares empirical performance with the CRLB-scale floor, showing why the remaining error after frequency agility is still meter-scale.

Further diagnostics showed that the error had a systematic elevation component tied to geometry. Array rotation tests, blind bias correction, lookup calibration, peak-margin correction, subgrid DOA refinement, and multi-ping averaging all failed to provide a general recovery path. This negative result is important: the problem is not simply that the filter needs more tuning. A persistent component remains in the measurement itself.

## 4. Carrier-Sensitive Coherent Interference Mechanism

The long-range residual becomes actionable when it is viewed as carrier-sensitive coherent interference. Suppose a direct component and a reflected component arriving within the 5 ms direct-path gate have an excess delay or path-difference term `\delta_k`. At 600 m in the present geometry, the surface-reflected excess delay is a few milliseconds and therefore falls inside this gate; at shorter 100--200 m ranges it falls outside the gate, which is why the carrier-locked bias is primarily a long-range phenomenon. The carrier-dependent interference phase can be written as

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

varies across pings. This rotates the coherent interference pattern and turns part of the deterministic DOA bias into a temporally whitened residual. Fig. 2 shows the carrier dependence of the residual elevation bias, while Fig. 1 illustrates the path geometry that motivates the phase model.

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

For static targets, the expected effect is reduced temporal correlation in the carrier-locked elevation residual. For moving targets, the expected effect is more limited because target motion already changes `\delta(t)` and can partially whiten the fixed-carrier residual. This distinction is important: the proposed schedule is expected to be strongest for static or very slow-drift long-range targets. The fixed and frequency-agile policies, together with the main validation metrics, are summarized in Table 2 at the end of Section 7.

## 6. Static Validation

The primary validation uses independent static 600 m trials with the carrier schedule fixed before evaluation. Each trial uses 20 pings, and the settled window is defined as the final 10 pings. The validation set comprises 20 independent geometries at 600 m, with 100, 200, and 400 m also run under the same frozen protocol on seed streams disjoint from all development experiments. All validation experiments use the canonical direct+surface+bottom channel; no additional roughness or higher-order multipath is enabled, so the reported gains isolate the carrier-schedule effect. Settled RMSE is computed over the post-transient ping set `K_s`:

```math
\mathrm{RMSE}_{\mathrm{settled}}
=
\sqrt{
\frac{1}{|K_s|}
\sum_{k\in K_s}
\|\hat{p}_k-p_k\|_2^2}.
```

With fixed 32 kHz transmission, mean settled RMSE was 13.01 m. With frequency-agile transmission, mean settled RMSE decreased to 8.87 m. This corresponds to a 32% reduction, with paired improvement of 4.14 m and p = 0.0008. The median error decreased from 13.97 m to 7.96 m. Fig. 3 shows the paired static 600 m validation result.

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

Moving-target experiments used four motion conditions: radial 0.05 m/s, radial 1.0 m/s, tangential 1.0 m/s, and tangential 1.0 m/s with 0.08 m/s vertical drift. Each condition used 16 independent geometries, giving `n=64`, with the same 20-ping and final-10-ping settled-window protocol. These experiments showed strong residual whitening: lag-1 correlation changed from +0.470 under fixed-carrier transmission to -0.208 under frequency-agile transmission, with p = 5.6e-10. However, pooled moving-target RMSE gain was not reliable (-0.10 m, p = 0.301). Fig. 4 reports this moving-target residual whitening result. The result establishes an applicability boundary: carrier agility can change the residual temporal structure without necessarily improving moving-target localization RMSE.

The quasi-static speed sweep further refines this boundary. The sweep pools radial and tangential drift directions with 12 geometries per speed-direction condition; the static speed contributes one 12-geometry set, giving 132 paired trials in total. Across all slow-drift trials, fixed transmission gave 11.98 m mean RMSE and frequency-agile transmission gave 10.49 m, with p = 8.00e-05. But speed-specific results were non-monotonic. Static and 0.005 m/s slow drift were validated, while 0.010 and 0.050 m/s were not supported. Positive results at 0.030 and 0.100 m/s are therefore treated as geometry-dependent recoveries rather than a monotonic speed threshold. Fig. 5 summarizes the slow-drift sweep and marks the continuous 0.005 m/s boundary.

The continuous validated quasi-static regime is consequently limited to 0.005 m/s under the present protocol. Table 2 collects the positive and negative validation outcomes to make the operating boundary explicit.

**Table 2.** Summary of positive and negative validation results. Positive RMSE gains are reported as fixed-carrier RMSE minus carrier-agile RMSE; positive values therefore favor carrier agility.

| Regime / test | Baseline | Carrier-agile or tested condition | Main metric | Result | Decision for manuscript |
|---|---|---|---|---|---|
| Static, 600 m independent validation | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Settled RMSE | 13.01 m to 8.87 m; gain +4.14 m; p = 0.0008 | Main positive performance claim. |
| Static, 600 m median behavior | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Median settled RMSE | 13.97 m to 7.96 m | Supports robust static improvement, but keep mean/p-value as primary. |
| Moving target, 600 m pooled RMSE | Fixed 32 kHz | Frequency-agile schedule | Pooled RMSE gain | gain -0.10 m; p = 0.301 | Do not claim moving-target RMSE improvement. |
| Moving target mechanism check | Fixed 32 kHz | Frequency-agile schedule | Elevation residual lag-1 correlation | +0.470 to -0.208; p = 5.56e-10 | Mechanism whitening is supported even when RMSE gain is not. |
| Moving target adaptive/sparse schedules | Fixed 32 kHz | R-inflation, jump gate, anchor-hop, condition-aware schedules | RMSE / tail behavior | No reproducible general-purpose moving improvement | Keep as limitation/future work. |
| Quasi-static sweep, all speeds pooled | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 11.98 m to 10.49 m; gain +1.49 m; p = 8.00e-05 | Useful supporting result, but not a broad speed-boundary claim. |
| Quasi-static mechanism sweep | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Elevation residual lag-1 correlation | +0.220 to -0.100; p = 9.17e-08 | Confirms whitening across the sweep. |
| Quasi-static 0.000 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 11.95 m to 8.62 m; gain +3.32 m; p = 0.0134 | Static/near-static validated. |
| Quasi-static 0.005 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 11.14 m to 9.72 m; gain +1.42 m; p = 0.0447 | Conservative continuous quasi-static boundary. |
| Quasi-static 0.010 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 12.13 m to 12.35 m; gain -0.22 m; p = 0.2031 | Boundary not supported. |
| Quasi-static 0.030 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 10.18 m to 8.19 m; gain +1.99 m; p = 0.0022 | Positive but non-continuous; discuss as geometry-dependent recovery, not speed boundary. |
| Quasi-static 0.050 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 12.35 m to 12.39 m; gain -0.04 m; p = 0.4498 | Not supported. |
| Quasi-static 0.100 m/s | Fixed 32 kHz | 30--34 kHz ping-to-ping schedule | Mean RMSE | 14.12 m to 10.75 m; gain +3.38 m; p = 0.0048 | Positive but non-continuous; do not present as "validated to 0.1 m/s." |
| Long-range floor comparison | Empirical CRLB-scale reference | Routed UKF / NLS | Error scale at 600 m | CRLB-scale 11.80 m; routed UKF 12.29 m; NLS 13.38 m; residual floor about 3.45 m | Explains why sub-meter 600 m performance is not expected with the compact aperture. |

The non-monotonic quasi-static results are important. They show that the carrier-agile schedule can remain beneficial beyond 0.005 m/s in some geometries, but the present evidence does not support a continuous speed boundary above 0.005 m/s. The validated operating region is therefore described as static to very slow drift, with higher-speed recoveries treated as geometry-dependent observations.

## 8. Discussion

The main lesson is that transmit-side observation design can change what the tracking filter sees. Frequency agility does not make a compact USBL array high-resolution, and it does not eliminate all multipath. It reduces one harmful component: the carrier-locked coherent DOA bias that survives direct-path gating. This is why the static result is strong but bounded.

The relationship to prior work should be stated carefully. Frequency agility is a classical idea in radar, and frequency-diverse acoustic signals have been used in underwater systems. The novelty here is the mechanism-driven application to post-gating coherent DOA bias in compact shallow-water USBL, evaluated inside a TOA/TDOA/DOA-UKF tracking loop with both positive static validation and negative/limited moving-boundary results. Table 1 distinguishes the present contribution from radar frequency agility, frequency-hopped USBL, Costas USBL, and acoustic frequency-comb positioning.

The deployment implication is also bounded. Static beacons, moored references, slow-drift assets, or calibration-like long-range localization scenarios are plausible beneficiaries. General AUV moving-target tracking requires additional logic. Future schedules may need to be motion- and geometry-aware, using innovation variance, NIS tails, estimated velocity direction, or hop/fixed residual disagreement to decide when carrier agility is helpful and when it increases tail risk.

Several limitations remain. The work is simulation-based and uses a specific compact array geometry and shallow-water channel model. Real-water and tank validation are required. The 30--34 kHz schedule is intentionally simple and not globally optimized. Exact citation audit is also required before submission, especially for radar frequency agility, frequency-hopped USBL, and Costas hopping USBL prior art. Table 3 maps these limitations to concrete follow-up actions.

**Table 3.** Limitations and corresponding follow-up work. The items are separated into submission-critical fixes, experimental validation, and future algorithmic extensions. *(If the target journal enforces strict page limits, this table may be compressed into a paragraph; the full version is retained here for planning.)*

| Limitation / open item | Current evidence | Risk if unresolved | Follow-up action | Paper placement |
|---|---|---|---|---|
| Final citation styling still pending | Principal metadata placeholders were closed in folder 96, but the manuscript is not yet converted to a target journal style | Reviewer/editor may require exact reference formatting | Convert references to the selected journal style and verify exported DOI/volume/page fields during template conversion | Before submission; Related Work |
| No real-water lake/sea experiment yet | Simulation and signal-level validation only | External validity remains limited | Run static 600 m and slow-drift trials in controlled water before strong applied claims | Discussion / Future Work |
| Moving-target RMSE gain not established | Whitening is strong, but pooled RMSE gain is not reproducible | Overclaiming would weaken the paper | Keep moving result as mechanism/boundary; develop risk-aware schedule only after tail predictors pass a diagnostic test | Results + Future Work |
| Frequency schedule ablation incomplete | 30--34 kHz schedule is frozen and validated, but alternatives remain underexplored | Reviewer may ask if schedule is arbitrary | Add or propose ablation over hop span, hop period, pseudo-random vs deterministic schedules | Future Work or supplemental |
| Compact aperture imposes meter-scale floor | CRLB-scale and empirical errors remain around meter-to-10 m scale at 600 m | Sub-meter expectation is unrealistic under current geometry | Present aperture/floor analysis clearly; avoid sub-meter claims | Discussion |
| Environmental model still simplified | Surface reflection and coherent multipath are modeled, but real underwater variability is broader | Field deployment may show additional noise modes | Extend to bathymetry, sound-speed gradients, platform motion, and hardware timing uncertainty | Future Work |
| Citation/claim language must remain conservative | Frequency hopping and radar frequency agility are not new | "Novelty" may be rejected if framed too broadly | Claim mechanism, underwater USBL transplantation, validation, and boundary; not first frequency hopping | Introduction + Related Work |

## 9. Conclusion

This paper reframes a long-range compact USBL localization error as a post-gating coherent multipath DOA-bias problem rather than only as a filtering problem. A fixed carrier can lock the interference phase between direct and in-gate reflected components, leaving a persistent elevation bias. Ping-to-ping carrier agility rotates this phase and whitens the residual entering a TOA/TDOA/DOA-UKF tracking loop.

Independent static validation at 600 m reduced settled RMSE from 13.01 m to 8.87 m, a 32% improvement. Moving experiments confirmed residual whitening but not reliable pooled RMSE improvement, and slow-drift validation supported continuous quasi-static use only up to 0.005 m/s. The result is therefore a bounded observation-design method for static long-range shallow-water USBL localization, and a starting point for future motion- and geometry-aware carrier scheduling.

Future work should move in three directions. First, the citation record should be kept conservative during final journal-style conversion so that the novelty claim remains precise rather than overstated. Second, the validated static and very-slow-drift regimes should be tested in lake or sea trials with the same compact eight-sensor geometry. Third, moving-target use should not be extended by intuition alone; any risk-aware adaptive hopping schedule should first prove that its runtime indicators predict tail degradation before being evaluated for RMSE improvement.

---

## Figure Captions

**Fig. 1.** Mechanism of carrier-agile whitening in compact shallow-water USBL localization. (a) A direct arrival and an in-gate surface-reflected component can both enter the 5 ms DOA-processing gate, so the compact eight-sensor array observes a coherent mixture rather than a purely direct arrival. (b) For a static target and fixed carrier, the interference phase can remain nearly locked across pings, producing correlated DOA bias before TOA/TDOA/DOA-UKF fusion. Ping-to-ping carrier agility changes `f_k`, rotates the coherent phase, and whitens part of the residual while keeping the receiver-side estimator unchanged.

**Fig. 2.** Carrier sensitivity of the long-range elevation-bias component. The fixed 32 kHz case retains a larger median absolute bias at 600 m, while the 30--34 kHz carrier-agile average strongly reduces the carrier-locked component. This supports the interpretation that the post-gating residual contains a coherent frequency-dependent term.

**Fig. 3.** Independent static 600 m validation of the frozen carrier-agile schedule. Mean settled RMSE decreased from 13.01 m under fixed 32 kHz transmission to 8.87 m under the 30--34 kHz ping-to-ping schedule, corresponding to a +4.14 m paired improvement (p = 0.0008).

**Fig. 4.** Moving-target residual whitening and performance boundary. Carrier agility changed the elevation residual lag-1 correlation from +0.470 to -0.208 (p = 5.56e-10), but the pooled moving-target RMSE gain was not significant (-0.10 m, p = 0.301). The figure therefore supports a mechanism claim, not a moving-target RMSE-improvement claim.

**Fig. 5.** Quasi-static speed sweep at 600 m. Static and 0.005 m/s drift were validated, whereas 0.010 and 0.050 m/s were not supported. Positive results at 0.030 and 0.100 m/s are treated as geometry-dependent recoveries rather than a continuous speed boundary. The conservative continuous boundary is 0.005 m/s under the present protocol.

**Fig. 6.** Compact-aperture floor at long range. The 600 m empirical CRLB-scale reference is about 11.80 m, routed UKF is about 12.29 m, and NLS is about 13.38 m, showing that sub-meter long-range performance is not expected under the present geometry and noise assumptions. Carrier agility mitigates one coherent residual component; it does not remove the aperture/geometry floor.

## Figure File Manifest (canonical, updated through folder 95)

| Callout | File (in `91. Figure file alignment/figures/`) | Note |
|---|---|---|
| Fig. 1 | `101. Fig1 visual polish/figures/fig1_system_concept_polished.svg` / `.png` | polished mechanism schematic; supersedes folder-95 concept draft |
| Fig. 2 | `fig2_frequency_agile_bias.svg` / `.png` | |
| Fig. 3 | `fig3_static_600m_paired_rmse.svg` / `.png` | |
| Fig. 4 | `fig4_moving_whitening_lag1.svg` / `.png` | |
| Fig. 5 | `fig5_quasi_static_speed_boundary.svg` / `.png` | PNG generated in folder 95 from folder-82 JSON |
| Fig. 6 | `fig6_crlb_floor.svg` / `.png` | canonical name; supersedes legacy `fig7_crlb_floor.*` |

## References

- J. M. Loomis and E. R. Graf, "Frequency-Agility Processing to Reduce Radar Glint Pointing Error," *IEEE Transactions on Aerospace and Electronic Systems*, vol. AES-10, no. 6, pp. 811--820, 1974, doi: 10.1109/TAES.1974.307889.
- R. Delano, "A Theory of Target Glint or Angular Scintillation in Radar Tracking," *Proceedings of the IRE*, vol. 41, no. 12, pp. 1778--1784, 1953, doi: 10.1109/JRPROC.1953.274368. *(Optional radar-glint background reference.)*
- P.-P. J. Beaujean, A. I. Mohamed, and R. Warin, "Acoustic positioning using a tetrahedral ultrashort baseline array of an acoustic modem source transmitting frequency-hopped sequences," *The Journal of the Acoustical Society of America*, vol. 121, no. 1, pp. 144--157, 2007, doi: 10.1121/1.2400616.
- H. B. Nhat, L. V. Hai, G. T. Quang, D. N. Van, H. V. Le, and T. T. Xuan, "Optimizing baseline in USBL using Costas hopping to increase navigation precision in shallow water," in *2022 16th International Conference on Ubiquitous Information Management and Communication (IMCOM)*, pp. 1--6, 2022, doi: 10.1109/IMCOM53663.2022.9721736.
- Z. Qian, S. Liu, Y. Zhu, and X. Fu, "Integrated Acoustic Frequency Comb Signal for Underwater Inverted Ultrashort Baseline Autonomous Positioning Systems," *IEEE Internet of Things Journal*, vol. 12, no. 14, pp. 27628--27637, 2025, doi: 10.1109/JIOT.2025.3564346.

## Supplementary Materials

To be completed. Recommended contents: simulation scripts, frozen carrier schedules, validation result JSON/CSV files, and the figure-generation scripts used for Figs. 1--6.

## Author Contributions

To be completed by the human authors before submission.

## Funding

To be completed before submission. If there was no external funding, use the target journal's required no-funding statement.

## Data Availability Statement

Dry-run placeholder: The simulation outputs and analysis scripts supporting the reported results are available in the project repository and can be provided as supplementary material. Before submission, replace this with the exact public repository, archive DOI, or access-on-request statement selected by the authors.

## Acknowledgments

To be completed before submission.

## Conflicts of Interest

To be completed before submission. If there are no conflicts, use the target journal's required no-conflict statement.
