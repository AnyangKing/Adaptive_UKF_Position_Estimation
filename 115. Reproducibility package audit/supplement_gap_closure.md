# Supplement gap closure

## 이미 준비된 것

| 항목 | 상태 |
|---|---|
| 핵심 실험 코드 | 58, 61, 63, 82, 45 폴더에 존재 |
| 핵심 결과 JSON/CSV | 로컬 `results/`에 존재 |
| 그림 PNG/SVG | 95번 figure package에 존재 |
| Method 상수 감사 | 93번 `results/method_facts.json` 존재 |
| LaTeX 원고 | 로컬 `paper/`에 존재, Git 제외 |
| 선행연구 대조 | 교수님 보고서·논문 구조 문서에 반영됨 |

## 투고 직전 닫아야 할 것

1. **공개 정책 결정**
   - 공개 GitHub + Zenodo/Figshare DOI
   - 저널 supplementary ZIP
   - 요청 시 제공

2. **결과 데이터 포함 방식**
   - 현재 `results/`는 GitHub에 없다.
   - 따라서 `static_hop_validation.json`, `moving_validation.json`, `quasi_static_boundary.json`,
     `quasi_static_trials.csv`, `agility.json`, `crlb.json`, `method_facts.json`을 별도 supplement로 묶어야 한다.

3. **논문 파일 취급**
   - `paper/`는 로컬 작업용이며 GitHub에 올리지 않는다.
   - 논문 파일을 공유해야 하면 GitHub push가 아니라 별도 ZIP/PDF 전달 또는 저널 제출 시스템을 사용한다.

4. **저널 확정 후 포맷**
   - 현재는 IEEE 공용 양식이다.
   - 목표 저널 확정 전에는 elsarticle, Sensors, Word template 등으로 고정하지 않는다.

## 절대 금지

- `git add .`
- `paper/` stage
- 루트 운영 MD, 교수님 보고서, study files stage
- 결과 `results/` 전체를 무차별 공개 패키지에 포함
- moving target RMSE improvement를 headline claim으로 작성
- 0.100 m/s quasi-static까지 연속 검증됐다고 작성

## 115번 이후 권장 순서

1. 116번: 원고 claim boundary audit
2. 117번: Related Work 표 최종화
3. 118번: real-water validation plan

이 순서가 좋은 이유는 재현성 근거가 이미 충분히 모였기 때문이다. 다음 위험은 “근거 부족”이 아니라
“문장이 근거보다 세게 나가는 것”이다.
