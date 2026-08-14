# 198. Moving result narrative tightening

## 목적

191번의 0--1000 m 이동 표적 독립 검증 결과를 원고 본문에서 더 방어적으로 읽히도록 서술을 정리했다.

이번 작업은 새 실험이 아니라 `paper/manuscript.tex`와 `paper/manuscript_ko.tex`의 로컬 원고 문장 정리다. 논문 파일은 로컬 전용이므로 GitHub에는 올리지 않고, 이 폴더만 기록·커밋한다.

## 핵심 수정

- plain frequency hopping의 이동 표적 실패를 “주파수 도약 자체가 무조건 좋다/나쁘다”로 쓰지 않고, “stand-alone waveform으로 판단하면 위험하며 필터 쪽 신뢰도 반응이 같이 필요하다”로 정리했다.
- 191번의 거리별 결과는 `0--1000 m 전체 sweep`임을 명확히 했다.
- 0 m 조건은 near-vertical degenerate case라서 장거리 성능 주장 근거로 쓰지 않는다고 명시했다.
- 800 m 결과는 cherry-picked 성공 사례가 아니라 plain hopping의 tail failure와 transition-aware soft-R 회복을 동시에 보여주는 대표 failure-and-recovery 사례라고 경계 문장을 넣었다.
- 기존 부정 결과(63, 64, 66, 67)와 충돌하지 않도록, 이번 성과를 “carrier transition이 관측 신뢰도 변화를 만들 때 필터가 그 변화를 흡수하는 설계”로 제한했다.

## 빌드 확인

- `paper/manuscript.tex` → `paper/manuscript.pdf`, 13 pages
- `paper/manuscript_ko.tex` → `paper/manuscript_ko.pdf`, 13 pages
- 치명적 LaTeX 오류 없음
- 남은 warning은 기존 수준의 underfull/hyperref/rerunfilecheck 계열이며 본 작업의 수치·참조 깨짐은 확인되지 않았다.

## 판단

191번 결과는 좋은 쪽으로 강하지만, 논문에서 가장 위험한 지점은 “이동 표적에서도 주파수 도약만으로 성공했다”처럼 과장되어 읽히는 것이다. 그래서 이번 198번은 강한 수치를 약하게 만드는 작업이 아니라, 리뷰어가 공격할 수 있는 claim boundary를 먼저 닫는 안정화 작업이다.
