# 223. Korean reading draft final alignment

## 목적

행정 결정(저널, 저자, 교신저자, funding 등)을 제외하고, 사용자가 직접 읽는 한글 독해본 `paper/manuscript_ko.tex`의 방향 문장이 현재 프로젝트 전략과 충돌하지 않는지 정리했다.

## 변경 요지

- 한글본의 실측 검증 관련 문장을 최신 방향으로 정렬했다.
- 현재 논문은 `controlled shallow-water channel simulation` 기반의 mechanism-and-boundary 논문으로 유지한다.
- 실제 해상/호수 검증은 이 논문의 필수 전제처럼 쓰지 않고, 후속 실험 및 별도 논문으로 분리하는 방향으로 표현했다.
- 새로운 수치, 새로운 실험 결과, 새로운 성능 claim은 추가하지 않았다.

## 검증

- `paper/manuscript_ko.tex`를 `pdflatex` 2회로 빌드했다.
- `paper/manuscript_ko.pdf` 생성 성공.
- 출력 페이지 수: 14쪽.
- 치명적 오류 없음.
- 기존 수준의 underfull/hyperref 경고만 확인했다.

## 커밋 규칙

이 폴더만 git에 올린다. `paper/` 원고 파일과 빌드 산출물은 로컬 전용으로 유지한다.
