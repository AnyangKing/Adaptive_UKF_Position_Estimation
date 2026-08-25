# 245. Bibliography coverage expansion

## 목적

현재 원고의 DOI 정확성은 242번에서 확인되었지만, 참고문헌 수와 문헌 지형 커버리지가 IEEE 계열/해양공학 계열 논문으로는 다소 얇았다.
본 작업은 참고문헌을 단순히 부풀리는 것이 아니라, 원고의 핵심 방어선에 필요한 문헌 축을 보강한다.

## 보강 원칙

- 실존과 DOI를 웹에서 확인한 문헌만 추가한다.
- 원고 주장 범위를 넓히지 않는다.
- 추가 문헌은 Related Work의 논리적 위치에만 삽입한다.
- frequency hopping 자체를 최초로 주장하지 않는 현재 claim boundary를 유지한다.
- adaptive/robust Kalman filtering 문헌은 “이미 존재하는 필터 계열”로 인용하고, 본 연구의 차별점은 송신 측 carrier-agile observation design과 transition-aware routing으로 둔다.

## 추가한 문헌 축

| 축 | 추가 문헌 | 원고에서의 역할 |
|---|---:|---|
| AUV/underwater localization review | 3 | USBL/LBL/SBL 및 underwater localization의 큰 지형 보강 |
| USBL calibration/error modeling | 2 | 소형 배열, 장거리 각도오차, 설치·정렬 보정 계열과의 위치 차이 명확화 |
| SINS/USBL 및 adaptive/robust filtering | 6 | adaptive-R/robust covariance handling이 기존 필터 문헌과 연결됨을 인정 |

## 원고 반영

- `paper/refs.bib`: DOI 확인된 11편 추가.
- `paper/manuscript.tex`: Related Work의 underwater acoustic positioning 문단과 shallow-water multipath/recursive tracking 문단에 문헌 연결.
- `paper/manuscript_ko.tex`: 한글 읽기용 원고의 관련 연구 절에도 동일한 논리 반영. 단, 한글 원고는 BibTeX 참고문헌 목록을 붙이는 정식 투고 파일이 아니므로 `\cite{}` 키는 넣지 않는다.

## 추가 문헌 목록

1. Vickery 1998 — acoustic positioning systems practical overview.
2. Paull et al. 2014 — AUV navigation and localization review.
3. Su et al. 2020 — underwater localization techniques review.
4. Chen 2008 — in-situ USBL alignment calibration.
5. Chen 2013 — USBL angular misalignment calibration.
6. Morgado et al. 2013 — tightly coupled USBL/INS experimental validation.
7. Wang et al. 2020 — adaptive robust UKF for AUV acoustic navigation.
8. Xu et al. 2021 — maximum correntropy delay Kalman filter for SINS/USBL.
9. Li and Zhang 2024 — robust Kalman filter for SINS/USBL.
10. Xu et al. 2024 — invariant-error SINS/DVL/USBL robust estimator.
11. Wu et al. 2026 — robust adaptive online smoothing for USBL/SINS.

## 주의

Vickery 1998, Paull 2014, Su 2020, Chen 2008, Chen 2013, Morgado 2013, Wang 2020, Xu 2021, Li 2024, Xu 2024, Wu 2026으로 총 11편을 추가했다.
초기 계획의 8--10편보다 1편 많지만, Vickery 1998은 acoustic positioning의 고전적 배경을 짧게 받치는 용도라 유지하는 편이 낫다고 판단했다.

## 검증

- `python tools/audits/run_all_audits.py`: PASS.
- 영문 `manuscript.tex`: BibTeX 반영 후 PDF 빌드 PASS, undefined citation/reference 0건.
- 한글 `manuscript_ko.tex`: 읽기용 원고 빌드 PASS, undefined citation/reference 0건.
- `paper/`와 `tools/`는 로컬 전용이므로 GitHub 커밋 대상에서 제외한다.
