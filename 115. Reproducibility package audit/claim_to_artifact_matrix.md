# Claim-to-artifact matrix

## 감사 원칙

- 원고의 숫자는 최종 원고 문장이 아니라 **채택 코드와 결과 JSON**을 기준으로 확인한다.
- 결과 파일은 대부분 `results/` 아래에 있으며 로컬 전용이다. GitHub 공개 저장소에는 없을 수 있다.
- `paper/` 원고 파일은 로컬 전용이며 GitHub에 올리지 않는다.

## 핵심 주장별 근거

| 원고 주장 / 그림 | 최종 수치·판정 | 실행 코드 | 결과 데이터 | 재현 상태 |
|---|---:|---|---|---|
| Fig.2 / 기전: 장거리에서 반송파 도약 평균이 고도각 편향을 줄임 | 400 m: 78.35% 감소, 600 m: 91.57% 감소. 100/200 m는 비일관 또는 악화 가능 | `58. 반송파 미세도약 코히어런트 편향 진단/run_agility.py` | `58.../results/agility.json` | JSON 존재, 수치 확인 |
| Fig.3 / 본체 성능: 정지 600 m에서 frequency-agile pinging이 RMSE 개선 | fixed 13.0065 m → hop 8.8698 m, 개선 +4.1368 m, p=0.000845, n=20 | `61. 정지표적 도약 대규모 독립검증/run_static_hop.py` | `61.../results/static_hop_validation.json` | JSON 존재, 수치 확인 |
| Fig.4 / 이동 경계: residual whitening은 강하지만 pooled RMSE gain은 미재현 | lag-1 +0.46995 → -0.20808, p=5.56e-10. pooled gain -0.103 m, p=0.301 | `63. 이동표적 도약 대규모검증 백색화 확인/run_moving_validation.py` | `63.../results/moving_validation.json` | JSON 존재, 수치 확인 |
| Fig.5 / 준정지 경계 | 전체 132 paired: fixed 11.9835 m → hop 10.4921 m, p=8.00e-05. 단, 연속 안전 경계는 0.005 m/s | `82. 준정지 속도 경계 검증 실행/run_quasi_static_boundary.py` | `82.../results/quasi_static_boundary.json`, `quasi_static_trials.csv` | JSON/CSV 존재, 수치 확인 |
| Fig.6 / 개구·CRLB 하한 | 600 m empirical CRLB 11.80 m, routing RMSE 12.29 m, residual bias floor 3.446 m | `45. CRLB 이론하한 대비 효율/` | `45.../results/crlb.json` | JSON 존재, 수치 확인 |
| Method / 신호·채널·배열·필터 상수 | 8 sensors, 33 mm ring radius, 79 mm vertical offset, fs 192 kHz, 5 ms direct gate, UKF α=0.3 β=2 κ=0 | `93. Method 세부 코드 대조/extract_method_facts.py` | `93.../results/method_facts.json` | JSON 존재, 수치 확인 |
| Fig.1 / 시스템·기전 개념도 | 정량 claim 없음. 직접파 + 게이트 내 표면반사 + fixed/hop phase-locking 구조 설명 | `101. Fig1 visual polish/make_fig1_polished.py` | `101...` 산출 PNG/SVG, `95.../figures/` 취합본 | 원고용 그림 패키지 존재 |
| Fig.2~6 원고용 그림 파일 | PNG/SVG 6종 | `70. 논문 그림 1차 생성/generate_core_figures.py`, `95.../generate_fig5_png.py` | `95. Fig5 PNG and submission packaging/figures/` | 그림 매니페스트 존재 |

## 주장의 안전 경계

| 항목 | 안전한 표현 | 금지 표현 |
|---|---|---|
| Novelty | “현재 조사 범위에서 직접 선행연구를 찾지 못했다”; “frequency hopping 자체가 아니라 post-gating coherent DOA bias whitening이 기여” | “세계 최초 frequency-hopping USBL” |
| 정지 표적 | “600 m static long-range에서 독립 seed 재현” | “모든 거리에서 향상” |
| 준정지 | “0.005 m/s까지의 very slow drift는 연속 경계로 안전” | “0.1 m/s까지 검증” |
| 이동 표적 | “lag-1 whitening은 강함, RMSE gain은 pooled 기준 미재현” | “moving target 위치추정 성능 개선 검증” |
| 성능 규모 | “13.0→8.9 m로 coherent bias 성분 감소” | “소형 USBL로 600 m sub-meter 달성” |

## 감사 판정

핵심 claim은 모두 실제 JSON/CSV 또는 그림 생성 산출물로 연결된다. 가장 큰 운영 리스크는 과학적 수치가
아니라 **패키징 정책**이다. 즉 결과 데이터가 GitHub에 없고, 논문 파일은 로컬 `paper/`에만 있어야 하므로,
투고 보충자료를 만들 때 임의로 `git add .`를 쓰면 안 된다.
