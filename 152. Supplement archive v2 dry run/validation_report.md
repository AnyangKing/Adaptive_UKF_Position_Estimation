# Validation report

## 결과

- manifest schema: `supplement-v2-dry-run-1`
- 후보 산출물: **90개**
- 총 크기: **2,330,009 bytes**
- manifest SHA256: `6D9FFEF87C0EFEB033F9D18E1A341ACDE41DC3BAFF41922FE11E466883304777`
- 존재하지 않는 source: **0개**
- 중복 archive path: **0개**
- manifest drift: **없음**

## 범주별 회계

| 범주 | 파일 수 |
|---|---:|
| code | 65 |
| data | 8 |
| document | 5 |
| figure | 8 |
| figure_script | 4 |
| 합계 | 90 |

## 실행 검증

```text
python validate_supplement_v2.py --write
wrote supplement_v2_manifest.json: 90 artifacts, 2330009 bytes

python validate_supplement_v2.py
ok: 90 artifacts, 2330009 bytes, no drift

python test_validator.py
ok
```

## 안전성 판정

- 실제 ZIP 생성 없음.
- 원본 파일 복사 없음.
- 원고 TEX/PDF와 LaTeX 부산물 포함 없음.
- `paper/`에서는 7개 PNG만 source 후보로 허용.
- 루트 인계·공부·교수 보고 파일 포함 없음.
- GitHub에는 152번의 manifest·스크립트·문서만 커밋한다.
