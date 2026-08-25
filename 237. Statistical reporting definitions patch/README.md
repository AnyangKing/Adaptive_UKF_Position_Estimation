# 237. Statistical reporting definitions patch

## 목적

새 실험 없이 원고에서 바로 닫을 수 있는 통계 보고 약점 3개를 보완했다.

처리한 약점:

1. divergence rate의 정의가 원고에 없었다.
2. 주 claim의 paired significance test 이름이 원고에 명확히 없었다.
3. 거리별/셀별 breakdown을 확증 검정처럼 읽을 수 있는 다중비교 해석 위험이 있었다.

## 원고 반영 내용

영문 `paper/manuscript.tex`와 한글 `paper/manuscript_ko.tex`의 평가 프로토콜 절에 다음을 추가했다.

- 발산 정의: 어느 ping에서든 3D 위치오차가 50 m를 넘으면 divergent trial로 판정.
- divergence rate 해석: RMSE가 아니라 thresholded failure fraction.
- 주 검정명: paired gain에 대한 one-sided Wilcoxon signed-rank test.
- 대립가설: gain > 0.
- 신뢰구간: bootstrap 95% confidence interval.
- 다중비교 경계: 거리별 표와 cell별 tail 분해는 descriptive diagnostics이며, 확증 claim은 사전 지정된 pooled paired comparison에 둔다.

## 코드 근거

- 191번 moving full-range 스크립트:
  - `diverged = np.any(errors > 50.0)`
  - `wilcoxon(gains, alternative="greater")`
- 233번 static full-range 스크립트:
  - `wilcoxon(gains, alternative="greater")`

## 감사

`audit_statistical_reporting_patch.py`를 추가했다.

감사 항목:

- 영문/한글 원고에 divergence threshold, Wilcoxon signed-rank, one-sided alternative, bootstrap CI, descriptive breakdown boundary가 존재하는지.
- 191/233 코드의 실제 divergence/test 구현과 원고 문장이 연결되는지.
- Bonferroni-significant cell 또는 cell-wise confirmatory claim 같은 unsupported claim이 없는지.

최종 결과: `audit_report.md` PASS.

## 빌드 확인

- 영문 `paper/manuscript.tex`: `latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex` 성공.
  - 출력: `manuscript.pdf`, 15 pages.
  - fatal error 없음. Underfull warning만 존재.
- 한글 `paper/manuscript_ko.tex`: `latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript_ko.tex` 성공.
  - 출력: `manuscript_ko.pdf`, 16 pages.
  - fatal error 없음. 표 안의 긴 영어/수식 때문에 underfull warning 존재.

## 해석

이번 작업은 새 실험이 아니다.
이미 사용하던 평가 방식과 코드에 있던 정의를 원고에 명시해 재현성과 방어력을 높인 문서/원고 정합성 보완이다.

다음으로 남은 실험성 보완은 softR NEES/NIS 일관성 재실행과 축별 오차 분해다.
