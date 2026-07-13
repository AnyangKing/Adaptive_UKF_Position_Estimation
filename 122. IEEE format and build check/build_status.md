# Build status

## 시도한 명령

```powershell
cd "C:\Users\HOSEO\OneDrive - 호서대학교\나는 개인이요\석사생\논문\Adaptive UKF 위치추정\paper"
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

## 결과

샌드박스 내부 실행은 실패했다.

원인:

```text
MiKTeX tried to create:
C:\Users\HOSEO\AppData\Roaming\MiKTeX\2.9
Access denied.
```

승인 권한 실행을 요청했지만 자동 검토에서 거부되어 최신 PDF 재빌드는 완료하지 못했다.

## 기존 빌드 로그

기존 `paper/manuscript.log` 기준:

- Output: `manuscript.pdf`
- Page count: 7 pages
- PDF size: 1,705,396 bytes
- Overfull: 1건, 3.29744 pt
- Underfull: 1건
- Warning: page 6 contains only floats
- Undefined citations/references: 기존 로그 기준 없음

## 중요한 주의

현재 `paper/manuscript.tex`의 수정 시각이 기존 PDF보다 늦다. 따라서 기존 PDF는 참고용이며, 최종 확인은
사용자 승인 후 재빌드해야 한다.

## 다음 재빌드 시 확인할 항목

- PDF page count.
- unresolved citations/references.
- overfull/underfull 증가 여부.
- float-only page warning 해소 여부.
- Fig.1~Fig.6 출력 위치.
- back matter placeholder가 의도한 것만 남아 있는지.
