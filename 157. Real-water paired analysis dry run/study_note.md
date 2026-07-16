# 공부 노트: mock 분석은 소프트웨어 검증이지 연구 증거가 아니다

mock 데이터는 파이프라인의 부호, grouping, exclusion, endpoint 계산을 확인하는 데 유용하다. 하지만
mock 값이 성공 기준을 통과하더라도 그것은 실험 결과가 아니다.

안전한 분석기는 mock을 기본 거부하고, 명시적인 `--allow-mock` 옵션에서만 실행해야 한다. 출력에도
`is_research_evidence=false`와 경고 문장을 저장해 나중에 파일만 보더라도 실제 결과와 혼동되지 않게
해야 한다.

paired 분석에서는 gain의 부호를 사전에 고정하는 것도 중요하다. 본 프로젝트는
`fixed - hop`을 improvement로 정의하고, P90은 `hop - fixed`를 사용해 0 이하를 비악화로 판단한다.
