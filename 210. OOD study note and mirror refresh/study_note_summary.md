# Study note summary

## File

`27_OOD_motion_validation과_claim_boundary.md`

## Main lesson

204번은 “transition-aware soft-R가 좋은 평균 RMSE를 냈다”보다 더 중요한 의미가 있다.

핵심은 다음이다.

> plain hopping은 moving target에서 여전히 tail-prone이지만, transition-aware soft-R는 OOD simulation에서도 mean/P90/divergence를 함께 줄였다.

## Boundary taught in the note

- Supported:
  - current signal-level simulation robustness,
  - structured + OOD moving family support,
  - observed-runtime indicator based transition-aware routing.
- Not supported:
  - real-water validation,
  - arbitrary motion guarantee,
  - hardware frequency response robustness,
  - “frequency hopping itself solves moving targets.”
