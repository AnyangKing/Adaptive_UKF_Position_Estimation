# 175. USBL protocol and metadata audit

## 목적

다른 논문 피드백에서 받은 “실제 USBL에서 획득 가능한 관측량과 공정한 검증 기준”을 현재 Adaptive UKF 프로젝트 수행 규칙에 반영한다. 새 성능 실험을 만들지 않고, 기존 채택 코드와 결과의 가정·truth 사용·metadata gap을 감사한다.

## 이번 폴더에서 한 일

1. USBL 수신 프로토콜 가정을 명시했다.
   - 현재 canonical validation은 one-way synchronized beacon 가정이다.
   - absolute TOA를 `range = c * TOA`로 직접 사용한다.
   - common clock bias, sensor별 hardware delay, sensor별 gain/phase mismatch는 canonical validation에 포함하지 않았다.

2. 채택 실험별 truth-leak audit을 정리했다.
   - truth는 신호 합성, 최종 RMSE/NEES, offline mechanism diagnosis에만 쓰인다.
   - TOA/TDOA/DOA 추출, GCC-SRP disagreement, adaptive-R, carrier schedule/guard decision에는 쓰지 않는다.

3. 결과 metadata 표준을 정리했다.
   - 다음 실험부터 `stage`, `protocol_frozen_before_execution`, `seed_roots`, `truth_usage`, `claim_allowed`, `claim_forbidden` 등을 결과 JSON에 남긴다.

4. 한국어 원고 로컬 파일에 Method 보강 문장을 반영했다.
   - `paper/manuscript_ko.tex`는 GitHub에 올리지 않는 로컬 전용 파일이다.
   - 본 폴더에는 원고에 반영한 문장과 위치만 기록한다.

## 산출물

- `usbl_protocol_assumptions.md`
- `truth_leak_audit.md`
- `metadata_standard.md`
- `manuscript_patch_note.md`

## 판정

이번 보완은 기존 알고리즘이나 기존 실험 결과를 바꾸지 않는다. 핵심 성능 claim은 그대로 유지한다.

- 유지되는 강한 claim: static/very-slow quasi-static long-range USBL에서 carrier-agile pinging이 coherent DOA bias의 시간상관을 낮추고 RMSE를 개선한다.
- 유지되는 금지 claim: moving target 일반 RMSE 개선, frequency hopping USBL 최초, practical USBL full-system 검증.

