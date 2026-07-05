"""센서별 absolute range 8개와 배열 SRP DOA 2개의 관측 정의."""

import numpy as np

from config import ChannelConfig,usb_array_global_m


def wrap_angle(value):
    return (value+np.pi)%(2*np.pi)-np.pi


def ideal_measurement(position,cfg:ChannelConfig):
    sensors=usb_array_global_m(cfg.receiver_depth_m); ranges=np.linalg.norm(np.asarray(position)-sensors,axis=1)
    delta=np.asarray(position)-sensors.mean(axis=0)
    return np.r_[ranges,np.arctan2(delta[1],delta[0]),np.arctan2(delta[2],np.hypot(delta[0],delta[1]))]


def initialize_position(observation,cfg:ChannelConfig):
    sensors=usb_array_global_m(cfg.receiver_depth_m); center=sensors.mean(axis=0)
    az,el=observation[8],observation[9]
    direction=np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])
    offset=center-sensors[0]; radius=observation[0]
    b=2*direction@offset; c=offset@offset-radius**2; disc=max(0.,b*b-4*c)
    return center+max((-b+np.sqrt(disc))/2,(-b-np.sqrt(disc))/2)*direction


def measurement_covariance(range_std_m=0.03,doa_std_deg=2.0):
    return np.diag([range_std_m**2]*8+[np.radians(doa_std_deg)**2]*2)
