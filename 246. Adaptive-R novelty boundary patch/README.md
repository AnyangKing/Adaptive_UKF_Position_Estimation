# 246. Adaptive-R novelty boundary patch

## 목적

245번에서 SINS/USBL 및 SINS/DVL/USBL robust/adaptive filtering 문헌을 보강하면서, 원고에는 새로운 방어 의무가 생겼다.
transition-aware soft-$R$이 기존 adaptive/robust Kalman covariance handling과 어떻게 다른지 명시해야 한다.

## 수정 내용

- `paper/manuscript.tex` Related Work 문단에 adaptive-R novelty boundary를 추가했다.
- Table I에 `Robust/adaptive SINS/USBL filtering` family 행을 추가했다.
- `paper/manuscript_ko.tex` 관련 연구 절에도 같은 해석을 한글로 반영했다.
- 새 감사 스크립트는 번호 폴더가 아니라 `tools/audits/audit_adaptive_r_novelty_boundary.py`에 로컬 전용으로 두었다.

## 핵심 프레이밍

본 논문은 soft-$R$을 일반적인 새 robust/adaptive Kalman filter로 주장하지 않는다.
기존 연구는 주로 acoustic outlier, delay, outage, time-varying noise가 관측된 뒤 covariance/robust filtering으로 반응한다.
본 연구의 transition-aware soft-$R$은 송신 측 carrier schedule이 만든 알려진 hop-transition event와 런타임 관측 불일치 지표를 이용해, 그 전환 위험을 UKF measurement covariance에 routing하는 제한된 규칙이다.

따라서 차별점은 다음 결합에 있다.

1. carrier-agile observation design
2. post-gating coherent DOA residual decorrelation
3. known hop-transition risk routing
4. TOA/TDOA/DOA-UKF tracking loop 안에서의 적용 경계 검증

## 새 실험 여부

새 실험은 수행하지 않았다.
이번 작업은 245번에서 추가된 문헌 family에 맞춰 논문 claim boundary와 Table I을 보강한 원고 패치다.

## 검증

- `python tools/audits/run_all_audits.py`: PASS.
- 영문 `manuscript.tex`: PDF 빌드 PASS.
- 한글 `manuscript_ko.tex`: PDF 빌드 PASS.
- 빌드 로그에서 undefined citation/reference, BibTeX warning/error, overfull warning 검색 0건.
- 새 감사 로직은 `tools/audits/`에 로컬 전용으로 두고, GitHub에는 이 246번 기록 폴더만 올린다.
