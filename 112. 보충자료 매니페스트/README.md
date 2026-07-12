# 112. 보충자료 매니페스트

## 목적

원고(`manuscript.tex`)의 Supplementary Materials 절이 약속한 항목 — 시뮬레이션 스크립트, 동결
반송파 스케줄, 검증 결과 JSON/CSV, Fig.1~6 생성 스크립트 — 을 저장소의 **실제 파일에 매핑**한다.
투고 시 보충자료 패키지를 조립할 때(또는 지도교수 검토 시) 바로 쓸 카탈로그다. 기존 산출물의
목록화일 뿐 새 코드/데이터를 만들지 않는다.

## 중요: 데이터 파일 위치

프로젝트 초기 `.gitignore`가 `results/`를 제외한다 → **결과 JSON/CSV는 로컬 전용(GitHub에 없음)**.
코드(`*.py`)와 README, 원고 소스(`manuscript.tex`/`refs.bib`/`figures/`)만 GitHub에 있다. 보충자료
패키지를 만들 때 결과 데이터는 로컬에서 수집해야 한다. (파일 경로는 프로젝트 루트 기준.)

## 매핑

### 본문 결과별 코드 + 데이터

| 결과(원고) | 스크립트(코드, git) | 결과 데이터(로컬 전용) |
|---|---|---|
| 정지 600m 검증 (Fig.3, §6) | `61. 정지표적 도약 대규모 독립검증/run_static_hop.py` | `61.../results/static_hop_validation.json` |
| 이동+백색화 (Fig.4, §7) | `63. 이동표적 도약 대규모검증 백색화 확인/run_moving_validation.py` | `63.../results/moving_validation.json` |
| 준정지 속도 경계 (Fig.5, §7) | `82. 준정지 속도 경계 검증 실행/run_quasi_static_boundary.py` | `82.../results/quasi_static_boundary.json`, `quasi_static_trials.csv` |
| 반송파 감도/편향 기전 (Fig.2, §4) | `58. 반송파 미세도약 코히어런트 편향 진단/run_agility.py` | `58.../results/agility.json` |
| CRLB/개구 하한 (Fig.6, §3·8) | `45. CRLB 이론하한 대비 효율/` (`crlb.py` + runner) | `45.../results/crlb.json` |

각 폴더는 자족적(self-contained): `channel.py`·`config.py`·`estimators.py`·`measurement.py`·
`peak_measurement.py`·`ukf.py`·`conditional_adaptive.py`·`consistency.py` 등 공통 파이프라인을
포함해 그 폴더만으로 재실행 가능.

### 동결 반송파 스케줄

- 정의: 각 runner 상단 `HOP_CARRIERS_HZ = np.linspace(30000.0, 34000.0, STEPS)` (STEPS=20),
  고정 기준선 `FIXED_CARRIER_HZ = 32000.0`.
- 등장 파일(동일 정책 동결): `59/60/61/62/63/64/82`의 `run_*.py`. 대표 = 61(정지)·63(이동)·82(준정지).

### Fig.1~6 생성 스크립트

| 그림 | 생성 스크립트 |
|---|---|
| Fig.1 시스템/기전 개념도 | `72. Fig1 시스템 개념도/generate_fig1_concept.py` → `101. Fig1 visual polish/make_fig1_polished.py`(최종본) |
| Fig.2·3·4·6 정량 그림 | `70. 논문 그림 1차 생성/generate_core_figures.py` |
| Fig.5 준정지 경계 | `82.../results/quasi_static_speed_boundary.svg`(원본) → `95. Fig5 PNG and submission packaging/generate_fig5_png.py`(PNG) |
| 원고용 canonical PNG 6종 | 루트 `figures/`(108에서 취합; Fig.1은 101, 나머지는 95) |

## 판정

**보충자료 매니페스트 완료.** 투고 시 이 표대로 코드(git)+결과데이터(로컬)+그림스크립트를 모으면
Supplementary 패키지가 된다. 단, 최종 구성·공개 범위(리포지토리/DOI/요청시 제공)는 저널 정책과
저자 결정에 따른다(체크리스트 C·D). 결과 데이터가 git에 없다는 점을 패키지 담당자가 유의.

## 다음

AI 완결 가능한 원고·부속 작업(108~112)은 여기서 사실상 소진. 이후는 사용자 확정 대기
(저자정보·저널선택·선행연구 원문 대조). 루프는 긴 유휴 하트비트로 전환.
