# 131. 참고문헌 보강 (4→10편)

## 목적

130번 시각 QA에서 "참고문헌이 [1]~[4] 4편뿐이라 SCI 기준 얇다"를 발견. 원고가 실제로 쓰는 표준
방법(GCC-PHAT, SRP-PHAT, UKF, Thorp 흡수)이 무인용 상태였고, 선행연구 대조에서 확보한 인용
후보도 미반영이었다. **정확 서지를 Crossref로 검증한 뒤에만** `paper/refs.bib`·`paper/manuscript.tex`에
edit in place로 추가했다(지어내지 않음). 원고 실체는 로컬 `paper/` 전용, 이 폴더는 근거 기록.

## 추가한 참고문헌 6편 (전부 Crossref 검증 2026-07-13)

방법(원고가 쓰는데 무인용이던 것):
- **Knapp & Carter 1976**, GCC 시간지연추정 — IEEE TASSP 24(4):320–327, doi:10.1109/TASSP.1976.1162830
  → GCC-PHAT 첫 언급(§Implementation)에 인용.
- **Do & Silverman 2010**, SRP-PHAT — ICASSP 2010:125–128, doi:10.1109/ICASSP.2010.5496133
  → SRP-PHAT 첫 언급에 인용.
- **Julier & Uhlmann 2004**, Unscented Filtering — Proc. IEEE 92(3):401–422, doi:10.1109/JPROC.2003.823141
  → 서론 "UKF-based tracker" 첫 언급에 인용.
- **Thorp 1967**, 저주파 감쇠계수 — JASA 42(1):270, doi:10.1121/1.1910566
  → 채널모델 "Thorp absorption"에 인용.

선행연구(선행연구 대조서 확보):
- **Blunt & Mokole 2016**, radar waveform diversity 리뷰 — IEEE AES Mag 31(11):2–42,
  doi:10.1109/MAES.2016.160071 → 서론 radar frequency-agility 유산 문장에 Loomis와 병기.
- **Zhang, Yan, Han 2024**, differential USBL 보정 — Ocean Engineering 305:117984,
  doi:10.1016/j.oceaneng.2024.117984 → Related Work Table I "USBL calibration" 행에 인용.

## 검증 (2026-07-13)

- `cd paper && latexmk manuscript.tex` → **참고문헌 4→10편**(`.bbl` bibitem 10개), **미해결 인용/참조
  0**, 9쪽 유지, overfull 0.
- 마지막 9쪽 렌더 육안 확인: References [1]~[10] IEEEtran 스타일 정상, 페이지 충실도 개선.

## 판정

**참고문헌 보강 완료(4→10, 전부 검증).** 방법 인용 공백(GCC/SRP/UKF/Thorp) 해소 + Related Work
차별화 근거(Blunt·Zhang) 추가. 지어낸 서지 없음.

주의: 여전히 SCI 최종본 기준으론 더 늘릴 수 있다(예: USBL 표준 문헌, CRLB 원전, image-source 채널
문헌). 다만 무리한 인용은 저자 검토 몫이라, 여기서는 **원고가 실제 쓰는 방법 + 이미 본문대조한
선행연구**만 넣었다. 추가 인용은 저자/지도교수 curation 권장.

## 다음 (판단)

참고문헌·조판·claim·선행연구까지 정리됨 → 남은 실질 AI작업은 축소. 후속 후보: (a) CRLB/image-source
등 방법 원전 1~2편 추가 검증, (b) 원고 전체 정합 최종 점검, (c) 그 외는 사람 결정(저자·Funding·저널).
