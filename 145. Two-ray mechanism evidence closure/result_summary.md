# Result summary

## 무엇을 닫았나

144번에서 발견한 약점은 “원고의 two-ray fit example 숫자가 어디서 왔는지 바로 보이지 않는다”는 점이었다.

145번은 58번 `run_agility.py`의 기하 생성, surface/direct delay 계산, carrier sweep, cosine/first-harmonic fit 함수를 그대로 사용해 원고의 대표 기하를 다시 계산했다.

## 핵심 결과

| distance | geometry index | delta_ms | period_khz | fit_R2 | 32 kHz bias | hop mean bias | abs bias reduction |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 400 | 1 | 1.337 | 0.748 | 0.995 | 0.628° | 0.122° | 80.5% |
| 600 | 5 | 1.875 | 0.533 | 0.750 | -1.370° | 0.760° | 44.5% |

위 값은 `results/two_ray_fit.json`에서 재확인 가능하다.

## 원고 claim과의 관계

- `400 m: delta=1.34 ms, R²=0.99`는 재계산값 `1.337 ms, R²=0.9947`의 정상 rounding이다.
- `600 m: delta=1.87 ms, R²=0.75`는 재계산값 `1.875 ms, R²=0.750`의 정상 rounding이다.
- 따라서 원고의 two-ray figure/caption claim은 유지 가능하다.

## 해석

400 m 대표 기하는 carrier grid가 예측 주기(약 0.748 kHz)를 충분히 샘플링하여 first-harmonic two-ray model과 거의 완전히 맞는다.

600 m 대표 기하는 예측 주기(약 0.533 kHz)가 250 Hz carrier step의 2배 수준이라 더 빡빡하게 샘플링된다. 그래도 R²=0.750으로, 기하에서 계산한 surface/direct delay가 measured carrier-bias oscillation의 상당 부분을 설명한다. 이 대표 기하의 hop-mean bias reduction은 44.5%이며, 원고의 600 m median collapse claim은 이 단일 대표 기하가 아니라 58번 600 m 집계 summary(0.632°→0.053°)에 근거한다.

이 결과는 “frequency hopping 자체가 새롭다”가 아니라, “compact shallow-water USBL의 post-gating coherent DOA bias가 carrier phase와 묶여 있고, carrier agility가 이 성분을 whitening한다”는 논문의 novelty framing을 지탱한다.

## 다음 작업

다음 원고/그림 정리 때 `paper/figures/fig_tworay_fit.*`의 source-data reference를 이 폴더로 연결하면 된다. 현재 `paper/`는 local-only/ignored이므로 145번에서는 원고 파일을 수정하지 않았다.
