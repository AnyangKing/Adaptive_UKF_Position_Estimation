# Submission readiness table

## 상태표

| 항목 | 상태 | 근거 | 남은 일 |
|---|---|---|---|
| 핵심 성능 결과 | 준비됨 | 61번 static 600 m: 13.01→8.87 m, p=0.0008 | 없음 |
| whitening 기전 | 준비됨 | 58/63/82: carrier sensitivity, lag-1 reduction | 없음 |
| moving boundary | 준비됨 | 63~67: RMSE gain 미재현, boundary로 정리 | 없음 |
| quasi-static boundary | 준비됨 | 82: continuous 0.005 m/s | 없음 |
| Method 수치 정합 | 준비됨 | 93: 수치 불일치 0건 | 원고 최종 패치 유지 확인 |
| 선행연구 방어 | 거의 준비됨 | 78/96/117 + Scholar/full-text 대조 | 선택 인용 추가 여부 |
| 원고 claim 안전성 | 준비됨 | 116 | 저널 변환 시 재검사 |
| LaTeX 원고 | 로컬 준비 | `paper/` IEEEtran | 빌드 재확인 권장 |
| 보충자료 구조 | 준비됨 | 115/120 | 공개 정책 결정 후 실제 ZIP |
| 실해역 계획 | 계획 준비 | 118 | 실제 장비/장소/허가 |
| schedule ablation | 계획 준비 | 119 | 실행은 선택 |
| 저자 정보 | 미정 | 사용자/교수님 결정 필요 | 필수 |
| 목표 저널 | 미정 | 사용자/교수님 결정 필요 | 필수 |
| Data/code availability | 미정 | 사용자/교수님 결정 필요 | 필수 |

## Go / no-go

### 지금 바로 가능한 것

- 로컬 PDF 빌드 확인.
- 저널 후보 matrix 작성.
- 보충자료 ZIP을 로컬 임시 폴더로 실제 조립해보기.

### 사람 결정 없이는 못 하는 것

- 최종 저널 확정.
- 저자/소속/교신저자 확정.
- Funding/conflict/data availability 확정.
- paper/ 공개 여부 결정.

### 하면 안 되는 것

- paper/를 GitHub에 push.
- `git add .`.
- moving-target RMSE improvement claim 추가.
- 0.1 m/s quasi-static continuous validation claim 추가.
- frequency hopping USBL 최초 주장.
