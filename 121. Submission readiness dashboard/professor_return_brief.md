# Professor return brief

교수님이 돌아오시면 아래 순서로 보고하면 된다.

## 1. 한 줄 결론

TOA/TDOA/DOA-UKF 기반 수중 USBL 위치추정 연구는, 필터 개선을 넘어 **게이트-내 표면반사 coherent
DOA bias** 문제를 규명했고, **ping-to-ping carrier agility**로 이 bias의 시간상관을 whitening하여 정지
600 m에서 RMSE를 13.01 m에서 8.87 m로 줄이는 결과를 얻었다.

## 2. 우리가 주장하지 않는 것

- frequency hopping USBL 최초가 아니다.
- moving target RMSE 개선 논문이 아니다.
- 0.1 m/s까지 quasi-static 검증됐다는 논문이 아니다.
- 600 m sub-meter 논문이 아니다.

## 3. 우리가 주장하는 것

- compact shallow-water USBL에서 post-gating coherent multipath DOA bias가 long-range floor를 만든다.
- carrier-agile pinging은 이 residual의 시간상관을 줄인다.
- static 600 m에서는 독립 seed로 RMSE 개선이 재현됐다.
- moving target에서는 whitening은 되지만 RMSE 개선은 일반화되지 않아 boundary로 보고한다.

## 4. 교수님께 필요한 결정

1. 이 논문 축으로 계속 갈지.
2. 목표 저널.
3. simulation 중심 투고인지, 실해역/수조 검증 후 투고인지.
4. 저자·소속·교신저자.
5. Funding / Conflict / Data availability.
6. 코드·데이터 공개 방식.

## 5. 교수님 부재 중 추가로 준비한 것

- 재현성 패키지 감사.
- claim boundary 감사.
- 선행연구 방어표.
- real-water validation plan.
- carrier schedule ablation plan.
- supplement archive dry run.

## 6. 추천 질문

> 교수님, 이 논문을 “static/very-slow-drift shallow-water USBL에서 coherent multipath DOA bias를
> carrier-agile pinging으로 whitening하는 논문”으로 잡고, moving target은 boundary/future work로 두는
> 방향으로 투고 준비해도 될까요?
