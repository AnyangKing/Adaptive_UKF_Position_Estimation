# 154. Supplement code smoke matrix

## 목적

152번 보충자료 후보에 포함된 핵심 실험 코드가 현재 환경에서 실제로 실행 가능한지 확인한다.
파일 존재·SHA256만 검사한 152번보다 한 단계 더 나아가, 45·58·61·63·82·93·145번의
`test_diagnostic.py`를 독립 프로세스로 병렬 실행한다.

## 실행

```powershell
python "154. Supplement code smoke matrix\run_smoke_matrix.py"
```

기준 결과를 의도적으로 갱신할 때만:

```powershell
python "154. Supplement code smoke matrix\run_smoke_matrix.py" --write
```

## 범위

| case | 검증 대상 |
|---|---|
| 45 | CRLB 계산의 양성·거리·잡음 단조성 |
| 58 | carrier band, cosine fit, delay, 단일 carrier DOA |
| 61 | fixed/hop 차이, 정지 기하, settle window |
| 63 | 이동 검증 diagnostic |
| 82 | 속도 조건, 궤적, carrier, lag-1, 관측 생성 |
| 93 | adaptive-R, 배열·채널, gate·filter, 프로토콜 |
| 145 | two-ray JSON/SVG claim closure |

## 판정

7개 case가 모두 통과해야 하며, stdout 결과가 기준 JSON과 달라지면 drift로 실패한다. 이 검사는
대규모 Monte Carlo를 재실행하는 검사가 아니라, 보충자료 코드가 import·핵심 계산·기본 불변식을
유지하는지 빠르게 확인하는 smoke test다.
