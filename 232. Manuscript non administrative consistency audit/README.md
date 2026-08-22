# 232. Manuscript non administrative consistency audit

## 목적

행정 요소를 제외하고 현재 논문 원고가 내부적으로 일관적인지 자동 점검했다.

이번 감사는 새 실험을 추가하지 않는다. 이미 원고에 들어간 주장, 수치, 그림, 빌드 로그가 서로 맞는지만 확인한다.

## 감사 항목

- 영문/한글 abstract 길이
- 핵심 수치 문자열 존재 여부
  - 600 m static: 13.01 m to 8.87 m, p=0.0008
  - 0--1000 m moving validation
  - transition-aware soft-R gain: 3.95 m vs hop, 4.80 m vs fixed
  - OOD 528 paired cases
- claim boundary 문구 존재 여부
  - real-water limitation
  - arbitrary-motion limitation
  - frequency hopping 최초성 금지
- 금지 claim의 긍정 주장 여부
- 원고에서 참조하는 figure 파일 존재 여부
- LaTeX 로그의 fatal error, undefined reference/citation, overfull hbox, hyperref warning 여부

## 결과

`audit_manuscript_consistency.py` 실행 결과:

```text
PASS
```

주요 확인값:

- English abstract tokens: 191
- Korean abstract space tokens: 181
- Forbidden-claim pattern hits: 0
- Included figure references: 8 / all OK
- `manuscript.log`: OK
- `manuscript_ko.log`: OK

## 참고

초기 감사에서는 `not the first use of frequency hopping in USBL`, `does not support a sub-meter long-range claim`처럼 금지 claim을 부정하는 문장까지 false positive로 잡았다.  
따라서 최종 스크립트는 주변 문맥의 부정 cue를 확인해, 금지 표현이 긍정 claim으로 쓰인 경우만 실패 처리하도록 수정했다.

## Git 규약

`paper/` 원고와 빌드 산출물은 로컬 전용이므로 GitHub에 올리지 않는다. 이번 커밋에는 232번 감사 폴더만 포함한다.

