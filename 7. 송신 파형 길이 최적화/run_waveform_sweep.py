"""chirp 길이가 멀티패스 중첩과 GCC-PHAT DOA에 미치는 영향 비교."""

from dataclasses import replace
from pathlib import Path
import json
import numpy as np

from channel import paths_for_sensor, synthesize_received
from config import ChannelConfig, usb_array_global_m
from estimators import estimate_gcc_phat_doa


def angle_error_deg(estimate, truth):
    return float(np.degrees(np.arccos(np.clip(estimate @ truth, -1.0, 1.0))))


def summarize(values):
    values=np.asarray(values)
    return {"mean_deg":float(np.mean(values)),"median_deg":float(np.median(values)),
            "p90_deg":float(np.percentile(values,90)),"max_deg":float(np.max(values)),
            "failure_over_10deg_rate":float(np.mean(values>10.0))}


def scenarios(count=20):
    rng=np.random.default_rng(20260703); result=[]
    for trial in range(count):
        distance=float(rng.choice([100.0,300.0,600.0])); az=rng.uniform(-np.pi,np.pi)
        result.append({"source":np.array([distance*np.cos(az),distance*np.sin(az),-rng.uniform(8,85)]),
            "seed":20260703+trial,"snr_db":float(rng.choice([10.0,20.0,30.0])),
            "surface":float(-rng.uniform(0.70,0.98)),"bottom":float(rng.uniform(0.30,0.80)),
            "velocity":float(rng.uniform(-1.5,1.5))})
    return result


def run():
    durations_ms=[1.0,2.0,5.0,10.0]; trial_set=scenarios(); result={}
    sensors=usb_array_global_m()
    for duration_ms in durations_ms:
        errors=[]; overlap=[]
        for item in trial_set:
            cfg=replace(ChannelConfig(),pulse_duration_s=duration_ms/1000.0,
                seed=item["seed"],snr_db=item["snr_db"],surface_reflection=item["surface"],
                bottom_reflection=item["bottom"],radial_velocity_m_s=item["velocity"])
            _,received,_=synthesize_received(item["source"],cfg)
            _,_,direction,_=estimate_gcc_phat_doa(received,cfg)
            truth=item["source"]-sensors.mean(axis=0); truth/=np.linalg.norm(truth)
            errors.append(angle_error_deg(direction,truth))
            paths=paths_for_sensor(item["source"],sensors[0],cfg)
            gap=paths[1].delay_s-paths[0].delay_s
            overlap.append(max(0.0,1.0-gap/cfg.pulse_duration_s))
        result[f"{duration_ms:g}ms"]={**summarize(errors),
            "mean_direct_surface_overlap_fraction":float(np.mean(overlap)),
            "overlap_scenario_rate":float(np.mean(np.asarray(overlap)>0))}
    output=Path(__file__).resolve().parent/"results"; output.mkdir(exist_ok=True)
    (output/"waveform_sweep.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2)); return result


if __name__=="__main__": run()
