# 228. Figure label overlap remediation

## 목적

226번에서 PDF/vector-first 그림을 만든 뒤 확인된 그림 내부 글자 겹침과 과도한 legend/annotation 문제를 수정했다.

## 문제 진단

- Fig.1: schematic 내부 텍스트가 선, gate, beacon과 겹치고 하단 claim 문장이 잘림.
- Fig.2: legend와 `-35%` 라벨이 겹침.
- Fig.3: annotation box와 legend가 데이터 영역을 과하게 차지함.
- Fig.4: annotation box가 boxplot과 paired-line data를 덮음.
- Fig.5: check/cross marker가 과대하고 축/상단에 가까움.
- Fig.6: legend/annotation이 슬라이드처럼 큼.
- Fig.7: legend가 지나치게 크고 플롯 공간을 많이 차지함.
- Fig. two-ray: legend가 곡선/점 위를 크게 덮음.

## 수정 원칙

- 새 수치나 새 claim은 추가하지 않는다.
- 캡션으로 설명 가능한 긴 문장은 그림 내부에서 제거한다.
- legend는 가능하면 데이터가 적은 위치 또는 figure-level legend로 이동한다.
- annotation box는 데이터 영역을 가리지 않도록 축 밖/상단/여백 쪽으로 옮긴다.
- PDF/vector-first 산출은 유지하고, PNG는 600 dpi 확인용으로 함께 생성한다.

## 재현

```powershell
python ".\228. Figure label overlap remediation\make_overlap_safe_figures.py"
```

산출물은 `paper/figures`에 저장된다.

## 커밋 규칙

이 폴더만 git에 올린다. `paper/figures`와 `paper/manuscript*.tex`는 로컬 전용으로 유지한다.
