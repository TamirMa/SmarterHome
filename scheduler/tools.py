import os
import requests

from server.control_router import LightState
from devices.aeg import AEGOven

SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")

def change_light_state(device_id, light_state : LightState):
    requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/light/{device_id}",
        params={"light_state": light_state}
    )

def turn_on_oven(program=AEGOven.PROGRAMS.TRUE_FAN_COOKING, temperature=180):
    """
    Turn On - Oven
    """
    requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/oven/AEGOven/on",
        params={
            "program": program,
            "temperature": temperature,
        }
    )

def turn_off_oven():
    """
    Turn Off - Oven
    """
    requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/oven/AEGOven/off",
    )

def get_all_devices():
    return requests.get(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/devices",
    ).json()