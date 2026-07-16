# 공부 노트: median 개선이 있어도 sparse schedule을 채택하지 않은 이유

four-carrier는 20기하 중 14개에서 fixed보다 좋았고 paired Wilcoxon도 한쪽 방향 신호를 보였다.
하지만 한 기하의 53 m 발산 때문에 mean과 P90이 fixed보다 나빠졌다. 위치추정 시스템에서는
평균적인 다수 개선보다 드문 큰 오차가 운용 안전성을 지배할 수 있다.

사전 기준에 mean, median, improved fraction, P90, 발산을 함께 둔 이유가 여기서 드러났다.
좋아 보이는 median만 골라 보고하면 sparse schedule이 성공한 것처럼 보이지만, 실제 결론은
tail-unsafe다. 독립검증은 개발표본의 순위를 확인하는 의식이 아니라 그 순위를 깨뜨릴 수 있는
검사여야 한다.

또한 linear20은 fixed보다 mean RMSE 약 24% 감소를 신규 seed에서 재현했다. 이것은 linear20이
모든 가능한 schedule 중 최적이라는 뜻이 아니라, 현재 검증 범위에서 sparse four-carrier보다
안정적이며 기존 주장을 유지할 근거가 추가됐다는 뜻이다.
