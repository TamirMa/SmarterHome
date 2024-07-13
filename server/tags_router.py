
from devices.manager import DeviceType
from starlette_context import context
from fastapi import APIRouter
import server.control_router as cr

tags_router = APIRouter()

@tags_router.get("/{tag}/devices")
async def get_all_devices_by_tag(tag):
    return context.devices.get_devices_by_tag(tag=tag)

@tags_router.get("/all")
async def get_all_tags():
    return context.devices.get_all_tags()

@tags_router.get("/{tag}/applystate")
async def apply_tag_state(tag, state : cr.OnOffDevice=cr.OnOffDevice.OFF):
    
    devices_of_tag = await get_all_devices_by_tag(tag)

    intersect = lambda x,y: list(set(x) & set(y))
    light_devices = intersect(devices_of_tag, await cr.get_all_devices_by_type(DeviceType.Lights))
    socket_devices = intersect(devices_of_tag, await cr.get_all_devices_by_type(DeviceType.Sockets))
    fan_devices = intersect(devices_of_tag, await cr.get_all_devices_by_type(DeviceType.Fans))
    heater_devices = intersect(devices_of_tag, await cr.get_all_devices_by_type(DeviceType.Heaters))
    ac_devices = intersect(devices_of_tag, await cr.get_all_devices_by_type(DeviceType.ACs))
    tv_devices = intersect(devices_of_tag, await cr.get_all_devices_by_type(DeviceType.TVs))

    for device in light_devices:
        await cr.change_light_state(device, cr.LightState.OFF if state == cr.OnOffDevice.OFF else cr.LightState.ON)
    for device in socket_devices:
        await cr.change_socket_state(device, cr.SocketState.OFF if state == cr.OnOffDevice.OFF else cr.SocketState.ON)
    for device in fan_devices:
        await cr.change_fan_state(device, cr.FanState.STOP if state == cr.OnOffDevice.OFF else cr.FanState.START)
    for device in ac_devices:
        await cr.change_ac_state(device, cr.ACState.OFF if state == cr.OnOffDevice.OFF else cr.ACState.ON)
    for device in heater_devices:
        await cr.change_heater_state(device, cr.HeaterState.OFF if state == cr.OnOffDevice.OFF else cr.HeaterState.ON)
    for device in tv_devices:
        await cr.change_tv_state(device, cr.TVCommands.OFF if state == cr.OnOffDevice.OFF else cr.TVCommands.ON)