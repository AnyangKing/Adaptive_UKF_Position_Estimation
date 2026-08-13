# 182 result summary

## 판정

800 m와 1000 m에서 carrier-agile pinging의 평균 RMSE 개선은 재현되었다. 그러나 1000 m에서 hop divergence가 발생했으므로 “장거리 일반 개선 검증 완료”라고 쓰면 안 된다.

최종 decision: `extended_range_not_validated_as_general_improvement`

## 핵심 수치

| distance | fixed mean RMSE (m) | hop mean RMSE (m) | mean gain (m) | CI95 (m) | p | improved fraction | fixed div | hop div |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 800 m | 18.041 | 14.248 | 3.793 | [1.607, 6.283] | 0.00342 | 0.833 | 0.000 | 0.000 |
| 1000 m | 22.738 | 17.352 | 5.386 | [2.437, 8.558] | 0.00464 | 0.750 | 0.000 | 0.083 |
| overall | 20.390 | 15.800 | 4.590 | [2.721, 6.559] | 5.38e-05 | 0.792 | 0.000 | 0.042 |

## 해석

- 600 m를 넘어 800/1000 m에서도 carrier agility는 평균 RMSE를 낮추는 방향으로 작동했다.
- 거리 증가에 따라 fixed carrier의 coherent bias floor가 커지고, hop의 평균 이득도 커지는 경향이 보인다.
- 그러나 1000 m에서 hop divergence가 1/12 발생했다. 따라서 “완벽 억제” 또는 “always safe”라고 쓰면 안 된다.

## 논문 claim 후보

가능:

- The carrier-agile mechanism remains beneficial in extended static ranges up to 1000 m in mean RMSE, but tail stability becomes a limiting factor.
- At 1000 m, the method reduces average error but introduces a nonzero divergence risk in the current implementation.

금지:

- 1 km에서도 성능을 완벽히 억제한다.
- 800/1000 m 결과를 real-water 1 km 성능으로 일반화한다.
- divergence를 숨기고 평균 RMSE만 제시한다.

## 다음 제안

183번은 두 갈래 중 하나가 적절하다.

1. 181 moving 성공의 tail case 진단.
2. 182 1000 m divergence case 진단 및 transition-aware softR를 static long-range에도 적용할 수 있는지 확인.

현재 논문 본체에는 182를 “선택적 확장 결과”로 넣을 수 있지만, 1000 m divergence를 반드시 함께 써야 한다.
