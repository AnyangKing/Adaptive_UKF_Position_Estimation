# Notation table

| Symbol | Meaning |
|---|---|
| `k` | ping index |
| `i` | sensor index |
| `\mathbf{p}_k` | source/target position at ping `k` |
| `\mathbf{s}_i` | position of sensor `i` |
| `\bar{\mathbf{s}}` | USBL array center |
| `\rho_{i,k}` | range from source to sensor `i` |
| `r_{0,k}` | TOA-derived range at reference sensor 0 |
| `\Delta r_{i,k}` | TDOA-derived range difference between sensor `i` and sensor 0 |
| `\alpha_k` | azimuth angle |
| `\epsilon_k` | elevation angle |
| `\mathbf{z}_k` | observation vector `[TOA, TDOA..., azimuth, elevation]` |
| `\mathbf{x}_k` | UKF state `[position, velocity]` |
| `\mathbf{F}` | constant-velocity transition matrix |
| `\mathbf{Q}` | process noise covariance |
| `\mathbf{R}_0` | nominal measurement covariance |
| `\mathbf{R}_k` | routed/adaptive measurement covariance |
| `g_k` | signal-consistency indicator, e.g., GCC/SRP DOA disagreement |
| `\tau` | routing threshold |
| `f_k` | carrier frequency at ping `k` |
| `\delta_k` | direct-reflected excess delay/path difference term |
| `\theta_r` | reflection phase term |
| `\phi_k` | carrier-dependent interference phase |
| `e_k` | elevation residual |
| `\mathcal{K}_s` | settled evaluation index set |

## Naming consistency recommendation

Use `carrier-agile` and `frequency-agile` consistently:

- `carrier-agile` when emphasizing the mechanism `phi = 2*pi*f*delta`
- `frequency-agile pinging` when describing the transmission policy

Avoid mixing too many terms such as frequency hopping, frequency diversity, carrier sweep, and agility without defining them.
