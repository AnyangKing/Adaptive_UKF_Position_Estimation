# 209. Supplement source data manifest OOD refresh

## 목적

204번 OOD 결과가 원고의 표와 결론에 들어갔으므로, supplement/source-data manifest에서 어떤 파일이 어떤 claim을 받치는지 추적 가능하게 정리했다.

## 원고 반영

`paper/manuscript.tex`의 `Supplementary Material and Data Availability` 절에 다음 내용을 추가했다.

- 191 structured moving aggregate table은 191 validation summary에서 재현.
- 204 OOD aggregate table은 204 compact metrics와 paired validation summary에서 재현.
- Table `oodmoving`의 mean/P90/divergence 값이 204 결과 파일과 연결됨.

## GitHub 규약

원고 파일은 local-only다. 이 폴더만 커밋한다.
