import os
import requests

from server.control_router import DeviceType, LightState, SocketState
from devices.aeg import AEGOven

SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")

def change_light_state(device_id, light_state : LightState):
    requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/light/{device_id}",
        params={"light_state": light_state}
    )

def change_socket_state(device_id, socket_state : SocketState):
    requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/socket/{device_id}",
        params={"socket_state": socket_state}
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

def get_all_devices(device_type:DeviceType):
    return requests.get(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/all",
        params={
            "device_type" : device_type
        }
    ).json()