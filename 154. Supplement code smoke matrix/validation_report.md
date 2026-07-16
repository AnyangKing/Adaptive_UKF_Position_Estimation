# Smoke matrix validation report

## 결과

- diagnostic folders: **7**
- passed: **7**
- failed: **0**
- counted checks: **23**

## case별 결과

| case | checks | 판정 |
|---|---:|---|
| 45 CRLB floor | 3 | PASS |
| 58 carrier sensitivity | 5 | PASS |
| 61 static validation | 3 | PASS |
| 63 moving boundary | 1 | PASS |
| 82 quasi-static boundary | 6 | PASS |
| 93 Method audit | 4 | PASS |
| 145 two-ray closure | 1 | PASS |

## 해석

핵심 보충자료 코드 7묶음은 현재 Python 환경에서 독립 프로세스로 실행된다. 단, 이 판정은 빠른
diagnostic 범위이며 61·63·82의 전체 seed Monte Carlo를 새로 수행한 것은 아니다. 논문 headline
통계의 수치 재현은 기존 result JSON과 152번 SHA256 manifest가 담당한다.
