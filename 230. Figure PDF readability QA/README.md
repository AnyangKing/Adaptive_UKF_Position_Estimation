# 230. Figure PDF readability QA

## 목적

226--228번에서 논문 그림을 vector-first PDF/PNG로 재생성하고 label overlap을 줄였기 때문에, 이번 단계에서는 실제 원고 삽입 상태에서 축소 인쇄 시 읽기 어려운 요소가 남았는지 점검했다.

행정 요소는 다루지 않았다. 저자, 소속, 저널, 교신저자, funding, data availability 최종 문구는 이번 범위에서 제외했다.

## 점검 방법

- `paper/figures/*.png`를 contact sheet로 묶어 전체 그림을 한 화면에서 육안 QA했다.
- `paper/manuscript.tex`의 figure 배치와 caption을 대조했다.
- 영문/한글 원고를 다시 빌드해 figure 교체가 LaTeX 문제를 만들지 않는지 확인했다.

## 발견 사항

대부분의 그림은 228번 이후 큰 겹침이 제거되어 논문용으로 사용 가능했다.

다만 Fig.5 quasi-static speed boundary는 원래 체크/엑스 기호만으로 유의/비유의를 표시하고 있어, 축소 인쇄나 글꼴 대체 상황에서 의미가 약해질 수 있었다. 특히 콘솔/스크립트 인코딩 환경에서는 해당 기호가 깨져 보일 위험도 있었다.

## 보완 내용

- `regenerate_fig5_ascii_labels.py`를 추가했다.
- Fig.5의 체크/엑스 기호를 ASCII 기반 `sig.` / `n.s.` label로 교체했다.
- 색상 의미는 유지했다.
  - green: validated/significant gain
  - red: not supported
- 본문과 caption의 claim boundary는 변경하지 않았다.
- 새 실험 결과나 새 수치는 추가하지 않았다.

## 산출물

- `make_contact_sheet.py`: 현재 `paper/figures`의 PNG 그림들을 QA용 contact sheet로 묶는 스크립트
- `figure_contact_sheet.png`: QA용 contact sheet
- `regenerate_fig5_ascii_labels.py`: Fig.5를 ASCII label 방식으로 재생성하는 스크립트

실제 논문 그림 파일은 `paper/figures/fig5_quasi_static_speed_boundary.pdf` 및 `.png`로 로컬 갱신되었다. `paper/`는 프로젝트 규약상 GitHub에 올리지 않는 로컬 전용 원고 작업물이다.

## 빌드 확인

- `paper/manuscript.pdf`: 15 pages, 563914 bytes
- `paper/manuscript_ko.pdf`: 16 pages, 3627201 bytes
- fatal LaTeX error 없음
- undefined citation/reference 없음
- overfull hbox 없음

남은 underfull/hyperref warning은 기존 조판성 경고이며, 최종 제출 직전 warning cleanup 단계에서 다루면 된다.

