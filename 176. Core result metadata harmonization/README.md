# 176. Core result metadata harmonization

## 목적

피드백의 “모든 결과에 trajectory seed, channel seed, noise seed, 환경 파라미터 및 코드 버전을 저장한다” 요구를 기존 핵심 결과에 대해 보완한다.

기존 실험 결과 파일을 직접 다시 쓰지 않고, 채택 결과를 읽어 표준 provenance manifest를 새로 만든다. 따라서 기존 수치와 claim은 바뀌지 않는다.

## 대상 결과

- 61. 정지표적 도약 대규모 독립검증
- 63. 이동표적 도약 대규모검증 백색화 확인
- 82. 준정지 속도 경계 검증 실행
- 160. Four carrier independent static validation
- 162. Carrier transition TOA guard pilot

## 산출물

- `build_metadata_manifest.py`: 핵심 결과 JSON과 코드 상수를 읽어 표준 metadata manifest 생성
- `core_result_metadata_manifest.json`: 표준화된 결과 provenance
- `metadata_gap_table.md`: 어떤 결과가 어떤 metadata를 갖고 있고 무엇이 부족한지 표로 정리

## 판정

이번 작업은 성능 실험이 아니다. 결과 수치 변경, threshold retuning, claim 확장을 하지 않는다.

핵심 결론은 그대로 유지한다.

- static 600 m: fixed 대비 canonical linear20 carrier agility의 RMSE 개선은 재현됨.
- moving target: residual lag-1 whitening은 확인됐지만 pooled RMSE 개선은 재현되지 않음.
- quasi-static: continuous safe boundary는 0.005 m/s까지만.
- four-carrier sparse schedule: 독립검증 실패.
- TOA transition guard: post-hoc pilot이며 독립검증 전 claim 금지.

