# Discussion section draft

작성일: 2026-07-09  
상태: SCI 원고용 1차 영어 초안. Fig. 7, 45번 CRLB 결과, 78번 Related Work 차별표와 연결.

## Section title candidate

Discussion: Performance Scale, Applicability, and Relation to Frequency-Diverse Positioning

## Draft text

### 1. Why the long-range error remains in the meter-to-10-meter scale

The proposed frequency-agile pinging strategy should not be interpreted as a sub-meter long-range USBL solution. The present array is a compact eight-sensor USBL aperture, and the long-range position error is strongly amplified by small DOA errors. The CRLB comparison in Fig. 7 shows that the empirical lower-bound scale itself grows rapidly with range. At 600 m, the empirical CRLB is approximately 11.80 m, while the routed UKF RMSE is approximately 12.29 m and the NLS RMSE is approximately 13.38 m. The residual bias floor relative to the empirical bound is approximately 3.45 m.

These values explain why the absolute RMSE remains large even after frequency agility. The proposed method reduces one coherent component of the DOA error, but it does not change the receiver aperture, the basic bearing geometry, or all environmental uncertainty. Therefore, the correct interpretation is not “frequency agility makes long-range USBL sub-meter accurate.” Rather, frequency agility reduces a carrier-locked coherent multipath bias component within an aperture-limited long-range regime.

### 2. Why the 32% static-target improvement is still meaningful

Although the absolute error remains in the meter-to-10-meter range at 600 m, the static-target validation is meaningful because it addresses a component of the error that previous filter-side methods could not remove. Earlier attempts, including adaptive covariance routing, blind bias states, peak-margin features, calibration-like lookup corrections, path-hypothesis marginalization, and sub-grid DOA interpolation, either failed or provided only limited improvement. This indicated that the dominant long-range residual was not simply random measurement noise or grid quantization.

Frequency-agile pinging changes the temporal structure of the residual before it reaches the UKF. For static or quasi-static geometry, fixed-carrier transmission locks the direct-reflection interference phase across pings. Carrier hopping rotates this phase and converts a coherent bias into a less correlated residual. The resulting static 600 m validation reduced the mean settled RMSE from 13.01 m to 8.87 m, a 32% mean reduction with p = 0.0008. This result is significant not because it eliminates the long-range geometry limit, but because it demonstrates a transmit-side method for reducing a previously persistent coherent bias component.

### 3. Relation to radar frequency agility and underwater frequency-hopped positioning

The proposed method is related to, but distinct from, radar frequency agility and existing underwater frequency-diverse positioning. Radar frequency agility provides an important prior concept: carrier changes can decorrelate carrier-sensitive angle errors such as glint. This paper does not claim to invent frequency agility. Instead, it transfers a related phase-diversity principle to a different underwater failure mode: in-gate surface-reflection leakage in shallow-water gated USBL DOA processing.

Likewise, frequency-hopped and Costas signals have already been used in underwater acoustic positioning. Frequency-hopped acoustic modem sequences have been used for tetrahedral USBL source localization, and Costas hopping has been applied to improve USBL correlation-peak time-delay estimation and baseline optimization. Acoustic frequency-comb iUSBL and MIMO sonar transmitting diversity methods also use multi-frequency or transmit-diverse signal structures. These studies motivate frequency diversity in underwater acoustics, but their primary goals differ from the present work. The contribution here is the identification of a carrier-locked coherent multipath DOA-bias floor and the use of ping-to-ping carrier agility to whiten that bias in a TOA/TDOA/DOA-UKF tracking loop.

### 4. Applicability boundary for moving targets

The moving-target results clarify an important boundary. Frequency agility strongly reduced the lag-1 correlation of DOA residuals in moving trajectories, from +0.470 to −0.208, with p = 5.6×10⁻¹⁰. However, the pooled moving-target RMSE gain was not statistically reproduced. This is consistent with motion-induced self-whitening: as the target moves, the direct-reflection delay difference `delta(t)` changes, so even a fixed carrier can experience a drifting interference phase.

Therefore, the validated performance claim should remain static or quasi-static long-range positioning. Moving-target carrier scheduling remains an open problem. The negative schedule experiments are useful because they prevent overclaiming: simple adaptive-R inflation, jump gating, sparse fixed/hop schedules, and condition-aware rules did not produce a robust general-purpose moving-target improvement.

### 5. Practical deployment and experimental validation

The method is attractive because it modifies the transmit schedule rather than the receiver geometry or the UKF state model. If the acoustic hardware can transmit a small set of carriers around the nominal operating frequency, the same TOA/TDOA/DOA-UKF framework can be retained. This makes the approach relevant for static or slowly moving beacons, docking references, moored monitoring nodes, calibration beacons, and long-range station-keeping scenarios where the target geometry changes slowly and coherent bias can remain locked.

The next experimental step is real-water or controlled-tank validation. A practical validation should compare fixed-carrier transmission and ping-to-ping carrier agility under paired geometries. The minimum evidence should include not only position RMSE but also DOA residual autocorrelation, because residual whitening is the mechanism that connects the signal design to the UKF improvement. If a full 600 m lake or sea experiment is not immediately available, a scaled geometry that places the reflected leakage inside the DOA gate may still test the carrier-sensitive interference mechanism.

### 6. Future technical directions

Three follow-up directions are especially useful.

First, quasi-static speed-boundary validation should quantify when the static-target benefit disappears. The current evidence supports static targets and shows that general moving-target improvement is not reproduced. A sweep over small speeds could define the practical “quasi-static” regime.

Second, carrier-schedule ablation should test whether the 30–34 kHz cycle is necessary or whether fewer carriers, randomized hopping, or narrower hop spans provide similar whitening. This would help convert the present mechanism into a design rule.

Third, risk-aware moving-target scheduling remains open. The failed moving-target schedules suggest that fixed patterns are insufficient. A future scheduler should use observable risk indicators such as DOA innovation variance, NIS tail behavior, estimated vertical velocity, and disagreement between fixed-carrier and hopped residuals.

## Discussion claims to preserve

- The method reduces one coherent DOA-bias component; it does not remove the aperture-limited geometry floor.
- Static 600 m improvement is meaningful because prior filter-side methods failed to remove this component.
- Frequency hopping/Costas USBL prior art exists and must be cited.
- The novelty is coherent multipath DOA-bias whitening in a TOA/TDOA/DOA-UKF tracking loop.
- Moving target results are an applicability boundary, not a hidden failure.

## Suggested figure references

- Fig. 1: mechanism overview
- Fig. 2: range-dependent bias whitening
- Fig. 3: static 600 m paired RMSE validation
- Fig. 4: moving residual whitening without RMSE gain
- Fig. 7: CRLB/RMSE floor explaining the long-range error scale
