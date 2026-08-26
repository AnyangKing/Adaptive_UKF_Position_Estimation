# 248. Full manuscript sweep closure

## 목적

다른 AI가 수행한 7개 항목 전수 점검에서 나온 원고 표기·참조·출처 누락 5건을 새 실험 없이 닫았다.

## 처리한 항목

1. `tab:movingfull` 캡션에 191번 근거 규모인 `528 paired cases`를 명시했다.
2. 본문 정지 0--1000 m sweep 문단에서 `Table~\ref{tab:staticfull}`을 직접 참조하도록 했다.
3. Data Availability 절에 233, 234, 238, 239 출처를 추가했다.
   - 233: 정지 0--1000 m sweep 표.
   - 234: moving-tail decomposition 및 limitations 논의.
   - 238/239: NEES/NIS 및 axis-wise diagnostic 표.
4. `tab:crlb` 캡션에 45번 근거 규모인 `16 trajectories per range, 64 total`을 명시했다.
5. 한글 원고의 미참조 그림/표 라벨 9개를 본문 callout으로 정리했다.

## 추가 판단 반영

구멍은 아니지만, 185/187의 direct-path control 결과가 기전 귀속 한계로 중요하므로 Limitations 표에 한 행을 추가했다.
핵심 문장은 “coherent multipath phase diversification과 정합하지만 단일 원인으로 확정하지 않는다”이다.

## 운영 방식

원고 점검 스크립트는 번호 폴더가 아니라 `tools/audits/`에 두었다.
이번 폴더는 수정 이력과 판단 근거만 보존한다.

## 검증

- `tools/audits/audit_full_sweep_closure.py` 추가.
- `tools/audits/run_all_audits.py`에 full-sweep closure 감사 등록.
- 전체 감사 `python tools\audits\run_all_audits.py` 통과.
- 영문 원고 `pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex` 2회 빌드 통과: 17 pages.
- 한글 원고 `pdflatex -interaction=nonstopmode -halt-on-error manuscript_ko.tex` 2회 빌드 통과: 18 pages.
- 로그에서 LaTeX fatal error, undefined citation/reference, rerun warning, overfull warning 없음.

## Claim boundary

이번 수정은 새 결과나 새 성능 claim을 추가하지 않는다.
이미 원고에 들어간 실험 결과의 표본 수, 본문 참조, 출처 매핑, 한계 배치를 명확히 한 원고 마감 보강이다.
