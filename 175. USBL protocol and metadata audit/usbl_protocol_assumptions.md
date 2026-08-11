# USBL 수신 프로토콜 가정

## 현재 canonical validation의 프로토콜

현재 채택 코드(43, 44, 46, 61, 63, 82, 160--162)의 기본 수신 프로토콜은 다음과 같이 해석한다.

| 항목 | 현재 가정 | 근거/설명 |
|---|---|---|
| 송신원 | synchronized beacon | 표적 또는 송신원이 알려진 ping waveform을 송신하고, 수신기는 one-way TOA를 range로 변환한다. |
| TOA 종류 | one-way absolute TOA | 관측 벡터의 첫 항은 `c * absolute_toas[0]`이다. |
| clock sync | 송신 시각 또는 TOA offset이 보정되어 있다고 가정 | common clock bias를 상태나 관측모델에 넣지 않는다. |
| transponder two-way time | 미사용 | 현재 코드에는 interrogation/reply turnaround time 모델이 없다. |
| common clock bias | canonical validation에서는 미모델링 | 절대 TOA에 공통 offset이 있으면 range 항에 직접 영향을 주므로 별도 실험이 필요하다. |
| sensor별 hardware delay | canonical validation에서는 미모델링 | 센서별 고정 delay/gain/phase mismatch는 현재 채택 성능 수치에 포함되지 않는다. |
| sensor/channel delay time variation | 미모델링 | canonical channel은 direct/surface/bottom image-source path와 noise 중심이다. |

## 논문에서 안전한 표현

쓸 수 있는 표현:

> We evaluate a one-way synchronized-beacon USBL setting in which the transmit epoch, or equivalently the common TOA offset, is assumed calibrated. The reported canonical validation does not include explicit common clock bias or per-sensor hardware delay mismatch.

한국어 원고 표현:

> 본 논문의 canonical validation은 송신 시각 또는 공통 TOA offset이 보정된 one-way synchronized beacon 설정을 가정한다. 따라서 기준 센서 TOA는 곧바로 거리 관측으로 환산된다. common clock bias, 센서별 hardware delay, gain/phase mismatch는 본 validation의 성능 수치에 포함하지 않았으며, 실제 해상 실험에서는 별도 보정 또는 확장 상태로 다루어야 한다.

## 쓰면 안 되는 표현

- 현재 결과를 two-way transponder USBL 검증으로 부르지 않는다.
- common clock bias나 sensor delay가 포함된 practical USBL 성능으로 말하지 않는다.
- clock/sensor calibration이 없어도 absolute TOA가 그대로 성립한다고 주장하지 않는다.

## 후속 실험이 필요한 경우

실제 field experiment 또는 더 현실적인 simulation으로 확장할 때는 다음을 별도 조건으로 분리한다.

1. common clock bias 상태 추가 또는 사전 보정 오차 sweep
2. sensor별 fixed delay mismatch
3. ping별 sensor delay jitter
4. sensor별 gain/phase mismatch
5. beacon one-way와 transponder two-way protocol 비교

