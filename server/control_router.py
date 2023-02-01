from enum import Enum
from devices.generic import SwitchInterface
from starlette_context import context
from fastapi import APIRouter

control_router = APIRouter()

class LightState(str, Enum):
    ON = "on"
    OFF = "off"
    
@control_router.get("/light/{device_id}/state")
async def get_light_state(device_id):
    light : SwitchInterface = context.devices.get_device_by_name(device_id)
    return light.is_on()


@control_router.post("/light/{device_id}")
async def change_light_state(device_id, light_state: LightState):
    light : SwitchInterface = context.devices.get_device_by_name(device_id)
    if light_state == LightState.ON:
        light.turn_on()
    elif light_state == LightState.OFF:
        light.turn_off()
    else:
        raise Exception(f"Invalid state for light {light_state}")
    
@control_router.get("/oven/{device_id}/status")
async def root(device_id):
    oven = context.devices.get_device_by_name(device_id)
    return {"message": f"Getting the status for the device {oven}"}
