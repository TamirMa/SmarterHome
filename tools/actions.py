import json
import os
import requests

from server.control_router import CurtainState, DeviceType, FanState, LightState, SocketState
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

def change_fan_state(device_id, fan_state : FanState):
    requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/fan/{device_id}",
        params={"fan_state": fan_state}
    )

def change_curtain_state(device_id, curtain_state : CurtainState):
    requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/curtain/{device_id}/state",
        params={"curtain_state": curtain_state}
    )

def start_dishwasher(device_id="Dishwasher"):
    requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/dishwasher/{device_id}/start"
    )

def turn_on_oven(device_id="AEGOven", program=AEGOven.PROGRAMS.TRUE_FAN_COOKING, temperature=180):
    """
    Turn On - Oven
    """
    requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/oven/{device_id}/on",
        params={
            "program": program,
            "temperature": temperature,
        }
    )

def turn_off_oven(device_id="AEGOven"):
    """
    Turn Off - Oven
    """
    requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/oven/{device_id}/off",
    )

def get_all_devices(device_type:DeviceType):
    return requests.get(
        f"http://{SERVER_IP}:{SERVER_PORT}/devices/all",
        params={
            "device_type" : device_type
        }
    ).json()

def test_shabat_tasks():
    return requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/shabat/test"
    ).status_code == 200

def generate_shabat_tasks():
    return requests.get(
        f"http://{SERVER_IP}:{SERVER_PORT}/shabat/generate_tasks"
    ).json()

def get_tasks():
    return requests.get(
        f"http://{SERVER_IP}:{SERVER_PORT}/shabat/schedule"
    ).json()

def set_tasks(tasks):
    return requests.post(
        f"http://{SERVER_IP}:{SERVER_PORT}/shabat/schedule",
        data=json.dumps(tasks)
    )

def clear_tasks():
    return requests.delete(
        f"http://{SERVER_IP}:{SERVER_PORT}/shabat/schedule"
    )
