# 78. Related Work 최근접 선행연구 차별표

## 목적

frequency-agile pinging 논문의 novelty를 방어하기 위해, 가장 가까운 선행연구들을 정면으로 정리한다.

중요한 수정점:

- “수중 USBL에서 frequency hopping 자체가 없었다”는 주장은 부정확하다.
- frequency-hopped acoustic modem, Costas hopping, acoustic frequency comb, MIMO sonar transmitting diversity 등은 이미 존재한다.
- 본 연구의 차별점은 **frequency hopping 자체**가 아니라, **얕은바다 gated USBL에서 carrier-locked coherent multipath DOA bias를 ping간 carrier schedule로 백색화하고, TOA/TDOA/DOA-UKF 추적 루프에서 정지/이동 적용경계를 검증한 것**이다.

## 결론

현재 논문 novelty는 여전히 살아있다. 단, 표현은 반드시 다음처럼 제한해야 한다.

> Prior underwater acoustic positioning studies have used frequency-hopped, Costas, and multi-frequency signals for communication-aided positioning, correlation improvement, baseline optimization, and DOA estimation. In contrast, this work targets a different failure mode: carrier-locked coherent multipath DOA bias after direct-path gating. We show that ping-to-ping carrier agility whitens this bias in the UKF measurement stream, improves static long-range localization, and quantifies the moving-target boundary.

## 출력 파일

- `related_work_differentiation.md`: 최근접 선행연구 차별표, Related Work 문단 초안, 리뷰어 대응 문장.

## 다음 단계

79번은 Discussion 절 초안이 자연스럽다. 특히 Fig.7 CRLB floor, sub-meter 장거리 기대치 정리, 실해역 검증 계획, 그리고 radar glint와 수중 USBL의 차이를 묶어야 한다.
