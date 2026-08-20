# 206. Manuscript OOD claim integration

## 목적

204번 OOD moving full validation 결과를 한글 기준 원고와 영어 IEEEtran 원고의 claim boundary에 반영했다.

## 원고 반영 위치

- `paper/manuscript_ko.tex`
  - 초록에 OOD 528 paired cases 요약 추가.
  - 이동 표적 검증 절에 204번 OOD 조건, 평균/P90/발산률, paired p-value 추가.
  - 결론에 structured motion 191과 OOD motion 204를 분리해 반영.
- `paper/manuscript.tex`
  - Abstract에 OOD robustness 결과 추가.
  - Moving-target validation 절에 204번 OOD 문단 추가.
  - Limitation table과 Conclusion에 OOD 결과와 남은 경계 반영.

## 핵심 claim boundary

- 191번: structured moving full-range simulation evidence.
- 204번: OOD moving simulation robustness evidence.
- 둘 다 실해역, arbitrary motion, hardware frequency response 일반화 증거는 아니다.
- plain carrier hopping 단독은 여전히 moving target solution으로 주장하지 않는다.

## GitHub 규약

`paper/` 원고 파일은 로컬 전용이다. 이 폴더만 커밋한다.
