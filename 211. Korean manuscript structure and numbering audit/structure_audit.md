# Korean manuscript structure audit

## Section flow

1. 서론
2. 관련 연구와 문제 정의
3. 시스템 모델과 UKF 결합
4. 기본 추적 성능과 한계
5. 제안 방법: Carrier-Agile Temporal Decorrelation
6. 실험 검증과 적용 경계
7. 논의
8. 결론

This flow is acceptable for the Korean baseline manuscript. It is not yet forced into exact IEEE section numbering because the Korean file is a readability-first baseline, but it maps cleanly to the English IEEEtran manuscript.

## Claim boundary status

- Static performance claim: centered on 600 m static validation.
- Plain moving hopping: failure/boundary only.
- Transition-aware moving: 191 structured + 204 OOD simulation-level claim.
- Quasi-static: continuous claim limited to 0.005 m/s.
- Real-water/arbitrary motion: future work only.

## Remaining future polish

The English manuscript should later be checked against this Korean v4 baseline to ensure the contribution count, OOD table, and limitation wording match.
