# 24. 600 m 장기 수렴 분석

## 목적

23번 600 m 평균 RMSE 10.93 m가 10-ping의 초기오차 때문인지 정상상태 한계인지 분리한다.
알고리즘과 파라미터를 바꾸지 않고 신규 4개 30-ping 궤적을 실행한다.

## 지표

- initial error
- step 3/10/20 이후 RMSE
- 마지막 5 ping 평균과 final error
- 5 ping 연속 5 m 미만에 처음 도달한 step
- 최소·최대오차와 조건부 라우팅 발동률

SNR, 방위, 수심, 속도, 반사계수와 Doppler는 trial별로 무작위이며 ping별 noise seed는
독립이다. 결과를 보고 Q/R이나 문턱을 수정하지 않는다.

## 실행

```powershell
python test_convergence.py
python run_convergence.py
```

## 최초 결과 (2026-07-03)

4개 30-ping 궤적 평균:

| 지표 | 결과 |
|---|---:|
| 초기오차 | 14.054 m |
| step 3 이후 RMSE | 11.908 m |
| step 10 이후 RMSE | 12.270 m |
| step 20 이후 RMSE | 11.444 m |
| 마지막 5 ping 평균오차 | 11.542 m |
| 최종오차 | 11.930 m |
| 5 ping 연속 5 m 미만 수렴률 | 25% |

시간을 30 ping으로 늘려도 평균오차가 감소하지 않았다. trial 하나만 step 21에 지속 5 m
이하로 진입했고, 나머지는 7.6~17.1 m 최종오차가 남았다. 조건부 라우팅 발동률도 모두
0%여서 GCC와 gated SRP가 서로 동의하면서 같은 방향으로 편향되는 상황이다.

따라서 600 m 병목은 짧은 시퀀스나 초기 P가 아니라 정상상태 DOA 정확도다. 더 긴 필터
실행은 채택할 개선안이 아니며, 다음 단계는 송신 bandwidth를 넓혀 시간지연 해상도와
gated SRP 방향분해능을 높일 수 있는지 별도 validation에서 확인한다.
