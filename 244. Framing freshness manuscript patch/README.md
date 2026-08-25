# 244. Framing freshness manuscript patch

## 목적

최근 이동표적 결과(191, 204, 216)가 원고에 반영된 뒤에도 일부 Discussion 및 prior-art 표 문장이 예전 “정지/준정지 중심” 프레이밍으로 남아 있어, 독자가 이동표적 claim과 충돌한다고 읽을 위험을 줄였다.

이번 작업은 새 실험이 아니라 원고 프레이밍 보정이다.

## 수정한 핵심

### 1. Discussion operating region 한정

기존 문장은 “validated operating region = static to very slow drift”처럼 논문 전체 결론으로 읽힐 수 있었다.

수정 후에는 다음을 분리한다.

- plain carrier agility without transition-aware routing: 연속 quasi-static 안전선은 0.005 m/s까지
- transition-aware Adaptive-R: 0.05--1.0 m/s structured/OOD moving family에서 별도 검증

따라서 준정지 경계가 이동표적 결과를 무효화하지 않고, 이동표적 결과도 plain hopping 단독 claim으로 오해되지 않는다.

### 2. Prior-art Table I 자기 위치 최신화

Table I caption과 Present work 행에 transition-aware Adaptive-R routing을 명시했다.

수정 후 자기 위치는 다음과 같다.

- frequency hopping USBL 최초 주장이 아님
- post-gating coherent DOA bias의 carrier-agile temporal decorrelation
- hop-transition risk를 UKF measurement covariance에 반영하는 transition-aware Adaptive-R
- static 600 m 및 0--1000 m static 검증
- plain-hopping moving failure 공개
- structured/OOD moving family에서 transition-aware rule 검증

### 3. 요약표 셀 명료화

`tab:results`의 static 0--1000 m 행에서 pooled 220-case mean과 600 m bin repeat를 문장으로 분리했다.

## 감사

새 감사 스크립트는 번호 폴더가 아니라 로컬 전용 `tools/audits/audit_framing_freshness.py`에 추가했다.

`tools/audits/run_all_audits.py`에도 이 감사가 포함되었다.

## Git 규칙

이 폴더만 GitHub에 올린다.

- `git add -- "244. Framing freshness manuscript patch"`
- commit message: `244. Framing freshness manuscript patch`

`paper/`와 `tools/`는 로컬 전용이며 커밋하지 않는다.
