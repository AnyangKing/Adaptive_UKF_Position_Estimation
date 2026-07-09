# Related Work differentiation table

작성일: 2026-07-09  
상태: 논문 Related Work / 교수님 보고 / reviewer response에 재사용할 차별표 초안.

## 1. 핵심 판단

본 연구의 novelty를 다음처럼 주장하면 위험하다.

> “수중 USBL에서 frequency hopping을 처음 사용했다.”

그 이유는 frequency-hopped acoustic modem USBL, Costas hopping USBL, acoustic frequency comb iUSBL 등 관련 선행연구가 실제로 존재하기 때문이다.

안전한 novelty 문장은 다음이다.

> Existing underwater USBL and sonar studies have used frequency-hopped, Costas, or multi-frequency signals for communication-aided positioning, correlation improvement, baseline optimization, source bearing estimation, or diversity receiver design. The present work addresses a different failure mode: carrier-locked coherent multipath DOA bias that remains after direct-path gating. We use ping-to-ping carrier agility to whiten this bias in a TOA/TDOA/DOA-UKF tracking loop, validate static long-range RMSE improvement, and quantify the moving-target boundary.

## 2. 최근접 선행연구 차별표

| 선행연구 | 확인 상태 | 사용한 frequency diversity | 목적/문제 설정 | 위치추정/처리 구조 | multipath DOA bias whitening? | 본 연구와의 핵심 차이 |
|---|---|---|---|---|---|---|
| Beaujean, Mohamed, Warin, “Acoustic positioning using a tetrahedral ultrashort baseline array of an acoustic modem source transmitting frequency-hopped sequences,” JASA 2007, DOI: `10.1121/1.2400616` | Google Scholar + AIP metadata 확인 | Frequency-hopped MFSK/acoustic modem sequence | 통신 신호를 별도 송신 없이 위치추정에 활용. Frequency-hopped pulse 수 증가에 따른 source positioning 정확도 향상 | Tetrahedral USBL array, maximum-likelihood azimuth/elevation/3D source estimation | 명시적 목표 아님 | 가장 가까운 선행연구 중 하나. 하지만 목적은 frequency-hopped modem source localization이고, 본 연구의 핵심인 direct-path gate 이후 coherent surface-leakage DOA bias floor, ping간 carrier schedule에 의한 residual whitening, UKF tracking boundary 검증은 다루지 않음 |
| “Maximum likelihood estimates of a spread-spectrum source position using a tetrahedral ultra-short baseline array,” OCEANS 2005, IEEE `1511699` | Scholar 확인 | Spread-spectrum / frequency-hopped active source 계열 | 주파수도약 active source의 source position ML 추정 | Tetrahedral USBL, ML source position | 명시적 목표 아님 | JASA 2007의 선행/관련 발표로 보임. 본 연구의 bias-floor mechanism이나 carrier-locked multipath whitening과는 문제 설정이 다름 |
| “Optimizing baseline in USBL using Costas hopping to increase navigation precision in shallow water,” IEEE Xplore `9721736`, 2022 | Scholar + IEEE metadata 확인 | Costas hopping waveform, 28–36 kHz 범위 | USBL active sonar navigator의 correlation peak/time-delay estimation 정밀도와 baseline 최적화 | Four-hydrophone USBL, time-delay estimation at correlation peak, FPGA processing, Monte Carlo | 명시적 목표 아님 | Costas 주파수도약 파형을 ping 내부 신호 설계/상관 정밀도에 사용. 본 연구는 fixed carrier의 coherent DOA bias time-correlation을 ping간 carrier schedule로 깨는 observation design |
| “A Passive Inverted Ultrashort Baseline Scheme for Underwater Positioning Based on the Acoustic Frequency Combs,” OES China Ocean Acoustics 2024, IEEE `10723627` | Scholar 확인 | Acoustic frequency combs / multi-frequency signal | Passive inverted USBL self-localization / 다중주파수 신호 설계 | iUSBL positioning scheme | 명시적 목표 아님 | 다중주파수 신호 설계와 inverted USBL 구조가 핵심. 본 연구의 gated SRP residual DOA bias whitening, static/moving boundary와 다름 |
| “Integrated Acoustic Frequency Comb Signal for Underwater Inverted Ultra-Short Baseline Autonomous Positioning Systems,” IEEE IoT Journal 2025, IEEE `10976981` | Scholar 확인 | Integrated acoustic frequency comb | iUSBL autonomous positioning + communication/navigation integration | Inverted USBL system | 명시적 목표 아님 | frequency comb 기반 통합 신호 설계. 본 연구처럼 carrier-locked multipath DOA bias를 식별하고 ping-to-ping agility로 whitening하는 구조가 아님 |
| Fan et al., “MIMO sonar DOA estimation based on improved transmitting diversity smoothing (TDS),” OCEANS 2018, IEEE `8604737` | Scholar 확인 | MIMO transmitting diversity / TDS | MIMO sonar DOA estimation에서 coherent source 문제 완화, SNR/DOA 추정 개선 | Covariance/smoothing 기반 DOA estimation | 부분적으로 “coherence” 문제를 다루지만, 본 연구의 시간축 tracking bias whitening은 아님 | 송신 다양성으로 snapshot/covariance coherence를 회복하는 DOA estimation 방법. 본 연구는 USBL tracking에서 coherent multipath bias의 ping간 시간상관을 깨는 송신 schedule |
| Ma, “Frequency diversity for active sonar/radar application and optimal receiver design,” OCEANS 2010, IEEE `5664071` | Scholar 확인 | K independent narrowband transmitters / frequency diversity | Active sonar/radar frequency diversity와 optimal receiver design | Receiver design / detection-oriented | 아님 | 주파수 다양성의 일반 수신기 설계. 본 연구의 gated USBL DOA bias floor와 UKF tracking validation은 아님 |
| Radar frequency agility / glint literature | 일부 exact 서지 도서관 확인 필요 | Pulse-to-pulse frequency agility | Radar target glint / angle-error decorrelation / ECCM | Radar tracking / monopulse angle-error context | radar glint 계열에서 유사한 원리 존재 | 원리 발명은 아님. 본 연구는 레이더 원리를 얕은바다 USBL의 다른 물리, 즉 gate 안 surface-reflection coherent leakage로 이식하고 적용경계를 검증 |

## 3. 논문에서 써야 할 Related Work 문단 초안

Frequency diversity and frequency-hopped signaling have been used previously in underwater acoustic positioning and sonar systems. Beaujean, Mohamed, and Warin used frequency-hopped acoustic modem sequences for source localization with a tetrahedral USBL array, showing that a communication waveform can also support azimuth/elevation and 3D position estimation. Costas hopping has also been applied to shallow-water USBL signal design to improve correlation-peak time-delay estimation and optimize the receiver baseline. More recent inverted USBL studies have explored acoustic frequency-comb signals, and MIMO sonar studies have used transmitting diversity smoothing for DOA estimation.

These studies motivate the use of frequency diversity in underwater acoustics, but they address different failure modes. Their primary goals are communication-aided localization, waveform correlation improvement, baseline optimization, multi-frequency signal design, or covariance-domain DOA estimation. In contrast, the present study begins from a post-gating error analysis of a TOA/TDOA/DOA-UKF USBL tracker. We identify a carrier-locked coherent multipath DOA bias caused by in-gate surface-reflection leakage and use ping-to-ping carrier agility to decorrelate this residual bias before it enters the UKF. The contribution is therefore not the first use of frequency hopping in USBL, but the use of carrier agility as a transmit-side observation design for coherent multipath DOA-bias whitening, together with static-target validation and moving-target applicability boundaries.

## 4. 리뷰어 공격별 대응 문장

### 공격 1: “USBL에서 frequency hopping은 이미 있다.”

인정한다. Frequency-hopped modem sequences and Costas hopping waveforms have been used in USBL or underwater acoustic positioning. Our claim is not the first use of frequency hopping in USBL. The novelty is the identification of a carrier-locked coherent multipath DOA-bias floor after direct-path gating and the use of ping-to-ping carrier agility to whiten that bias in a UKF tracking loop.

### 공격 2: “Costas hopping USBL와 무엇이 다른가?”

Costas USBL work uses frequency-hopping waveform structure to improve correlation-peak/time-delay precision and baseline optimization. Our method changes the carrier schedule across pings to rotate the direct-reflection interference phase `φ=2πfδ`, thereby reducing the temporal correlation of DOA bias. The target error source and the estimator-level validation are different.

### 공격 3: “Radar frequency agility/glint와 같은 아이디어 아닌가?”

원리적 관련성은 인정한다. Radar frequency agility provides an important prior concept for decorrelating carrier-sensitive angle errors. However, the underwater mechanism here is different: in-gate surface-reflection leakage in shallow-water gated USBL processing, not radar target-scatterer glint. The paper contributes the underwater mechanism, the USBL/UKF validation, and the static/moving applicability boundary.

### 공격 4: “Moving target에서는 성능 개선이 없는데 방법이라고 할 수 있는가?”

The moving-target result is treated as an applicability boundary, not as a positive performance claim. Frequency agility strongly whitens the moving DOA residuals, but target motion already changes the interference delay difference `δ(t)`, producing motion-induced self-whitening under fixed carrier transmission. The validated performance claim is static/quasi-static long-range localization.

## 5. 원고 표현 가이드

### 피해야 할 표현

- “first frequency-hopping USBL method”
- “first use of frequency diversity in underwater positioning”
- “frequency agility universally improves underwater localization”
- “moving-target RMSE improvement”

### 써도 되는 표현

- “frequency-agile pinging for coherent multipath DOA-bias whitening”
- “ping-to-ping carrier agility as transmit-side observation design”
- “static/quasi-static long-range USBL validation”
- “moving-target boundary due to motion-induced self-whitening”
- “distinct from frequency-hopped modem localization, Costas waveform correlation improvement, and MIMO transmitting diversity smoothing”

## 6. 남은 확인

- JASA 2007 원문에서 multipath/DOA bias/whitening 언급 여부 확인.
- IEEE 2022 Costas USBL 원문에서 목적함수와 실험 조건 확인.
- Scopus/WoS에서 “USBL + multipath DOA bias + frequency hopping/carrier agility” 조합 최종 스팟체크.
- 레이더 glint/frequency agility old IEEE exact citation의 저자·연도·쪽수 확정.
