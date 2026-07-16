# Korean-first manuscript policy

## 핵심 규칙

2026-07-16부터 원고 작성 순서는 다음과 같이 고정한다.

1. 한글 기준 원고를 먼저 완성한다.
2. 한글 원고에서 논리, 장 구조, claim boundary, 수치 해석을 확정한다.
3. 확정된 한글 원고를 영어 IEEEtran 원고에 반영한다.
4. 영어 단계에서는 표현과 저널 형식을 다듬되, claim을 새로 키우지 않는다.

## 파일 위치

- 한글 기준 원고: `paper/manuscript_ko.tex`
- 기존 영어 IEEE 원고: `paper/manuscript.tex`
- 참고문헌: `paper/refs.bib`
- 그림: `paper/figures/`

`paper/`는 로컬 전용이다. GitHub에는 올리지 않는다.

## 왜 이렇게 바꾸는가

현재 논문은 영어로 작성되어 있어 사용자가 연구 흐름과 주장 범위를 직접 검토하기 어렵다.
이 상태에서 영어 문장만 계속 다듬으면, 사용자가 승인하지 않은 논리 구조가 원고에 굳어질 수 있다.
따라서 먼저 한글 기준본을 만들고, 사용자가 이해하고 판단할 수 있는 상태에서 논문 구조를 확정한다.

## 영어 원고 반영 기준

영어 `paper/manuscript.tex`를 수정할 때는 항상 한글 기준 원고와 다음 항목을 대조한다.

- 장 제목과 장 순서
- 핵심 claim
- 정지 600 m 수치: 13.01 m to 8.87 m, improvement 4.14 m, p=0.0008
- moving target claim: residual whitening only, no pooled RMSE improvement
- quasi-static claim: continuous safe boundary 0.005 m/s
- 160--162번 추가 schedule 결과: manuscript claim으로 쓰지 않고 limitation/future work로 제한

## GitHub 규칙

커밋할 때는 `git add .`를 쓰지 않는다.
반드시 해당 numbered folder만 stage한다.
`paper/`, 루트 MD, `study_exports/`, 보고서 파일은 stage하지 않는다.
