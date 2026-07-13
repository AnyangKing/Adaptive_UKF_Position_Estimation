# 120. Supplement archive dry run

## 목적

115번에서 재현성 매핑을 끝냈고, 118~119번에서 실험/스케줄 후속 계획을 정리했다. 120번은 실제 투고용
보충자료 ZIP을 만들기 전, **무엇을 포함해야 하는지**와 **현재 로컬 파일이 어떤 해시를 갖는지**를
기록한 dry run이다.

중요: 이 폴더에는 결과 JSON/CSV 원본을 복사하지 않는다. 결과 데이터는 로컬 `results/` 전용이고,
GitHub에는 올리지 않는다.

## 결론

보충자료 패키지는 다음 4묶음이면 충분하다.

1. 핵심 결과 데이터: 58, 61, 63, 82, 45, 93의 JSON/CSV.
2. 재실행 코드: 각 핵심 폴더의 runner와 공통 pipeline 파일.
3. 그림 생성 코드: 70, 95, 101.
4. 문서: README, reproduction guide, data/code availability statement.

## 산출물

- `archive_manifest.md`: 포함 후보 파일과 SHA256.
- `archive_layout.md`: 투고용 ZIP 폴더 구조.
- `collection_steps.md`: 실제 ZIP을 만들 때의 절차와 금지사항.

## 다음

이제 교수님 없이 할 수 있는 큰 마감 작업은 상당히 정리됐다. 다음 후보는 121번
`Submission readiness dashboard`로, 115~120번 결과를 한 장짜리 상태판으로 묶는 것이다.
