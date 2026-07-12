# 108. LaTeX IEEEtran 원고 이관

## 목적 (사용자 지시 2026-07-12)

프로젝트의 모든 산출물을 **LaTeX**로 하고, 양식은 **기본 IEEE 논문지 양식(IEEEtran)**을 쓴다.
Word/DOCX는 폐기. 최신 원고(105 tightened MD)를 IEEEtran `.tex`로 이관하고, 이 환경에서 실제
컴파일해 PDF까지 확인한다. 100~107의 DOCX/Word 마감 라인은 이 지시로 대체됨.

## 위치 규칙 (사용자 지시)

LaTeX 실체는 **프로젝트 루트**(운영 MD 파일들과 같은 위치)에 둔다. numbered 폴더마다 복사하지
않는다. 폴더가 진행돼도 `.tex`는 루트에 그대로 두고 **거기서 직접 수정(edit in place)**한다.
이 폴더(108)는 "이관을 했다"는 변경 기록만 담고, 원고 실체는 담지 않는다.

- 원고 실체(루트, git 커밋): `manuscript.tex`, `refs.bib`, `figures/`(Fig.1~6 PNG)
- 규약 명시 위치(루트, 로컬 전용): `새_채팅_인계.md`·`연구_인계_현황.md`·`논문_초고_구조.md` 최상단

## 이관 내용

- 소스: `105/manuscript_sensors_candidate_tightened.md`(내용) + `96/bibtex_entries.md`(서지).
  **내용·수치·claim 경계는 불변, 형식만 LaTeX로 이관.**
- 변환: Markdown heading→`\section`/`\subsection`; fenced math→`equation`/`align`(번호부여);
  인라인 백틱 수식→`$...$`; MD 표 3종→`table*`+`tabularx`(전폭, `\footnotesize`);
  Figure Captions→`figure`+`\includegraphics`(6종); References→`\bibliography{refs}`+IEEEtran.bst.
- 문서클래스: `\documentclass[journal]{IEEEtran}`. 패키지: amsmath, graphicx, booktabs, tabularx,
  hyperref.
- 그림: Fig.1은 101 폴리시본, Fig.2~6은 95 패키지 PNG를 루트 `figures/`로 취합.

## 컴파일 검증 (이 환경 = MiKTeX)

- 절차: `pdflatex` → `bibtex` → `pdflatex` ×2 (MiKTeX AutoInstall=1 설정 후).
- 결과: **manuscript.pdf 8쪽 정상 생성. 미해결 인용/참조 0건**(참고문헌 5편 IEEEtran 스타일로 연결).
- Overfull hbox 27건은 전부 §2.1 구현 파라미터 문단의 긴 인라인 수식에서 7~13pt 소량(여백 미세
  넘침, 기능 문제 없음) — 다음 편집에서 미세조정 대상. 표(table*)는 전폭에 정상 배치.
- 빌드 아티팩트(.aux/.log/.pdf/.bbl 등)는 `.gitignore`에 추가해 커밋 제외(소스만 버전관리).

## 판정

**이관 완료·컴파일 검증 통과.** Word 경로(107 DOCX, soffice 부재로 렌더 QA 불가)와 달리 LaTeX는
이 환경에서 직접 빌드·PDF 확인이 되므로 완결성이 높다. 앞으로 원고 수정은 루트 `manuscript.tex`
에서 직접 한다.

## 다음 (마감 잔여)

1. Overfull 미세조정(§2.1 인라인 수식 줄바꿈 허용) — 미관.
2. 저자/소속·Author Contributions·Funding·Data Availability 등 human-author 필드(투고 전 사용자 확정).
3. IEEE 그림 캡션·표 스타일 최종 점검, SVG→고해상 PDF 그림 교체(선택).
4. 저널 선택 후 해당 저널 IEEEtran 옵션/길이 맞춤.

주의: `results/`는 프로젝트 초기 `.gitignore`로 GitHub 제외(코드+README+원고소스만 올라감).
실험 결과 JSON/CSV는 로컬 전용 — 기존 관례 유지.
