# Final Related Work defense table

## 원고에서 절대 지킬 프레임

본 논문은 “frequency hopping USBL 최초”가 아니다. Related Work의 첫 문장은 다음 톤이어야 한다.

> Frequency-diverse acoustic signaling has already appeared in underwater positioning and sonar.
> The present work addresses a narrower failure mode: post-gating coherent multipath DOA bias in
> compact shallow-water USBL tracking.

## 최종 차별표

| 선행연구군 | 현재 인용 상태 | frequency diversity 방식 | 주된 목적 | 우리와 다른 핵심 |
|---|---|---|---|---|
| Radar frequency agility / glint — Loomis & Graf 1974, Delano 1953 | `paper/refs.bib` 포함 | pulse-to-pulse 또는 waveform/frequency diversity | radar glint / angular scintillation 완화 | 원리적 유산은 인정. 그러나 도메인은 radar target scattering이고, 우리는 shallow-water USBL의 in-gate surface-reflection coherent DOA bias |
| Frequency-hopped acoustic modem USBL — Beaujean et al. 2007 | `paper/refs.bib` 포함 | frequency-hopped modem sequence | acoustic modem source의 range/AoA/3D positioning | frequency-hopped signal을 위치추정에 쓰지만, post-gating DOA elevation bias floor나 ping간 residual whitening을 다루지 않음 |
| Costas hopping USBL — Nhat et al. 2022 | `paper/refs.bib` 포함 | intra-ping Costas waveform, 28–36 kHz 계열 | sharp autocorrelation peak, TOA/time-delay precision, baseline optimization | 우리와 가장 가까운 위험논문. 그러나 목적은 time-delay/ranging precision이며, multipath 저항도 delay-domain pulse compression. 우리는 inter-ping carrier schedule로 DOA bias time-correlation을 whitening |
| Frequency-comb iUSBL — Qian et al. 2025 | `paper/refs.bib` 포함 | coherent multi-frequency comb | positioning + communication integration, spectral efficiency, ranging | comb/multi-frequency 신호이지만, multipath DOA bias whitening이 아님. 원문상 multipath는 beamforming/channel estimation 쪽으로 미룸 |
| Acoustic glint / broadband direction finding — Henderson 1985 | BibTeX 미포함, 선택 후보 | broadband matched beam / direction finding | acoustic extended-target glint 또는 angular ambiguity 완화 | “acoustic에서 glint를 다룬 선례”로 위험하지만, target-scatterer/beamforming 문제이고 USBL in-gate surface reflection + UKF tracking 문제가 아님 |
| MIMO sonar transmitting diversity smoothing | BibTeX 미포함, 선택 후보 | MIMO transmit diversity / covariance smoothing | coherent source DOA estimation 개선 | covariance-domain DOA estimation. 본 논문은 tracking residual의 ping-to-ping temporal correlation whitening |
| Frequency diverse array sonar — Liu & Yang 2026 계열 | BibTeX 미포함, 선택 후보 | array element별 frequency increment | range-angle coupled beampattern / ambiguity function | 같은 frequency diversity라도 공간 배열 개념. 우리는 시간축 ping간 carrier agility |
| USBL differential/calibration correction — Zhang et al. 2024 등 | BibTeX 미포함, 선택 후보 | 보통 frequency diversity 아님 | positioning bias correction, calibration, differential correction | bias를 다루지만 carrier-locked coherent multipath DOA residual을 whitening하는 송신 observation design이 아님 |

## 원고 테이블에 꼭 들어가야 하는 4개 축

1. Radar glint/frequency agility: “원리 유산 인정”
2. Frequency-hopped modem USBL: “USBL frequency hopping 선행 인정”
3. Costas USBL: “가장 가까운 shallow-water waveform 선행 인정”
4. Frequency-comb iUSBL: “multi-frequency underwater positioning 선행 인정”

이 네 축이 있으면 reviewer가 “이미 있다”고 공격할 때 정면 대응이 가능하다.

## 선택 인용 판단

Henderson, Zhang, Liu/FDA까지 모두 넣으면 Related Work가 매우 단단해지지만 표가 과밀해질 수 있다.
저널 분량이 빡빡하면 Discussion 또는 reviewer response용으로 보류해도 된다.

권고:

- 1차 투고 원고: 현재 5개 핵심 인용 유지 + Nhat/Qian 차이 설명 강화.
- 여유가 있으면: Henderson 1985 또는 Zhang 2024 중 하나를 추가.
- reviewer response 대비: Liu/FDA, MIMO TDS, Qin radar height/multipath는 back-pocket 문헌으로 유지.
