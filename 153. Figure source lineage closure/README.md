# 153. Figure source lineage closure

## 목적

로컬 원고의 7개 PNG가 번호 폴더의 원본·생성 스크립트·결과 데이터와 연결되는지 기계 검사한다.
147번은 two-ray PNG 생성 경로를 미해결로 기록했지만, 실제로는 138번
`generate_tworay_fit_figure.py`가 존재한다. 153번은 이 누락을 바로잡고 현재 PNG를 임시 경로에
재생성해 픽셀 단위로 비교한다.

## 실행

```powershell
python "153. Figure source lineage closure\audit_figure_lineage.py"
```

의도적으로 기준 보고서를 갱신할 때만:

```powershell
python "153. Figure source lineage closure\audit_figure_lineage.py" --write
```

## 판정 기준

- 7개 paper PNG와 reference PNG의 크기·SHA256 비교.
- PNG metadata 차이가 있더라도 RGBA 픽셀을 직접 비교.
- generator와 수치 source의 존재 및 SHA256 기록.
- two-ray PNG는 138번 생성기를 `153/fig_tworay_fit_reproduced.png`로 재지정해 원고 파일을
  덮어쓰지 않고 재현한다.

## 정정

145번은 two-ray JSON/SVG와 수치 claim을 닫았고, 138번은 원고 PNG 생성기를 이미 제공한다.
따라서 “PNG production path가 없다”는 이전 기록은 **검색 누락에 따른 문서상 gap**이었으며,
과학적·코드 재현성 gap은 아니었다.

## 결과

- 7/7 paper PNG가 reference PNG와 byte-identical.
- 7/7 paper PNG가 RGBA pixel-identical.
- 7/7 generator 존재 확인.
- 모든 연결 data JSON/CSV 존재 및 SHA256 기록.
- two-ray 재생성 PNG SHA256:
  `DE3D71050CA6BF86024604F3F1DC66D259E65B9D6257158076D6D8CE7E4E7C8C`.
- 로컬 `paper/` 파일은 덮어쓰거나 GitHub에 올리지 않음.
