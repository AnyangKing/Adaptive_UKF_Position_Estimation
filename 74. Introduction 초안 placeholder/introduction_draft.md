# Introduction draft with citation placeholders

작성일: 2026-07-08  
상태: SCI 원고용 1차 영어 초안. 참고문헌 placeholder는 최종 전 반드시 정확 서지로 교체해야 한다.

## Draft title

Frequency-Agile Pinging for Whitening Coherent Multipath DOA Bias in Shallow-Water USBL Positioning

## Introduction

Underwater acoustic positioning is a core capability for submerged navigation, docking, inspection, and long-duration monitoring in GPS-denied environments. Ultra-short baseline (USBL) systems are attractive because they estimate a target position from a compact receiver array without deploying a wide seafloor baseline. A typical USBL solution combines acoustic time-of-arrival or range information with angle information inferred from inter-sensor phase or time differences. However, the same compact aperture that makes USBL systems easy to deploy also makes their position estimates sensitive to small direction-of-arrival (DOA) errors, especially at long range. In shallow water, this sensitivity is amplified by coherent multipath, boundary reflections, colored noise, and imperfect propagation modeling [USBL_REF], [UNDERWATER_MULTIPATH_REF].

Kalman-filter-based fusion is a natural framework for this problem because TOA, TDOA, and DOA measurements carry complementary information. In this study, the baseline estimator fuses one absolute TOA/range measurement, seven TDOA measurements, and two DOA measurements in a UKF state model for three-dimensional position and velocity. Earlier stages of this project showed that conditional measurement-noise routing and consistency checks can improve robustness over a plain filter. Nevertheless, long-range simulations revealed a persistent error floor that could not be explained by random observation noise alone. Increasing the number of pings, refining the DOA grid, adding blind bias states, inflating measurement covariance, using peak-margin features, and testing calibration-like lookup corrections all failed to remove the dominant long-range residual.

The central observation of this paper is that the remaining long-range error is a coherent bias problem before it is a filtering problem. Even after direct-path time gating, a surface-reflected component can remain inside the gated SRP/DOA processing window at long range. The direct path and the in-gate reflected leakage then combine coherently, producing a deterministic elevation-bias component. For a fixed carrier frequency, the direct-reflection phase relation remains locked across pings, so the bias is temporally correlated and can be absorbed by the tracking filter as a slowly varying geometric error. This mechanism differs from a simple increase in random DOA variance and explains why conventional covariance tuning or blind bias estimation is insufficient.

We address this failure mode using transmit carrier-frequency agility. Frequency agility is not a new idea in radar: pulse-to-pulse carrier variation and frequency-diverse radar processing have long been used for electronic counter-countermeasures and for decorrelating carrier-sensitive radar effects [RADAR_FREQ_AGILITY_REF]. Radar tracking literature also discusses target glint and monopulse angle-error phenomena [RADAR_GLINT_REF]. Our claim is therefore not that frequency agility itself is newly invented. Rather, we show that a related principle can be transferred to a distinct underwater USBL mechanism. In shallow-water gated USBL processing, varying the acoustic carrier across pings rotates the direct-reflection interference phase

```text
phi = 2*pi*f*delta,
```

where `f` is the carrier frequency and `delta` is the direct-reflection delay difference. This changes a fixed coherent DOA bias into a less correlated ping-to-ping residual that the UKF can average more safely.

The resulting behavior is strongly regime-dependent. At short range, where the reflected component is outside the selected DOA gate or the residual bias has a different origin, frequency agility provides little or no benefit. At long range, where the surface-reflected leakage remains inside the gate, the carrier-sensitive bias component becomes dominant. In our simulations, carrier hopping reduced the median absolute long-range DOA bias by approximately 78% at 400 m and 92% at 600 m. More importantly, the mechanism translated into a statistically reproducible localization improvement for static 600 m targets: the mean settled RMSE decreased from 13.01 m to 8.87 m, with a paired improvement of 4.14 m and p = 0.0008.

We also identify an important boundary condition. Moving targets still show residual whitening under frequency agility: the lag-1 correlation of the DOA residual decreased from +0.470 to −0.208 with p = 5.6×10⁻¹⁰. However, the pooled moving-target RMSE improvement was not statistically reproduced. This suggests that target motion changes the direct-reflection delay difference `delta` over time, producing a form of motion-induced self-whitening even at a fixed carrier. Consequently, frequency-agile pinging should be interpreted as a validated transmit-side observation design for static or quasi-static long-range targets, not as a universal moving-target localization improvement.

The contributions of this paper are fourfold.

1. We identify a post-gating coherent multipath bias mechanism in shallow-water USBL DOA processing, where in-gate surface-reflection leakage creates a deterministic elevation-bias floor.
2. We show that carrier-frequency agility rotates the direct-reflection phase relation and whitens the coherent DOA residual without changing the receiver array or the UKF state model.
3. We validate the resulting static-target localization improvement in an independent large-scale simulation, obtaining a 32% mean RMSE reduction at 600 m.
4. We quantify the applicability boundary for moving targets, where residual whitening remains measurable but RMSE improvement is not reproduced because target motion already induces partial self-whitening.

Together, these results reposition the problem from “another adaptive UKF tuning method” to a transmit-side observation-design problem. The UKF remains the fusion backbone for TOA, TDOA, and DOA measurements, but the key improvement comes from changing the temporal structure of the DOA bias presented to the filter. This distinction is important for practical deployment: the proposed strategy requires only carrier scheduling within the acoustic waveform design, while the receiver geometry and tracking filter can remain largely unchanged.

## Citation placeholders to resolve

| Placeholder | Needed source |
|---|---|
| `[USBL_REF]` | USBL/SBL/LBL acoustic positioning reference, preferably Milne or a modern survey/system paper |
| `[UNDERWATER_MULTIPATH_REF]` | Shallow-water acoustic multipath / boundary reflection reference |
| `[RADAR_FREQ_AGILITY_REF]` | Authoritative radar frequency agility reference, preferably IEEE/IET/book |
| `[RADAR_GLINT_REF]` | Radar target glint / monopulse angle-error reference |

## Korean notes

- 이 Introduction은 일부러 “우리가 frequency agility를 발명했다”고 쓰지 않는다.
- 가장 강한 성능 문장은 정지 600 m fixed 13.01 m → hop 8.87 m다.
- 이동 표적은 “whitening confirmed, RMSE not reproduced”로만 둔다.
- 마지막 문단에서 중심축 `TOA/TDOA/DOA → UKF`를 다시 확인시켜, 송신 정책 novelty가 원래 프로젝트 축을 벗어나지 않게 했다.
