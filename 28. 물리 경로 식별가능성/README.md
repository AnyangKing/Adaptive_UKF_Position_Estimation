# 28. 물리 경로 식별가능성

## 목적

물리 경로 확률을 이용하는 신규 칼만필터를 만들기 전에, 12 kHz LFM 신호에서 직접파·표면반사·
해저반사의 matched-filter peak가 실제로 분리되어 관측되는지 확인한다.

## 설계

- 거리: 100/200/400/600 m
- 송신기 수심: 15/45/75 m
- SNR: 10/20/30 dB
- 반사계수와 방위 및 noise seed 변화, 총 180개 장면
- 8센서 합계 1,440개 관측
- 검출 허용오차: `2 / bandwidth = 166.7 µs`
- Ground Truth 경로 지연은 평가에만 사용하며 peak 추출에는 사용하지 않음

## 실행

```powershell
python test_path_identifiability.py
python path_identifiability.py
```

## 결과 (2026-07-05)

- 직접파 recall: 모든 거리/SNR에서 100%
- 표면반사 recall: 모든 거리/SNR에서 100%
- 해저반사 recall: 모든 거리/SNR에서 100%
- 경로 지연오차 P90: 대략 11.3~12.4 µs
- 직접파-표면반사 최소 간격: 997.1 µs
- 직접파-해저반사 최소 간격: 3,857.1 µs

## 판정과 제한

물리 경로의 시간 구조는 현재 파형 분해능에서 충분히 관측 가능하므로 신규 알고리즘의 전제는
**통과**한다. 다음 단계는 Ground Truth 없이 UKF 사전 위치가 예측한 지연 패턴만으로 peak를
direct/surface/bottom에 연관하고 경로 확률을 계산하는 것이다.

단, 현재 채널은 정확히 세 개의 평면 image-source 경로만 생성한다. 100% recall은 현실 해양의
완벽한 식별을 뜻하지 않으며, blind association 이후 확산 다중경로·음속 구배·해수면 변동을
추가한 채널에서 반드시 다시 검증해야 한다.
