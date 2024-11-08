from enum import Enum
from devices.aeg import AEGOven
from devices.generic import AirConditionInterface, FingerbotInterface, HeaterInterface, CurtainInterface, FanInterface, LightInterface, OvenInterface, SocketInterface, SwitchInterface, TVInterface
from devices.homeconnect import BoschDishwasher
from devices.smartthings import SamsungTVDevice
from devices.manager import DeviceType
from starlette_context import context
from fastapi import APIRouter

control_router = APIRouter()

class OnOffDevice(str, Enum):
    ON = "on"
    OFF = "off"
    
class LightState(str, Enum):
    ON = "on"
    OFF = "off"

class HeaterState(str, Enum):
    ON = "on"
    OFF = "off"

class SocketState(str, Enum):
    ON = "on"
    OFF = "off"

class OvenState(str, Enum):
    ON = "on"
    OFF = "off"

class ACState(str, Enum):
    ON = "on"
    OFF = "off"
    
class CurtainState(str, Enum):
    OPEN = "open"
    CLOSE = "close"
    STOP = "stop"

class FanState(str, Enum):
    LIGHT_ON = "light_on"
    LIGHT_OFF = "light_off"
    LIGHT_TOGGLE = "light_toggle"
    FAN2 = "fan2"
    FAN3 = "fan3"
    STOP = "stop"
    START = "start"

class TVCommands(str, Enum):
    ON = "On"
    OFF = "Off"
    # MUTE = "Mute"

@control_router.get("/all")
async def get_all_devices_by_type(device_type:DeviceType):
    return context.devices.get_devices_by_type(device_type=device_type)

@control_router.get("/light/{device_id}/state")
async def get_light_state(device_id):
    device = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, LightInterface):
        raise Exception(f"This is not a light device ({device_id})")
    light : LightInterface = device
    return light.is_on()

@control_router.get("/light/{device_id}")
@control_router.post("/light/{device_id}")
async def change_light_state(device_id, light_state: LightState):
    device = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, LightInterface):
        raise Exception(f"This is not a light device ({device_id})")
    light : LightInterface = device
    
    if light_state == LightState.ON:
        light.turn_on()
    elif light_state == LightState.OFF:
        light.turn_off()
    else:
        raise Exception(f"Invalid state for light {light_state}")

@control_router.get("/light/{device_id}/toggle")
async def change_light_state_toggler(device_id):
    device = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, LightInterface):
        raise Exception(f"This is not a light device ({device_id})")
    light : LightInterface = device
    
    if light.is_on():
        light.turn_off()
    else:
        light.turn_on()
    
@control_router.get("/socket/{device_id}/state")
async def get_socket_state(device_id):
    device = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, SocketInterface):
        raise Exception(f"This is not a socket device ({device_id})")
    socket : SocketInterface = device
    return socket.is_on()

@control_router.post("/socket/{device_id}")
async def change_socket_state(device_id, socket_state: SocketState):
    device = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, SocketInterface):
        raise Exception(f"This is not a socket device ({device_id})")
    socket : SocketInterface = device
    
    if socket_state == SocketState.ON:
        socket.turn_on()
    elif socket_state == SocketState.OFF:
        socket.turn_off()
    else:
        raise Exception(f"Invalid state for socket {socket_state}")
     
@control_router.post("/fan/{device_id}")
@control_router.get("/fan/{device_id}")
async def change_fan_state(device_id, fan_state: FanState):
    device = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, FanInterface):
        raise Exception(f"This is not a fan device ({device_id})")
    fan : FanInterface = device
    
    if fan_state == FanState.FAN2:
        fan.start_fan2()
    elif fan_state == FanState.FAN3:
        fan.start_fan3()
    elif fan_state == FanState.STOP:
        fan.stop_fan()
    elif fan_state == FanState.START:
        fan.start_fan2()
    elif fan_state == FanState.LIGHT_TOGGLE:
        fan.toggle()
    elif fan_state == FanState.LIGHT_ON:
        fan.turn_on()
    elif fan_state == FanState.LIGHT_OFF:
        fan.turn_off()
    else:
        raise Exception(f"Invalid state for fan {fan_state}")

@control_router.post("/heater/{device_id}")
async def change_heater_state(device_id, 
                                heater_state: HeaterState,
                                timer : int = None, 
                                ):
    device = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, HeaterInterface):
        raise Exception(f"This is not a heater device ({device_id})")
    heater : HeaterInterface = device
    
    if heater_state == HeaterState.ON:
        heater.turn_on(timer=timer)
    elif heater_state == HeaterState.OFF:
        heater.turn_off()
    else:
        raise Exception(f"Invalid state for heater {heater_state}")

@control_router.post("/ac/{device_id}")
async def change_ac_state(device_id, 
                              ac_state : ACState, 
                              temperature : int = None, 
                              ac_mode : AirConditionInterface.AC_MODE = None, 
                              fan_speed : AirConditionInterface.FAN_SPEED = None):
    device = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, AirConditionInterface):
        raise Exception(f"This is not a AC device ({device_id})")
    ac : AirConditionInterface = device
    
    if ac_state == ACState.ON:
        ac.turn_on()

        if temperature != None:
            ac.set_temperature(temperature)
            
        if ac_mode != None:
            ac.set_mode(ac_mode)
        
        if fan_speed != None:
            ac.set_fan_speed(fan_speed)   
              
    elif ac_state == ACState.OFF:
        ac.turn_off()


@control_router.post("/curtain/{device_id}/state")
async def change_curtain_state(device_id, curtain_state: CurtainState):
    device = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, CurtainInterface):
        raise Exception(f"This is not a curtain device ({device_id})")
    curtain : CurtainInterface = device

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
    device : OvenInterface = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, OvenInterface):
        raise Exception(f"This is not a oven device ({device_id})")
    oven : OvenInterface = device
    return await oven.turn_on(program, temperature)
    

@control_router.post("/oven/{device_id}/off")
async def turn_off_oven(device_id):
    device : OvenInterface = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, OvenInterface):
        raise Exception(f"This is not a oven device ({device_id})")
    oven : OvenInterface = device
    return await oven.turn_off()

@control_router.post("/dishwasher/{device_id}/start")
async def turn_on_dishwasher(device_id, program: BoschDishwasher.PROGRAMS = BoschDishwasher.PROGRAMS.AUTO):
    dishwasher : BoschDishwasher = context.devices.get_device_by_name(device_id)
    dishwasher.start(program)
    return True

@control_router.post("/tv/{device_id}")
async def change_tv_state(device_id, tv_command: TVCommands):
    device = context.devices.get_device_by_name(device_id)
    if device == None or not isinstance(device, TVInterface):
        raise Exception(f"This is not a curtain device ({device_id})")
    tv : TVInterface = device

    if tv_command == TVCommands.ON:
        tv.switch_on()
    elif tv_command == TVCommands.OFF:
        tv.switch_off()
    else:
        raise Exception(f"Invalid command for tv {tv_command}")
    
@control_router.post("/fingerbot/{device_id}/click")
async def click_fingerbot(device_id, duration=0.2, arm_movement_percentages=100):
    fingerbot : FingerbotInterface = context.devices.get_device_by_name(device_id)
    fingerbot.click(duration=duration, arm_movement_percentages=arm_movement_percentages)
    return True