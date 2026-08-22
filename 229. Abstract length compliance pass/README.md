# 229. Abstract length compliance pass

## 목적

논문 초안의 영문/한글 abstract가 대부분의 저널에서 흔히 요구하는 200단어 내외 제한을 넘지 않도록 압축했다.  
새 실험 결과나 새 claim은 추가하지 않고, 기존 원고의 핵심 주장과 수치만 유지했다.

## 처리 내용

- `paper/manuscript.tex` 영문 abstract를 200단어 이하로 재작성했다.
- `paper/manuscript_ko.tex` 한글 abstract를 200어절 이하 수준으로 재작성했다.
- 한글 원고의 기존 장문 abstract는 추적성을 위해 `\iffalse ... \fi`로 비활성 보존했다.
- `paper/`는 로컬 전용 작업물이며 GitHub에는 올리지 않는다.

## 길이 점검 결과

| 원고 | 수정 전 | 수정 후 | 판정 |
|---|---:|---:|---|
| 영문 abstract | 약 316 words | 194 tokens | 200 이하 충족 |
| 한글 abstract | 약 259 space tokens | 172 space tokens | 200 이하 충족 |

## 유지한 핵심 claim

- 600 m 정지 표적에서 carrier-agile 관측 설계가 fixed carrier 대비 RMSE를 낮춤.
- 0--1000 m 거리 sweep과 이동/OOD 검증을 통해 효과의 적용 경계를 함께 제시함.
- frequency hopping 자체의 최초 발명이 아니라, 얕은 수중 USBL에서 coherent multipath bias를 시간적으로 백색화하는 관측 설계와 transition-risk routing의 검증이라는 위치를 유지함.
- 실해역 검증 부재, hardware frequency response 미검증, 임의 이동 표적 전체 일반화 금지라는 한계 문구는 유지함.

## 빌드 확인

- `paper/manuscript.pdf`: 15 pages
- `paper/manuscript_ko.pdf`: 16 pages
- fatal error, undefined citation/reference, overfull hbox 없음
- 남은 경고는 기존의 underfull/hyperref 계열로, 최종 조판 단계에서 정리하면 되는 비치명 경고임

