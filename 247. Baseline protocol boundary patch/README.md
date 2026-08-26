# 247. Baseline protocol boundary patch

## 목적

Section IV의 초기 기반 성능 실험(43·44·46번)이 뒤쪽 carrier-agile 동결 검증 프로토콜과 다른 지표를 사용한다는 점을 원고에 명시했다.

## 확인한 실제 프로토콜

- 43번 Estimator 비교: 100/200/400/600 m, 거리당 16개 독립 test trajectory, 총 64개.
- 44번 조건부 Adaptive-R ablation: 100/200/400/600 m, 거리당 16개.
- 46번 대규모 확인: 100/200/400/600 m, 거리당 40개, 총 160개.
- 43·44·46 계열은 모두 10-ping 등속 궤적 기반이다.
- 43·44 코드의 RMSE 함수는 `start=3` 이후 구간을 사용한다.

## 원고 반영

- 영문 원고 Section IV에 `pre-frozen-protocol baseline checks` 문구를 추가했다.
- Table II 캡션에 `16 independent trajectories per range, 64 total; 10-ping trajectories with RMSE after ping 3`을 추가했다.
- Table III 캡션에 같은 Section IV baseline metric을 사용한다는 문장을 추가했다.
- Evaluation Protocol 절에 Section IV baseline check가 20-ping/final-10 규칙의 예외임을 명시했다.
- 한글 원고에도 같은 의미를 추가했다.

## Claim boundary

이번 수정은 새 성능 claim이나 새 실험을 추가하지 않는다.
Section IV의 수치는 “필터가 약해서 장거리 오차가 생긴 것이 아니다”를 보이는 기반 점검으로만 사용한다.
정지/이동 carrier-agile 성능 claim은 뒤쪽의 20-ping/final-10 동결 검증에 근거한다.

## 검증

- `tools/audits/audit_baseline_protocol_boundary.py`를 추가했다.
- `tools/audits/run_all_audits.py`에 baseline protocol boundary 감사를 등록했다.
- 감사 스크립트는 번호 폴더에 넣지 않고 `tools/audits/`에서 운영한다.
- 전체 감사 `python tools\audits\run_all_audits.py` 통과.
- 영문 원고 `pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex` 2회 빌드 통과: 16 pages.
- 한글 원고 `pdflatex -interaction=nonstopmode -halt-on-error manuscript_ko.tex` 2회 빌드 통과: 17 pages.
- 로그에서 LaTeX fatal error, undefined citation/reference, rerun warning, overfull warning 없음.
