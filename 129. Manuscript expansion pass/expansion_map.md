# Expansion map

## Added content by section

### II. Related Work and Problem Statement

추가 내용:

- 논문의 research question 3개:
  1. diagnostic question
  2. mechanistic question
  3. operational boundary question
- negative experiments를 숨기지 않고 claim boundary를 좁히는 근거로 쓰는 이유.

목적:

- Introduction/Related Work가 단순 배경 설명이 아니라 논문 전체 논리의 지도 역할을 하도록 강화.

### III. System Model and UKF Fusion

추가 내용:

- compact aperture가 long-range angular error를 증폭한다는 설명.
- direct/surface/bottom image-source signal model:

```latex
y_{i,k}(t)=\sum_{\ell\in\mathcal{P}} a_{\ell,i,k}
q_k(t-\tau_{\ell,i,k}) e^{j2\pi f_k(t-\tau_{\ell,i,k})}+n_{i,k}(t)
```

- TOA/TDOA/DOA의 역할 분리.
- 28개 pairwise GCC-PHAT TDOA를 7개 reference difference로 줄이는 설명.
- adaptive-R UKF가 coherent residual 자체를 white하게 만들지는 못한다는 한계.
- 5 ms DOA gate가 late multipath는 줄이지만 in-gate reflection은 제거하지 못한다는 설명.

목적:

- 리뷰어가 “채널/관측/필터가 너무 간단히 설명됐다”고 지적할 가능성 감소.

### IV. Proposed Carrier-Agile Whitening Method

추가 내용:

- 연구가 filter tuning에서 observation design으로 전환된 이유.
- 실패한 filter/calibration/SRP refinement 계열이 왜 중요한 negative evidence인지 설명.
- carrier phase rotation:

```latex
\Delta\phi = 2\pi (f_b-f_a)\delta_k
```

- whitening이 explicit multipath cancellation이 아니라는 점.
- frozen deterministic sweep이 post-hoc schedule optimization이 아니라는 점.

목적:

- novelty를 “주파수 도약 자체”가 아니라 “coherent residual whitening mechanism”으로 정렬.

### V. Experimental Validation and Applicability Boundary

추가 내용:

- `Evaluation Protocol and Statistical Testing` subsection 신설.
- paired comparison, settled window, geometry effect 통제 설명.
- RMSE evidence와 residual-whitening evidence를 분리하는 이유.
- moving/quasi-static negative results를 boundary evidence로 해석.
- real-water validation 순서상 static/very-slow-drift부터 가야 한다는 계획 논리.

목적:

- 실험 프로토콜과 통계 해석이 본문 안에서 더 자립적으로 보이게 함.

### VI. Discussion

추가 내용:

- novelty claim을 좁게 읽어야 하는 이유.
- transmitter schedule이 waveform design과 tracking 사이의 design lever라는 해석.
- frequency-dependent array calibration이라는 practical cost.

목적:

- SCI reviewer가 물을 “그래서 실제 시스템에서는?” 질문에 대한 1차 답변 확보.

