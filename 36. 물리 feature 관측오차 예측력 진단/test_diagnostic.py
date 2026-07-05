"""한 장면에서 feature와 오차가 유한하게 계산되는지 확인하는 smoke test."""

import numpy as np

from feature_diagnostic import FEATURE_NAMES, measure_scene
from run_diagnostic import roc_auc


def test_measure_scene_finite():
    result = measure_scene(200, 0, "validation", (0.0, 5.0))
    for std in (0.0, 5.0):
        features = result[std]["features"]
        errors = result[std]["errors"]
        assert set(features) == set(FEATURE_NAMES)
        assert all(np.isfinite(v) for v in features.values())
        assert errors["doa_error_deg"] >= 0.0


def test_roc_auc_monotone():
    # feature가 label과 완전히 정렬되면 AUC=1, 반대면 0.
    labels = [0, 0, 1, 1]
    assert roc_auc([0.1, 0.2, 0.8, 0.9], labels) == 1.0
    assert roc_auc([0.9, 0.8, 0.2, 0.1], labels) == 0.0


if __name__ == "__main__":
    test_measure_scene_finite()
    test_roc_auc_monotone()
    print("smoke test 통과")
