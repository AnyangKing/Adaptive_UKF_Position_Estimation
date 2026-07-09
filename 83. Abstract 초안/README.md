# 83. Abstract 초안

## 목적

82번 준정지 속도 경계 검증까지 반영해 논문 초록의 claim 범위를 고정한다.

이번 초록의 역할은 단순 요약이 아니라, 논문의 방어선을 맨 앞에서 잠그는 것이다. 특히 다음 세 가지를 과장 없이 반영한다.

1. 본체 claim은 `static long-range USBL`에서의 frequency-agile coherent multipath DOA-bias whitening이다.
2. `quasi-static`은 82번 결과상 “very slow drift up to 0.005 m/s under this protocol”로만 제한한다.
3. moving target에서는 residual whitening은 재현되지만 pooled RMSE improvement는 reliable하지 않다.

## 포함 파일

- `abstract_draft.md`: SCI/IEEE용 초록 여러 버전과 한국어 설명
- `contribution_claims.md`: 초록과 Introduction에서 쓸 수 있는 안전한 claim / 피해야 할 claim
- `abstract_quality_gate.md`: 초록 제출 전 점검표

## 핵심 수치

| 항목 | 값 |
|---|---|
| static 600 m fixed → hop | 13.01 m → 8.87 m |
| static 600 m gain | -32%, p = 0.0008 |
| static median | 13.97 m → 7.96 m |
| moving residual lag-1 | +0.470 → -0.208, p = 5.6e-10 |
| moving pooled RMSE gain | -0.10 m, p = 0.301 |
| quasi-static 82번 전체 | 11.98 m → 10.49 m, p = 8.00e-05 |
| continuous quasi-static boundary | 0.005 m/s까지 |

## 이번 폴더의 결론

초록은 다음 구조가 가장 안전하다.

1. 문제: compact USBL에서 direct-path gating 이후에도 shallow-water coherent multipath가 deterministic elevation bias를 남김.
2. 방법: TOA/TDOA/DOA-UKF tracking loop 안에서 ping-to-ping carrier agility를 observation design으로 사용.
3. 기전: carrier-locked phase `phi = 2*pi*f*delta`를 ping마다 회전시켜 residual DOA bias를 whiten.
4. 검증: static 600 m에서 RMSE -32%, p = 0.0008.
5. 경계: moving target은 whitening만 확실하고 RMSE gain은 미재현; very slow drift는 0.005 m/s까지만 조심스럽게 claim.

## 다음 단계

84번에서는 전체 manuscript skeleton을 만들거나, 83번 초록을 기준으로 Introduction/Discussion 문단을 정합화하는 것이 좋다.
