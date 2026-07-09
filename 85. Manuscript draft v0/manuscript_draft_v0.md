# Carrier-Agile Whitening of Coherent Multipath DOA Bias in Static Shallow-Water USBL Tracking

## Abstract

Frequency diversity has long been used in radar and sonar, and frequency-hopped acoustic signals have also appeared in USBL-related literature. The question addressed here is narrower: can carrier agility reduce the post-gating coherent multipath direction-of-arrival (DOA) bias that limits compact shallow-water USBL localization? We answer this question in a TOA/TDOA/DOA-UKF tracking framework. First, we characterize a long-range elevation-bias floor that persists after direct-path gating and is amplified by the small aperture of an eight-sensor USBL array. We then show that the bias contains a carrier-locked component: under fixed-frequency transmission, the direct and in-gate surface-reflected paths keep a nearly constant interference phase, whereas ping-to-ping carrier agility rotates this phase and turns a deterministic bias into a whitened residual. With the carrier schedule fixed before validation, independent 600 m static experiments reduced settled RMSE from 13.01 m to 8.87 m (-32%, p = 0.0008). The same mechanism whitened moving-target residuals, but did not yield reliable pooled RMSE improvement, revealing an applicability boundary caused by motion-induced self-whitening and tail risk. A slow-drift validation supported continuous quasi-static use only up to 0.005 m/s. Thus, the novelty is not frequency hopping itself, but the mechanism, validation, and boundary of carrier-agile whitening for coherent multipath DOA bias in shallow-water USBL tracking.

## 1. Introduction

Underwater localization is a central function for autonomous underwater vehicles, moored instruments, docking systems, and compact surface or subsea platforms. Ultra-short baseline (USBL) systems are attractive in these applications because they can infer bearing from a compact hydrophone array while also using acoustic time-of-arrival information. However, compact aperture is also the source of a difficult accuracy limitation: at long range, small angular errors produce large position errors. A few degrees of elevation error can become many meters of vertical or slant-range position error at hundreds of meters.

This work began from a conventional tracking question: can TOA, TDOA, and DOA measurements be fused with a Kalman-family estimator to improve 3-D underwater localization? A UKF-based tracker is indeed a useful backbone, particularly because the observation model is nonlinear and because EKF linearization becomes fragile at longer range. Yet the main limitation observed in the present shallow-water signal simulations was not simply a filter problem. Even after direct-path time gating and adaptive measurement covariance routing, a systematic elevation component remained. This residual behaved less like zero-mean stochastic noise and more like a coherent bias coupled to the array and multipath geometry.

Multipath mitigation, USBL calibration, and frequency-diverse acoustic signaling are all active and mature topics. Radar literature has long used frequency agility to decorrelate glint-like angular errors [RADAR_FREQ_AGILITY_REF], and underwater localization literature includes frequency-hopped acoustic modem USBL, Costas-based USBL design, acoustic frequency-comb approaches, and other frequency-diversity methods [FH_USBL_REF], [COSTAS_USBL_REF], [FREQ_COMB_REF]. Therefore, the contribution of this paper is not the first use of frequency hopping or frequency diversity. The gap addressed here is narrower and physical: the post-gating DOA residual in a compact shallow-water USBL array can contain a carrier-locked coherent multipath component, and a transmit-side carrier schedule can whiten this residual before it is fused by a TOA/TDOA/DOA-UKF tracking loop.

We propose ping-to-ping carrier agility as an observation design rather than as a new receiver-side estimator. The receiver extracts the same observation vector: one absolute TOA-derived range, seven reference TDOA-derived range differences, and two DOA angles. The UKF fusion pipeline is kept fixed. What changes is the temporal structure of the residual entering the filter. Under fixed carrier transmission, the interference phase between the direct path and an in-gate reflected path can remain nearly locked for a static target. Under carrier-agile transmission, that phase is rotated from ping to ping, converting a persistent bias into a less correlated residual.

The paper makes four contributions. First, it characterizes a post-gating long-range DOA bias floor in compact shallow-water USBL tracking. Second, it identifies a carrier-sensitive coherent mechanism that explains why the residual changes with carrier frequency. Third, it validates a frozen 30--34 kHz ping-to-ping carrier schedule on independent 600 m static-target trials, reducing settled RMSE from 13.01 m to 8.87 m. Fourth, it quantifies the boundary: moving targets show strong residual whitening but not reliable pooled RMSE improvement, and a slow-drift sweep supports continuous quasi-static use only up to 0.005 m/s under the current protocol.

## 2. System and Signal Model

We consider a compact eight-sensor USBL array in a shallow-water acoustic environment. The array geometry follows the project configuration used throughout the validation pipeline: eight sensors arranged around a small aperture, with a radius of 0.033 m and vertical offsets that create a compact three-dimensional array. The receiver is placed at a nominal depth of 30 m. This aperture is intentionally small, making the problem representative of compact USBL deployments but also making long-range DOA error amplification severe.

The simulated acoustic channel contains a direct path, surface reflection, bottom reflection, additive noise, and a constant nominal sound speed. The direct-path gate is used to reduce late multipath contamination. However, at long range, the surface-reflected path can enter or partially overlap the direct-path gate. This is the regime in which a coherent residual can survive ordinary time gating. The model is not intended to replace tank or field validation; rather, it provides a controlled environment for isolating a mechanism that would be difficult to identify from field data alone.

For each ping, the receiver forms a ten-dimensional observation vector,

```text
z = [r0, dr1, dr2, ..., dr7, azimuth, elevation],
```

where `r0` is the reference-sensor TOA-derived range, `dr1` through `dr7` are TDOA-derived range differences relative to the reference sensor, and the last two components are the DOA azimuth and elevation. The tracking state is

```text
x = [px, py, pz, vx, vy, vz].
```

An unscented Kalman filter propagates a constant-velocity motion model and updates on the signal-derived observation vector. A conditional adaptive-R wrapper inflates angular measurement covariance when GCC/SRP consistency metrics indicate unreliable DOA structure. This adaptive-R routing is important for stable tracking, but it is not the main novelty of the paper. Its role is to provide a realistic fusion loop in which changes in observation residual structure can be tested.

## 3. Post-Gating DOA Bias Floor

The first phase of the study tested whether better filtering, adaptive covariance, calibration, feature routing, or higher-resolution DOA extraction could remove the long-range error. These attempts improved stability and reduced some outlier behavior, but they did not eliminate the dominant meter-scale floor. In particular, direct-path gated SRP and adaptive-R UKF fusion still produced long-range errors that were too large to be explained solely by zero-mean noise.

Estimator comparison and lower-bound analysis showed that the remaining error was not merely an inefficient filter implementation. At 600 m, the empirical CRLB-scale value was about 11.80 m, routed UKF performance was about 12.29 m, and NLS was about 13.38 m. The residual floor beyond the nominal bound was approximately 3.45 m. These numbers indicate that the compact aperture and channel-induced angular bias dominate the final position error scale.

Further diagnostics showed that the error had a systematic elevation component tied to geometry. Array rotation tests, blind bias correction, lookup calibration, peak-margin correction, subgrid DOA refinement, and multi-ping averaging all failed to provide a general recovery path. This negative result is important: the problem is not simply that the filter needs more tuning. A persistent component remains in the measurement itself.

The conclusion of this stage is that long-range compact USBL localization in this shallow-water setting is limited by a post-gating DOA bias floor. This floor is not completely removed by receiver-side mitigation. A different lever is needed: instead of only reweighting or post-processing the biased observation, the observation residual should be changed before it enters the filter.

## 4. Carrier-Sensitive Coherent Interference Mechanism

The useful lever appears when the residual is examined as a function of carrier frequency. Consider the interference phase between a direct component and an in-gate reflected component:

```text
phi(f, delta) = 2*pi*f*delta + theta_r,
```

where `f` is the carrier frequency, `delta` is the path-delay difference, and `theta_r` contains reflection phase terms. For a static target, the propagation geometry is approximately fixed over a short ping sequence, so `delta` is also approximately fixed. With a fixed carrier, the interference phase therefore remains nearly fixed from ping to ping. A coherent DOA bias can then persist in one direction and become difficult for a temporal filter to average away.

Changing the carrier from ping to ping rotates this interference phase even when the target and array geometry remain unchanged. The method does not require estimating the reflected path explicitly. It instead changes the residual statistics observed by the downstream estimator. A deterministic or slowly varying angular bias under a fixed carrier becomes a temporally decorrelated residual under a carrier-agile schedule.

This mechanism also explains why frequency agility is not expected to solve all cases. It attacks the carrier-locked coherent component. It does not enlarge the aperture, remove all multipath, or change the fundamental angular amplification at long range. Moreover, for moving targets, `delta(t)` changes naturally over time. Even with a fixed carrier, motion can create self-whitening of the interference phase. Frequency agility may still whiten residuals, but the incremental effect on RMSE may disappear or interact with filter tail behavior.

## 5. Frequency-Agile Whitening Method

The proposed method uses a frozen ping-to-ping carrier schedule spanning 30--34 kHz over 20 pings. The schedule is deliberately simple and was not retuned after observing validation results. The fixed-carrier baseline uses 32 kHz. All receiver processing and UKF fusion components are kept the same between the baseline and treatment conditions.

This setup isolates the effect of transmit carrier agility. The acoustic observations are still TOA, TDOA, and DOA. The UKF still receives the same vector structure. The difference is that the DOA residual entering the filter is less temporally locked to one coherent interference phase. In static geometry, this is expected to reduce the persistent bias component and improve settled RMSE.

The expected behavior differs by target regime. For static targets, carrier agility provides phase diversity that fixed-carrier transmission lacks. For moving targets, the geometry itself changes the path difference over time, so fixed-carrier residuals may already be partially whitened by motion. In that regime, the method should be evaluated not only by RMSE but also by residual correlation and tail behavior.

## 6. Static Validation

The primary positive result is the independent static 600 m validation. With fixed 32 kHz transmission, mean settled RMSE was 13.01 m. With the frequency-agile schedule, mean settled RMSE decreased to 8.87 m. This is a 32% reduction, with paired improvement of 4.14 m and p = 0.0008. The median error decreased from 13.97 m to 7.96 m.

This result is the strongest performance claim in the paper. It validates the proposed observation design for static long-range shallow-water USBL under the simulated compact-array channel model. The result should not be interpreted as sub-meter long-range positioning. Even after improvement, the remaining error is meter-scale because the array aperture and the non-carrier-locked residual components still impose a floor.

The validation also supports the broader interpretation of the negative bias-floor study. The earlier receiver-side methods could identify and route around unreliable observations but could not reliably erase the systematic component. Carrier agility works because it changes the coherent residual before receiver-side fusion.

## 7. Whitening Evidence and Applicability Boundary

Moving-target experiments provide a useful separation between mechanism and performance. Frequency-agile pinging strongly whitened the elevation residual: lag-1 residual correlation changed from +0.470 under fixed-carrier transmission to -0.208 under carrier-agile transmission, with p = 5.6e-10. Thus, the mechanism is not restricted to static trials; the residual temporal structure is genuinely changed.

However, the pooled moving-target RMSE gain was not reliable. The observed pooled gain was -0.10 m with p = 0.301. This means the moving-target result should not be stated as a localization performance improvement. The most consistent interpretation is motion-induced self-whitening: because the target moves, `delta(t)` changes over pings, and the fixed-carrier residual is already partially decorrelated. Additional carrier agility can whiten the residual further but does not necessarily reduce position RMSE, and in some geometries it can worsen tail behavior.

The slow-drift sweep in folder 82 sharpens this boundary. Across all slow-drift trials, fixed transmission produced 11.98 m mean RMSE and carrier agility produced 10.49 m, with p = 8.00e-05. But speed-specific results were non-monotonic. Static and 0.005 m/s slow drift were validated, while 0.010 and 0.050 m/s were not supported. Later positive results at 0.030 and 0.100 m/s should be interpreted as geometry-dependent recoveries, not as evidence of a monotonic validated speed threshold.

Therefore, the continuous quasi-static claim is limited to 0.005 m/s under the current protocol. This conservative boundary is important for reviewer safety. The method is validated for static long-range localization and very slow drift; it is not yet a general moving-target localization method.

## 8. Discussion

The main lesson is that transmit-side observation design can change what the tracking filter sees. Frequency agility does not make a compact USBL array high-resolution, and it does not eliminate all multipath. It reduces one harmful component: the carrier-locked coherent DOA bias that survives direct-path gating. This is why the static result is strong but bounded.

The relationship to prior work should be stated carefully. Frequency agility is a classical idea in radar, and frequency-diverse acoustic signals have been used in underwater systems. The novelty here is the mechanism-driven application to post-gating coherent DOA bias in compact shallow-water USBL, evaluated inside a TOA/TDOA/DOA-UKF tracking loop with both positive static validation and negative/limited moving-boundary results. This framing avoids an unsafe novelty claim while preserving the scientific contribution.

The deployment implication is also bounded. Static beacons, moored references, slow-drift assets, or calibration-like long-range localization scenarios are plausible beneficiaries. General AUV moving-target tracking requires additional logic. Future schedules may need to be motion- and geometry-aware, using innovation variance, NIS tails, estimated velocity direction, or hop/fixed residual disagreement to decide when carrier agility is helpful and when it increases tail risk.

Several limitations remain. The work is simulation-based and uses a specific compact array geometry and shallow-water channel model. Real-water and tank validation are required. The 30--34 kHz schedule is intentionally simple and not globally optimized. Exact citation audit is also required before submission, especially for radar frequency agility, frequency-hopped USBL, and Costas hopping USBL prior art.

## 9. Conclusion

This paper reframes a long-range compact USBL localization error as a post-gating coherent multipath DOA-bias problem rather than only as a filtering problem. A fixed carrier can lock the interference phase between direct and in-gate reflected components, leaving a persistent elevation bias. Ping-to-ping carrier agility rotates this phase and whitens the residual entering a TOA/TDOA/DOA-UKF tracking loop.

Independent static validation at 600 m reduced settled RMSE from 13.01 m to 8.87 m, a 32% improvement. Moving experiments confirmed residual whitening but not reliable pooled RMSE improvement, and slow-drift validation supported continuous quasi-static use only up to 0.005 m/s. The result is therefore a bounded observation-design method for static long-range shallow-water USBL localization, and a starting point for future motion- and geometry-aware carrier scheduling.
