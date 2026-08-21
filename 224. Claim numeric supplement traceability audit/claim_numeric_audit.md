# Claim/numeric traceability audit

## 1. 191 structured moving validation

원천 파일: `191. Moving full range transition aware independent validation/moving_full_range_independent_validation.json`

| 항목 | JSON 값 | 원고 사용 |
| --- | ---: | --- |
| paired cases | 528 | 528 paired cases |
| fixed mean RMSE | 12.1857 m | gain 계산의 fixed 기준 |
| hop mean RMSE | 11.3368 m | gain 계산의 hop 기준 |
| transition-aware soft-R mean RMSE | 7.3890 m | gain 계산의 proposed 기준 |
| soft-R gain vs hop | 3.9479 m | 3.95 m |
| soft-R gain vs fixed | 4.7968 m | 4.80 m |

판정: 일치. 단, 0 m에서는 soft-R이 fixed 대비 약간 악화되므로 “모든 거리에서 항상 개선” 식의 표현은 금지한다. 현재 원고는 이 경계를 노출하고 있다.

## 2. 204 OOD moving aggregate

원천 파일: `204. Overnight OOD validation aggregate result/compact_metrics.json`

| 항목 | JSON 값 | 원고 사용 |
| --- | ---: | --- |
| completed cases | 528 | 528 paired cases |
| fixed mean RMSE | 10.8322 m | 10.83 m |
| hop mean RMSE | 10.6909 m | 10.69 m |
| transition-aware soft-R mean RMSE | 7.8095 m | 7.81 m |
| fixed P90 | 22.3394 m | 22.34 m |
| hop P90 | 21.6110 m | 21.61 m |
| soft-R P90 | 15.9360 m | 15.94 m |

판정: 일치. 이 결과는 OOD robustness support로만 사용해야 하며 arbitrary-motion/general real-water 보장으로 쓰면 안 된다. 현재 원고는 이 경계를 명시한다.

## 3. 215 hardware frequency response sensitivity

원천 파일: `215. Hardware frequency response sensitivity/hardware_response_sensitivity.json`

| profile | soft-R mean RMSE | cases/profile |
| --- | ---: | ---: |
| flat reference | 7.6839 m | 192 |
| edge loss 3 dB | 7.6769 m | 192 |
| edge loss 6 dB | 7.6873 m | 192 |

판정: 일치. 원고의 `7.68--7.69 m over 192 paired cases per profile` 표현은 JSON 반올림과 맞다.

주의: 이것은 측정된 transducer/hydrophone response 검증이 아니라, 이상화된 edge-loss sensitivity simulation이다.

## 4. 216 extended OOD-family check

원천 파일: `216. Extended OOD motion family validation/extended_ood_motion_family_validation.json`

| 항목 | JSON 값 | 원고 사용 |
| --- | ---: | --- |
| paired cases | 144 | 144 additional OOD-family cases |
| fixed mean RMSE | 12.4752 m | 12.48 m |
| hop mean RMSE | 11.3712 m | 11.37 m |
| transition-aware soft-R mean RMSE | 8.1284 m | 8.13 m |

판정: 일치. 이 결과는 추가 OOD-family robustness check이며, 일반 이동 표적 전체를 보장하는 결과가 아니다.

## 전체 판정

현재 원고의 핵심 수치·경계 문구는 주요 결과 파일과 정합한다.

새로운 시뮬레이션 없이도 논문에 들어간 수치 추적성은 방어 가능한 상태다.
