# 124. IEEE float layout patch

## 목적

123번에서 IEEE식 7장 구조를 맞춘 뒤, 이번에는 그림 float 배치를 정리했다.

기존 원고는 Fig.1--Fig.6 `figure` 환경이 모두 Conclusion 뒤에 몰려 있었다. 이 상태는 IEEEtran이
자동 배치를 하더라도 후반부 float-only page를 만들기 쉽고, 독자가 그림을 첫 언급과 함께 보지 못하게
한다.

## 적용한 변경

로컬 `paper/manuscript.tex`에서만 다음을 수정했다. 논문 파일 자체는 Git에 올리지 않는다.

- Fig.1 system concept: System Model 설명 직후로 이동.
- Fig.6 CRLB/floor: Post-Gating DOA Bias Floor subsection 직후로 이동.
- Fig.2 carrier-bias sensitivity: coherent-interference mechanism subsection 직후로 이동.
- Fig.3 static validation: Static Long-Range Validation subsection 직후로 이동.
- Fig.4 moving whitening: Moving-target whitening 문단 직후로 이동.
- Fig.5 quasi-static boundary: quasi-static speed sweep 문단 직후로 이동.

## 검증

정적 검사 결과:

- `figure` 환경 6개 유지.
- `fig:concept`, `fig:floor`, `fig:bias`, `fig:static`, `fig:moving`, `fig:quasi` label이 각각 1회만 존재.
- Conclusion 뒤에 남아 있던 figure block 제거.
- `paper/`는 Git ignored 상태 유지.

## 판단

이번 수정은 원고의 claim, 수치, caption 문구를 바꾸지 않는다. 그림의 위치만 IEEE 논문 독자가 보기 쉬운
흐름으로 옮긴 조판 패치다.

## 다음 작업

다음 우선순위는 `125. IEEE table length triage`다.

현재 full-width `table*`가 3개 있다. IEEE 2단 양식에서는 `table*`가 너무 길면 페이지 흐름을 크게
흔들 수 있으므로, 각 표를 본문 유지/축약/supplement 이동 후보로 나눠야 한다.

