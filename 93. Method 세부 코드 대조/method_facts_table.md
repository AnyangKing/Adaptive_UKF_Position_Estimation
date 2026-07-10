# Method facts table — 원고 v2 ↔ 채택 코드 대조 (authoritative)

추출 스크립트: `extract_method_facts.py` → `results/method_facts.json` (2026-07-09).
근거 폴더: 61(정지 검증)·63(이동)·82(준정지) + 공통 파이프라인 파일. 세 검증 폴더 모두
**canonical 3경로 채널**(현실화 플래그 없음)과 **동일 동결 hop 스케줄**을 사용함을 확인.

## A. 신호/채널 (61/config.py)

| 항목 | 값 | 원고 v2 상태 |
|---|---|---|
| 음속 | 1500 m/s | 미기재 → 패치 P1 |
| 수심 / 수신기 깊이 | 100 m / 30 m | 미기재 → P1 |
| 표본화율 | 192 kHz | 미기재 → P1 |
| LFM 중심/대역/길이 | 32 kHz / 12 kHz / 10 ms (Tukey 창) | §5에 32kHz만 존재 → P1 |
| 채널 | 직접+해수면+해저 image-source, Thorp, Doppler, 유색잡음 | 개괄만 → P1 |
| guard time | 15 ms | 미기재(선택) |

## B. 배열 (61/config.py `usb_array_global_m`)

| 항목 | 값 | 원고 v2 상태 |
|---|---|---|
| 소자 수 | 8 (상단 4 z=0, 하단 4 z=−79 mm, 45° 엇갈림) | "eight-sensor"만 → P1 |
| 링 반경 | 33 mm (개구 지름 ~66 mm ≈ 1.4λ@32kHz) | 미기재 → P1 (compact 주장의 정량 근거) |

## C. 관측 추출 (61/peak_measurement.py·estimators.py)

| 항목 | 값 | 원고 v2 상태 |
|---|---|---|
| **직접파 게이트** | **5 ms** (+0.1 ms pre) | **수치 부재(전문 검색) → P3 (기전 §4의 핵심 상수)** |
| SRP 격자 | coarse 2° → fine 0.2° | 미기재(선택, P1에 포함) |
| TDOA | 28쌍 GCC-PHAT(대역 제한) → LS로 기준센서 7차분 | §2 서술과 정합(수치 보강 P1) |

## D. 필터 (61/ukf.py·measurement.py·run_static_hop.py)

| 항목 | 값 | 원고 v2 상태 |
|---|---|---|
| UKF 파라미터 | α=0.3, β=2, κ=0 | 미기재 → P1 |
| 초기 P | diag(8² m² ×3, 1.5² (m/s)² ×3) | 미기재 → P1 |
| 프로세스 잡음 | 가속도 std 0.20 m/s² (CV+가속 white), Δt=1 s | 미기재 → P1 |
| 고정 R | TOA-range 0.03 m, TDOA(센서) 0.025 m, DOA 2.0° | 미기재 → P1 |

## E. 조건부 adaptive-R — **불일치 1건 (핵심)**

| | 원고 v2 §2 수식 | 실제 코드 (61/conditional_adaptive.py) |
|---|---|---|
| 규칙 | 이진: g≤τ→R₀, g>τ→R_inflated | **2단계**: ① g=GCC-SRP 불일치, s=min(100, 1+(g/2)²); g≤τ(=5°)면 **DOA 블록**×s, g>τ면 **TDOA 블록**×s ② 블록별 NIS를 χ²₀.₀₁(dof 1/7/2 → 6.63/18.48/9.21)과 비교해 R_block×min(100, max(1, NIS/limit)) |
| 판정 | **§2 수식을 실제 규칙으로 교체 필요 → 패치 P2** | |

## F. 검증 프로토콜 (헤드라인 결과의 재현 정보)

| 실험 | 코드 사실 | 원고 v2 상태 |
|---|---|---|
| 61 정지 | 거리 {100,200,400,600} m × 20기하, 20 ping, 정착=후반 10, hop=linspace(30–34 kHz, 20), fixed=32 kHz, seed 계열 60번과 분리 | "independent 600 m trials"만 — **n=20, ping/정착창 미기재 → P4** |
| 63 이동 | 600 m, 4조건(radial 0.05/1.0, tangential 1.0, tang+vz0.08)×16=64, 20 ping 정착 10 | "n=64" 정합 ✓, 조건 구성 미기재 → P4 |
| 82 준정지 | 600 m, 속도 6×{radial,tangential}×12기하, **132 paired** (정지 12 + 5속도×2방향×12) | "132" 정합 ✓(보고서), 방향 pooling 미기재 → P4 |
| 공통 | 세 실험 모두 canonical 3경로 채널·동결 hop | 명시 안 됨 → P4 |

## 종합 판정

- **수치 불일치: 0건** — 원고의 모든 헤드라인 수치(13.01→8.87 p=0.0008, lag-1 +0.470→−0.208,
  0.005 m/s 경계, n=64, 132 등)가 코드·결과 JSON과 정합.
- **서술 불일치: 1건** — §2 adaptive-R 수식(이진)이 실제 2단계 규칙과 다름 → P2로 교체.
- **재현성 누락: 3묶음** — 구현 파라미터 표(P1), 5 ms 게이트 수치(P3), 검증 프로토콜 세부(P4).
- 패치 전문은 `manuscript_v2_section2_patch.md`.
