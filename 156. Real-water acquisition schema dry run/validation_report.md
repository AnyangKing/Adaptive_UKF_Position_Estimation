# Field-log schema validation report

## dry run

| 항목 | 결과 |
|---|---:|
| CSV fields | 48 |
| mock sessions | 1 |
| mock blocks | 4 |
| fixed blocks | 2 |
| hop blocks | 2 |
| sequence | fixed → hop → hop → fixed |
| validation errors | 0 |

## 자동 검사

- field type, required value, enum, min/max.
- timezone 포함 timestamp.
- fixed 32 kHz 단일 carrier.
- hop 복수 carrier 및 비영 대역.
- static/drift 속도·방향 정합.
- sensor depth ≤ water depth.
- RMSE P90 ≥ median.
- exclusion flag/reason 정합.
- mock/measured URI 분리.
- ABBA 순서와 paired fixed/hop 존재.

## 테스트 결과

```text
wrote dry_run_report.json: 4 rows, 0 errors
ok: 4 rows, 1 session, 0 errors
test_validator.py: ok
```

## 판정

데이터 형식과 validation pipeline은 현장 전 dry run을 통과했다. 그러나 현재 CSV의 수치는 전부
mock이며 연구 결과로 사용할 수 없다. 실제 로그는 `field_log_template.csv`에서 시작하고
`--require-measured`로 검사해야 한다.
