"""138번: 해석모델(원고 식 18)의 이론-실측 오버레이 그림 생성.

58번 agility.json의 bias(f) 측정 곡선(17 carriers, 30-34 kHz) 위에, 진동 주기를 **기하에서
예측된 δ로 고정**한 2-ray 모델의 1차 조화 성분(a + b·cos2πδf + c·sin2πδf)을 최소제곱으로
겹친다. 주기는 fitting 파라미터가 아니므로("geometry-predicted δ"), 일치는 모델의 구조적
검증이다. 출력: paper/figures/fig_tworay_fit.png (원고 Fig. 삽입용).
"""

from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "58. 반송파 미세도약 코히어런트 편향 진단" / "results" / "agility.json"
OUT = ROOT / "paper" / "figures" / "fig_tworay_fit.png"

# 오버레이할 기하: (distance, index).
# 중요(정직성): 250 Hz 캐리어 스텝은 주기 > 500 Hz(2·step)인 진동만 unaliased로 분해한다.
# 따라서 Nyquist를 만족하는 기하만 사용: 400m idx1(1/δ=748 Hz), 600m idx5(1/δ=533 Hz).
# 600m idx3(235 Hz) 같은 사례는 주기가 샘플링 한계 아래라 오버레이가 aliased — 제외.
PICKS = [(400, 1), (600, 5)]


def first_harmonic_fit(f_hz, y, delta_s):
    """주기 1/delta 고정, a+b cos+c sin 최소제곱. 반환: fitted curve(밀집 grid), R^2."""
    w = 2 * np.pi * delta_s
    A = np.column_stack([np.ones_like(f_hz), np.cos(w * f_hz), np.sin(w * f_hz)])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    r2 = 1 - np.sum(resid**2) / np.sum((y - y.mean())**2)
    fd = np.linspace(f_hz.min(), f_hz.max(), 400)
    Ad = np.column_stack([np.ones_like(fd), np.cos(w * fd), np.sin(w * fd)])
    return fd, Ad @ coef, r2


def main():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    carriers_khz = np.array(d["config"]["carriers_khz"])
    f_hz = carriers_khz * 1000.0
    geoms = {(g["distance"], g["index"]): g for g in d["geometries"]}

    fig, axes = plt.subplots(2, 1, figsize=(3.5, 4.4), sharex=True)
    for ax, key in zip(axes, PICKS):
        g = geoms[key]
        y = np.array(g["curve_deg"])
        delta_s = g["delta_us"] * 1e-6
        fd, yfit, r2 = first_harmonic_fit(f_hz, y, delta_s)
        ax.plot(fd / 1000, yfit, "-", color="#d95f02", lw=1.6,
                label="two-ray model ($\\delta$ fixed by geometry)")
        ax.plot(carriers_khz, y, "o", color="#1b6ca8", ms=4.5, label="measured bias")
        ax.axhline(np.mean(y), color="0.55", lw=0.8, ls="--")
        ax.set_ylabel("elev. bias (deg)")
        ax.set_title(f"{key[0]} m: $\\delta$={g['delta_us']/1000:.2f} ms, "
                     f"period $1/\\delta$={g['predicted_period_khz']*1000:.0f} Hz, $R^2$={r2:.2f}",
                     fontsize=8.5)
        ax.tick_params(labelsize=8)
        ax.grid(alpha=0.25, lw=0.5)
        print(f"{key}: fixed-delta fit R^2 = {r2:.3f}")
    axes[0].legend(fontsize=7, loc="lower left", framealpha=0.92)
    axes[-1].set_xlabel("carrier frequency (kHz)")
    fig.tight_layout(h_pad=1.0)
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=300)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
