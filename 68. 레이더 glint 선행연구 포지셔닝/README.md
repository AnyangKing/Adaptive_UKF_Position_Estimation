# 68. 레이더 glint 선행연구 포지셔닝

## 목적

67번 이후 연구 방향은 실험 추가보다 논문 조립으로 전환됐다. 이 폴더의 목적은 frequency-agile pinging 논문의 선행연구 방어선을 정리하는 것이다.

핵심 질문:

1. 주파수 도약으로 각도오차/glint를 탈상관하는 원리가 이미 알려져 있는가?
2. 그렇다면 우리 논문의 novelty를 어떻게 정직하게 재정의해야 하는가?
3. 원고 작성 전에 어떤 문헌 확인이 추가로 필요한가?

## 결론

원리 자체를 “우리가 처음 발명했다”고 주장하면 안 된다. 레이더 분야에는 pulse-to-pulse frequency agility, frequency diversity, glint/angle-error decorrelation 계열의 오래된 문헌과 Barton 계열 참고문헌이 존재한다.

따라서 논문 기여는 다음으로 재정의한다.

> 레이더 glint 탈상관 원리를 얕은바다 USBL의 coherent multipath DOA bias 문제로 이식하고, 수중 고유의 게이트-내 표면반사 기전, 정지/이동 적용 경계, 그리고 정지표적 대규모 독립검증을 제시했다.

## 기여 재정의

### C1. 수중 고유 편향 기전 규명

직접파 time-gating을 적용해도 얕은바다 USBL에서는 게이트 안에 표면반사 coherent leakage가 남는다. 이 잔여 성분은 고도각 DOA에 결정론적 계통 편향을 만들고, 거리가 멀어질수록 위치오차로 증폭된다.

이 부분은 레이더 glint와 다르다. 레이더 glint는 표적 산란점의 간섭이 핵심이지만, 우리는 얕은바다 표면반사와 소형 배열 개구/게이트 구조가 핵심이다.

### C2. 반송파 도약에 의한 편향 백색화

표면반사와 직접파의 상대 위상은 다음 항을 따른다.

```text
phi = 2π f δ
```

고정 반송파에서는 `f`가 고정되어 편향도 반복된다. ping마다 반송파를 30~34 kHz 범위에서 바꾸면 `phi`가 회전하고, 편향이 ping 간 백색화된다.

63번에서 이동 표적 기준 고도각 오차 lag-1 자기상관은 fixed +0.470에서 hop -0.208로 감소했다. p = 5.56e-10이다.

### C3. 정지/준정지 표적 대규모 독립검증

61번에서 정책 동결, 독립 seed 조건으로 정지 표적 대규모 검증을 통과했다.

- 600 m fixed: 13.01 m
- 600 m hop: 8.87 m
- 개선: -32%
- 평균 이득: +4.14 m
- p = 0.0008
- median 개선: -43%

이 결과가 논문 본체의 가장 강한 성능 근거다.

### C4. 적용 경계 규명

이동 표적에서는 기하가 변하면서 상대 지연 `δ`도 변한다. 따라서 고정 반송파에서도 편향이 어느 정도 자연 진동·평균된다. 이를 motion-induced self-whitening으로 해석한다.

63번에서 hop은 lag-1 자기상관을 강하게 낮췄지만, pooled RMSE 이득은 유의하지 않았다.

- 이동 표적 pooled 이득: -0.10 m
- p = 0.301

64~67번의 adaptive-R, anchor-hop, condition-aware schedule도 보편 개선법으로는 미재현됐다. 이 결과는 실패라기보다 적용 경계를 정직하게 보여주는 자료다.

## 현재 문헌 확인 상태

### 웹 quick-check에서 확인한 것

- frequency agility는 레이더 분야와 강하게 연결된 용어이며, 레이더에서 운용 주파수를 빠르게 바꾸는 개념으로 설명된다.
- David K. Barton은 레이더 시스템 분석/모델링 및 radar reference book 계열의 핵심 인물이며, `Radars` 시리즈 중 `Frequency Agility and Diversity` 권이 존재한다는 서지 단서가 있다.
- 일반 웹 검색에서는 `Reduction of Radar Tracking Errors with Frequency Agility`, `Frequency-Agility Processing to Reduce Radar Glint Pointing Error` 같은 정확 제목의 원문/서지 정보가 바로 안정적으로 회수되지는 않았다.

### 주의

현재 상태는 “정식 인용 확정”이 아니다. 일반 웹 검색은 부정확하거나 누락이 많다. 원고에 들어갈 참고문헌은 반드시 IEEE Xplore, Google Scholar, Scopus, Web of Science, 도서관 검색으로 재확인해야 한다.

## 원고에서 안전한 표현

좋은 표현:

> Frequency agility has a long history in radar tracking as a means of reducing glint or angle-error correlation. We do not claim this principle as new. Instead, we show that an analogous transmit-frequency agility can whiten a distinct shallow-water USBL bias mechanism caused by in-gate coherent surface-reflection leakage.

피해야 할 표현:

> We propose the first frequency-agile method for whitening angle errors.

더 안전한 한국어 요약:

> 본 연구는 주파수 agility 원리 자체를 새로 발명한 것이 아니라, 레이더 glint 탈상관에서 알려진 원리를 얕은바다 USBL의 게이트-내 표면반사 coherent DOA 편향 문제에 이식하고, 그 기전과 적용 경계를 정량 검증한 것이다.

## 원고 Introduction에 들어갈 기여 문장 초안

1. We identify a deterministic elevation-bias floor that persists after direct-path gating in a shallow-water USBL array and show that it is driven by carrier-sensitive coherent surface-reflection leakage.
2. Inspired by frequency-agile radar tracking, we introduce a transmit-side frequency-agile pinging strategy that rotates the interference phase and whitens the bias across pings without modifying the receiver or Kalman filter.
3. We validate the method on static/near-static targets with frozen policies and independent Monte Carlo seeds, achieving a 32% RMSE reduction at 600 m.
4. We characterize the boundary of applicability: moving targets exhibit motion-induced self-whitening, and additional adaptive scheduling attempts did not yield reproducible RMSE gains.

## 다음 확인 체크리스트

- [ ] IEEE Xplore에서 radar glint + frequency agility 논문 2~3편 정확 서지 확인
- [ ] Barton `Radars` vol. 6 `Frequency Agility and Diversity` 또는 관련 book chapter 확인
- [ ] `Radar System Analysis and Modeling`, `Radar Technology Encyclopedia`, `Monopulse Principles and Techniques`에서 glint/frequency diversity 관련 구절 확인
- [ ] Google Scholar에서 `underwater acoustic USBL frequency agile pinging multipath DOA bias` 계열 재검색
- [ ] 수중 frequency diversity가 수신단 처리인지, 송신 반송파 도약 기반 DOA bias whitening과 다른지 표로 정리

## 판정

문헌 포지셔닝 방향은 채택한다.

다만 정확 인용은 아직 미완성이다. 68번의 결론은 “원고에서 novelty를 어떻게 주장해야 하는가”에 대한 포지셔닝 확정이며, 최종 참고문헌 확정은 별도 단계로 남긴다.
