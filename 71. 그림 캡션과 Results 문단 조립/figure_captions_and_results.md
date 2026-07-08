# Figure captions and Results narrative draft

작성일: 2026-07-08  
상태: 1차 논문 문장 초안. 최종 원고 전 영문 다듬기와 참고문헌 번호 삽입 필요.

## Overall Results storyline

The results should be read in the following order.

1. Fig. 2 shows that carrier frequency is a physical lever on coherent DOA bias, but only in the long-range in-gate reflection regime.
2. Fig. 3 shows that this bias reduction becomes a statistically reproducible localization improvement for static 600 m targets.
3. Fig. 4 shows the applicability boundary: moving targets still exhibit residual whitening, but not a reproducible RMSE gain.
4. Fig. 7 explains the absolute error scale and prevents overclaiming sub-meter long-range performance under the present aperture and noise assumptions.

This order gives the paper a defensible chain:

```text
mechanism → static validation → moving-target boundary → performance floor
```

## Fig. 2 caption draft

**Figure 2. Carrier-frequency agility suppresses long-range coherent DOA bias.**  
Median absolute DOA bias was evaluated under fixed 32 kHz transmission and under a frequency-agile average using the validated coherent multipath model. At 400 m and 600 m, where the surface-reflected leakage remains inside the gated SRP window, frequency agility reduced the median absolute bias by approximately 78% and 92%, respectively. In contrast, 100 m and 200 m did not benefit, indicating that the proposed mechanism is range- and geometry-dependent rather than a universal frequency-selection effect.

### What this figure claims

- The bias is carrier-sensitive in the long-range regime.
- The useful lever is not “choosing a better single carrier” but not staying at one carrier.
- The range boundary is part of the mechanism.

### What this figure does not claim

- It does not claim localization RMSE improvement by itself.
- It does not claim frequency agility helps at all ranges.
- It does not claim the principle is newly invented independent of radar glint literature.

## Fig. 3 caption draft

**Figure 3. Frequency-agile pinging improves static 600 m USBL localization.**  
Paired trials compare fixed 32 kHz transmission and frequency-agile pinging for static targets at 600 m. The mean settled RMSE decreased from 13.01 m to 8.87 m, corresponding to a mean improvement of 4.14 m. The improvement was statistically significant under a paired one-sided Wilcoxon test (p = 0.0008), and the median RMSE decreased from 13.97 m to 7.96 m. These results provide the main performance validation for the static/quasi-static target regime.

### What this figure claims

- The mechanism in Fig. 2 survives at the localization-filter level.
- The strongest validated performance result is static/quasi-static 600 m.
- The result is not a one-seed pilot; it is the 61번 independent validation result.

### What this figure does not claim

- It does not claim sub-meter long-range performance.
- It does not claim moving-target improvement.
- It does not prove lake/sea experimental performance yet; it is simulation validation under the current channel model.

## Fig. 4 caption draft

**Figure 4. Moving targets show residual whitening but not reliable RMSE improvement.**  
For moving 600 m targets, frequency agility strongly reduced the lag-1 correlation of the DOA residuals, from +0.470 under fixed-frequency transmission to −0.208 under frequency-agile transmission (p = 5.6×10⁻¹⁰). However, the pooled localization RMSE gain was not statistically reproduced (mean gain = −0.10 m, p = 0.301). This indicates that carrier hopping changes the residual statistics, but target motion already induces partial self-whitening of the interference geometry and can introduce tail-risk regimes where RMSE does not improve.

### What this figure claims

- The whitening mechanism is real even in moving trajectories.
- Whitening alone is insufficient as a moving-target performance claim.
- Moving-target schedule design belongs in limitations/future work unless a new independent validation passes.

### What this figure does not claim

- It does not claim frequency agility worsens all moving cases.
- It does not claim adaptive schedules are impossible.
- It does not support using moving-target RMSE improvement as the paper’s headline.

## Fig. 7 caption draft

**Figure 7. Aperture-limited lower bounds explain the long-range error scale.**  
The empirical CRLB, NLS RMSE, and routed UKF RMSE were compared across target ranges. The error scale grows rapidly with range under the current compact USBL aperture and realistic observation noise. At 600 m, the residual bias floor relative to the empirical lower bound is approximately 3.45 m. This explains why the current study should not be framed around sub-meter 600 m performance and why the frequency-agile contribution is best interpreted as a reduction of coherent bias within an aperture-limited regime.

### What this figure claims

- The large 600 m RMSE is not simply because the filter is bad.
- The current array/noise/channel assumptions impose a meter-to-10-meter-scale long-range floor.
- Frequency agility improves part of the coherent bias, not the entire geometric limitation.

### What this figure does not claim

- It does not set an absolute physical limit for all possible arrays.
- It does not rule out larger-aperture or multi-node systems achieving lower error.
- It does not replace real-water validation.

## Results section draft

### Carrier-dependent bias mechanism

We first examined whether the post-gating DOA bias identified in the baseline USBL estimator was sensitive to the transmit carrier frequency. Under fixed 32 kHz transmission, the long-range elevation bias remained coherent across pings, which allowed the UKF to absorb part of the bias as a slowly varying geometric error. When the carrier was varied across pings, the relative phase between the direct path and the in-gate surface-reflected leakage changed according to \(\phi = 2\pi f\delta\). This converted a carrier-locked coherent bias into a less correlated ping-to-ping error. As shown in Fig. 2, this effect was weak or adverse at 100–200 m, but became dominant at 400–600 m, where the reflected component remained inside the gated SRP window. The median absolute DOA bias was reduced by approximately 78% at 400 m and 92% at 600 m.

### Static-target localization validation

We then tested whether the DOA-bias reduction translated into localization accuracy. In the independent static-target validation at 600 m, frequency-agile pinging reduced the mean settled RMSE from 13.01 m to 8.87 m (Fig. 3). The mean paired improvement was 4.14 m and was statistically significant (p = 0.0008). The median RMSE also decreased from 13.97 m to 7.96 m. This result is the strongest performance evidence in the current study and supports frequency-agile pinging as a transmit-side observation design for static or quasi-static long-range USBL targets.

### Moving-target boundary

The same transmit strategy did not generalize into a reliable moving-target RMSE improvement. For moving 600 m trajectories, frequency agility reduced the mean lag-1 residual correlation from +0.470 to −0.208 (p = 5.6×10⁻¹⁰), confirming that the residual-whitening mechanism still occurs. However, the pooled RMSE gain was −0.10 m and was not statistically significant (p = 0.301). This suggests that target motion already changes the path-delay difference \(\delta\), producing motion-induced self-whitening even under a fixed carrier. Consequently, frequency agility should not be claimed as a universal moving-target improvement without an additional validated scheduling or risk-detection mechanism.

### Error-scale interpretation

Finally, the CRLB comparison clarifies the absolute performance scale. The compact USBL aperture and realistic observation noise produce a rapidly increasing lower-bound scale with range. At 600 m, the routed UKF and NLS estimates remain in the same 10 m-scale regime as the empirical CRLB, with an additional residual bias floor of approximately 3.45 m (Fig. 7). Thus, the present contribution is not a sub-meter long-range positioning method. Rather, it reduces a coherent multipath-induced component of the long-range error while operating within an aperture-limited USBL geometry.

## Reviewer-risk notes

1. If a reviewer cites radar frequency agility/glint literature, accept it and position this work as a cross-domain underwater USBL transfer with new mechanism and boundary evidence.
2. Do not hide the 100–200 m non-improvement in Fig. 2; it is evidence for the gate-regime mechanism.
3. Do not present moving-target RMSE as positive. The honest claim is “whitening confirmed, performance boundary identified.”
4. Keep Fig. 7 near Discussion or late Results to prevent unrealistic interpretation of the 600 m error magnitude.
