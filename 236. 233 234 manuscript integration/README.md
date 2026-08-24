# 236. 233 234 manuscript integration

## 목적

다른 AI가 지적한 원고 반영 누락을 닫기 위한 마감 작업이다.

확인된 문제:

1. 233번 `Static full range independent validation`의 정지 0--1000 m, 거리별 n=20, 총 220 paired cases 결과가 영문/한글 원고에 없었다.
2. 234번 `Moving tail case decomposition`의 이동 residual tail 분해가 영문/한글 원고에 없었다.
3. 235번 mechanism boundary는 이미 영문 원고에 반영되어 있었으므로, 본 폴더에서는 233/234 누락만 처리했다.

## 원고 반영 내용

### 233 정지 full-range 검증

영문 `paper/manuscript.tex`와 한글 `paper/manuscript_ko.tex`에 다음을 반영했다.

- 정지 0--1000 m, 100 m 간격, 거리별 n=20, 총 220 paired cases.
- fixed mean settled RMSE 10.37 m.
- hop mean settled RMSE 8.37 m.
- mean paired gain +2.00 m.
- 95% CI [1.29, 2.74], p=5.34e-09.
- 0/200/500 m는 중립 또는 악화였고, 600--1000 m 장거리 구간에서 평균 이득이 뚜렷하다는 경계.

이 결과는 “정지 claim의 증거 밀도 보강”으로만 사용한다. 모든 거리 개선 또는 실해역 일반화 claim으로 쓰지 않는다.

### 234 이동 tail 분해

영문 `paper/manuscript.tex`와 한글 `paper/manuscript_ko.tex`에 다음을 반영했다.

- softR vs fixed residual tail fraction 0.131.
- softR vs hop tail fraction 0.028는 기존 평균 성능 문맥과 함께 유지.
- worst cell: 700 m radial 1.0 m/s, tail fraction 0.417.
- condition-level highest risk: `tang_1.0_vz`, tail fraction 0.182.
- 이동 표적 claim은 mean/P90 개선과 residual tail risk를 동시에 보고해야 한다는 경계.
- future work로 online tail-risk prediction, tangential+vertical guard, radial transition guard를 명시.

## 감사

`audit_233_234_integration.py`를 추가해 다음을 자동 확인한다.

- 233/234 핵심 수치가 영문/한글 원고에 존재하는지.
- 원본 결과 요약 파일의 수치와 연결되는지.
- 모든 거리 개선, tail 제거 같은 과장 표현이 없는지.

최종 감사 결과: `audit_report.md` PASS.

## 빌드 확인

- 영문 `paper/manuscript.tex`: `latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex` 성공.
  - 출력: `manuscript.pdf`, 15 pages.
  - fatal/undefined error 없음.
  - Underfull warning만 존재.
- 한글 `paper/manuscript_ko.tex`: `latexmk -g -pdf -interaction=nonstopmode -halt-on-error manuscript_ko.tex` 성공.
  - 출력: `manuscript_ko.pdf`, 16 pages.
  - fatal error 없음.
  - 긴 영어/수식이 들어간 표에서 underfull warning 발생. 최종 조판 단계에서 정리 가능.

## 해석

이번 작업은 새 실험이 아니라, 이미 끝난 233/234 결과를 원고에 반영하는 정합성 보완이다.

교수님이 PDF만 읽어도 다음 질문에 답할 수 있게 되었다.

- “정지 표적은 왜 600 m 한 점만 검증했는가?”
- “이동 softR의 13.1% residual tail은 어디에서 생기는가?”
