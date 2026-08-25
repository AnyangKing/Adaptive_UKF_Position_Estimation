# Adaptive-R novelty boundary report

## 지적된 문제

245번에서 추가한 Xu 2021, Li 2024, Xu 2024, Wu 2026 등은 모두 강건/적응 공분산 처리로 USBL/SINS 계열의 acoustic outlier, delay, outage, time-varying noise를 완화하는 문헌이다.
이 문헌들을 인용하면, 리뷰어는 자연스럽게 다음 질문을 할 수 있다.

> transition-aware soft-$R$은 기존 robust/adaptive Kalman covariance inflation과 무엇이 다른가?

기존 원고는 carrier schedule 차별화는 설명했지만, soft-$R$ 자체의 novelty boundary는 상대적으로 약했다.

## 반영한 답

원고에는 다음 구분을 추가했다.

- 기존 robust/adaptive filtering: acoustic outlier, delay, outage, time-varying noise에 사후적으로 반응하는 filter-centric 방법.
- 본 연구의 soft-$R$: 송신 schedule이 만든 known hop-transition event와 runtime-observable disagreement indicator를 사용해, carrier-agile observation design 안에서 전환 위험을 measurement covariance에 routing하는 제한된 규칙.

즉 본 연구는 일반적인 새 robust filter를 주장하지 않고, carrier-agile observation design과 결합된 transition-risk routing을 주장한다.

## 파일 변경

- `paper/manuscript.tex`
  - Related Work 문단에 adaptive-R novelty boundary 문장 추가.
  - Table I에 `Robust/adaptive SINS/USBL filtering` 행 추가.
- `paper/manuscript_ko.tex`
  - 한글 관련 연구 절에 같은 해석 추가.
- `tools/audits/audit_adaptive_r_novelty_boundary.py`
  - 로컬 전용 회귀 감사 추가.

## 검증 예정

- 전체 audit runner PASS 확인 완료.
- 영문/한글 PDF 빌드 확인 완료.
- undefined citation/reference 0건 확인 완료.
- BibTeX warning/error 및 overfull warning 0건 확인 완료.

## 운영 메모

이번 작업에서 새 감사는 번호 폴더 안에 만들지 않고 `tools/audits/`에 두었다.
이는 244번 이후의 도구 운영 규칙과 일치한다.
단, `tools/`는 로컬 전용이므로 GitHub 커밋 대상은 이 246번 기록 폴더뿐이다.
