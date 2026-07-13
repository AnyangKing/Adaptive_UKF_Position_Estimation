# Next step: 128. PDF visual QA pass

## Why

LaTeX 로그가 깨끗해도 PDF가 독자 눈에 자연스럽다는 뜻은 아니다. 다음 단계는 실제 페이지 단위 시각 QA다.

확인할 것:

1. 7쪽 전체에서 section 흐름이 자연스러운가.
2. Fig.1--Fig.6이 첫 언급 근처에 보이는가.
3. Table 1--3이 페이지 흐름을 과도하게 끊지 않는가.
4. 마지막 페이지가 bibliography/back matter 때문에 비정상적으로 비어 보이지 않는가.
5. IEEE heading 번호가 `I`--`VII`로 정상 생성되는가.

## Expected action

PDF page image를 생성하거나 PDF viewer로 열어 page-by-page로 확인한다.

문제가 있으면 다음은 figure/table 위치 조정이고, 문제가 없으면 교수님 보고용 “현재 논문 상태” 요약을
업데이트하면 된다.

