from enum import Enum
from devices.aeg import AEGOven
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
@control_router.get("/light/{device_id}")
async def change_light_state(device_id, light_state: LightState):
    light : SwitchInterface = context.devices.get_device_by_name(device_id)
    if light_state == LightState.ON:
        light.turn_on()
    elif light_state == LightState.OFF:
        light.turn_off()
    else:
        raise Exception(f"Invalid state for light {light_state}")
    
@control_router.post("/oven/{device_id}/on")
async def turn_on_oven(device_id, program: AEGOven.PROGRAMS, temperature: int):
    oven : AEGOven = context.devices.get_device_by_name(device_id)
    oven.turn_on(program, temperature)
    return {"message": f"Getting the status for the device {oven}"}

@control_router.post("/oven/{device_id}/off")
async def turn_off_oven(device_id):
    oven : AEGOven = context.devices.get_device_by_name(device_id)
    oven.turn_off()
    return {"message": f"Getting the status for the device {oven}"}
