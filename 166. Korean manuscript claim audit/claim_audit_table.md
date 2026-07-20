# Claim audit table

| 원고 claim | 원천 근거 | 감사 판정 | 메모 |
|---|---|---:|---|
| 정지 600 m fixed 13.01 m → agile 8.87 m | 61번 README, 실험 레지스트리 61행 | 통과 | paired improvement 4.14 m, p=0.0008도 정합 |
| 정지 600 m median 13.97 → 7.96 | 61번 README | 통과 | 원고 본문 수치와 정합 |
| 이동 표적 lag-1 +0.470 → -0.208 | 63번 README, 실험 레지스트리 63행 | 통과 | p=5.56e-10은 원고에는 직접 숫자로 쓰지 않음 |
| 이동 표적 pooled RMSE gain 미재현 | 63번 레지스트리 | 통과 | -0.10 m, p=0.301로 기각. 원고는 성능개선 미주장 |
| 준정지 fixed 11.98 m → hop 10.49 m | 82번 README/result_summary, 레지스트리 82행 | 통과 | 전체 평균 개선 수치 정합 |
| 준정지 continuous safe boundary 0.005 m/s | 82번 README/result_summary, 레지스트리 82행 | 통과 | 0.010/0.050 깨짐, 0.030/0.100 양성은 비단조 회복 |
| 5 ms direct-path gate | 61/63/82/160/161/162 peak_measurement.py 및 93번 README | 통과 | 원고 구현 파라미터 절에 반영됨 |
| 160 four-carrier 독립검증 실패 | 160번 result_summary, 레지스트리 160행 | 통과 | 본문 성능 claim이 아니라 limitation |
| 161 sparse tail 기전 3.557 m, 32.013 m, 53.001 m | 161번 README/result_summary | 통과 | 원고에는 정량 일부만 서술. 세부 수치는 future/supplement 후보 |
| 162 TOA guard post-hoc 53.001 → 8.224 m | 162번 README/result_summary | 통과 | 독립검증 전이므로 claim 금지 |

## 발견된 문구 리스크

| 위치 | 리스크 | 조치 |
|---|---|---|
| 초록 결론 | `정지 및 준정지`가 0.005 m/s 제한보다 넓게 읽힐 수 있음 | `정지 및 매우 느린 준정지`로 수정 |
| claim 표 핵심 방법 | `정지/준정지`가 일반 준정지 전체로 읽힐 수 있음 | `정지 및 매우 느린 준정지`로 수정 |

## 최종 판정

원고 수치와 claim boundary는 감사 통과.
166번 이후 영어 원고에 반영할 때도 이 표를 기준으로 claim 확대를 막는다.
