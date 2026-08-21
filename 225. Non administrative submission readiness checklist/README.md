# 225. Non administrative submission readiness checklist

## 목적

저널 선택, 저자 정보, 교신저자, funding, conflicts, data-availability 최종 URL 같은 행정 결정을 제외하고, 현재 컴퓨터에서 진행 가능한 논문 마감 상태를 정리했다.

## 현재 판정

행정 결정과 실제 실해역 실험을 제외하면, 현재 원고는 추가로 큰 시뮬레이션을 요구하는 상태는 아니다.

남은 작업은 주로 다음 두 종류다.

1. 사람이 정해야 하는 행정/투고 정보
2. 실제 장비·해상/호수 실험으로만 보완 가능한 외부 검증

## 확인한 항목

- 영문 원고 빌드 로그 확인: `paper/manuscript.pdf`, 14쪽.
- 한글 독해본 빌드 로그 확인: `paper/manuscript_ko.pdf`, 14쪽.
- fatal LaTeX error 없음.
- undefined reference/citation 없음.
- overfull hbox 없음.
- 191/204/215/216 핵심 수치와 원고 claim 토큰 일치.
- 215/216은 본문 주 claim이 아니라 supplementary robustness/sensitivity로 구분됨.
- real-water, arbitrary-motion, measured hardware calibration claim 없음.

## 새 시뮬레이션 필요성

현재 감사 기준에서는 핵심 결론을 바꿀 추가 시뮬레이션 필요성은 발견하지 않았다.

다만 아래 항목은 컴퓨터 추가 시뮬레이션이 아니라, 실제 실험 또는 사용자/교수 판단이 필요한 범위다.

- 실제 호수/해상 검증
- 실제 transducer/hydrophone frequency response 측정
- 최종 투고 저널 및 template 확정
- 저자, 소속, 교신저자, funding, conflicts, data-availability 문구 확정

## 커밋 규칙

이 폴더만 git에 올린다. `paper/`, 루트 MD, `study_exports/`, `.claude/`, raw overnight 산출물은 로컬 전용으로 유지한다.
