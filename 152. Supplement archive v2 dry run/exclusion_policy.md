# Exclusion policy

## 자동 차단

검증 스크립트는 다음 경로 또는 확장자를 source manifest에 넣지 못하게 한다.

- `.git`, `.claude`, `study_exports`, `__pycache__`
- `.aux`, `.bbl`, `.blg`, `.fdb_latexmk`, `.fls`, `.log`, `.out`
- `.pdf`, `.tex`
- `paper/` 아래에서 `paper/figures/`가 아닌 파일

## 수동 결정이 필요한 항목

- 실제 공개 저장소와 DOI.
- 데이터/코드 완전 공개 또는 요청 시 제공 정책.
- 저널별 supplementary ZIP 크기 및 파일 형식 제한.
- lake/sea validation 추가 후 결과 포함 범위.

## GitHub 규칙

152번에는 manifest, 검증 스크립트와 문서만 올린다. 실제 보충자료 ZIP, 로컬 `paper/`, 원본 복사본은
사용자 지시 전까지 GitHub에 올리지 않는다. 스테이징은 반드시 152번 폴더 경로만 지정한다.
