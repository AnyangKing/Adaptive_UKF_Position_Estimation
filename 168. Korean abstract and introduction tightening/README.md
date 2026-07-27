# 168. Korean abstract and introduction tightening

## 목적

한글 기준 원고 `paper/manuscript_ko.tex`의 초록과 서론을 166번 claim audit 및 167번 caption
policy와 정합하도록 안정화했다.

이번 단계는 새 실험이나 새 claim 추가가 아니라, 사용자가 교수님께 보여줄 때 초록·서론만 읽어도
논문 축과 한계가 안전하게 드러나도록 문장 흐름을 다듬는 작업이다.

## 수행 내용

- 한글 기준 원고 버전을 `v3`로 갱신했다.
- 초록에서 핵심 병목을 `필터 내부`가 아니라 `direct-path gate 안 coherent DOA bias`로 더 선명히 표현했다.
- carrier-agile pinging을 `새 localization solver`가 아니라 `송신 측 관측 설계`로 고정했다.
- 정지 600 m 결과는 유지했다: 13.01 m → 8.87 m, improvement 4.14 m, p=0.0008.
- moving target은 whitening만 확인, pooled RMSE 개선 미재현이라는 경계를 유지했다.
- 서론 첫 문단의 반복을 줄이고 TOA/TDOA/DOA-UKF 출발점을 압축했다.
- 기여 문단에서 `준정지`를 `매우 느린 준정지`로 좁혀 82번 경계와 맞췄다.

## 유지한 claim boundary

- frequency hopping USBL 최초 주장 금지
- 모든 이동 표적 성능 개선 주장 금지
- 0.100 m/s까지 일반 quasi-static 개선 주장 금지
- sub-meter long-range 주장 금지
- 160--162번 schedule/guard 결과를 본문 성능 claim으로 사용 금지

## paper 변경

실제 원고 수정은 로컬 전용 `paper/manuscript_ko.tex`에서 직접 수행했다.
`paper/`는 GitHub에 올리지 않는다.
이 168번 폴더에는 변경 이유와 감사 결과만 기록한다.

## 다음 단계

169번 후보는 `Korean discussion and conclusion tightening`이다.
목표는 Discussion과 Conclusion에서 한계·future work·real-water 검증 필요성을 정직하게 배치하고,
160--162번 결과가 본문 성능 claim처럼 읽히지 않도록 안정화하는 것이다.
