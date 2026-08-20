# 212. English Korean claim synchronization audit

## 목적

211번에서 정리한 한글 기준 원고 v4와 영어 IEEEtran 원고의 contribution count, OOD claim, boundary language가 같은지 감사했다.

## 발견한 문제

영어 원고 Introduction은 아직 “five contributions”라고 되어 있었다. 204 OOD motion validation이 본문과 결론에는 들어갔지만, contribution list에서는 별도 기여로 분리되지 않아 한글 v4와 어긋났다.

## 수정

- “five contributions” → “six contributions”
- Fifth: structured 0--1000 m transition-aware moving validation
- Sixth: OOD moving family check + slow-drift boundary evidence

## Claim synchronization status

- 한글 v4와 영어 원고 모두 plain hopping 단독 claim을 금지한다.
- 양쪽 모두 transition-aware moving claim을 191 structured + 204 OOD simulation evidence로 제한한다.
- 양쪽 모두 real-water/arbitrary-motion/hardware-response 일반화를 금지한다.

## GitHub 규약

`paper/` 원고는 local-only다. 이 폴더만 커밋한다.
