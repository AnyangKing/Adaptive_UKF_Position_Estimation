# Real-water / tank validation protocol

## 고정해야 할 연구 중심축

- 배열: 기존 8센서 USBL 배열 유지.
- 관측: TOA, TDOA, DOA를 모두 사용.
- 필터: 기존 conditional adaptive-R UKF 유지.
- 비교: fixed 32 kHz vs ping-to-ping 30–34 kHz carrier-agile schedule.
- 핵심 기전: direct-path gate 안에 남는 surface-reflection coherent leakage가 DOA residual 시간상관을 만들고,
  carrier agility가 이를 whitening하는지 확인.

## Tier 1. Mechanism validation

### 목적

실제 물에서 “성능 개선”보다 먼저 **carrier-sensitive DOA residual whitening**이 보이는지 확인한다.
이 단계는 논문 본체의 물리 기전을 방어하는 실험이다.

### 권장 구성

- 8센서 USBL 수신 배열.
- 30–34 kHz LFM 송신 가능한 pinger/transducer.
- fixed 32 kHz 모드와 20-ping linear carrier-agile 모드.
- 송수신 동기 또는 기준시각 기록.
- 수심, 송수신기 깊이, 수온/음속, 표면 상태 기록.
- ground-truth geometry: 수조/부두/호수에서 줄자·RTK-GPS·depth sensor 등으로 가능한 한 고정.

### 조건

| 조건 | 권장값 |
|---|---|
| 거리 | 가능한 범위에서 50, 100, 200 m부터 시작 |
| 수심 | surface reflection이 direct gate 근처에 들어오는 조건 우선 |
| 표적 | 정지 pinger 또는 고정된 transponder |
| ping 수 | 조건당 최소 40, 권장 60~100 |
| schedule | fixed block과 hop block을 ABBA 또는 randomized block으로 교차 |

### 1차 지표

- DOA elevation residual lag-1 correlation.
- fixed vs hop residual autocorrelation 차이.
- carrier별 DOA residual 평균/분산.
- matched-filter peak와 direct gate 내 후속 energy.

### 해석

- fixed에서 residual lag-1이 충분히 크고 hop에서 감소하면 기전 확인.
- fixed에서도 lag-1이 작으면 “환경이 이미 self-whitened / coherent leakage가 약함”으로 해석한다.
- RMSE 개선이 없어도 Tier 1은 실패가 아닐 수 있다. 기전 확인이 목적이다.

## Tier 2. Static long-range validation

### 목적

시뮬레이션의 핵심 claim인 static 600 m 개선을 실제 물에서 검증한다.

### 권장 조건

| 조건 | 최소 | 권장 |
|---|---:|---:|
| 거리 | 200, 400 m | 100, 200, 400, 600 m |
| 기하 반복 | 거리당 6 geometry | 거리당 12~20 geometry |
| ping 수 | geometry당 40 | geometry당 60~100 |
| 비교 | fixed vs hop paired | randomized ABBA block |
| 정착창 | 후반 50% | 시뮬레이션과 맞추려면 후반 10 ping도 병행 계산 |

### 분석

각 geometry에서 fixed/hop을 paired로 비교한다.

- settled RMSE.
- median RMSE.
- P90 / tail.
- divergence or gross-error rate.
- DOA elevation residual lag-1.
- lag-1 reduction vs RMSE gain correlation.

### 주의

실제 600 m에서 ground truth가 가장 어렵다. RTK-GPS buoy + depth sensor + mooring line geometry를
사용하더라도 표적 흔들림이 생길 수 있다. 따라서 실험 기록에는 표적 위치 불확실도를 별도로 남겨야 한다.

## Tier 3. Very-slow-drift validation

### 목적

82번 시뮬레이션에서 안전했던 0.005 m/s very slow drift 경계를 실제 물에서 확인한다.

### 구성

- 정지 pinger를 매우 천천히 이동시키거나, mooring/boat drift를 이용하되 ground-truth 궤적을 기록.
- 목표 속도: 0.005 m/s 근처.
- 0.010 m/s 이상은 연속 경계로 주장하지 말고 탐색 조건으로 둔다.

### 분석

- static과 동일한 paired RMSE/lag-1 분석.
- 속도별 단조 경계를 주장하지 않는다.
- drift 방향(radial/tangential)을 분리해 기록한다.

## 권장 현장 순서

1. dry run: 장비 동작, 동기, 녹음, carrier schedule 확인.
2. Tier 1: 짧은 거리에서 fixed/hop residual lag-1 확인.
3. Tier 2 pilot: 200/400 m 정지 조건.
4. Tier 2 full: 가능하면 600 m 정지 조건.
5. Tier 3: 0.005 m/s very slow drift 조건.

## 원고 반영 규칙

- Tier 1만 성공: “real-water mechanism evidence”로 보조자료/후속연구에 사용.
- Tier 2까지 성공: 논문 본체의 simulation limitation을 크게 완화 가능.
- Tier 3까지 성공: static/quasi-static claim을 더 강하게 만들 수 있음.
- moving target 일반 성능은 별도 실험 없이는 주장하지 않는다.
