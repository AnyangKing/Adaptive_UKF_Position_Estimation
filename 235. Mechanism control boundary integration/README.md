# 235. Mechanism control boundary integration

## 목적

다른 AI가 지적한 두 번째 미해결 약점인 **185/187 기전 통제 실험의 원고 반영 부족**을 보완했다.

핵심 문제는 다음이었다.

- 185번 direct-path-only control에서 explicit multipath를 제거해도 1000 m noisy direct-only 조건에서 carrier-agile 이득이 일부 남았다.
- 187번 no-noise direct-path-only control에서는 그 1000 m 이득이 사라졌다.
- 따라서 원고가 `carrier agility의 이득 = 오직 in-gate multipath phase rotation`처럼 읽히면 과잉 귀속이 된다.

## 원고 반영

영문 원고 `paper/manuscript.tex`의 Mechanism 절에 다음 boundary를 추가했다.

- direct-path/no-noise controls가 단일 기전 귀속을 제한한다.
- coherent multipath phase diversification은 장거리 얕은 수중 결과와 가장 정합적인 dominant explanation이다.
- 그러나 carrier-dependent observation-extraction/noise-response interaction도 일부 기여할 수 있다.
- 따라서 제안법은 `모든 개선이 two-ray phase rotation에서만 온다는 증명`이 아니라, 추출된 TOA/TDOA/DOA 관측의 시간적 오차 구조를 바꾸는 carrier-agile observation design으로 해석해야 한다.

`paper/`는 로컬 전용이므로 GitHub에 올리지 않는다.

## 감사

`audit_mechanism_boundary.py`를 추가해 다음을 검사했다.

- 원고에 185/187 control boundary marker가 있는지
- 185/187 source summary에 필요한 근거 marker가 있는지
- 금지된 과잉 귀속 문장이 원고에 없는지

실행 결과:

```text
PASS
```

확인된 marker:

- `Direct-path control runs`
- `no-noise direct-path control`
- `carrier-dependent observation-extraction and noise-response interactions`
- `not as proof that all improvement arises only from two-ray multipath phase rotation`

## 빌드 확인

영문 원고 빌드 확인:

- `paper/manuscript.pdf`: 15 pages, 564394 bytes
- fatal LaTeX error 없음
- undefined citation/reference 없음
- overfull hbox 없음

남은 underfull vbox는 최종 조판 단계에서 다룰 수 있는 비치명 경고다.

## 한글 원고 상태

한글 원고에는 이미 185번 direct-path-only control을 근거로 단일 기전 귀속을 조심해야 한다는 설명이 들어가 있다.  
다만 187번 no-noise control까지 한글 문장에 명시적으로 더 넣는 작업은 터미널 인코딩 문제로 이번 자동 패치에서 보류했다. 영문 투고 원고의 Mechanism 절에는 185/187이 모두 반영되어 있다.

