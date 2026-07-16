# 교수님 보고용 요약 초안

교수님께 보여드릴 때는 아래 순서로 설명하면 됩니다.

## 1. 연구 출발점

처음 아이디어는 수중 USBL 위치추정에서 TOA, TDOA, DOA 관측을 UKF에 넣어 3차원 위치를 안정적으로 추정하는
것이었습니다. 그런데 시뮬레이션을 진행하면서, 장거리 compact USBL에서는 단순히 필터를 바꾸거나 R을 튜닝하는
것만으로는 오차가 충분히 줄지 않는다는 점이 확인되었습니다.

## 2. 발견한 핵심 한계

장거리 600 m 조건에서 남는 오차는 zero-mean noise라기보다, direct-path gate 안에 들어오는 surface reflection이
compact array의 DOA 추정에 coherent bias를 만드는 문제로 해석되었습니다. 즉, 필터가 나쁜 것이 아니라 필터에
들어가는 DOA 관측 자체에 carrier-locked residual이 남는 구조였습니다.

## 3. 제안 방법

수신기 알고리즘은 그대로 둡니다.

- TOA 추출
- TDOA 추출
- DOA 추출
- adaptive-R UKF fusion

대신 송신 carrier를 ping마다 30--34 kHz 범위에서 바꿉니다. 그러면 direct path와 in-gate reflected path 사이의
coherent phase가 고정되지 않고 회전하면서, 반복 ping에서 같은 방향으로 쌓이던 DOA bias가 whitening됩니다.

## 4. 핵심 검증 결과

가장 강한 결과는 static 600 m입니다.

- fixed 32 kHz: 13.01 m settled RMSE
- carrier-agile: 8.87 m settled RMSE
- improvement: 32%
- paired gain: +4.14 m
- p = 0.0008

기전 검증도 있습니다.

- moving residual lag-1 correlation: +0.470 to -0.208
- p = 5.56e-10
- two-ray carrier-bias prediction: R² up to 0.99

## 5. 주장하지 않는 것

moving target 일반 개선은 주장하지 않습니다.

moving case에서는 residual whitening은 강하게 확인됐지만, pooled RMSE improvement는 재현되지 않았습니다.

- moving RMSE gain: -0.10 m
- p = 0.301

따라서 논문은 “moving AUV 전체에 적용되는 만능 위치추정 방법”이 아니라, static 또는 very-slow-drift 장거리
USBL에서 coherent DOA bias를 줄이는 bounded observation-design 방법으로 정리했습니다.

## 6. 현재 논문 상태

현재 원고는 IEEEtran journal-format neutral draft입니다.

- 12 pages
- unresolved citation/reference 없음
- overfull/underfull hbox 없음
- 저자/소속/Funding/Data Availability/Acknowledgment는 placeholder

즉, 과학적 구조와 원고 골격은 보여드릴 수 있는 상태이고, 제출 전에는 저자정보와 실제 목표 저널, 그리고
실험 추가 여부를 결정해야 합니다.

## 7. 교수님께 여쭤볼 것

1. 이 논문을 simulation + mechanism + boundary paper로 먼저 진행할지.
2. 제출 전 수조/호수 실험을 반드시 붙일지.
3. 목표 저널을 IEEE 계열로 둘지, Ocean Engineering/Applied Acoustics/Sensors 계열로 돌릴지.
4. 저자 순서와 소속 표기를 어떻게 할지.
5. 코드/데이터 공개를 GitHub/Zenodo/요청 시 제공 중 어느 방식으로 할지.

