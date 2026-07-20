# 164. Korean manuscript structure pass

## 목적

163번에서 만든 `paper/manuscript_ko.tex`를 단순 설명문이 아니라 실제 논문 기준본으로 한 단계 올렸다.
이번 단계는 새 실험이 아니라 원고 구조 정리다.

## 수행 내용

- 한글 기준 원고를 v0에서 v1로 갱신했다.
- 초록 뒤에 핵심어와 "한글 기준 원고의 역할" 절을 추가했다.
- IEEE 계열 영문 원고로 옮기기 쉬운 장 흐름을 명시했다.
- 핵심 claim boundary 표를 추가했다.
- 그림 7개에 대한 본문 callout을 배치했다.
- 검증 결과 요약 표를 추가했다.
- 실패/한계 결과의 논문 내 배치 표를 추가했다.
- 160--162번 결과는 본문 성능 claim이 아니라 schedule limitation/future work 후보로 고정했다.

## paper 변경

실제 원고 파일은 로컬 전용 `paper/manuscript_ko.tex`에서 직접 수정했다.
`paper/`는 `.gitignore` 대상이며 GitHub에 올리지 않는다.
이 164번 폴더에는 무엇을 왜 바꿨는지 기록만 둔다.

## 확정된 원고 구조

1. 서론
2. 관련 연구와 문제 정의
3. 시스템 모델과 UKF 결합
4. 기본 추적 성능과 한계
5. 제안 방법: Carrier-Agile Whitening
6. 실험 검증과 적용 경계
7. 논의
8. 결론

## 핵심 claim boundary

- 정지 600 m 성능 개선은 본문 중심 claim으로 유지한다.
- 이동 표적은 residual whitening만 claim하고, pooled RMSE gain은 주장하지 않는다.
- 준정지 표적은 continuous safe boundary를 0.005 m/s로 제한한다.
- four-carrier/sparse schedule과 TOA guard는 검증 전이므로 본문 성능 claim에 넣지 않는다.

## 빌드 상태

`xelatex` 빌드는 이전 163번과 같은 MiKTeX 초기 설정/권한 문제로 아직 PDF 확인 대상에서 제외했다.
이번 단계의 검증은 LaTeX source structure와 figure/table reference 배치 확인으로 제한한다.

## 다음 작업

165번 후보는 `Korean manuscript language tightening`이다.
목표는 한글 원고를 사용자가 실제로 읽기 편한 문장으로 더 다듬고, 중복 설명을 줄이며, 수식/표/그림 주변 문장을 더 자연스럽게 만드는 것이다.
