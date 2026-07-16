# 163. Korean-first manuscript workflow

## 목적

사용자가 현재 영어 원고를 직접 검토하기 어렵기 때문에, 앞으로의 원고 작업 순서를 바꾼다.
기존 영어 IEEEtran 원고를 바로 확장하는 대신, 먼저 한글 기준 원고를 완성하고 그 내용을 확정한 뒤 영어 원고로 번역·정리한다.

## 결정

- 기존 `paper/manuscript.tex`는 보존한다.
- 새 한글 기준 원고는 `paper/manuscript_ko.tex`에 둔다.
- `paper/`는 계속 로컬 전용이며 GitHub에 올리지 않는다.
- GitHub에는 이 163번 폴더처럼 numbered 작업 폴더만 올린다.
- 이후 원고 작업은 `한글 기준 원고 확정 → 영어 IEEEtran 반영 → 영어 표현/저널 형식 마감` 순서로 진행한다.

## 이번 폴더에서 한 일

1. 현재 영어 원고의 장 구조를 확인했다.
2. 한글 기준 원고 v0를 별도 LaTeX 파일로 만들었다.
3. 인계 문서 최상단 규약에 “한글 원고 우선” 작업 순서를 추가했다.
4. 기존 GitHub 규칙을 유지했다. 즉, 논문 실체 파일은 stage하지 않고 이 numbered folder만 커밋 대상으로 삼는다.

## 한글 원고 v0의 성격

`paper/manuscript_ko.tex`는 최종 투고 파일이 아니다.
사용자가 연구 논리와 주장 범위를 읽고 판단하기 위한 기준 원고이다.
현재 내용은 다음 중심축을 따른다.

- 출발점: 8센서 USBL에서 TOA/TDOA/DOA를 UKF로 결합해 3D 위치 추정
- 병목 발견: 장거리에서 필터보다 post-gating coherent multipath DOA bias가 더 큰 한계
- 제안 방법: 30--34 kHz carrier-agile pinging으로 편향의 시간상관을 낮춤
- 강한 결과: 정지 600 m RMSE 13.01 m에서 8.87 m, paired improvement 4.14 m, p=0.0008
- 경계: 이동 표적에서는 whitening은 확인되나 pooled RMSE gain은 미재현
- 준정지 claim: continuous safe boundary는 0.005 m/s까지
- 160--162번 추가 실험은 본문 핵심 claim이 아니라 schedule limitation/future work 후보

## 다음 작업

164번 후보는 `Korean manuscript structure pass`이다.
목표는 `paper/manuscript_ko.tex`를 사용자가 읽기 좋은 논문 구조로 더 다듬는 것이다.

- IEEE 계열 논문처럼 장 번호와 소절 밀도를 정리한다.
- 표와 그림 callout을 한글 원고에 명확히 배치한다.
- 160--162번 결과를 본문에 넣을지, 보충/한계/future work로만 둘지 문장 수준에서 잠근다.
- 한글 원고가 안정된 뒤 영어 `paper/manuscript.tex`에 반영한다.
