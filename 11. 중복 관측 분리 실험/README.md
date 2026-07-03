# 11. 중복 관측 분리 실험

## 목적

TDOA와 SRP-PHAT DOA는 같은 센서쌍 지연을 재사용하므로 강하게 상관된다. cross
covariance를 무시한 채 함께 넣으면 방향정보를 중복 계산할 수 있다. 관측 block을
선택적으로 비활성화해 실제 영향을 확인한다.

## 조합

- full: TOA + TDOA + SRP DOA
- TOA + SRP DOA
- TDOA + SRP DOA
- tracked TOA + SRP DOA
- TOA + TDOA, DOA 제외

비활성 block은 분산을 `1e8`로 두고 다른 block과 cross term을 0으로 만들어 Kalman
gain이 사실상 0이 되게 한다. 필터 코드와 관측 차원은 동일하게 유지한다.

모든 조합은 같은 30개 원시 ping, 독립 noise seed, Q, 초기 공분산과 adaptive 규칙을
사용한다. 약 200 m 단일 궤적의 구조 ablation이며 최종 거리별 결과가 아니다.

## 실행

```powershell
python test_blocks.py
python run_compare.py
```

## 최초 결과 (2026-07-03)

| 조합 | 수렴 후 RMSE | 방사 RMSE | 횡방향 RMSE |
|---|---:|---:|---:|
| TOA + TDOA + SRP | **8.284 m** | 1.189 m | **8.198 m** |
| TOA + SRP | 12.299 m | 1.244 m | 12.236 m |
| TDOA + SRP | 17.788 m | 15.446 m | 8.823 m |
| tracked TOA + SRP | 12.387 m | **0.816 m** | 12.360 m |
| TOA + TDOA | 15.102 m | 1.875 m | 14.985 m |

중복정보 우려와 달리 full 조합이 가장 좋았다. 작은 aperture에서 TDOA와 SRP는 같은
원시 지연을 쓰더라도 서로 다른 집계 방식으로 방향을 보완한다. TOA는 방사거리와
전체 위치 안정성에 필수적이었다.

따라서 관측 block을 단순 제거하는 방법은 채택하지 않고 TOA+TDOA+SRP 구조를 유지한다.
이는 cross covariance가 불필요하다는 뜻은 아니다. 단지 현재 오차 수준에서는 정보
제거 손실이 중복 과신 위험보다 컸다는 결과다. 향후 충분한 calibration 표본으로 full
cross covariance를 추정하거나 covariance intersection을 비교해야 한다.
