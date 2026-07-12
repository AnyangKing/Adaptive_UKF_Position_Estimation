# 110. LaTeX 빌드 재현과 투고 체크리스트

## 목적

(1) 루트 LaTeX 원고를 누구나 한 명령으로 재빌드할 수 있게 `latexmkrc`를 두고 재현성을 검증한다.
(2) DOCX 시절 체크리스트(99·103)를 대체하는 **LaTeX/IEEEtran 경로 투고 준비 체크리스트**를 만든다.
원고 실체(`manuscript.tex` 등)는 규칙대로 루트에 있고 여기서 수정하지 않는다. 이 폴더는 기록·보조
문서만.

## 빌드 방법 (재현)

프로젝트 루트에서(이 환경: MiKTeX 설치됨):

```
latexmk manuscript.tex     # pdflatex + bibtex + 재실행까지 자동 → manuscript.pdf
latexmk -c                 # aux 정리(.aux/.log/.bbl 등)
latexmk -C                 # PDF 포함 전부 정리
```

- 루트 `latexmkrc`가 `$pdf_mode=1`, `$bibtex_use=2` 등을 설정 → 인자 없이도 PDF까지 생성.
- 최초 1회 MiKTeX 패키지 자동설치가 필요하면 `initexmf --set-config-value "[MPM]AutoInstall=1"`을
  먼저 실행(무프롬프트). 이 설정을 안 하면 첫 컴파일이 설치 프롬프트에서 멈출 수 있음(108에서 겪음).
- PDF 미리보기 이미지가 필요하면 MiKTeX 번들 `pdftoppm -png -r 90 manuscript.pdf page` 사용.

## 재현성 검증 (2026-07-13)

- `latexmk -C`로 완전 클린 후 `latexmk manuscript.tex` 단일 명령 → **PDF 1.70 MB 재생성,
  미해결 인용/참조 0건, Overfull 1건(3.3pt)**. 클린 상태에서 원커맨드 빌드 성립 확인.

## 판정

**빌드 재현성 확보.** 원고는 소스만 git에 있고(108의 `.gitignore`), 어느 환경이든 MiKTeX+`latexmk`
로 동일 PDF를 얻는다. Word 경로(107)가 soffice 부재로 렌더조차 막혔던 것과 대비된다.

## 투고 체크리스트는 `submission_checklist_latex.md` 참조

DOCX용 99·103 체크리스트를 대체. 상태: 조판·컴파일·서지 연결은 완료, human-author 필드와 저널
선택이 사용자 확정 대기.
