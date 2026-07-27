# Abstract and introduction changes

## 초록 변경 요약

Before의 문제:

- 초록이 전반적으로 안전했지만, 첫 문단에서 `필터 구조 개선`과 실제 병목 사이의 전환이 약간 느슨했다.
- `carrier-agile pinging`이 새 solver가 아니라 송신 측 observation design이라는 점을 더 선명히 할 필요가 있었다.

After:

- 병목을 `얕은바다 direct-path gate 안 표면반사 coherent DOA bias`로 명시했다.
- 방법을 `새로운 localization solver가 아니라 동일 TOA/TDOA/DOA-UKF 루프에 들어오는 관측 오차 시간상관을 바꾸는 송신 측 관측 설계`로 표현했다.
- 성능 수치와 moving boundary는 변경하지 않았다.

## 서론 변경 요약

Before의 문제:

- 첫 문단이 USBL 일반 설명과 본 연구 출발점을 따로 말해 약간 늘어졌다.
- 기여 문단의 `준정지` 표현이 82번의 0.005 m/s 제한보다 넓게 읽힐 수 있었다.

After:

- USBL 일반 설명과 본 연구의 TOA/TDOA/DOA-UKF 출발점을 한 문단으로 압축했다.
- 기여 문단을 `이동 표적과 매우 느린 준정지 표적에서 적용 경계를 제시`로 수정했다.

## 검증

- 정지 600 m headline 수치 유지: 13.01 m → 8.87 m, improvement 4.14 m, p=0.0008.
- moving pooled RMSE gain 미재현 표현 유지.
- quasi-static boundary를 넓히는 표현 없음.
- frequency hopping USBL 최초성 주장 없음.
- 원고 표·그림 캡션·본문 수식 변경 없음.
