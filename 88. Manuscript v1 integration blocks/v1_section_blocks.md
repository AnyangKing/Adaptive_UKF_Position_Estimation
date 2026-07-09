# v1 section replacement blocks

These blocks are designed to replace or expand corresponding sections in `85. Manuscript draft v0/manuscript_draft_v0.md`.

## Replacement block for Section 2 — System and Signal Model

We consider a compact eight-sensor USBL array in a shallow-water acoustic environment. Let the source position at ping `k` be `p_k = [x_k,y_k,z_k]^T`, and let the `i`-th receiver element position be `s_i`, `i=0,...,7`. The array center is

```math
\bar{s}=\frac{1}{8}\sum_{i=0}^{7}s_i,
```

and the geometric source-to-sensor range is

```math
\rho_{i,k}=\|p_k-s_i\|_2.
```

The signal-derived observation vector is

```math
z_k =
\begin{bmatrix}
r_{0,k} &
\Delta r_{1,k} &
\cdots &
\Delta r_{7,k} &
\alpha_k &
\epsilon_k
\end{bmatrix}^{T},
```

where `r_{0,k}` is the reference-sensor TOA-derived range, `\Delta r_{i,k}` is the TDOA-derived range difference, and `\alpha_k`, `\epsilon_k` are azimuth and elevation. The ideal range and TDOA terms are

```math
r_{0,k}=\rho_{0,k},\quad
\Delta r_{i,k}=\rho_{i,k}-\rho_{0,k},\quad i=1,\ldots,7.
```

With `d_k=p_k-\bar{s}`, the ideal DOA components are

```math
\alpha_k=\operatorname{atan2}(d_{k,y},d_{k,x}),
```

```math
\epsilon_k=\operatorname{atan2}\left(d_{k,z},\sqrt{d_{k,x}^2+d_{k,y}^2}\right).
```

The UKF state is

```math
x_k=[p_k^T,u_k^T]^T
=
\begin{bmatrix}
x_k & y_k & z_k & v_{x,k} & v_{y,k} & v_{z,k}
\end{bmatrix}^T,
```

and a constant-velocity transition is used:

```math
x_{k+1}=Fx_k+w_k,\quad
F=
\begin{bmatrix}
I_3 & \Delta t I_3 \\
0_3 & I_3
\end{bmatrix}.
```

The measurement model is

```math
z_k=h(x_k)+v_k,
```

where `v_k` includes timing, TDOA, DOA, and coherent multipath residual components. A conditional adaptive-R wrapper changes the measurement covariance according to a signal-consistency indicator `g_k`, such as GCC/SRP DOA disagreement:

```math
R_k=
\begin{cases}
R_0, & g_k\le\tau,\\
R_{\mathrm{inflated}}, & g_k>\tau.
\end{cases}
```

This adaptive-R rule is used as the tracking backbone. The proposed contribution in this paper is not a new UKF variant; it is the transmit-side carrier schedule that changes the residual statistics entering this backbone.

Suggested figure callout:

> The array, propagation paths, and observation construction are summarized in Fig. 1.

## Replacement block for Section 4 — Carrier-Sensitive Coherent Interference Mechanism

The long-range residual becomes actionable when it is viewed as carrier-sensitive coherent interference. Suppose a direct component and an in-gate reflected component have an excess delay or path-difference term `\delta_k`. The carrier-dependent interference phase can be written as

```math
\phi_k(f_k,\delta_k)=2\pi f_k\delta_k+\theta_r,
```

where `f_k` is the transmit carrier frequency and `\theta_r` contains reflection-dependent phase terms. This expression is not used as a full reflected-path estimator. It is a mechanism-level model explaining why a coherent residual can remain temporally locked under fixed-carrier transmission.

For a static target and fixed carrier,

```math
f_k=f_0,\quad \delta_k\approx\delta_0,
```

so

```math
\phi_k\approx 2\pi f_0\delta_0+\theta_r.
```

The residual DOA bias can therefore persist with similar sign and magnitude across pings. In contrast, with carrier-agile pinging,

```math
f_k\in\{f_1,f_2,\ldots,f_K\},
```

so even if `\delta_k\approx\delta_0`,

```math
\phi_k\approx 2\pi f_k\delta_0+\theta_r
```

varies across pings. This rotates the coherent interference pattern and turns part of the deterministic DOA bias into a temporally whitened residual.

For moving targets, the path-difference term itself changes:

```math
\delta_k=\delta(t_k).
```

Thus, even fixed-carrier transmission can experience

```math
\phi_k\approx 2\pi f_0\delta(t_k)+\theta_r,
```

which explains the motion-induced self-whitening observed later in the moving-target experiments.

Suggested figure callout:

> Fig. 2 shows the carrier dependence of the residual bias, while Fig. 1 illustrates the direct and in-gate reflected paths that motivate the phase model.

## Replacement block for Section 5 — Frequency-Agile Whitening Method

The fixed-carrier baseline uses

```math
f_k=32\ \mathrm{kHz}.
```

The frequency-agile policy uses a frozen 20-ping linear sweep over

```math
f_k\in[30,34]\ \mathrm{kHz}.
```

All receiver-side processing is kept unchanged. The same TOA/TDOA/DOA observation vector is extracted, and the same adaptive-R UKF tracking backbone is used. Therefore, performance differences between fixed and frequency-agile transmission are attributed to the changed temporal structure of the measurement residual, not to a different estimator.

For static targets, the expected effect is reduced temporal correlation in the carrier-locked elevation residual. For moving targets, the expected effect is more limited because target motion already changes `\delta(t)` and can partially whiten the fixed-carrier residual. This distinction is important: the proposed schedule is expected to be strongest for static or very slow-drift long-range targets.

Suggested table callout:

> The fixed and frequency-agile policies are summarized in Table 2 with the main validation metrics.

## Replacement block for Section 6 — Static Validation

The primary validation uses independent static 600 m trials with the carrier schedule fixed before evaluation. Settled RMSE is computed over the post-transient ping set `K_s`:

```math
\mathrm{RMSE}_{\mathrm{settled}}
=
\sqrt{
\frac{1}{|K_s|}
\sum_{k\in K_s}
\|\hat{p}_k-p_k\|_2^2}.
```

With fixed 32 kHz transmission, mean settled RMSE was 13.01 m. With frequency-agile transmission, mean settled RMSE decreased to 8.87 m. This corresponds to a 32% reduction, with paired improvement of 4.14 m and p = 0.0008. The median error decreased from 13.97 m to 7.96 m.

This is the paper's strongest performance result. It supports the claim that carrier-agile pinging can mitigate a carrier-locked coherent DOA residual in static long-range shallow-water USBL localization. It does not support a sub-meter long-range claim, nor does it imply that all multipath or aperture limitations have been removed.

Suggested figure callout:

> The paired 600 m static validation result is shown in Fig. 3.

## Replacement block for Section 7 — Whitening Evidence and Applicability Boundary

To separate mechanism from localization performance, we examine the elevation residual sequence

```math
e_k=\epsilon^{\mathrm{meas}}_k-\epsilon^{\mathrm{ideal}}_k
```

and its lag-1 correlation:

```math
\operatorname{corr}_1(e)=
\frac{
\sum_{k=1}^{K-1}(e_k-\bar{e}_{1:K-1})(e_{k+1}-\bar{e}_{2:K})
}{
\sqrt{
\sum_{k=1}^{K-1}(e_k-\bar{e}_{1:K-1})^2
\sum_{k=2}^{K}(e_k-\bar{e}_{2:K})^2
}
}.
```

Moving-target experiments showed strong residual whitening: lag-1 correlation changed from +0.470 under fixed-carrier transmission to -0.208 under frequency-agile transmission, with p = 5.6e-10. However, pooled moving-target RMSE gain was not reliable (-0.10 m, p = 0.301). This establishes an applicability boundary: carrier agility can change the residual temporal structure without necessarily improving moving-target localization RMSE.

The quasi-static speed sweep further refines this boundary. Across all slow-drift trials, fixed transmission gave 11.98 m mean RMSE and frequency-agile transmission gave 10.49 m, with p = 8.00e-05. But speed-specific results were non-monotonic. Static and 0.005 m/s slow drift were validated, while 0.010 and 0.050 m/s were not supported. Positive results at 0.030 and 0.100 m/s are therefore treated as geometry-dependent recoveries rather than a monotonic speed threshold.

The continuous validated quasi-static regime is consequently limited to 0.005 m/s under the present protocol.

Suggested figure callouts:

> Fig. 4 reports the moving-target residual whitening result.

> Fig. 5 summarizes the quasi-static speed sweep and marks the continuous 0.005 m/s boundary.
