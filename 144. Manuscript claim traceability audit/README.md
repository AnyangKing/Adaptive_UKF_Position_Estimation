# 144. Manuscript claim traceability audit

## 목적

12쪽으로 확장된 `paper/manuscript.tex`의 핵심 수치와 claim이 실제 numbered research folder의 산출물과 연결되는지 점검했다.

이 폴더는 원고를 고치는 작업이 아니라, 투고 전 reviewer 대응 관점에서 “어떤 문장이 어떤 실험 결과에 기대고 있는가”를 추적하는 감사 기록이다. `paper/`는 local-only/ignored 상태를 유지하며, GitHub에는 이 144번 폴더만 올리는 규약을 따른다.

## 결론

대부분의 중심 claim은 기존 실험 폴더와 잘 연결된다.

- 정지 600 m frequency-agile 성능 개선: 61번에 직접 근거 있음.
- moving target에서는 residual whitening은 강하지만 pooled RMSE 개선은 주장하지 않음: 63번과 원고 표현이 정합.
- quasi-static claim은 0.005 m/s까지로 제한됨: 82번과 정합.
- 장거리 sub-meter 불가/한계 해석: 45번 CRLB/floor와 정합.
- adaptive-R UKF 및 estimator 비교: 43, 44, 46번과 정합.
- 주파수 선택 및 robustness: 54, 48번과 정합.
- Method/protocol 세부: 93번 감사와 정합.

가장 주의할 부분은 two-ray fit 수치(`R^2=0.99/0.75`, `delta=1.34/1.87 ms`)다. 원고에는 포함되어 있지만, 현재 번호 폴더 검색에서는 해당 수치를 직접 산출한 별도 결과 파일이 확인되지 않았다. 58번은 기전과 cos-fit 절차의 초기 근거를 제공하지만, 원고의 최신 수치까지 완전히 닫아 주지는 않는다. 따라서 다음 목표는 two-ray figure/result 재현 폴더를 별도로 만들어 이 gap을 닫는 것이 좋다.

## 산출물

- `claim_traceability_matrix.md` — 원고 claim별 근거 폴더 추적표
- `weak_points.md` — 투고 전 보강이 필요한 근거/서술 약점
- `reviewer_response_ready_claims.md` — reviewer가 물었을 때 바로 쓸 수 있는 안전한 답변 문장

## 다음 권장 목표

`145. Two-ray mechanism evidence closure`

원고의 two-ray R²/δ 수치를 재현하는 독립 스크립트와 JSON/그림 산출물을 만든다. 완료 후 원고 Figure/본문의 two-ray 수치가 그 폴더와 직접 연결되도록 한다.
