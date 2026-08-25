# 238/239 원고 반영 보고

## 반영 위치

- 영문 원고: `Transition-Aware Adaptive-R Moving Validation` 절
- 한글 원고: `Transition-aware Adaptive-R 이동 표적 검증` 절
- 새 표: `tab:consistencyaxis`

## 반영한 핵심 문장

238번 결과는 soft-$R$가 RMSE 개선만 만든 것이 아니라 hopping baseline의 심한 과신도 줄였다는 근거로 반영했다.

- position NEES: 255.84 → 16.00
- total NIS 99% exceedance fraction: 0.119 → 0.038
- total NIS: 23.02 → 3.65

다만 이상적 3D position NEES 평균은 약 3이므로, 완전 calibration claim은 금지했다. 원고에서는 soft-$R$를 “robust adaptive covariance-inflation rule”로 정의했다.

239번 결과는 3D RMSE 개선이 특정 축 하나의 착시가 아니라는 근거로 반영했다.

- horizontal RMSE: 7.46 → 4.85 m
- vertical RMSE: 7.44 → 4.58 m
- cross-range RMSE: 7.28 → 4.66 m
- radial RMSE: 0.94 → 0.63 m

## 넣지 않은 주장

다른 AI가 언급한 DOA block NIS 우세 주장은 238 최종 JSON의 최종 업데이트 기준 block NIS 요약과 맞지 않았다. 따라서 원고에는 넣지 않았다.

## Claim boundary

이 반영은 simulation-level structured moving-target diagnostic이다. 실해역, 실제 하드웨어 주파수 응답, 임의 moving-target 보장을 의미하지 않는다.

## 검증

- `audit_manuscript_integration.py`: PASS
- `latexmk manuscript.tex`: PASS, 영문 PDF 16쪽 생성
- `latexmk manuscript_ko.tex`: PASS, 한글 PDF 17쪽 생성

빌드는 MiKTeX 사용자 AppData 초기화 경로 때문에 권한 승격으로 확인했다. 남은 메시지는 underfull 계열 조판 경고이며 fatal error는 없었다.
