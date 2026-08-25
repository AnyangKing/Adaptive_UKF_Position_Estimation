# Bibliography expansion report

## 왜 추가했는가

242번 DOI 검증은 기존 참고문헌의 정확성을 확인하는 작업이었다.
이번 245번은 다른 성격이다.
현재 원고는 frequency agility, USBL, TOA/TDOA/DOA-UKF, adaptive-R, moving target validation까지 다루므로, 22편만으로는 문헌 지형이 얇게 보일 수 있었다.

따라서 다음 네 축을 보강했다.

1. underwater acoustic positioning / AUV localization review
2. USBL alignment calibration and error modeling
3. SINS/USBL and SINS/DVL/USBL robust/adaptive filtering
4. adaptive robust UKF / covariance inflation 계열의 기존성 인정

## 원고 프레이밍 변화

추가 문헌은 본 연구의 novelty를 넓히기 위해 넣은 것이 아니다.
오히려 반대로, 다음 경계를 더 분명히 하기 위해 넣었다.

- TOA/TDOA/DOA + UKF 자체는 새롭지 않다.
- USBL/SINS robust/adaptive Kalman filtering도 새롭지 않다.
- frequency hopping/frequency diversity도 새롭지 않다.
- 본 연구의 좁은 기여는 compact shallow-water USBL에서 post-gating coherent DOA residual의 시간상관을 carrier-agile observation design으로 바꾸고, 이동표적에서는 transition-aware Adaptive-R로 hop-transition risk를 routing한다는 점이다.

## DOI 확인 근거

| Key | DOI | 확인한 역할 |
|---|---|---|
| `Vickery1998AcousticPositioning` | `10.1109/AUV.1998.744434` | acoustic positioning 고전 개요 |
| `Paull2014AUVReview` | `10.1109/JOE.2013.2278891` | AUV navigation/localization review |
| `Su2020UnderwaterLocalizationReview` | `10.1155/2020/6403161` | underwater localization review |
| `Chen2008InSituUSBLAlignment` | `10.1016/j.oceaneng.2008.06.013` | USBL alignment calibration |
| `Chen2013USBLMisalignment` | `10.1017/S0373463313000222` | USBL angular misalignment calibration |
| `Morgado2013TightlyCoupledUSBLINS` | `10.1002/rob.21442` | tightly coupled USBL/INS validation |
| `Wang2020AdaptiveRobustUKFAUV` | `10.3390/s20010060` | adaptive robust UKF for AUV acoustic navigation |
| `Xu2021MCDKFUSBL` | `10.1016/j.isatra.2021.01.055` | SINS/USBL delay and non-Gaussian noise filtering |
| `Li2024GaussianExponentialUSBL` | `10.1177/14750902231224832` | robust SINS/USBL filter with field validation |
| `Xu2024InvariantSINSUSBL` | `10.1016/j.oceaneng.2023.116511` | invariant-error SINS/DVL/USBL robust estimator |
| `Wu2026OnlineSmoothingUSBL` | `10.1016/j.oceaneng.2025.123315` | USBL/SINS robust adaptive smoothing with lake/sea trials |

## 파일 변경

- `paper/refs.bib`에 위 DOI 확인 문헌 11편 추가.
- `paper/manuscript.tex` Related Work에 문헌 축 반영.
- `paper/manuscript_ko.tex` 관련 연구 절에 동일한 해석 반영. 한글 원고는 읽기용이며 BibTeX 참고문헌 목록이 없으므로 citation key는 영문 원고에만 유지했다.

`paper/`는 로컬 전용이므로 GitHub에는 올리지 않는다.
GitHub에는 이 245번 기록 폴더만 커밋한다.

## 빌드 및 감사

- 전체 감사 runner: PASS.
- 영문 원고: BibTeX 반영 후 `manuscript.pdf` 생성, undefined citation/reference 0건.
- 한글 원고: `manuscript_ko.pdf` 생성, undefined citation/reference 0건.
- MiKTeX가 사용자 설정 디렉터리 초기화를 요구해 `pdflatex`/`bibtex` 일부 실행은 권한을 열어 수행했다. 이는 원고 파일 문제가 아니라 로컬 TeX 환경 초기화 문제다.
