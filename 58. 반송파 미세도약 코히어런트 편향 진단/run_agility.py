"""58번 (신규 레버 진단): 계통 고도각 편향이 반송파 미세 변화에 따라 진동하는가 —
진동한다면 반송파 도약(frequency hopping) 평균으로 편향을 상쇄할 수 있는가.

기전 가설: gated SRP 편향은 게이트 안에 남는 표면반사 누설과 직접파의 코히어런트 간섭에서
나오고, 그 간섭 위상은 phi = 2*pi*f_c*delta (delta = 표면-직접 지연차)로 반송파 f_c에 민감하다.
그렇다면 bias(f_c) ~ A*cos(2*pi*delta*f_c + phi0) + C 형태로 진동해야 하고(주기 1/delta),
여러 반송파로 ping을 나눠 평균하면 진동 성분 A가 상쇄되고 상수 성분 C(순수 개구 기하)만 남는다.

54번은 16~64 kHz 큰 스텝만 봐(공간 aliasing 영역 포함) 이 미세구조를 못 봤다. 여기서는 배열
최적대역 안(30~34 kHz, 250 Hz 스텝)에서 고정 기하의 bias(f_c) 곡선을 재고,
(a) 진동 존재(진폭 vs 상수), (b) 도약 평균의 편향 저감률, (c) 진동 주기가 이론 1/delta와 맞는지
(cos-fit R^2)를 판정한다. GT는 편향 label에만. 채널은 ② 기준 3경로 canonical.
"""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import paths_for_sensor, synthesize_received
from config import ChannelConfig, usb_array_global_m
from measurement import ideal_measurement
from peak_measurement import extract_measurement

DISTANCES = (100, 200, 400, 600)
GEOMS = 6
REPEATS = 2                     # 37번: 고정 기하에서 random≈0이라 소수로 충분
CARRIERS_HZ = np.arange(30000.0, 34000.1, 250.0)   # 17개, 배열 최적대역 내
GEOM_ROOT = 580000
NOISE_ROOT = 583000


def geometry(distance, index):
    rng = np.random.default_rng(GEOM_ROOT + distance * 50 + index)
    az = rng.uniform(-np.pi, np.pi)
    depth = rng.uniform(12.0, 78.0)
    pos = np.array([distance * np.cos(az), distance * np.sin(az), -depth])
    env = dict(snr_db=float(rng.choice([10.0, 20.0, 30.0])),
               surface_reflection=float(-rng.uniform(0.72, 0.97)),
               bottom_reflection=float(rng.uniform(0.32, 0.78)),
               radial_velocity_m_s=float(rng.uniform(-1.3, 1.3)))
    return pos, env


def surface_direct_delta_s(pos, env):
    """기준 센서(0)에서 표면반사-직접파 지연차 delta (반송파와 무관)."""
    cfg = replace(ChannelConfig(), **env)
    sensor0 = usb_array_global_m(cfg.receiver_depth_m)[0]
    paths = {p.name: p.delay_s for p in paths_for_sensor(pos, sensor0, cfg)}
    return float(paths["surface"] - paths["direct"])


def el_bias_deg(pos, env, distance, index, carrier):
    vals = []
    for r in range(REPEATS):
        cfg = replace(ChannelConfig(), seed=NOISE_ROOT + distance * 2000 + index * 40 + r,
                      carrier_hz=float(carrier), **env)
        _, received, _ = synthesize_received(pos, cfg)
        z, _ = extract_measurement(received, cfg)
        truth = ideal_measurement(pos, cfg)
        vals.append(np.degrees(z[9] - truth[9]))
    return float(np.mean(vals))


def cos_fit_r2(freqs_hz, curve, delta_s):
    """bias(f) ~ a + b*cos(2*pi*delta*f) + c*sin(...) 적합의 설명력 R^2와 진동 진폭."""
    f = np.asarray(freqs_hz, float)
    y = np.asarray(curve, float)
    X = np.column_stack([np.ones_like(f), np.cos(2*np.pi*delta_s*f), np.sin(2*np.pi*delta_s*f)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    ss_tot = float(np.sum((y - y.mean())**2))
    r2 = 1.0 - float(np.sum(res**2))/ss_tot if ss_tot > 1e-12 else 0.0
    amplitude = float(np.hypot(beta[1], beta[2]))
    return r2, amplitude, float(beta[0])


def run():
    rows = []
    for d in DISTANCES:
        for i in range(GEOMS):
            pos, env = geometry(d, i)
            delta = surface_direct_delta_s(pos, env)
            curve = [el_bias_deg(pos, env, d, i, c) for c in CARRIERS_HZ]
            curve = np.asarray(curve)
            r2, amp, const = cos_fit_r2(CARRIERS_HZ, curve, delta)
            i32 = int(np.argmin(np.abs(CARRIERS_HZ - 32000.0)))
            rows.append({
                "distance": d, "index": i,
                "delta_us": delta * 1e6,
                "predicted_period_khz": 1e-3 / delta,
                "bias_at_32k_deg": float(curve[i32]),
                "hop_mean_bias_deg": float(np.mean(curve)),
                "osc_std_deg": float(np.std(curve)),
                "cos_fit_r2": r2, "cos_amplitude_deg": amp, "const_deg": const,
                "curve_deg": curve.tolist(),
            })
    summary = {}
    for d in list(DISTANCES) + ["overall"]:
        sub = rows if d == "overall" else [r for r in rows if r["distance"] == d]
        b32 = np.array([abs(r["bias_at_32k_deg"]) for r in sub])
        bhop = np.array([abs(r["hop_mean_bias_deg"]) for r in sub])
        summary[str(d)] = {
            "median_abs_bias_32k_deg": float(np.median(b32)),
            "median_abs_bias_hopavg_deg": float(np.median(bhop)),
            "hop_reduction_pct": float(100.0 * (1.0 - np.median(bhop)/max(np.median(b32), 1e-9))),
            "improved_fraction": float(np.mean(bhop < b32)),
            "median_osc_std_deg": float(np.median([r["osc_std_deg"] for r in sub])),
            "median_cos_fit_r2": float(np.median([r["cos_fit_r2"] for r in sub])),
            "median_predicted_period_khz": float(np.median([r["predicted_period_khz"] for r in sub])),
            "n": len(sub)}
    payload = {"config": {"distances_m": list(DISTANCES), "geoms_per_distance": GEOMS,
                          "repeats": REPEATS, "carriers_khz": [c/1000 for c in CARRIERS_HZ],
                          "note": "고정 기하 bias(f_c) 곡선: 진동성·도약평균 저감·cos(2π·δ·f) 기전 검증"},
               "summary": summary, "geometries": rows}
    out = Path(__file__).resolve().parent / "results"; out.mkdir(exist_ok=True)
    (out / "agility.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                                      encoding="utf-8")
    print(json.dumps({"config": payload["config"], "summary": summary}, indent=2, ensure_ascii=False))
    return payload


if __name__ == "__main__":
    run()
