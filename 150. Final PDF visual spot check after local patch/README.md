# 150. Final PDF visual spot check after local patch

## 목적

148번 local-only Data Availability patch 이후 생성된 `paper/manuscript.pdf`를 페이지 이미지로 렌더링해 육안 QA했다.

이미지 렌더는 임시 QA용이며 GitHub에 올리지 않는다. 이 폴더에는 결과 기록만 남긴다.

## 렌더링

명령:

```powershell
pdftoppm -png -r 120 "paper\manuscript.pdf" "<visualization_dir>\page"
```

결과:

- 12 pages rendered.
- contact sheet generated locally for QA.
- rendered images stored under `.codex/visualizations/.../pdf_qa_140/` only.

## 판정

전체적으로 출판 draft로 볼 수 있는 상태다.

- 12쪽 모두 내용이 충분히 채워짐.
- 마지막 페이지가 거의 빈 페이지처럼 보이지 않음.
- two-ray figure page는 잘림 없이 읽힘.
- Data Availability patch가 page 11에 자연스럽게 들어감.
- References가 page 12에서 정상적으로 이어짐.
- 심각한 float collision이나 표 잘림은 보이지 않음.

## 주의점

- `fig_tworay_fit.png`는 manuscript figure number상 Fig. 3으로 표시된다. 파일명 번호와 논문 figure 번호가 일치하지 않으므로 supplement/manifest에서는 label 기준으로 관리해야 한다.
- Data Availability의 `two_ray_fit.json` typewriter text는 좁은 column에서 약간 눈에 띄지만 정상적으로 읽힌다.
- Underfull vbox 1개는 육안상 큰 문제를 만들지 않는 것으로 보인다.

## 다음 후보

이제 AI가 계속할 수 있는 다음 작업은 `151. BibTeX and reference formatting audit`이다. 현재 원고가 문헌 novelty 방어에 기대고 있으므로, refs.bib의 필수 항목/저널명/연도/페이지/DOI 누락을 점검하는 것이 유용하다.
