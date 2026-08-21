# Non-administrative readiness checklist

## A. 논문 내용

| 항목 | 상태 | 메모 |
| --- | --- | --- |
| 핵심 연구선 | 완료 | TOA/TDOA/DOA-UKF에서 carrier-agile observation design + transition-aware Adaptive-R로 발전한 흐름 유지 |
| 정지/준정지 경계 | 완료 | mechanism-and-boundary evidence로 유지 |
| moving-target main claim | 완료 | 191 structured 0--1000 m independent validation 기반 |
| OOD robustness | 완료 | 204 OOD aggregate + 216 extended OOD-family check로 보강 |
| hardware frequency response 약점 | 부분 보완 | 215 idealized edge-loss sensitivity로 simulation-level 방어. 실측 calibration은 후속 실험 |
| 실해역 검증 부재 | 한계로 명시 | 현재 논문은 simulation-level claim으로 제한 |

## B. 수치/claim 추적성

| 항목 | 상태 | 근거 |
| --- | --- | --- |
| 191 structured moving 수치 | 통과 | 224 감사 스크립트 |
| 204 OOD aggregate 수치 | 통과 | 224 감사 스크립트 |
| 215 frequency-response sensitivity 수치 | 통과 | 224 감사 스크립트 |
| 216 extended OOD-family 수치 | 통과 | 224 감사 스크립트 |
| 과장 claim 차단 | 통과 | real-water/arbitrary-motion/measured calibration 보장 문구 없음 |

## C. 빌드 상태

| 파일 | 상태 |
| --- | --- |
| `paper/manuscript.tex` | PDF 14쪽 생성 |
| `paper/manuscript_ko.tex` | PDF 14쪽 생성 |
| LaTeX fatal error | 없음 |
| undefined reference/citation | 없음 |
| overfull hbox | 없음 |

## D. 일부러 남겨둔 행정 항목

아래는 사용자가 확정하기 전까지 AI가 임의로 채우면 안 된다.

- 투고 저널/최종 template
- 저자명, 소속, 교신저자
- ORCID
- Author Contributions
- Funding
- Conflicts of Interest
- Data Availability 최종 공개 URL 또는 repository DOI
- 보충자료 공개 방식

## E. 현재 다음 단계 판단

지금 바로 추가 시뮬레이션을 돌려야 하는 뚜렷한 공백은 발견하지 않았다.

따라서 다음 자연스러운 작업은 새 연구가 아니라, 사용자가 논문을 읽고 이해하기 쉬운 형태로 검토하는 것이다.

추천 순서:

1. 한글 독해본을 먼저 읽고, 사용자 표현으로 어색한 부분 표시.
2. 영어 원고가 한글본과 같은 주장 강도를 유지하는지 비교.
3. 교수님 복귀 후 행정 항목과 실험 가능성을 결정.
4. 실험 장비/해역이 확보되면 실해역 논문을 별도 후속 연구로 시작.
