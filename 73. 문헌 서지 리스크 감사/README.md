# 73. 문헌 서지 리스크 감사

## 목적

68번에서 정한 novelty 포지셔닝을 실제 참고문헌으로 방어할 수 있는지 점검한다. 핵심은 “frequency agility 원리 자체는 레이더 고전”이라는 문장을 쓰되, 정확히 확인되지 않은 고전 논문 제목을 확정 인용처럼 쓰지 않는 것이다.

## 이번 감사의 결론

일반 웹 검색 기준으로는 다음이 확인됐다.

1. `frequency agility`가 레이더 분야의 확립된 개념이라는 일반 근거는 확보 가능하다.
2. USBL이 range + angle을 이용하고, 소형 baseline에서는 거리 증가에 따라 각도 오차가 위치 오차로 커진다는 배경 근거도 확보 가능하다.
3. 수중 음향에서는 FHSS/FSK/OFDM 등 주파수 사용·통신 문헌은 많지만, “USBL DOA bias를 송신 carrier hopping으로 whiten한다”는 직접 선행연구는 일반 웹에서 바로 확인되지 않았다.
4. 그러나 이전에 후보로 적었던 `Reduction of Radar Tracking Errors with Frequency Agility`, `Frequency-Agility Processing to Reduce Radar Glint Pointing Error` 같은 정확 제목은 일반 웹 검색에서 안정적으로 검증되지 않았다.

따라서 현재 원고에서는 고전 논문 제목을 확정적으로 박기보다, 아래처럼 안전하게 써야 한다.

> Frequency agility is a well-established radar concept, especially in electronic counter-countermeasure and pulse-to-pulse frequency-diverse radar processing. Related radar literature also discusses target glint and monopulse angle-error phenomena. However, the present contribution is not the invention of frequency agility itself, but its transfer to shallow-water USBL DOA-bias whitening with a distinct in-gate surface-reflection mechanism and validated static-target boundary.

## 현재 확보된 공개 근거

| 구분 | 공개 근거 | 원고에서의 용도 | 주의 |
|---|---|---|---|
| Radar frequency agility 일반 개념 | Wikipedia `Frequency agility`, Galati 등 참고문헌 언급 | “frequency agility는 레이더 분야의 기존 개념”이라는 배경 | Wikipedia는 최종 SCI 참고문헌으로 부적합. Galati/IET 같은 원서 또는 IEEE 문헌으로 대체 필요 |
| Monopulse/glint/angle error 배경 | Wikipedia `Monopulse radar`, `Angle deception jamming` 등 | 레이더 각도추적/monopulse/glint 계열 배경 확인 | 최종 인용은 Sherman/Barton/Mahafza 등 교재·논문으로 대체 |
| Modern frequency-agile radar | Huang et al. arXiv `Analysis of Frequency Agile Radar via Compressed Sensing` | 최근 FAR가 여전히 활발한 연구분야임을 보여주는 보조 배경 | 본 연구의 glint/DOA-bias 백색화와 직접 연결은 약함 |
| Underwater acoustic positioning/USBL | Wikipedia `Underwater acoustic positioning system` | USBL은 range+direction으로 위치를 정하고, 거리 증가에 따라 각도오차가 커지는 배경 | 최종 인용은 Milne, ROV Manual, USBL 시스템 논문 등으로 대체 필요 |
| Underwater acoustic frequency use | Wikipedia `Underwater acoustic communication` | 수중 주파수 hopping/FHSS는 통신 쪽에 존재함 | 위치추정 DOA-bias whitening 직접 선행근거로 쓰면 안 됨 |

## 정확 서지 미확정 후보

아래 항목들은 이전 AI/검색 과정에서 단서로 언급됐지만, 이번 일반 웹 검색에서는 정확 서지 검증이 안 됐다. 원고에 넣기 전 반드시 IEEE Xplore, Google Scholar, Scopus, Web of Science 중 하나로 확인해야 한다.

- `Reduction of Radar Tracking Errors with Frequency Agility`
- `Frequency-Agility Processing to Reduce Radar Glint Pointing Error`
- Barton 계열 radar glint/frequency diversity 설명의 정확 책/장/쪽수
- Sherman `Monopulse Principles and Techniques`에서 glint와 frequency diversity를 연결하는 정확 위치

## 원고 작성 시 안전한 전략

### 쓰면 되는 주장

- Frequency agility 자체는 레이더에서 오래된 개념이다.
- Radar target glint/monopulse angle error는 기존에 알려진 문제다.
- 본 연구의 novelty는 원리 발명이 아니라 다음 네 가지다.
  - 얕은바다 gated USBL의 게이트-내 표면반사 coherent leakage 기전
  - `phi = 2πfδ` 기반 carrier-sensitive DOA bias 백색화
  - 정지/준정지 600 m 대규모 독립검증
  - 이동 표적에서 motion self-whitening으로 이득이 소멸하는 적용 경계

### 아직 쓰면 위험한 주장

- “레이더 논문 A가 정확히 RMS √N 개선을 보였다”처럼 정확 제목·수치·쪽수 없이 말하는 것
- “수중에서 아무도 한 적 없다”를 단정하는 것
- “frequency agility를 우리가 처음 제안했다”는 식의 표현
- 통신용 FHSS 문헌을 위치추정 DOA-bias whitening 선행연구처럼 쓰는 것

## 다음 단계

이 폴더의 결론은 “문헌 축은 아직 완전 확정이 아니다”이다. 따라서 다음 연구 폴더는 두 갈래다.

1. DB 접근이 가능하면 `74. 레이더 glint 정확 서지 확정`을 수행한다.
   - IEEE Xplore / Google Scholar / Scopus / Web of Science에서 exact title, DOI, 저자, 연도 확인.
2. DB 접근이 제한되면 `74. Introduction 초안`을 먼저 작성하되, 참고문헌 자리는 `[RADAR_GLINT_REF]`, `[FREQUENCY_AGILITY_REF]` placeholder로 남긴다.

현재 Codex 환경에서는 일반 웹 검색만으로 exact old IEEE citation을 확정하기 어렵다. 이 부분은 나중에 학교망/도서관 DB 또는 Scholar 접근으로 반드시 닫아야 한다.

## 검색 로그 요약

- 검색어: `"Reduction of Radar Tracking Errors with Frequency Agility"`
- 검색어: `"Frequency-Agility Processing" "glint" "pointing error"`
- 검색어: `radar glint frequency agility tracking errors`
- 검색어: `monopulse radar glint reduction frequency diversity`
- 검색어: `underwater acoustic USBL frequency diversity multipath DOA bias`

결과: 일반 개념 근거는 있으나, exact 고전 논문 서지는 미확정.
