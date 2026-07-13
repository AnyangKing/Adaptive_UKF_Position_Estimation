# Risk and fallback plan

## Risk 1. 실제 물에서 coherent locked bias가 약하게 나타남

### 증상

- fixed 32 kHz에서도 DOA residual lag-1이 낮음.
- carrier별 residual 차이가 작음.

### 해석

방법 실패가 아니라 실험 조건에서 direct/surface reflection interference가 gate 안에 강하게 형성되지 않은
것일 수 있다.

### 대응

- 송수신 깊이와 거리 조합을 바꿔 surface-reflection excess delay가 5 ms gate 근처에 들어오게 조정.
- 더 잔잔한 표면 조건에서 반복.
- Tier 1을 수조/부두 조건으로 되돌려 기전부터 확인.

## Risk 2. ground truth 오차가 RMSE gain보다 큼

### 증상

- fixed/hop 차이가 1~2 m 수준인데 표적 위치 불확실도도 비슷함.
- GPS buoy, mooring line, depth sensor 기록이 불충분.

### 대응

- RMSE headline 대신 residual whitening을 primary metric으로 둔다.
- static long-range 성능 claim에는 사용하지 않는다.
- ground truth 보강 후 재실험.

## Risk 3. 송신 carrier별 출력/대역 차이가 공정하지 않음

### 증상

- 특정 carrier에서 SNR이 낮거나 matched-filter peak가 작음.
- hop 성능 변화가 whitening이 아니라 SNR 변화로 설명될 수 있음.

### 대응

- carrier별 송신 출력 calibration.
- 각 carrier의 matched-filter SNR을 공변량으로 기록.
- 가능하면 동일 received level이 되도록 보정.

## Risk 4. 해상/호수 환경 변화가 fixed/hop paired 비교를 깨뜨림

### 증상

- fixed block과 hop block 사이에 배 위치, 표면 상태, 소음 조건이 바뀜.

### 대응

- ABBA 또는 randomized block으로 순서 효과를 줄임.
- block 시간을 짧게 유지.
- 환경 변화가 큰 block은 exclusion rule로 제외.

## Risk 5. 600 m 실험이 물리적으로 어렵거나 허가가 늦음

### 대응

- 200/400 m에서 mechanism + partial performance pilot 수행.
- 논문 본체는 simulation validation으로 유지하고, field pilot은 future work 또는 supplementary로 둔다.
- 600 m는 교수님 복귀 후 장비/장소/허가가 확정되면 별도 계획으로 승격.

## Risk 6. Tier 2에서 hop이 tail을 악화

### 해석

시뮬레이션의 moving/tail 교훈과 일치할 수 있다. 즉 항상-on hop은 일부 기하에서 위험할 수 있다.

### 대응

- 성능 claim을 축소.
- lag-1 whitening과 tail 악화를 분리해 보고.
- future work로 risk-aware schedule을 둔다.

## 최종 fallback

실해역 실험이 불발되어도 현재 논문은 “simulation/signal-level validation + 정직한 limitation”으로 제출
가능한 구조를 유지한다. 단, 목표 저널이 field validation을 강하게 요구하면 투고 목표를 조정하거나
real-water validation을 선행해야 한다.
