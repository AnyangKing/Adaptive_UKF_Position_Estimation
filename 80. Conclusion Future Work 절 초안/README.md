# 80. Conclusion Future Work 절 초안

## 목적

논문 Conclusion and Future Work 절 1차 초안을 작성한다. 이 절은 본 연구의 기여를 간결하게 닫고, 과잉주장 없이 남은 과제를 제시한다.

## 핵심 결론

- 본 연구는 TOA/TDOA/DOA를 UKF로 융합하는 USBL 위치추정에서 출발했다.
- 현실 수중 멀티패스 조건에서 장거리 병목은 필터 비효율이 아니라 coherent multipath DOA bias floor였다.
- Frequency-agile pinging은 그중 carrier-locked coherent 성분을 ping간 백색화하는 transmit-side observation design이다.
- 정지 600 m에서 RMSE 13.01 m → 8.87 m, p=0.0008로 검증됐다.
- 이동 표적에서는 residual whitening은 확인됐지만 RMSE 이득은 미재현되어 적용 경계로 남긴다.

## 다음 단계

81번은 실험 보강을 한다면 `준정지 속도 경계 검증`이 가장 좋다. 논문 조립을 계속한다면 Abstract 초안이나 전체 원고 조립으로 넘어갈 수 있다.
