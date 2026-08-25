# Framing freshness patch report

## 처리한 문제

최근 191, 204, 216번 이동표적 결과가 원고에 반영되었지만, 일부 Discussion 문장과 prior-art Table I 자기 위치 설명이 예전 static/quasi-static 중심 프레이밍으로 남아 있었다.

이 상태에서는 다음 오해가 가능했다.

- `validated operating region = static to very slow drift`가 논문 전체 결론처럼 읽힘
- 0.05--1.0 m/s 이동표적 검증이 quasi-static 0.005 m/s 경계와 충돌하는 것처럼 보임
- Table I에서 transition-aware Adaptive-R 기여가 충분히 드러나지 않음

## 원고 반영

### Discussion

`validated operating region` 문장을 plain carrier agility without transition-aware routing의 경계로 한정했다.

추가로, transition-aware rule은 0.05--1.0 m/s moving families에서 별도 검증된 결과라고 명시했다.

### Prior-art Table I

Table I caption과 Present work 행에 transition-aware Adaptive-R routing을 명시했다.

수정 후 Table I은 다음을 함께 보여준다.

- frequency hopping USBL 최초 주장이 아님
- carrier-agile temporal decorrelation
- hop-transition risk routing
- static 600 m 및 0--1000 m static 검증
- plain-hopping moving failure
- transition-aware 0--1000 m structured/OOD moving validation

### Results summary table

Static 0--1000 m 행에서 pooled 220-case mean과 600 m bin repeat를 분리해서 읽히도록 문장을 다듬었다.

## 감사

새 감사 로직은 번호 폴더가 아니라 로컬 전용 `tools/audits/audit_framing_freshness.py`에 추가했다.

실행 결과:

```text
PASS: framing freshness markers are present and stale framing markers are absent.
```

전체 감사 러너도 통과했다.

```text
PASS: all available audits passed.
```

## 성격

새 실험 없음. 수치 변경 없음. 원고 프레이밍/claim boundary 보정 작업이다.
