# Collection steps

## 실제 ZIP 생성 전 확인

1. 목표 저널의 supplementary file 규정 확인.
2. data/code availability 정책 확정.
3. 저자/교수님에게 공개 가능한 파일 범위 확인.
4. `paper/` 포함 여부를 명시적으로 결정. 기본값은 포함하지 않음.

## 수집 절차

PowerShell 기준:

```powershell
cd "C:\Users\HOSEO\OneDrive - 호서대학교\나는 개인이요\석사생\논문\Adaptive UKF 위치추정"
```

1. 새 임시 폴더 생성.
2. `archive_layout.md` 구조대로 하위 폴더 생성.
3. 핵심 결과 JSON/CSV만 `data/`에 복사.
4. 핵심 실험 폴더의 `.py`, `README.md`, `test_diagnostic.py`만 `code/`에 복사.
5. `__pycache__`, `_stdout.txt`, `_err.txt`, partial cache는 제외.
6. figure PNG/SVG와 generation scripts 복사.
7. SHA256 재계산 후 `archive_manifest.md`와 비교.
8. ZIP 생성.

## 제외 규칙

절대 `git add .` 또는 전체 폴더 통째 복사를 하지 않는다.

제외:

- `paper/`
- `.git/`
- `.claude/`
- `study_exports/`
- root operation MD
- professor report
- `__pycache__/`
- 대규모 intermediate cache
- unrelated exploratory folders

## 검증 체크리스트

- [ ] static 600 m result JSON 포함.
- [ ] moving whitening result JSON 포함.
- [ ] quasi-static summary JSON + trial CSV 포함.
- [ ] CRLB/floor JSON 포함.
- [ ] method facts JSON 포함.
- [ ] figure scripts 포함.
- [ ] 핵심 runners와 공통 pipeline `.py` 포함.
- [ ] README에 “simulation-based” 한계 명시.
- [ ] moving RMSE improvement claim 없음.
- [ ] 0.1 m/s continuous validation claim 없음.

## GitHub 규칙

이 120번 폴더는 manifest/dry-run 문서이므로 GitHub에 올릴 수 있다. 실제 supplement ZIP이나 raw result
data는 사용자 지시 전까지 GitHub에 올리지 않는다.
