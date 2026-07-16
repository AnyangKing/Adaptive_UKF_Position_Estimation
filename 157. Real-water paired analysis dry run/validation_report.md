# Paired-analysis dry-run validation report

## software flow

```text
156 field-log validation
  → session grouping
  → exclusion filtering
  → fixed/hop block aggregation
  → RMSE/P90/lag-1/gross-error endpoints
  → decision candidate
```

## 검증 결과

- mock session: 1
- ABBA blocks: 4
- included fixed/hop: 2/2
- schema validation errors: 0
- endpoint unit tests: PASS
- default mock rejection: PASS
- explicit dry-run execution: PASS
- `is_research_evidence`: **false**
- decision: **DRY_RUN_ONLY_NOT_EVIDENCE**

## mock endpoint 주의

dry-run JSON에 계산된 RMSE gain, reduction percentage, lag-1 reduction과 P90 차이가 존재하지만 모두
파이프라인 검사용 합성값이다. 이 수치를 현재 연구 성능, 예상 실해역 성능 또는 논문 근거로 인용하면
안 된다.

## 다음 실제 단계

1. 156 `field_log_template.csv`로 measured log 생성.
2. 156 validator를 `--require-measured`로 실행.
3. 157 analyzer에 measured CSV 입력.
4. session-level candidate를 geometry-level paired inference로 집계.
5. preregistered success criteria에 따라 claim update 여부 결정.
