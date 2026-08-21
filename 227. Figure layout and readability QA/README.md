# 227. Figure layout and readability QA

## 목적

226번에서 논문 그림을 PDF/vector-first로 재생성한 뒤, 실제 IEEE two-column 원고에서 그림 배치와 가독성을 점검했다.

## 핵심 판단

- Fig.1은 두 패널을 포함하는 mechanism overview라 single-column 배치에서는 정보량이 과하다.
- Fig.1을 `figure*`로 바꿔 두 컬럼 폭에서 보여주는 것이 더 논문답고 읽기 쉽다.
- Fig.2--Fig.7과 Fig.5/Fig.6/two-ray plot은 수치 플롯이므로 single-column 유지가 적절하다.
- Fig.8은 PDF로 생성되어 있으나 현재 본문에는 직접 포함하지 않는다. 필요하면 supplementary figure 또는 Fig.7 보조그림 후보로 남긴다.

## 로컬 원고 변경

`paper/manuscript.tex`에서 Fig.1만 다음처럼 로컬 수정했다.

```tex
\begin{figure*}[!t]
\centering
\includegraphics[width=0.92\textwidth]{fig1_system_concept}
...
\end{figure*}
```

`paper/`는 로컬 전용이므로 이 변경은 커밋하지 않는다.

## 빌드 QA

영문 원고를 `pdflatex` 2회로 빌드했다.

- `paper/manuscript.pdf`
- 15 pages
- Fig.1은 `figures/fig1_system_concept.pdf`로 삽입됨
- fatal LaTeX error 없음
- undefined reference/citation 없음
- overfull hbox 없음
- 남은 경고는 `Underfull \vbox`뿐

## 경고 해석

사용자 환경의 LaTeX Workshop/Antigravity Problems 창에 뜨는 다수의 문제는 현재 로그 기준으로 치명적 오류가 아니다.

특히 다음은 검토 단계에서 무시 가능하다.

- `Underfull \hbox`
- `Underfull \vbox`
- 한글 독해본의 hyperref bookmark 수식 경고

반대로 아래가 보이면 즉시 확인해야 한다.

- `! LaTeX Error`
- `Undefined control sequence`
- `Citation ... undefined`
- `Reference ... undefined`
- `Overfull \hbox`가 큰 값으로 반복되는 경우

## 남은 선택지

Fig.1을 두 컬럼으로 키우면 가독성은 좋아지지만 영문 원고가 14쪽에서 15쪽으로 늘어난다.

현재 단계에서는 가독성을 우선해 이 변경을 유지하는 것이 낫다. 최종 저널/template 및 page budget이 정해지면 Fig.1을 다시 single-column simplified schematic으로 줄이는 선택지도 가능하다.
