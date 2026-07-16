# Claim traceability matrix

범위: 현재 local `paper/manuscript.tex`의 핵심 수치/claim. line number는 144번 감사 시점의 `rg -n` 결과 기준이다.

| 원고 claim / 수치 | 원고 위치 | 근거 폴더 | 정합도 | 감사 메모 |
|---|---:|---|---|---|
| 정지 600 m에서 fixed 32 kHz RMSE 13.01 m → 30--34 kHz agile 8.87 m, 평균 gain +4.14 m, p=0.0008, median 13.97→7.96 | lines 56, 752--754, 766--767, 850--851, 1016--1018 | `61. 정지표적 도약 대규모 독립검증` | 높음 | README 표에 `13.01`, `8.87`, `+4.137`, `p=0.0008`, `13.97→7.96`가 직접 기재됨. 원고 claim과 일치. |
| frequency-agile pinging은 moving target에서 residual whitening은 강하지만 pooled moving RMSE 개선은 유의하지 않음 | lines 783--785, 794--795, 853--856 | `63. 이동표적 도약 대규모검증 백색화 확인` | 높음 | README에 pooled RMSE gain `-0.103 m`, Wilcoxon `p=0.301`, lag-1 fixed `+0.470`, hop `-0.208`, whitening p=`5.56e-10` 기재. 원고가 RMSE 개선을 주장하지 않는 점이 안전함. |
| continuous quasi-static validated boundary는 0.005 m/s까지만 | lines 59, 148, 804--808, 820, 828, 861--873, 879--893 | `82. 준정지 속도 경계 검증 실행` | 높음 | README/result_summary에 132 paired trials, pooled p=`8.00e-05`, speed 0.005 m/s fixed 11.14 / hop 9.72 / p=0.0447, 0.010과 0.050 깨짐, continuous boundary 0.005 m/s 명시. |
| 장거리 600 m에서 CRLB-scale 11.80 m, routed UKF 12.29 m, NLS 13.38 m, residual systematic floor ≈3.45 m | lines 141, 473--475, 493, 524, 864--865 | `45. CRLB 이론하한 대비 효율` | 높음 | README 표에 600 m CRLB(emp) 11.80, NLS 13.38, routing 12.29, efficiency 0.92, bias floor 3.45 직접 기재. sub-meter long range 기대를 낮추는 핵심 근거. |
| EKF는 장거리에서 붕괴하고 UKF가 recursive backbone으로 적합; NLS는 snapshot baseline으로 좋지만 recursive tracking/backbone은 아님 | lines 373--381, 393--400 | `43. 추정기 비교 골격 EKF UKF NLS` | 높음 | README에 400/600 m EKF divergence 31%/25%, overall EKF RMSE 17.25, NLS overall 6.65, UKF divergence ≤6%, UKF NEES 341/NIS 30 기재. |
| conditional adaptive-R wrapper는 plain UKF 대비 일관성과 divergence를 개선; NEES 341→27, NIS 30→16; large-scale에서는 divergence 3%→0%, NEES 164→22 | lines 300--306, 411, 419, 440 | `44. 조건부 adaptive-R 라우팅 ablation`, `46. 대규모 몬테카를로 라우팅 이득 확정`, `93. Method 세부 코드 대조` | 높음 | 44번 README에 NEES/NIS 및 600 m routing 13.16→12.29, 전체 7.73→6.39. 46번 README에 전체 6.79→5.75, p=0.0006, divergence 3%→0%, NEES 164→22. 93번은 실제 adaptive-R 수식/구현 대조. |
| center frequency sweep 16--64 kHz에서 32 kHz가 현재 compact array의 near-optimal point이며 48/64 kHz는 grating/aliasing tail이 커짐 | lines 679--688, 948--970, 989 | `54. 송신 중심주파수와 계통편향` | 높음 | README 표에 16/24/32/48/64 kHz 결과, 32 kHz median el_bias 0.396°, median DOA 0.980°, 48/64 kHz P90 12.13°/17.22° 직접 기재. |
| 30--34 kHz hopping은 32 kHz near-optimal 주변의 narrow-band schedule이며, fixed-frequency 자체가 아니라 carrier-locked coherent bias를 white/decorrelate하는 목적 | lines 145, 568, 665, 679--688, 752--754 | `58. 반송파 미세도약 코히어런트 편향 진단`, `61. 정지표적 도약 대규모 독립검증`, `63. 이동표적 도약 대규모검증 백색화 확인`, `82. 준정지 속도 경계 검증 실행` | 중~높음 | 58번은 phase-sensitive bias(f) 메커니즘과 30--34 kHz 탐침을 제공. 61/63/82는 frozen schedule의 성능/whitening 검증. |
| sound-speed mismatch ±15 m/s는 중간 민감하지만 graceful, clock offset 0.5--1.0 ms는 영향이 작음 | lines 900--908, 997 | `48. 음속 시각동기 오차 강건성` | 높음 | README 표에 c_true 1485/1515에서 overall RMSE 7.20/7.40, 1470/1530에서 9.64/8.77, clock 0.5/1.0 ms에서 6.02/6.27 직접 기재. |
| Method/protocol: 8 sensors, 33 mm radius, upper/lower 79 mm spacing, fs 192 kHz, 5 ms direct gate, 20 ping/settled last 10, n=20/64/132, canonical 3-path, frozen 30--34 kHz schedule | lines 300--306 and Method/protocol sections; protocol claims scattered through results | `93. Method 세부 코드 대조` | 높음 | 93번 method_facts_table이 code/result JSON을 기준으로 Method 수치와 원고 patch P1--P4를 대조. 현재 원고는 93번 패치가 대체로 반영된 상태로 보임. |
| two-ray/surface-reflection mechanism fit: bias-versus-carrier curves with R² up to 0.99; 400 m R²=0.99, δ=1.34 ms; 600 m R²=0.75, δ=1.87 ms | lines 54, 141--145, 641, 654, 1014 | `58. 반송파 미세도약 코히어런트 편향 진단` + 현재 `paper/` figure/manuscript | **중간/보강 필요** | 58번은 cos-fit 함수와 carrier phase mechanism을 제공하지만 README의 median cos-fit R²는 0.38--0.44 수준이고, 원고의 최신 R²=0.99/0.75 및 δ=1.34/1.87 ms를 직접 산출한 numbered result 파일은 144번 검색에서 확인되지 않음. 다음 폴더에서 재현 산출물로 닫아야 함. |

## 감사 판정

현재 원고의 중심 성능 claim은 대체로 안전하다. 특히 논문을 위험하게 만드는 “moving RMSE도 개선된다” 같은 과잉 claim은 원고가 피하고 있다.

다만 two-ray fit 수치는 논문의 novelty/mechanism을 설명하는 예쁜 숫자라서, reviewer 대응을 위해 반드시 직접 재현 가능한 `results/*.json`과 figure generation script가 필요하다. 이 gap만 닫으면 원고의 claim traceability가 훨씬 단단해진다.
