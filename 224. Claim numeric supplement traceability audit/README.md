# 224. Claim numeric supplement traceability audit

## 목적

원고의 핵심 성능 claim과 보충 검증 claim이 실제 결과 JSON에서 온 숫자와 일치하는지 확인했다.

행정 결정(저널 선택, 저자/교신저자, funding 등)은 이 감사 범위에서 제외했다.

## 감사 대상

- `paper/manuscript.tex`
- `191. Moving full range transition aware independent validation/moving_full_range_independent_validation.json`
- `204. Overnight OOD validation aggregate result/compact_metrics.json`
- `215. Hardware frequency response sensitivity/hardware_response_sensitivity.json`
- `216. Extended OOD motion family validation/extended_ood_motion_family_validation.json`

## 결론

- 핵심 수치 불일치 없음.
- 원고는 191/204를 주 moving-target simulation evidence로 사용하고, 215/216은 supplementary robustness/sensitivity evidence로 구분하고 있다.
- 실해역 검증, 하드웨어 주파수 응답 실측, arbitrary-motion 보장은 주장하지 않는다.
- 현재 감사 기준에서는 원고 결론을 바꿀 추가 시뮬레이션 필요성은 발견하지 않았다.

## 재현

```powershell
python ".\224. Claim numeric supplement traceability audit\verify_claim_tokens.py"
```

검증 스크립트는 결과 JSON에서 핵심 수치를 계산하고, 원고에 대응되는 반올림 수치·경계 문구가 존재하는지 확인한다.

## 커밋 규칙

이 폴더만 git에 올린다. `paper/` 원고 파일과 빌드 산출물은 로컬 전용으로 유지한다.
