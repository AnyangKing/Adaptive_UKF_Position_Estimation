# Abstract draft after quasi-static boundary validation

## Version A — compact SCI abstract

Ultra-short baseline (USBL) localization with compact arrays is highly sensitive to direction-of-arrival (DOA) errors at long range. In shallow water, we show that even after direct-path time gating, in-gate surface-reflection leakage can leave a carrier-locked coherent elevation bias that is not removed by blind calibration or by Kalman filtering alone. We propose a transmit-side observation design for TOA/TDOA/DOA-UKF localization: ping-to-ping carrier agility over a 30--34 kHz band. The method rotates the interference phase, `phi = 2*pi*f*delta`, so that a deterministic DOA bias under a fixed carrier becomes a temporally whitened residual before UKF fusion. In independent 600 m static-target validation, fixed 32 kHz transmission gave 13.01 m settled RMSE, whereas frequency-agile pinging gave 8.87 m, a 32% reduction (p = 0.0008), with the median error decreasing from 13.97 m to 7.96 m. Moving-target experiments confirmed residual whitening (lag-1 correlation +0.470 to -0.208, p = 5.6e-10), but did not produce reliable pooled RMSE improvement, indicating motion-induced self-whitening and geometry-dependent tail risk. A slow-drift sweep further supported a continuous quasi-static claim only up to 0.005 m/s. These results position frequency-agile pinging not as a first use of frequency hopping in USBL, but as a mechanism-driven mitigation of carrier-locked coherent multipath DOA bias in static long-range shallow-water USBL tracking.

## Version B — more method-forward IEEE style

This paper investigates signal-based underwater USBL localization using TOA, TDOA, and DOA measurements fused by an unscented Kalman filter. The study begins from a practical failure mode: for a compact eight-sensor array, long-range performance is limited less by the nonlinear filter than by a systematic elevation bias caused by shallow-water coherent multipath. We identify a carrier-sensitive residual mechanism that remains after direct-path gating. When the carrier frequency is fixed, the direct and surface-reflected components preserve a nearly constant interference phase, producing a ping-persistent DOA bias. We therefore introduce frequency-agile pinging as a transmit-side measurement design: the carrier is varied from ping to ping while the receiver and TOA/TDOA/DOA-UKF pipeline remain unchanged. This rotates the coherent interference phase and whitens the DOA residual observed by the filter. In independent 600 m static validation, the proposed schedule reduced settled RMSE from 13.01 m to 8.87 m (-32%, p = 0.0008). Median error decreased from 13.97 m to 7.96 m. Mechanism validation on moving trajectories showed strong whitening of elevation residuals, but not a reliable RMSE gain, because target motion already changes the multipath geometry. A quasi-static speed sweep showed that the continuous validated slow-drift regime extends only to 0.005 m/s; higher-speed positive cases were non-monotonic and geometry-dependent. The contribution is therefore a bounded but reproducible method for mitigating carrier-locked coherent multipath bias in static long-range USBL localization.

## Version C — cautious journal abstract with explicit prior-art boundary

Frequency diversity has long been used in radar and sonar, and frequency-hopped acoustic signals have also appeared in USBL-related literature. The question addressed here is narrower: can carrier agility reduce the post-gating coherent multipath DOA bias that limits compact shallow-water USBL localization? We answer this question in a TOA/TDOA/DOA-UKF tracking framework. First, we characterize a long-range elevation-bias floor that persists after direct-path gating and is amplified by the small aperture of an eight-sensor USBL array. We then show that the bias contains a carrier-locked component: under fixed-frequency transmission, the direct and in-gate surface-reflected paths keep a nearly constant interference phase, whereas ping-to-ping carrier agility rotates this phase and turns a deterministic bias into a whitened residual. With the carrier schedule fixed before validation, independent 600 m static experiments reduced settled RMSE from 13.01 m to 8.87 m (-32%, p = 0.0008). The same mechanism whitened moving-target residuals, but did not yield reliable pooled RMSE improvement, revealing an applicability boundary caused by motion-induced self-whitening and tail risk. A slow-drift validation supported continuous quasi-static use only up to 0.005 m/s. Thus, the novelty is not frequency hopping itself, but the mechanism, validation, and boundary of carrier-agile whitening for coherent multipath DOA bias in shallow-water USBL tracking.

## Korean explanation for 교수님/팀 공유

이 초록의 핵심은 “우리가 frequency hopping을 처음 썼다”가 아니다. 그 주장은 선행연구 때문에 위험하다. 대신 다음처럼 잡는다.

> 얕은 바다 USBL에서 direct-path gating을 해도 표면반사 누설이 carrier-locked coherent DOA 고도각 편향을 남긴다. 이 편향은 fixed carrier에서는 ping마다 같은 방향으로 남아 UKF가 평균내기 어렵다. 반송파를 ping마다 30--34 kHz로 도약시키면 `phi = 2*pi*f*delta`가 회전하면서 편향이 시간적으로 백색화되고, 정지 600 m에서 RMSE가 13.01 m에서 8.87 m로 줄었다. 다만 이동 표적에서는 기하가 자체적으로 변해 self-whitening이 생기므로 RMSE 개선은 재현되지 않았고, 준정지 claim도 0.005 m/s까지로 제한한다.

## Recommended final abstract direction

현재로서는 Version C가 가장 방어력이 좋다. 이유는 세 가지다.

1. frequency hopping/Costas USBL 선행연구를 먼저 인정한다.
2. novelty를 “주파수 도약 자체”가 아니라 “post-gating coherent multipath DOA-bias whitening + UKF tracking validation + applicability boundary”로 정의한다.
3. 82번의 비단조 준정지 결과를 숨기지 않고, claim 범위를 0.005 m/s로 제한한다.

Version A는 더 짧고 강해서 저널 초록으로 다듬기 좋고, Version B는 방법론 논문 느낌이 강하다. 실제 투고용 1차 원고는 Version C를 기반으로 줄이는 편을 권장한다.
