# Static validation section draft

작성일: 2026-07-08  
상태: SCI 원고용 1차 영어 초안. 61번 결과와 Fig. 3 중심.

## Section title candidate

Static-Target Validation of Frequency-Agile Pinging

## Draft text

The mechanism analysis predicts that frequency agility should be most beneficial when the target geometry is static or quasi-static. In this regime, the direct-reflection delay difference `delta` remains approximately constant across pings. A fixed carrier therefore preserves a nearly fixed interference phase, causing the DOA bias to remain correlated over time. Carrier hopping, by contrast, introduces phase diversity even when the target geometry itself does not change.

We evaluated this prediction using an independent static-target validation experiment. The estimator, measurement model, carrier schedule, and evaluation metric were fixed before the validation run. For each range condition, paired trials compared fixed 32 kHz transmission against the frequency-agile schedule, using the same geometry and noise seeds within each pair. The primary performance metric was the settled position RMSE after the initial transient period.

The strongest effect appeared at 600 m, where the mechanism predicts in-gate surface-reflection leakage and strong carrier-sensitive DOA bias. As shown in Fig. 3, the mean settled RMSE decreased from 13.01 m under fixed-frequency transmission to 8.87 m under frequency-agile pinging. The paired mean improvement was 4.14 m, with a 95% confidence interval of approximately 2.17–6.05 m. A one-sided paired Wilcoxon test indicated that the improvement was statistically significant (p = 0.0008). The median settled RMSE also decreased substantially, from 13.97 m to 7.96 m.

This result is important for two reasons. First, it shows that the carrier-sensitive DOA-bias reduction observed in the mechanism diagnostic is not merely a signal-level artifact; it survives the complete localization pipeline and improves UKF position estimates. Second, it validates a regime-specific prediction. The largest improvement occurs in the long-range static case where the fixed-carrier bias is expected to be phase-locked across pings. Shorter-range cases do not provide the same evidence for a universal improvement, consistent with the mechanism section and Fig. 2.

The validation should therefore be interpreted as support for static or quasi-static long-range USBL positioning, not as a general performance claim for all trajectories. This distinction is central to the paper. The proposed carrier schedule modifies the temporal structure of coherent DOA bias, but the amount of benefit depends on whether the target motion and propagation geometry already provide phase diversity. The next section examines this boundary explicitly using moving-target trajectories.

## Numbers to preserve

| Quantity | Value |
|---|---|
| Fixed 600 m mean settled RMSE | 13.01 m |
| Frequency-agile 600 m mean settled RMSE | 8.87 m |
| Mean paired improvement | 4.14 m |
| 95% CI | +2.17 to +6.05 m |
| Wilcoxon one-sided p | 0.0008 |
| Fixed 600 m median settled RMSE | 13.97 m |
| Frequency-agile 600 m median settled RMSE | 7.96 m |

## Claims allowed

- Frequency-agile pinging significantly improves static 600 m settled RMSE in the current validated simulation.
- The effect is consistent with the carrier-sensitive coherent bias mechanism.
- The result supports static/quasi-static long-range positioning.

## Claims to avoid

- Do not claim all ranges improve.
- Do not claim moving targets improve.
- Do not claim real-water validation has already been done.
- Do not claim sub-meter long-range accuracy.
