# 240. Consistency and axis wise manuscript integration

## 목적

238번 NEES/NIS 필터 일관성 감사와 239번 축별 오차 분해 결과를 한글/영문 원고에 반영했다.

## 원고 반영 내용

- 238 결과:
  - plain hopping 대비 soft-$R$ position NEES: 255.84 → 16.00
  - total NIS 99% exceedance fraction: 0.119 → 0.038
  - total NIS: 23.02 → 3.65
  - 완전 calibration claim 금지
  - robust adaptive covariance-inflation rule로 해석

- 239 결과:
  - 3D RMSE: 11.34 → 7.39 m
  - horizontal RMSE: 7.46 → 4.85 m
  - vertical RMSE: 7.44 → 4.58 m
  - radial RMSE: 0.94 → 0.63 m
  - cross-range RMSE: 7.28 → 4.66 m
  - 수평/수직 동시 개선과 cross-range/vertical 우세를 상태공간 진단으로 반영

## 의도적으로 넣지 않은 내용

다른 AI가 언급한 “DOA block NIS가 mean 6.80으로 우세하다”는 주장은 238 최종 JSON의 최종 업데이트 기준 block NIS 요약과 맞지 않아 원고에 넣지 않았다. 원고에는 확인된 수치만 반영했다.

## 산출물

- `audit_manuscript_integration.py`: 한글/영문 원고에 필수 marker가 들어갔는지 확인
- `integration_report.md`: 반영 위치와 claim boundary 요약

