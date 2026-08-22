# 231. Korean hyperref bookmark warning cleanup

## 목적

한글 원고 `paper/manuscript_ko.tex` 빌드에서 발생하던 hyperref bookmark warning을 제거했다.

이 작업은 행정 정보나 논문 claim을 바꾸지 않는 조판 안정화 작업이다.

## 원인

한글 원고의 subsection 제목에 `Adaptive-$R$`처럼 수식 모드가 들어가 있었다. LaTeX 본문 제목에서는 정상적으로 보이지만, `hyperref`가 PDF bookmark 문자열을 만들 때 `$...$` 수식 토큰을 사용할 수 없어 다음 경고가 발생했다.

```text
Package hyperref Warning: Token not allowed in a PDF string (Unicode):
(hyperref) removing `math shift'
```

## 보완 내용

본문 제목은 유지하고, PDF bookmark용 optional title만 추가했다.

```tex
\subsection[Transition-aware Adaptive-R 이동 표적 검증]{Transition-aware Adaptive-$R$ 이동 표적 검증}
```

즉 PDF 본문에서는 기존처럼 `Adaptive-R`의 수식 표기가 유지되고, PDF bookmark에는 수식 토큰 없는 문자열이 들어간다.

## 빌드 확인

- `paper/manuscript_ko.pdf`: 16 pages, 3627201 bytes
- hyperref warning 없음
- fatal LaTeX error 없음
- undefined citation/reference 없음
- overfull hbox 없음

남은 underfull hbox는 한글/영문 혼합 표와 문단 줄맞춤에서 생기는 비치명 조판 경고이며, 최종 제출 직전 layout cleanup 대상으로 남긴다.

## Git 규약

실제 수정 대상인 `paper/manuscript_ko.tex`는 로컬 전용 원고 파일이므로 GitHub에 올리지 않는다.  
이번 커밋에는 231번 기록 폴더만 포함한다.

