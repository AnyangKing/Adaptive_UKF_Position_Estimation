# 117. Related work table finalization

## 목적

116번에서 원고 claim boundary가 안전하다는 것을 확인했으므로, 이번 단계에서는 reviewer가 가장 먼저
공격할 선행연구 축을 원고용으로 정리했다.

핵심 질문:

> “USBL에서 frequency hopping, Costas hopping, frequency comb이 이미 있는데 이 논문이 뭐가 다른가?”

답:

> 맞다. frequency diversity 자체가 새롭다는 주장은 하지 않는다. 본 논문의 기여는 direct-path gate
> 이후 남는 carrier-locked coherent multipath DOA bias를 문제로 정의하고, ping-to-ping carrier agility로
> 그 residual의 시간상관을 백색화해 TOA/TDOA/DOA-UKF tracking loop 안에서 static 성능과 moving boundary를
> 검증한 것이다.

## 결론

현재 원고의 Related Work 표는 기본 방어선으로 충분하다. 다만 투고 직전에는 다음 보강이 좋다.

1. Nhat 2022 Costas-USBL 행에 “intra-ping waveform / time-delay precision” 차이를 더 직접적으로 넣기.
2. Qian 2025 frequency-comb iUSBL 행에 “multipath는 comb로 직접 제거하지 않고 beamforming/channel estimation으로 미룸” 차이를 넣기.
3. Henderson 1985 acoustic glint/broadband direction finding, Zhang 2024 USBL differential correction, Liu 2026 FDA sonar는 선택 인용 후보로 남기기.

## 산출물

- `final_related_work_table.md`: 최종 방어 표.
- `reviewer_response_templates.md`: 리뷰어 공격별 답변 문장.
- `citation_priority.md`: 필수/권장/선택 인용 구분.
- `manuscript_related_work_patch.md`: 현재 원고에 넣을 수 있는 안전한 패치 문장.

## 다음

117번 이후의 자연스러운 순서는 118번 `Real-water validation plan`이다. 선행연구 방어는 이제 충분히
정리되었고, 남은 큰 약점은 “시뮬레이션 기반”이라는 점이므로 호수/해상/수조 실험 계획을 교수님 없이도
구체화해두는 것이 좋다.
