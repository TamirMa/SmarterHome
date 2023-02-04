from enum import Enum
from devices.aeg import AEGOven
from devices.generic import CurtainInterface, SwitchInterface
from devices.homeconnect import BoschDishwasher
from devices.smartthings import SamsungTVDevice
from starlette_context import context
from fastapi import APIRouter

control_router = APIRouter()

class LightState(str, Enum):
    ON = "on"
    OFF = "off"
    
class CurtainState(str, Enum):
    OPEN = "open"
    CLOSE = "close"
    STOP = "stop"

class TVCommands(str, Enum):
    ON = "On"
    OFF = "Off"
    # MUTE = "Mute"


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
    
@control_router.post("/curtain/{device_id}/state")
async def change_light_state(device_id, curtain_state: CurtainState):
    curtain : CurtainInterface = context.devices.get_device_by_name(device_id)
    if curtain_state == CurtainState.OPEN:
        curtain.open()
    elif curtain_state == CurtainState.CLOSE:
        curtain.close()
    elif curtain_state == CurtainState.STOP:
        curtain.stop()
    else:
        raise Exception(f"Invalid state for curtain {curtain_state}")

@control_router.post("/oven/{device_id}/on")
async def turn_on_oven(device_id, program: AEGOven.PROGRAMS, temperature: int):
    oven : AEGOven = context.devices.get_device_by_name(device_id)
    oven.turn_on(program, temperature)
    return True

@control_router.post("/oven/{device_id}/off")
async def turn_off_oven(device_id):
    oven : AEGOven = context.devices.get_device_by_name(device_id)
    oven.turn_off()
    return True

@control_router.post("/dishwasher/{device_id}/start")
async def turn_on_oven(device_id, program: BoschDishwasher.PROGRAMS):
    dishwasher : BoschDishwasher = context.devices.get_device_by_name(device_id)
    dishwasher.start(program)
    return True

@control_router.post("/tv/{device_id}")
async def change_light_state(device_id, tv_command: TVCommands):
    tv : SamsungTVDevice = context.devices.get_device_by_name(device_id)
    if tv_command == TVCommands.ON:
        tv.switch_on()
    elif tv_command == TVCommands.OFF:
        tv.switch_off()
    else:
        raise Exception(f"Invalid command for tv {tv_command}")
    