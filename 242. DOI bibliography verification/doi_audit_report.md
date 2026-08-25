# DOI / 선행문헌 서지 감사 보고

## 1. 현재 상태

`paper/refs.bib`의 현재 상태는 다음과 같다.

| 항목 | 결과 |
| --- | --- |
| BibTeX entry 수 | 22 |
| DOI 필드가 있는 entry | 22 |
| DOI 필드가 없는 entry | 0 |
| 이번에 보정한 서지 | `Zhang2019USBLCalib` pages `254--265` → `254--262` |

따라서 “22편 중 DOI가 0편”이라는 지적은 현재 파일 기준으로는 사실이 아니다. 다만 이전 버전 또는 잘못된 awk/regex 감사에서 그렇게 보였을 가능성이 있으므로, 이번 폴더에 재발 방지용 감사 스크립트를 남겼다.

## 2. 고위험 문헌 대조

| BibTeX key | 현재 DOI | 대조 판정 | 원고에서 안전한 사용 범위 |
| --- | --- | --- | --- |
| `Beaujean2007FrequencyHoppedUSBL` | `10.1121/1.2400616` | 확인 | frequency-hopped acoustic modem sequence를 이용한 3D USBL positioning 선행연구. “frequency-hopped USBL 계열은 기존에 존재한다”는 방어 근거로 적합하다. |
| `Nhat2022CostasUSBL` | `10.1109/IMCOM53663.2022.9721736` | 확인 | Costas hopping을 USBL baseline/navigation precision 개선에 사용한 선행연구. “Costas/hopped USBL shallow-water design”으로 부르는 것은 안전하다. |
| `Qian2025FrequencyCombIUSBL` | `10.1109/JIOT.2025.3564346` | 확인 | acoustic frequency comb 기반 iUSBL integrated waveform 선행연구. frequency hopping USBL이라고 부르면 안 되고, 현재처럼 “frequency-comb / iUSBL”로만 써야 한다. |
| `Zhang2024DifferentialUSBL` | `10.1016/j.oceaneng.2024.117984` | 확인 | USBL positioning result correction / calibration 계열. 본 논문의 residual decorrelation과 직접 동일하지 않다. |
| `Zhang2019USBLCalib` | `10.1504/IJSNET.2019.101243` | 확인 | USBL installation-error online calibration. page range는 `254--262`로 보정했다. |
| `Tong2019USBLError` | `10.3390/s19204373` | 확인 | USBL positioning model / rotating array / error analysis. USBL error-analysis 배경으로 적합하다. |
| `Li2019UnderwaterSRUKF` | `10.3390/e21080740` | 확인 | underwater bearing-only / bearing-Doppler target tracking with SRUKF. USBL TOA/TDOA/DOA fusion 자체는 아니므로 “underwater UKF tracking prior art” 범위로만 사용한다. |
| `RaviKumar2021HybridUKF` | `10.1016/j.ijleo.2020.165813` | 확인 | passive sonar measurement 기반 underwater target tracking. USBL 측위 논문처럼 쓰지 않는다. |
| `AlAboosi2016Multipath` | `10.11591/ijeecs.v2.i2.pp351-358` | 확인 | shallow-water underwater acoustic multipath delay profile 실험. 위치추정 알고리즘 선행연구가 아니라 채널/멀티패스 배경 문헌으로만 사용한다. |

## 3. Related Work 표 점검

현재 `paper/manuscript.tex`의 Related Work 표는 다음 경계를 지키고 있다.

- Beaujean: “Frequency-hopped acoustic modem USBL” → 적합
- Nhat: “Costas / hopped USBL shallow-water designs” → 적합
- Qian: “Acoustic frequency-comb / iUSBL approaches” → 적합
- Zhang 2024: “USBL calibration / installation-error correction” → 적합

즉 현재 원고는 frequency agility/frequency diversity 자체를 최초 발명으로 주장하지 않고, 얕은 수중 USBL에서 post-gating DOA residual decorrelation과 UKF 적용 경계를 기여로 좁히고 있다. 이 방향은 서지 감사 결과와 충돌하지 않는다.

## 4. 앞으로의 주의점

참고문헌 확충은 별도 작업으로 남긴다. 이번 작업은 “현재 22편의 DOI/서지 정확성 감사”이며, IEEE JOE급 원고를 위해 35--50편 수준으로 늘리는 문헌 확충은 아직 하지 않았다.

특히 다음 계열은 교수님 또는 도서관 접근으로 원문을 확인한 뒤 확충하는 편이 안전하다.

- shallow-water multipath mitigation
- USBL tracking / integrated navigation filtering
- hardware transducer frequency response and frequency-agile acoustic positioning
- sea-trial USBL error analysis

## 5. 웹 대조 근거

이번 감사에서 직접 대조한 공개 웹 근거는 다음과 같다.

| 문헌 | 근거 URL | 확인 내용 |
| --- | --- | --- |
| Beaujean et al. 2007 | https://pubmed.ncbi.nlm.nih.gov/17297770/ | JASA 121(1), 144--157, DOI, frequency-hopped acoustic modem source를 이용한 tetrahedral USBL positioning |
| Nhat et al. 2022 | https://ouci.dntb.gov.ua/en/works/4r1M8pY7/ | IMCOM 2022, pages 1--6, DOI, Costas hopping / USBL / shallow-water navigation precision |
| Qian et al. 2025 | https://eurekamag.com/research/100/102/100102346.php | IEEE Internet of Things Journal 12(14), 27628--27637, DOI, integrated acoustic frequency-comb signal for iUSBL |
| Zhang et al. 2024 | https://www.sciencedirect.com/science/article/pii/S0029801824013222 | Ocean Engineering 305, article 117984, DOI, USBL correction/calibration 계열 |
| Zhang et al. 2019 | https://www.inderscience.com/info/inarticle.php?artid=101243 | International Journal of Sensor Networks 30(4), 254--262, DOI, USBL installation-error online calibration |
| Tong et al. 2019 | https://www.mdpi.com/1424-8220/19/20/4373 | Sensors 19(20), 4373, DOI, USBL positioning model/error analysis |
| Li et al. 2019 | https://pubmed.ncbi.nlm.nih.gov/33267454/ | Entropy 21(8), 740, DOI, underwater bearing-only/bearing-Doppler SRUKF tracking |
| Ravi Kumar 2021 | https://www.sciencedirect.com/science/article/pii/S0030402620316363 | Optik 226, article 165813, DOI, passive-sonar-measurement underwater target tracking |
| Al-Aboosi and Sha'ameri 2016 | https://ijeecs.iaescore.com/index.php/IJEECS/article/view/407/0 | IJEECS 2(2), 351--358, DOI, shallow-water underwater acoustic multipath delay profile |
