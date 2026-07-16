# 공부 노트: 현장실험은 데이터 계약부터 시작한다

현장실험에서 가장 흔한 실패는 신호가 없어서가 아니라, 나중에 비교에 필요한 메타데이터가 빠져 결과를
논문 증거로 쓰지 못하는 것이다. 특히 frequency agility는 carrier별 출력·SNR 차이가 whitening 효과와
섞일 수 있으므로 calibration ID, SNR, late-energy ratio를 함께 기록해야 한다.

CSV schema는 필드 이름만 정하는 문서가 아니다. 단위, 허용 범위, fixed/hop 조건, ABBA 순서,
mock/measured 구분과 제외 사유까지 포함해야 사후 선택 편향을 줄일 수 있다.

실제 데이터를 넣기 전 mock log로 validator를 실행하면 템플릿과 분석 파이프라인의 형식 오류를 현장에
가기 전에 발견할 수 있다.
