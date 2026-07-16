# 공부 노트: carrier set과 order는 다른 설계변수다

정지 기하에서 schedule 평균 편향은 어떤 carrier들을 포함하는지에 크게 좌우된다. 같은 carrier set을
순열만 바꾸면 전체 평균은 같지만 ping-to-ping 상관 구조는 달라질 수 있다.

이번 Stage 0에서 linear와 seeded random은 평균 편향 상쇄량이 동일했지만 random order의 |lag-1|가
더 낮았다. 반대로 30/34 kHz two-extreme은 평균 편향을 줄이면서도 완전 교대 상관을 만들어 whitening
관점에서는 좋지 않았다.

따라서 schedule ablation은 최소 두 축을 분리해야 한다.

1. carrier-set coverage: bias phase를 얼마나 넓게 평균하는가.
2. order correlation: ping-to-ping sequence가 잔차 상관을 어떻게 만드는가.

Stage 0 bias proxy는 후보를 줄이는 도구일 뿐이며 UKF 위치 RMSE를 대신하지 않는다.
