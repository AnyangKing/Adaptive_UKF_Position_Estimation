"""93번: manuscript v2의 Method/프로토콜 수치를 실제 채택 코드에서 기계적으로 추출해 대조한다.

원고 §2·§5·§6·§7이 주장하는 모든 구현 파라미터의 authoritative 값을, 헤드라인 결과를 만든
폴더들(61 static validation, 63 moving, 82 quasi-static)과 공통 파이프라인 파일에서 regex로
추출해 results/method_facts.json으로 저장한다. import가 아니라 텍스트 파싱을 쓰는 이유는
폴더 간 동명 모듈 충돌을 피하고, '커밋된 파일 그대로'를 근거로 삼기 위해서다.
"""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
F61 = ROOT / "61. 정지표적 도약 대규모 독립검증"
F63 = ROOT / "63. 이동표적 도약 대규모검증 백색화 확인"
F82 = ROOT / "82. 준정지 속도 경계 검증 실행"


def _read(p):
    return Path(p).read_text(encoding="utf-8")


def _num(pattern, text, cast=float):
    m = re.search(pattern, text)
    return cast(m.group(1)) if m else None


def extract():
    facts = {}

    # --- 채널/신호 (61/config.py = canonical 3-path) ---
    cfg = _read(F61 / "config.py")
    facts["channel"] = {
        "sound_speed_m_s": _num(r"sound_speed_m_s:\s*float\s*=\s*([\d.]+)", cfg),
        "water_depth_m": _num(r"water_depth_m:\s*float\s*=\s*([\d.]+)", cfg),
        "receiver_depth_m": _num(r"receiver_depth_m:\s*float\s*=\s*([\d.]+)", cfg),
        "sample_rate_hz": _num(r"sample_rate_hz:\s*float\s*=\s*([\d.]+)", cfg),
        "carrier_hz_default": _num(r"carrier_hz:\s*float\s*=\s*([\d.]+)", cfg),
        "chirp_bandwidth_hz": _num(r"chirp_bandwidth_hz:\s*float\s*=\s*([\d.]+)", cfg),
        "pulse_duration_s": _num(r"pulse_duration_s:\s*float\s*=\s*([\d.]+)", cfg),
        "guard_time_s": _num(r"guard_time_s:\s*float\s*=\s*([\d.]+)", cfg),
        "realism_flags_present": bool(re.search(r"second_order|roughness", cfg)),
    }
    facts["array"] = {
        "n_sensors": 8,
        "ring_radius_m": _num(r"r,\s*height\s*=\s*([\d.]+)", cfg),
        "ring_vertical_offset_m": _num(r"r,\s*height\s*=\s*[\d.]+,\s*([\d.]+)", cfg),
    }

    # --- 관측 추출 (61/peak_measurement.py, estimators.py, measurement.py) ---
    pk = _read(F61 / "peak_measurement.py")
    facts["gating"] = {
        "direct_gate_window_s": _num(r"window_s=([\d.]+)", pk),
        "pre_window_s": _num(r"pre_s=([\d.]+)", pk),
    }
    est = _read(F61 / "estimators.py")
    facts["srp_grid_deg"] = {
        "coarse_step": _num(r"np\.arange\(-180\.0,\s*180\.0,\s*([\d.]+)\)", est),
        "fine_step": _num(r"center_az\s*-\s*2\.0,\s*center_az\s*\+\s*2\.01,\s*([\d.]+)", est),
    }
    meas = _read(F61 / "measurement.py")
    facts["fixed_R"] = {
        "toa_range_std_m": _num(r"toa_range_std_m:\s*float\s*=\s*([\d.]+)", meas),
        "tdoa_sensor_std_m": _num(r"tdoa_sensor_std_m:\s*float\s*=\s*([\d.]+)", meas),
        "doa_std_deg": _num(r"doa_std_deg:\s*float\s*=\s*([\d.]+)", meas),
    }

    # --- UKF/필터 (61/ukf.py, run_static_hop.py) ---
    ukf = _read(F61 / "ukf.py")
    facts["ukf"] = {
        "alpha": _num(r"alpha:\s*float\s*=\s*([\d.]+)", ukf),
        "beta": _num(r"beta:\s*float\s*=\s*([\d.]+)", ukf),
        "kappa": _num(r"kappa:\s*float\s*=\s*([\d.]+)", ukf),
    }
    run61 = _read(F61 / "run_static_hop.py")
    facts["filter_init"] = {
        "pos_std_m": _num(r"np\.diag\(\[([\d.]+)\*\*2\]\*3", run61),
        "vel_std_m_s": _num(r"\*3\s*\+\s*\[([\d.]+)\*\*2\]\*3", run61),
        "accel_process_std_m_s2": _num(r"acceleration_process_covariance\(1\.0,\s*([\d.]+)\)", run61),
        "dt_s": 1.0,
    }

    # --- 조건부 adaptive-R 실제 규칙 (61/conditional_adaptive.py) ---
    ca = _read(F61 / "conditional_adaptive.py")
    facts["adaptive_R_actual"] = {
        "threshold_deg": _num(r"ROUTING_THRESHOLD_DEG\s*=\s*([\d.]+)", run61),
        "scale_formula": "s = min(100, 1 + (g/2)^2); g<=tau -> DOA block *= s, g>tau -> TDOA block *= s",
        "scale_divisor": _num(r"disagreement/([\d.]+)\)", ca),
        "scale_cap": _num(r"min\(([\d.]+)\.?,\s*1\.", ca),
        "nis_limits_chi2_99": [
            _num(r"slice\(0,\s*1\),\s*([\d.]+)", ca),
            _num(r"slice\(1,\s*8\),\s*([\d.]+)", ca),
            _num(r"slice\(8,\s*10\),\s*([\d.]+)", ca),
        ],
        "nis_inflation": "R_block *= min(100, max(1, NIS/limit)) per block (dof 1/7/2)",
    }

    # --- 검증 프로토콜: 61 static ---
    facts["protocol_61_static"] = {
        "distances_m": [100, 200, 400, 600],
        "geoms_per_distance": _num(r"GEOMS\s*=\s*(\d+)", run61, int),
        "steps": _num(r"STEPS\s*=\s*(\d+)", run61, int),
        "settle_start": _num(r"SETTLE_START\s*=\s*(\d+)", run61, int),
        "hop_span_hz": [30000.0, 34000.0],
        "hop_carriers": _num(r"linspace\(30000\.0,\s*34000\.0,\s*(\w+)\)", run61, str),
        "fixed_carrier_hz": _num(r"FIXED_CARRIER_HZ\s*=\s*([\d.]+)", run61),
    }

    # --- 검증 프로토콜: 63 moving ---
    run63 = _read(F63 / "run_moving_validation.py")
    facts["protocol_63_moving"] = {
        "distance_m": _num(r"DISTANCE\s*=\s*([\d.]+)", run63),
        "geoms_per_condition": _num(r"GEOMS\s*=\s*(\d+)", run63, int),
        "n_conditions": len(re.findall(r'\("\w+', run63.split("CONDITIONS")[1][:600])),
        "steps": _num(r"STEPS\s*=\s*(\d+)", run63, int),
        "settle_start": _num(r"SETTLE_START\s*=\s*(\d+)", run63, int),
        "total_trials": None,  # 아래에서 계산
    }
    p63 = facts["protocol_63_moving"]
    p63["total_trials"] = p63["geoms_per_condition"] * p63["n_conditions"]

    # --- 검증 프로토콜: 82 quasi-static (실행 당시 config는 결과 JSON이 authoritative) ---
    j82 = json.loads(_read(F82 / "results" / "quasi_static_boundary.json"))
    c82 = j82["config"]
    facts["protocol_82_quasistatic"] = {
        "distance_m": c82["distance_m"],
        "geoms_per_condition": c82["geoms_per_condition"],
        "speeds_m_s": c82["speeds_m_s"],
        "motion_modes": c82["motion_modes"],
        "steps": c82["steps"],
        "settle_start": c82["settle_start"],
        "total_paired_trials": len(j82["runs"]),
        "trial_accounting": "static(1 set) x 12 + 5 speeds x 2 modes x 12 = 132",
    }

    return facts


def main():
    facts = extract()
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    (out / "method_facts.json").write_text(json.dumps(facts, indent=2, ensure_ascii=False),
                                           encoding="utf-8")
    print(json.dumps(facts, indent=2, ensure_ascii=False))
    return facts


if __name__ == "__main__":
    main()
