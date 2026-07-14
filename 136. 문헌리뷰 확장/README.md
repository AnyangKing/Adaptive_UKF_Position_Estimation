# 136. 문헌 리뷰 확장 (참고문헌 10 → 21편)

## 목적 (사용자 지시)

원고 Related Work(§II)가 표 하나 + 프론트 문단 수준으로 얇았다. 문헌군별로 실제 문헌을 엮어
IEEE JOE 수준에 근접시킨다. **모든 참고문헌을 Crossref로 실재·정확 서지 검증한 뒤에만 추가**
(지어냄 0). `paper/`에 edit in place.

## 추가한 문헌 11편 (전부 Crossref 검증 2026-07-13)

**배열 신호처리 / DOA**
- Schmidt 1986 MUSIC — IEEE TAP 34(3):276–280, 10.1109/TAP.1986.1143830
- Paulraj, Roy, Kailath 1985 ESPRIT — Asilomar:83–89, 10.1109/ACSSC.1985.671426
- Krim & Viberg 1996 배열처리 리뷰 — IEEE SP Mag 13(4):67–94, 10.1109/79.526899
- DiBiase, Silverman, Brandstein 2001 SRP-PHAT — Microphone Arrays:157–180, 10.1007/978-3-662-04619-7_8

**수중 음향 측위 / USBL**
- Wang & Pang 2018 AUV INS+음향 항법 — OCEANS 2018, 10.1109/OCEANS.2018.8604773
- Thomson & Dosso 2013 AUV 측위 — OCEANS Bergen 2013, 10.1109/OCEANS-Bergen.2013.6608140
- Zhang et al. 2019 USBL 설치오차 온라인 캘리브 — IJSNet 30(4):254–265, 10.1504/IJSNET.2019.101243
- Tong et al. 2019 USBL 회전배열 오차분석 — Sensors 19(20):4373, 10.3390/s19204373

**수중 표적추적 (UKF)**
- Li et al. 2019 수중 bearing-only 제곱근 UKF — Entropy 21(8):740, 10.3390/e21080740
- Ravi Kumar 2021 하이브리드 UKF 수동소나 추적 — Optik 226:165813, 10.1016/j.ijleo.2020.165813

**얕은바다 멀티패스**
- Al-Aboosi & Sha'ameri 2016 shallow-water 멀티패스 지연프로파일 — IJEECS 2(2):351–358,
  10.11591/ijeecs.v2.i2.pp351-358

## Related Work 재구성

§II 앞부분에 문헌군 4개 문단 신설(각 문단 이탤릭 소제목):
1. Underwater acoustic positioning — LBL/SBL/USBL, compact aperture 한계, 수신·기하측 접근(캘리브·
   음속)이 주류였음 → 우리는 송신 파형측.
2. DOA estimation — MUSIC·ESPRIT·배열처리 리뷰·SRP-PHAT/GCC-PHAT → 우리는 새 추정기가 아니라
   송신신호로 잔차를 바꿈.
3. Shallow-water multipath & recursive tracking — 멀티패스 지배·UKF 표준 backbone → 오차는 추정기·
   필터 상류의 송신-멀티패스 상호작용에서 발생.
4. Frequency and waveform diversity(기존 문단, 소제목화) → 우리 차별점.

## 검증 (2026-07-13)

- `cd paper && latexmk manuscript.tex` → **참고문헌 21편(bibitem), 미해결 인용/참조 0, overfull 0,
  11쪽.** §II·참고문헌 페이지 렌더 확인(IEEE 스타일 [1]~[21] 정상).

## 판정

**문헌 리뷰 확장 완료(10→21, 전부 검증).** Related Work가 이제 USBL 측위·DOA·멀티패스·수중 추적·
캘리브·주파수다양성 문헌군을 실제로 engage. 지어낸 서지 0.

## 남은 것 (정직하게)

21편은 top-tier 기준으론 여전히 다소 얇다(이상적 30~40). 다만 무리하게 관련 낮은 문헌으로 수를
채우는 건 또 다른 과장이라, 온-토픽·검증본만 넣었다. 추가 여지: USBL/수중측위 세부, CRLB-for-
localization 원전 몇 편. **여전히 실해역 검증은 없음**(핵심 리스크, 사용자 나중에 실측 예정).
