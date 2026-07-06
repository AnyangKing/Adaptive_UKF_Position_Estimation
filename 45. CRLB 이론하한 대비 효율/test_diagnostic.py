"""45번 CRLB 계약을 최소 검증한다 (pytest 없이 순수 Python)."""

import numpy as np

from config import ChannelConfig
from crlb import position_crlb
from measurement import fixed_measurement_covariance


def test_crlb_positive_and_shape():
    cfg = ChannelConfig()
    cov, bound = position_crlb(np.array([300.0, 40.0, -30.0]), cfg)
    assert cov.shape == (3, 3)
    assert bound > 0.0 and np.isfinite(bound)
    # 대각 성분(분산)은 양수여야 한다.
    assert np.all(np.diag(cov) > 0.0)


def test_crlb_grows_with_range():
    """관측 R가 같으면 먼 거리에서 위치 CRLB가 더 크다(각도오차의 거리 증폭)."""
    cfg = ChannelConfig()
    near = position_crlb(np.array([100.0, 0.0, -30.0]), cfg)[1]
    far = position_crlb(np.array([600.0, 0.0, -30.0]), cfg)[1]
    assert far > near


def test_crlb_tightens_with_smaller_noise():
    """관측 잡음을 줄이면 CRLB 하한도 작아진다."""
    cfg = ChannelConfig()
    pos = np.array([400.0, 20.0, -35.0])
    base = position_crlb(pos, cfg)[1]
    tight = position_crlb(pos, cfg, 0.25 * fixed_measurement_covariance())[1]
    assert tight < base


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("all tests passed")
