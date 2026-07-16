# Decision logic

## Tier 1 mechanism candidate

```text
fixed lag-1 >= 0.2
AND fixed-minus-hop lag-1 reduction > 0.2
```

이 조건은 session-level candidate일 뿐이다. 여러 geometry의 paired inference가 있어야 원고 claim을
업데이트할 수 있다.

## Tier 2 static candidate

```text
RMSE reduction >= 10%
AND hop P90 <= fixed P90
AND hop gross-error mean <= fixed
AND lag-1 reduction > 0
```

## Tier 3

0.005 m/s 조건과 drift 방향을 별도로 검토한다. 0.010 m/s 이상을 연속 경계로 자동 승격하지 않는다.

## 부호 규약

- `rmse_gain_m = fixed_rmse - hop_rmse`: 양수일수록 hop 개선.
- `rmse_reduction_pct = 100 * gain / fixed_rmse`: 양수일수록 개선.
- `lag1_reduction = fixed_lag1 - hop_lag1`: 양수일수록 whitening.
- `p90_hop_minus_fixed_m = hop_p90 - fixed_p90`: 0 이하이면 tail 비악화.

부호 규약을 사전에 고정해 결과 확인 후 해석 방향을 바꾸지 않는다.
