# 71. 그림 캡션과 Results 문단 조립

## 목적

70번에서 생성한 핵심 정량그림 4개를 논문 문장으로 연결한다. 이 폴더는 새 실험이 아니라 manuscript assembly 단계다.

## 입력

- `70. 논문 그림 1차 생성/figures/fig2_frequency_agile_bias.*`
- `70. 논문 그림 1차 생성/figures/fig3_static_600m_paired_rmse.*`
- `70. 논문 그림 1차 생성/figures/fig4_moving_whitening_lag1.*`
- `70. 논문 그림 1차 생성/figures/fig7_crlb_floor.*`
- `70. 논문 그림 1차 생성/figures/summary_numbers.json`

## 출력

- `figure_captions_and_results.md`
  - Fig. 2/3/4/7 영어 캡션 초안
  - Results 섹션 문단 초안
  - 각 그림이 주장하는 것과 주장하지 않는 것

## 핵심 판단

현재 논문 본체는 “frequency agility가 모든 상황에서 위치추정을 개선한다”가 아니다. 더 정확한 주장은 다음이다.

> In shallow-water gated USBL processing, carrier-frequency agility decorrelates coherent multipath-induced DOA bias. This yields reproducible RMSE improvement for static/quasi-static long-range targets, while moving targets exhibit residual whitening without reliable RMSE gain because motion already changes the interference geometry.

이 문장이 논문 결과부의 안전한 중심선이다.

## 다음 단계

72번은 둘 중 하나가 좋다.

1. Fig. 1 시스템/게이트-내 표면반사 개념도 생성
2. Introduction 초안 작성 및 레이더 glint 선행문헌 정확 서지 채우기

개인적으로는 Fig. 1을 먼저 만들면 Mechanism 절이 훨씬 쓰기 쉬워진다.
