# Manuscript v2 → v3 patch: Method/protocol details from code audit

적용 대상: `92. Manuscript v2 통합/manuscript_draft_v2.md`. 각 패치는 삽입 위치와 원문 교체
지시를 포함한다. (v3 폴더에서 적용; 92는 스냅샷 원칙상 수정하지 않는다.)

---

## P1 — §2 끝에 "Implementation parameters" 소절 추가

**위치**: §2 마지막 문단("...are summarized in Fig. 1.") 뒤.

**삽입 텍스트**:

> ### 2.1 Implementation parameters
>
> All experiments use the following fixed implementation. The array has eight elements on two
> rings of radius 33 mm (four at z = 0 and four at z = −79 mm, rotated by 45°), giving an
> aperture of roughly 66 mm, i.e., about 1.4 wavelengths at 32 kHz. The receiver is at 30 m
> depth in a 100 m-deep waveguide with sound speed 1500 m/s. The probe is a 10 ms linear FM
> chirp of 12 kHz bandwidth (Tukey-windowed), sampled at 192 kHz; the channel model contains
> the direct path and first-order surface and bottom image-source reflections with Thorp
> absorption, Doppler, and colored ambient noise. TOA is taken from the strongest matched-filter
> peak of the reference sensor; TDOA uses band-limited GCC-PHAT over all 28 sensor pairs,
> reduced to seven reference differences by least squares; DOA uses SRP-PHAT on the 5 ms
> direct-path gate with a 2° global grid refined to 0.2°. The UKF uses α = 0.3, β = 2, κ = 0,
> Δt = 1 s, constant-velocity dynamics with white-acceleration process noise of standard
> deviation 0.20 m/s², initial covariance diag(8² m² I₃, 1.5² (m/s)² I₃), and a fixed base
> measurement covariance built from 0.03 m TOA-range, 0.025 m per-sensor TDOA, and 2.0° DOA
> standard deviations.

## P2 — §2 adaptive-R 수식 교체 (서술 불일치 수정)

**대상 원문** (§2):

> ```math
> R_k=\begin{cases} R_0, & g_k\le\tau,\\ R_{\mathrm{inflated}}, & g_k>\tau. \end{cases}
> ```

**교체 텍스트**:

> The conditional adaptive-R wrapper operates in two stages. First, a graded scale is computed
> from the GCC/SRP DOA disagreement `g_k` (in degrees),
>
> ```math
> s_k=\min\!\left(100,\;1+\left(\frac{g_k}{2}\right)^{2}\right),
> ```
>
> and applied to the DOA block of `R_k` when `g_k\le\tau` (small disagreement: distrust the
> refined DOA less than the TDOA set is trusted) or to the TDOA block when `g_k>\tau`
> (large disagreement: distrust the TDOA-consistent solution), with `\tau=5^{\circ}`.
> Second, a per-block innovation test inflates each observation block independently:
>
> ```math
> R_k^{(b)}\leftarrow R_k^{(b)}\cdot
> \min\!\left(100,\;\max\!\left(1,\;\frac{\mathrm{NIS}_k^{(b)}}{\chi^2_{0.99}(d_b)}\right)\right),
> ```
>
> where the blocks `b` are TOA-range, TDOA, and DOA with degrees of freedom `d_b = 1, 7, 2`
> and `\chi^2_{0.99}` thresholds 6.63, 18.48, and 9.21, respectively.

**이유**: v2의 이진 수식은 실제 코드(연속 스케일 + 블록별 NIS 팽창)와 다르다. 리뷰어가 코드를
요구하면 불일치가 드러난다.

## P3 — 5 ms 게이트 수치 명기 (2곳)

1. **§2** 관측 서술 문장에 반영(P1에 이미 포함: "SRP-PHAT on the 5 ms direct-path gate").
2. **§4 첫 문단** 교체: "Suppose a direct component and an in-gate reflected component..."
   → "Suppose a direct component and a reflected component arriving **within the 5 ms
   direct-path gate** have an excess delay or path-difference term `\delta_k`. At 600 m in the
   present geometry, the surface-reflected excess delay is a few milliseconds and therefore
   falls inside this gate; at 100–200 m it falls outside, which is why the carrier-locked bias
   is a long-range phenomenon."

**이유**: 기전(§4)·거리 경계(§7)의 물리가 게이트 폭 5 ms에 걸려 있는데 v2 전문에 수치가 없다.

## P4 — 검증 프로토콜 세부 (3곳)

1. **§6 첫 문단**에 추가:
   > Each trial uses 20 pings with the settled window defined as the final 10 pings; the
   > validation set comprises 20 independent geometries at 600 m (with 100/200/400 m also run
   > under the same frozen protocol), on seed streams disjoint from all development experiments.
2. **§7 moving 문단**에 추가:
   > The moving set comprises four motion conditions (radial 0.05 and 1.0 m/s, tangential
   > 1.0 m/s, and tangential 1.0 m/s with 0.08 m/s vertical drift) with 16 independent
   > geometries each (n = 64), using the same 20-ping settled-window protocol.
3. **§7 quasi-static 문단**에 추가:
   > The sweep pools radial and tangential drift directions (12 geometries per
   > speed–direction condition; the static speed contributes one set), giving 132 paired
   > trials in total.
4. **§5 또는 §6**에 채널 명시 한 문장:
   > All validation experiments use the canonical direct+surface+bottom channel; no additional
   > roughness or higher-order multipath is enabled, so the reported gains isolate the
   > carrier-schedule effect.

## 적용 체크리스트 (v3에서)

- [ ] P1 삽입 후 §5의 "fixed-carrier baseline uses 32 kHz" 문장과 중복 없는지 확인
- [ ] P2 교체 후 §2의 "backbone" 문단 연결 자연스러운지 확인
- [ ] P3-2 적용 시 §7 거리-경계 서술과 표현 통일("long-range phenomenon")
- [ ] P4 수치가 Table 2와 재차 일치하는지 교차 확인 (n=20/64/132)
