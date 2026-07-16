# 161. Sparse carrier tail mechanism diagnostic

## 목적

160번에서 four-carrier cycle이 다수 기하의 median은 개선했지만 geometry 2에서 53 m tail을
만든 이유를 per-ping 수준으로 진단한다. geometry 2(대형 실패), 5(중간 실패), 19(강한 성공)를
160번과 동일한 seed로 정확히 재생한다.

## 기록 항목

- ping별 carrier, raw azimuth/elevation bias, GCC-SRP disagreement.
- UKF elevation innovation, total NIS, adaptive-R routing, position error.
- four-carrier schedule의 carrier별 반복 평균.
- 기준 센서의 surface-direct delay.

## 주장 제한

세 geometry는 160번 결과를 본 뒤 선택한 진단 표본이다. 따라서 성능의 독립검증이나 일반화
근거가 아니며, 실패한 four-carrier 후보를 구제하는 데 쓰지 않는다. 목적은 tail이 단순한
관측 outlier인지, 반복 carrier와 필터 상태의 누적 상호작용인지 구분해 후속 schedule 연구의
사전검증 지표를 찾는 것이다.

## 실행

```powershell
python test_protocol.py
python run_tail_diagnostic.py
```

## 완료 결과

geometry 2에서 four-carrier cycle은 3.557 m raw range 단차를 9회 반복해 range-error total
variation 32.013 m, max TOA NIS 111.69, settled RMSE 53.001 m를 만들었다. linear20은 같은
단차를 한 번만 통과해 total variation 3.558 m, RMSE 7.360 m였다. raw elevation bias는
four-carrier에서도 최대 0.771°로 작았다.

따라서 tail의 직접 기전은 DOA spike가 아니라 **carrier-dependent TOA branch switch의 반복
횡단과 UKF 상태 누적 상호작용**이다. 결과 상세는 `result_summary.md`에 정리했다.
