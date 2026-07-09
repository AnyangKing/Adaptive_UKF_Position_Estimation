# Conclusion and Future Work draft

작성일: 2026-07-09  
상태: SCI 원고용 1차 영어 초안.

## Section title

Conclusion and Future Work

## Draft text

This paper investigated signal-based underwater USBL positioning using TOA, TDOA, and DOA measurements fused in a UKF tracking framework. The original objective was to improve 3D localization through robust Kalman-filter-based fusion. However, extensive simulation under shallow-water multipath conditions showed that the dominant long-range limitation was not simply filter inefficiency or random measurement noise. Instead, after direct-path gating, surface-reflected leakage can remain inside the DOA processing window and produce a carrier-locked coherent elevation-bias component.

To address this failure mode, we proposed frequency-agile pinging as a transmit-side observation design. By varying the acoustic carrier across pings, the direct-reflection interference phase `φ=2πfδ` is rotated, converting a fixed coherent DOA bias into a less correlated residual sequence. The receiver array, measurement set, and UKF state model remain unchanged; the improvement comes from changing the temporal structure of the DOA error before it enters the filter.

The strongest validated result is the static long-range regime. In the independent static 600 m validation, frequency-agile pinging reduced the mean settled RMSE from 13.01 m to 8.87 m, corresponding to a 32% reduction and a paired mean improvement of 4.14 m (p = 0.0008). The median RMSE decreased from 13.97 m to 7.96 m. These results support frequency-agile pinging as a practical observation-design strategy for static or quasi-static long-range USBL targets affected by coherent multipath DOA bias.

The method also has a clear applicability boundary. In moving-target trajectories, frequency agility strongly reduced the lag-1 correlation of DOA residuals, but the pooled RMSE improvement was not statistically reproduced. This indicates that target motion already changes the direct-reflection delay difference and can induce self-whitening even under fixed-carrier transmission. Therefore, moving-target carrier scheduling remains an open problem rather than a validated performance claim.

The main contributions are summarized as follows. First, we characterized a post-gating coherent multipath DOA-bias floor in compact shallow-water USBL positioning. Second, we showed that ping-to-ping carrier agility can whiten the carrier-locked component of this bias. Third, we validated a statistically significant static 600 m localization improvement. Fourth, we quantified the moving-target boundary and clarified the relation to existing frequency-hopped, Costas, acoustic-comb, and radar frequency-agility literature.

Future work should proceed in four directions. First, quasi-static speed-boundary experiments should quantify the target-motion regime in which static-target gains remain valid. Second, carrier-schedule ablation should determine how many carriers, what hop span, and what deterministic or random sequence are required for reliable whitening. Third, risk-aware moving-target schedules should be developed using observable indicators such as DOA innovation variance, NIS tail behavior, estimated vertical velocity, and fixed/hopped residual disagreement. Finally, controlled-tank or field validation should test whether the simulated in-gate reflection mechanism and residual whitening are reproduced in real water.

## Short conclusion variant

This study shows that, in shallow-water USBL positioning, long-range errors can be dominated by carrier-locked coherent multipath DOA bias rather than by filter inefficiency alone. Frequency-agile pinging whitens this bias by rotating the direct-reflection interference phase across pings. The method significantly improves static 600 m localization while revealing a moving-target boundary caused by motion-induced self-whitening. The contribution is therefore a transmit-side observation design for TOA/TDOA/DOA-UKF positioning, not a universal frequency-hopping localization method.

## Future work bullets for final paper

- Quasi-static speed boundary: define when static gains disappear.
- Carrier schedule ablation: hop span, number of carriers, deterministic vs random schedule.
- Risk-aware moving-target schedule: innovation/NIS/velocity indicators.
- Real-water validation: paired fixed vs frequency-agile tests with DOA residual autocorrelation and RMSE metrics.
- Exact citation audit: radar glint/frequency agility and frequency-hopped USBL prior work.
