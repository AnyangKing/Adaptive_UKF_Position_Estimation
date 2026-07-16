# 공부 노트: 모달리티 선택적 격리

센서융합에서 한 관측 벡터의 일부만 깨졌을 때 전체 ping을 버리면 다른 유용한 정보도 잃는다.
162번 guard는 carrier transition과 큰 absolute-TOA jump가 동시에 있을 때 measurement index 0만
거의 무한 분산으로 만들고, TDOA 7개와 DOA 2개는 계속 UKF update에 사용한다.

기존 adaptive-R도 TOA NIS가 크면 분산을 최대 100배 키웠지만, base TOA 표준편차가 0.03 m라
3.557 m branch jump를 반복해서 충분히 차단하지 못했다. hard isolation은 전환 ping의 range
정보를 제거하되 방향·상대지연 정보로 상태를 이어간다.

중요한 한계는 0.5 m 기준이 static 전용이라는 점이다. 이동 표적에서는 실제 1초 range 변화와
branch switch를 분리해야 하므로 속도 예측과 결합한 threshold가 필요하다. 현재 방법을 moving에
그대로 적용하면 실제 운동을 이상치로 오인할 수 있다.
