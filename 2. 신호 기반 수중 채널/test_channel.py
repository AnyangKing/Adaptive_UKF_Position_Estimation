import unittest
import numpy as np

from channel import make_probe, paths_for_sensor, synthesize_received, thorp_absorption_db_per_km
from config import ChannelConfig, usb_array_global_m
from estimators import estimate_array_doa, estimate_toa_matched_filter
from run_smoke import run


class ChannelTests(unittest.TestCase):
    def setUp(self):
        self.cfg = ChannelConfig(radial_velocity_m_s=0.0)
        self.source = np.array([100.0, 20.0, -20.0])

    def test_probe_properties(self):
        probe = make_probe(self.cfg)
        self.assertEqual(len(probe), round(self.cfg.sample_rate_hz * self.cfg.pulse_duration_s))
        self.assertAlmostEqual(float(np.sqrt(np.mean(probe**2))), 1.0, places=12)

    def test_geometry_and_paths(self):
        sensors = usb_array_global_m(self.cfg.receiver_depth_m)
        np.testing.assert_allclose(sensors.mean(axis=0), [0.0, 0.0, -30.0], atol=1e-12)
        paths = paths_for_sensor(self.source, sensors[0], self.cfg)
        self.assertEqual([p.name for p in paths], ["direct", "surface", "bottom"])
        self.assertLess(paths[0].distance_m, paths[1].distance_m)
        self.assertLess(paths[1].distance_m, paths[2].distance_m)

    def test_absorption_positive(self):
        self.assertGreater(thorp_absorption_db_per_km(self.cfg.carrier_hz), 0.0)

    def test_noiseless_direct_toa_and_doa(self):
        _, received, paths = synthesize_received(
            self.source, self.cfg, include_multipath=False, include_noise=False
        )
        estimated, _ = estimate_toa_matched_filter(received, self.cfg)
        truth = np.array([p[0].delay_s for p in paths])
        self.assertLess(np.max(np.abs(estimated - truth)), 1.1 / self.cfg.sample_rate_hz)
        _, _, direction = estimate_array_doa(estimated, self.cfg)
        true_direction = self.source - usb_array_global_m(self.cfg.receiver_depth_m).mean(axis=0)
        true_direction /= np.linalg.norm(true_direction)
        self.assertLess(np.degrees(np.arccos(np.clip(direction @ true_direction, -1, 1))), 8.0)

    def test_realistic_smoke(self):
        metrics = run()
        # 이 단계는 멀티패스 성능을 튜닝하지 않고 파이프라인의 건전성만 검사한다.
        self.assertLess(metrics["tdoa_rmse_us"], 20.0)
        self.assertLess(metrics["azimuth_error_deg"], 10.0)
        self.assertLess(metrics["elevation_error_deg"], 25.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
