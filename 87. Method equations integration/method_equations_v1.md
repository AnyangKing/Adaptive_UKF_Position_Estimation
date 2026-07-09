# Method equations v1

## 1. Coordinate and array notation

Let the source position at ping `k` be

```math
\mathbf{p}_k = [x_k, y_k, z_k]^\top
```

and the `i`-th receiver element position be

```math
\mathbf{s}_i = [s_{i,x}, s_{i,y}, s_{i,z}]^\top,\quad i=0,\ldots,7.
```

The compact USBL array center is

```math
\bar{\mathbf{s}} = \frac{1}{8}\sum_{i=0}^{7}\mathbf{s}_i.
```

The geometric range from source to sensor `i` is

```math
\rho_{i,k} = \|\mathbf{p}_k - \mathbf{s}_i\|_2.
```

## 2. Observation vector

The signal-derived observation vector at ping `k` is

```math
\mathbf{z}_k =
\begin{bmatrix}
r_{0,k} &
\Delta r_{1,k} &
\cdots &
\Delta r_{7,k} &
\alpha_k &
\epsilon_k
\end{bmatrix}^{\top},
```

where `r_{0,k}` is the reference-sensor TOA-derived range, `\Delta r_{i,k}` is the TDOA-derived range difference between sensor `i` and reference sensor `0`, and `\alpha_k`, `\epsilon_k` are azimuth and elevation.

The ideal range and TDOA components are

```math
r_{0,k} = \rho_{0,k},
```

```math
\Delta r_{i,k} = \rho_{i,k} - \rho_{0,k},\quad i=1,\ldots,7.
```

Let

```math
\mathbf{d}_k = \mathbf{p}_k - \bar{\mathbf{s}}.
```

Then the ideal DOA angles are

```math
\alpha_k = \operatorname{atan2}(d_{k,y}, d_{k,x}),
```

```math
\epsilon_k = \operatorname{atan2}\left(d_{k,z}, \sqrt{d_{k,x}^2+d_{k,y}^2}\right).
```

Thus the ideal observation model is

```math
\mathbf{z}_k = h(\mathbf{x}_k) + \mathbf{v}_k,
```

with `\mathbf{x}_k = [\mathbf{p}_k^\top,\mathbf{u}_k^\top]^\top` and measurement residual `\mathbf{v}_k`.

## 3. State model

The tracking state is

```math
\mathbf{x}_k =
\begin{bmatrix}
x_k & y_k & z_k & v_{x,k} & v_{y,k} & v_{z,k}
\end{bmatrix}^{\top}.
```

A constant-velocity model is used:

```math
\mathbf{x}_{k+1} =
\mathbf{F}\mathbf{x}_k + \mathbf{w}_k,
```

where

```math
\mathbf{F} =
\begin{bmatrix}
\mathbf{I}_3 & \Delta t\,\mathbf{I}_3 \\
\mathbf{0}_3 & \mathbf{I}_3
\end{bmatrix},
```

and `\mathbf{w}_k` is process noise induced by acceleration uncertainty.

For compactness, the process covariance can be described as the standard white-acceleration covariance:

```math
\mathbf{Q} = \sigma_a^2
\begin{bmatrix}
\frac{\Delta t^4}{4}\mathbf{I}_3 & \frac{\Delta t^3}{2}\mathbf{I}_3 \\
\frac{\Delta t^3}{2}\mathbf{I}_3 & \Delta t^2\mathbf{I}_3
\end{bmatrix}.
```

## 4. Conditional adaptive measurement covariance

The baseline measurement covariance is

```math
\mathbf{R}_0 =
\operatorname{diag/structured}
\left(
\sigma_{\mathrm{TOA}}^2,
\mathbf{R}_{\mathrm{TDOA}},
\sigma_{\alpha}^2,
\sigma_{\epsilon}^2
\right),
```

where the TDOA block includes the shared reference-sensor timing component.

Let `g_k` be a signal-consistency indicator such as the angular disagreement between GCC- and SRP-derived DOA estimates. A simple conditional routing rule is

```math
\mathbf{R}_k =
\begin{cases}
\mathbf{R}_0, & g_k \leq \tau,\\
\mathbf{R}_{\mathrm{inflated}}, & g_k > \tau.
\end{cases}
```

This adaptive-R rule is not the primary novelty. It is the stable tracking backbone used to evaluate how transmit-side carrier agility changes the residual entering the filter.

## 5. Carrier-locked coherent residual model

Let a direct path and an in-gate reflected path have an excess delay difference `\delta_k`. The carrier-dependent interference phase is

```math
\phi_k(f_k,\delta_k) = 2\pi f_k \delta_k + \theta_r,
```

where `f_k` is the carrier frequency at ping `k`, and `\theta_r` contains reflection-dependent phase terms.

For a static target under fixed carrier transmission,

```math
f_k = f_0,\quad \delta_k \approx \delta_0,
```

so

```math
\phi_k \approx 2\pi f_0\delta_0 + \theta_r,
```

which can produce a persistent DOA bias.

With carrier-agile pinging,

```math
f_k \in \{f_1,f_2,\ldots,f_K\},
```

so even when `\delta_k \approx \delta_0`,

```math
\phi_k \approx 2\pi f_k\delta_0 + \theta_r
```

varies across pings. This rotates the coherent residual and can reduce temporal correlation in the DOA error observed by the UKF.

## 6. Moving-target self-whitening condition

For a moving target, `\delta_k` is not constant:

```math
\delta_k = \delta(t_k).
```

Even under fixed carrier transmission,

```math
\phi_k \approx 2\pi f_0\delta(t_k) + \theta_r
```

can vary across pings. This is the motion-induced self-whitening mechanism. It explains why moving-target residual whitening can be observed without reliable additional RMSE improvement from carrier agility.

## 7. Carrier schedule used in validation

The fixed baseline is

```math
f_k = 32\,\mathrm{kHz}.
```

The carrier-agile schedule is

```math
f_k \in [30,34]\,\mathrm{kHz},
```

implemented as a frozen 20-ping linear sweep in the validation scripts. The schedule was not retuned after observing validation outcomes.

## 8. Performance metrics

Settled RMSE over a post-transient index set `\mathcal{K}_s` is

```math
\mathrm{RMSE}_{\mathrm{settled}} =
\sqrt{
\frac{1}{|\mathcal{K}_s|}
\sum_{k\in\mathcal{K}_s}
\|\hat{\mathbf{p}}_k-\mathbf{p}_k\|_2^2
}.
```

Residual whitening is summarized by lag-1 correlation of the elevation residual sequence:

```math
\mathrm{corr}_1(e) =
\frac{
\sum_{k=1}^{K-1}(e_k-\bar{e}_{1:K-1})(e_{k+1}-\bar{e}_{2:K})
}{
\sqrt{
\sum_{k=1}^{K-1}(e_k-\bar{e}_{1:K-1})^2
\sum_{k=2}^{K}(e_k-\bar{e}_{2:K})^2
}
}.
```

Here

```math
e_k = \epsilon^{\mathrm{meas}}_k-\epsilon^{\mathrm{ideal}}_k.
```

## 9. Insertion note

The manuscript should not imply that the residual model is a complete multipath estimator. It is a mechanism-level explanation for why carrier agility changes the temporal bias structure.
