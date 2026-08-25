# 243. Evidence crosswalk manuscript audit

## 목적

다른 AI가 반복해서 지적한 “폴더에는 있는데 원고에는 없다” 계열의 누락을 줄이기 위해, 핵심 실험 폴더의 수치 marker가 영문/한글 원고에 실제로 들어갔는지 감사했다.

이번 작업의 직접 계기는 61번 정지 600 m 독립검증과 233번 정지 0--1000 m sweep의 600 m bin이 모두 같은 프로토콜의 독립 시행인데, 원고가 이 차이를 충분히 설명하지 못한다는 지적이었다.

## 처리한 구멍

### 1. 600 m 정지 결과 두 값의 관계 명시

원고에 다음 해석을 추가했다.

- 61번 600 m 독립검증: fixed 13.01 m → hop 8.87 m, gain +4.14 m, p=0.0008.
- 233번 full-range sweep의 600 m bin: fixed 10.75 m → hop 7.99 m, gain +2.76 m.
- 233번의 +2.76 m는 61번 bootstrap CI `[+2.17,+6.05]` m 안에 있다.
- 따라서 두 값은 모순이 아니라 같은 동결 protocol을 독립 seed로 반복했을 때 나타나는 effect-size variation으로 해석한다.

### 2. 10.37 → 8.37 값의 pooled 성격 명시

원고에서 233번 `10.37 m → 8.37 m`는 단일 600 m 값이 아니라 0--1000 m, 100 m 간격, 총 220 paired cases의 pooled full-range static validation 평균임을 명시했다.

### 3. 폴더↔원고 crosswalk 감사

`audit_evidence_crosswalk.py`는 다음 marker들이 영문/한글 원고에 존재하는지 확인한다.

- 61번: 600 m headline static validation
- 233번: 0--1000 m pooled static validation 및 600 m repeat
- 234번: moving tail decomposition
- 238번: NEES/NIS consistency audit
- 239번: axis-wise error decomposition
- 241번: finite axis n=511 / full 3D n=528 clarification

## 실행

```powershell
python "243. Evidence crosswalk manuscript audit\audit_evidence_crosswalk.py"
```

예상 결과:

```text
PASS: evidence crosswalk markers are present and forbidden overclaims are absent.
```

## Git 규칙

이 폴더만 커밋한다.

- `git add -- "243. Evidence crosswalk manuscript audit"`
- commit message: `243. Evidence crosswalk manuscript audit`

`paper/` 원고 수정은 로컬 전용이며, 사용자 지시 전에는 GitHub에 올리지 않는다.
