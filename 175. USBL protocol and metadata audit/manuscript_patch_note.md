# Manuscript patch note

## 대상

로컬 전용 파일:

- `paper/manuscript_ko.tex`

GitHub에는 `paper/`를 올리지 않는다.

## 반영 내용

한국어 원고의 시스템 모델/관측 모델 부근에 다음 의미를 반영한다.

1. 현재 validation은 one-way synchronized beacon 설정이다.
2. 송신 시각 또는 common TOA offset은 보정된 것으로 가정한다.
3. 기준 센서 TOA는 `range = c * TOA`로 환산된다.
4. common clock bias, sensor별 hardware delay, gain/phase mismatch는 canonical validation에 포함하지 않는다.
5. 따라서 현재 결과를 full practical USBL protocol 검증으로 과장하지 않는다.

## 원고에 들어간 핵심 문장

> 본 논문의 canonical validation은 송신 시각 또는 공통 TOA offset이 보정된 one-way synchronized beacon 설정을 가정한다. 따라서 기준 센서 TOA는 곧바로 거리 관측으로 환산된다. common clock bias, 센서별 hardware delay, gain/phase mismatch는 본 validation의 성능 수치에 포함하지 않았으며, 실제 해상 실험에서는 별도 보정 또는 확장 상태로 다루어야 한다.

## claim 영향

기존 성능 수치는 바뀌지 않는다. 다만 논문 주장의 범위가 더 명확해진다.

- allowed: controlled one-way synchronized-beacon USBL simulation에서의 carrier-agile observation design 효과
- forbidden: uncalibrated practical USBL system 전체 성능 검증

