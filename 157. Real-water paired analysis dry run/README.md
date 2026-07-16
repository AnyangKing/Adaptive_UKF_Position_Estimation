# 157. Real-water paired analysis dry run

## 목적

156번 CSV 계약을 통과한 ABBA field log에서 fixed/hop primary endpoint를 자동 계산한다. 실제 데이터가
오기 전에 import→validation→pairing→endpoint→decision candidate 흐름을 mock으로 검증한다.

## 안전 기본값

```powershell
python "157. Real-water paired analysis dry run\analyze_paired_blocks.py"
```

위 명령은 mock 입력을 **실패로 거부**한다. 소프트웨어 dry run에만 다음을 사용한다.

```powershell
python "157. Real-water paired analysis dry run\analyze_paired_blocks.py" --allow-mock
```

실제 현장 로그:

```powershell
python "157. Real-water paired analysis dry run\analyze_paired_blocks.py" --input "현장로그.csv"
```

## 계산 endpoint

- fixed/hop mean RMSE와 paired gain.
- RMSE reduction percentage.
- P90 hop-minus-fixed.
- elevation residual lag-1 reduction.
- gross-error mean 차이.
- 포함된 fixed/hop block 수.

## 중요

`paired_analysis_dry_run.json`의 모든 수치는 mock이다. 값의 방향이나 크기를 논문·보고서·성능 주장에
사용할 수 없다. 이 파일은 분석 코드의 흐름과 부호 정의를 확인하기 위한 테스트 산출물이다.
