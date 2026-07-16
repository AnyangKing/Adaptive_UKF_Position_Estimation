# 156. Real-water acquisition schema dry run

## 목적

118번의 실해역 검증 계획을 실제 수집 가능한 block-level CSV 계약으로 바꾼다. fixed/hop 비교에서
환경·동기·보정·ground truth 기록이 빠지면 결과를 논문 증거로 사용할 수 없으므로, 필수 필드·단위·
범위·조건부 규칙을 기계 검증한다.

## 실행

```powershell
python "156. Real-water acquisition schema dry run\validate_field_log.py"
```

실제 측정 로그 검사:

```powershell
python "156. Real-water acquisition schema dry run\validate_field_log.py" `
  --input "현장로그.csv" --require-measured
```

## 중요

- `mock_field_log.csv`는 validator dry run 전용이며 실제 측정 증거가 아니다.
- `record_status=mock`과 `mock://` URI로 실제 데이터와 기계적으로 구분한다.
- 실제 분석 전에는 `--require-measured`를 반드시 사용한다.
- 현재 폴더는 실험 완료를 의미하지 않으며, 장비·장소·허가·ground truth 결정은 남아 있다.

## 검증 규칙

- 조건당 최소 40 ping.
- fixed는 32 kHz 단일 carrier.
- hop은 비영(非零) 대역과 복수 carrier.
- static은 속도 0 및 drift direction 없음.
- ABBA는 fixed→hop→hop→fixed.
- 수신기·송신기 깊이는 수심을 넘지 않음.
- RMSE P90은 median 이상.
- 제외 block은 이유 필수.
- mock/measured raw URI 혼용 금지.
