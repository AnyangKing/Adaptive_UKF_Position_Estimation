# 공부 노트: 백색화와 위치 RMSE는 같은 목적함수가 아니다

같은 20개 carrier를 쓰는 linear와 random schedule은 평균적인 carrier 편향 상쇄 능력이 같아도
시간 순서 때문에 innovation autocorrelation이 달라진다. 그러나 lag-1이 더 낮았던 random이
linear보다 RMSE가 낮지는 않았다. UKF 성능은 잔차의 자기상관뿐 아니라 ping별 편향 부호,
초기화, 비선형 기하, adaptive-R routing이 함께 결정한다.

따라서 schedule 설계는 `carrier set → 평균 편향 상쇄`와 `carrier order → 시간 상관 구조`를
분리해 보되, 최종 선택은 항상 full localization RMSE와 tail에서 해야 한다. whitening proxy만
최적화하면 moving schedule 연구에서 이미 본 것처럼 실제 오차가 악화될 수 있다.
