"""200 m 발산 궤적의 시점별 SRP 방향오차와 jump 진단."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import synthesize_received
from config import ChannelConfig,usb_array_global_m
from measurement import signal_measurement
from run_compare import trajectory


def direction(az,el):
    return np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])


def angle_deg(a,b):
    return float(np.degrees(np.arccos(np.clip(a@b,-1,1))))


def run():
    cfg=ChannelConfig(); truth=trajectory(200); center=usb_array_global_m().mean(axis=0)
    rows=[]; previous=None
    for k,position in enumerate(truth):
        ping_cfg=replace(cfg,seed=172000+k,radial_velocity_m_s=0.55+0.2*np.sin(k/4),
            snr_db=20.,surface_reflection=-0.90,bottom_reflection=0.60)
        _,received,_=synthesize_received(position,ping_cfg); _,q=signal_measurement(received,ping_cfg)
        estimate=direction(q["srp_azimuth_rad"],q["srp_elevation_rad"])
        actual=position-center; actual/=np.linalg.norm(actual)
        rows.append({"step":k,"true_error_deg":angle_deg(estimate,actual),
            "jump_deg":0.0 if previous is None else angle_deg(estimate,previous),
            "gcc_srp_disagreement_deg":q["doa_disagreement_deg"]})
        previous=estimate
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"srp_200_diagnostics.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
    print(json.dumps(rows,indent=2)); return rows


if __name__=="__main__": run()
