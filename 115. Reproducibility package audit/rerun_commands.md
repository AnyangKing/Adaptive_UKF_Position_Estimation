# Rerun commands

## 공통 전제

작업 루트:

```powershell
cd "C:\Users\HOSEO\OneDrive - 호서대학교\나는 개인이요\석사생\논문\Adaptive UKF 위치추정"
```

각 실험 폴더는 `channel.py`, `config.py`, `measurement.py`, `peak_measurement.py`, `ukf.py`,
`conditional_adaptive.py` 등 필요한 공통 파일을 자체 포함한다. 따라서 해당 폴더로 들어가 runner를
실행하는 방식이 가장 안전하다.

## 핵심 실험 재실행

### 58. 반송파 민감도 / 기전

```powershell
cd "58. 반송파 미세도약 코히어런트 편향 진단"
python run_agility.py
```

예상 산출물:

- `results/agility.json`
- 핵심 확인: 400 m 78.35%, 600 m 91.57% hop reduction.

### 61. 정지 600 m 독립 검증

```powershell
cd "61. 정지표적 도약 대규모 독립검증"
python run_static_hop.py
```

예상 산출물:

- `results/static_hop_validation.json`
- 핵심 확인: 600 m fixed 13.0065 m, hop 8.8698 m, p=0.000845, n=20.

### 63. 이동 표적 whitening / 성능 경계

```powershell
cd "63. 이동표적 도약 대규모검증 백색화 확인"
python run_moving_validation.py
```

예상 산출물:

- `results/moving_validation.json`
- 핵심 확인: lag-1 +0.46995 → -0.20808, p=5.56e-10.
- 핵심 경계: pooled RMSE gain -0.103 m, p=0.301 → 성능 개선 claim 금지.

### 82. 준정지 속도 경계

```powershell
cd "82. 준정지 속도 경계 검증 실행"
python run_quasi_static_boundary.py
```

예상 산출물:

- `results/quasi_static_boundary.json`
- `results/quasi_static_trials.csv`
- `results/quasi_static_speed_boundary.svg`
- 핵심 확인: 전체 n=132 paired, 연속 quasi-static boundary는 0.005 m/s.

### 45. CRLB / 개구 하한

45번은 폴더 내 runner 이름이 다른 폴더처럼 표준화되어 있지 않으므로, 재실행 전 `README.md`와 Python
파일명을 먼저 확인한다. 현재 투고 방어에 필요한 결과는 이미 아래 파일에 있다.

- `45. CRLB 이론하한 대비 효율/results/crlb.json`
- 핵심 확인: 600 m empirical CRLB 11.80 m, routing RMSE 12.29 m, residual bias floor 3.446 m.

## 그림 재생성

| 그림 | 재생성 경로 |
|---|---|
| Fig.1 | `101. Fig1 visual polish/make_fig1_polished.py` |
| Fig.2~4, Fig.6 | `70. 논문 그림 1차 생성/generate_core_figures.py` |
| Fig.5 | `95. Fig5 PNG and submission packaging/generate_fig5_png.py` |
| 원고용 취합본 | `95. Fig5 PNG and submission packaging/figures/` |

## 원고 PDF 빌드

현재 논문 파일은 GitHub에 올리지 않는 로컬 전용 `paper/` 폴더에 있다.

```powershell
cd "paper"
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

주의:

- 110번에는 `latexmk manuscript.tex` 단일 명령이 적혀 있지만, 현재 PC에서는 Perl 부재로 `latexmk`가
  막힐 수 있다.
- `paper/`는 `.gitignore` 대상이며 GitHub에 올리지 않는다.
- 빌드 아티팩트(`.aux`, `.log`, `.bbl`, `.pdf` 등)도 GitHub에 올리지 않는다.

## 재현성 테스트

각 검증 폴더의 `test_diagnostic.py`는 가벼운 계약 테스트다. 예:

```powershell
cd "61. 정지표적 도약 대규모 독립검증"
python -m pytest test_diagnostic.py
```

전체 대규모 실험 재실행은 시간이 걸릴 수 있으므로, 투고 직전에는 먼저 JSON 존재·수치 일치 감사 후
필요한 대표 폴더만 재실행한다.
