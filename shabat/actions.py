from devices.manager import DeviceType

from server.control_router import FanState, LightState, OvenState, SocketState
from tools import actions
from tools.logger import logger


def run_action_command(command_details, test=False):
    command_type = command_details.get("type")
    command = command_details.get("command")
    device_id = command_details.get("device_id")

    if command_type == DeviceType.Lights:
        if command == LightState.OFF:
            actions.change_light_state(device_id, LightState.OFF)
        elif command == LightState.ON:
            actions.change_light_state(device_id, LightState.ON)

    elif command_type == DeviceType.Sockets:
        if command == SocketState.OFF:
            actions.change_socket_state(device_id, SocketState.OFF)
        elif command == SocketState.ON:
            actions.change_socket_state(device_id, SocketState.ON)

    elif command_type == DeviceType.Ovens:
        if command == OvenState.ON:
            actions.turn_on_oven(device_id)
        elif command == OvenState.OFF:
            actions.turn_off_oven(device_id)

    elif command_type == DeviceType.Fans:
        if command == FanState.FAN3:
            actions.change_fan_state(device_id, FanState.FAN3)
        elif command == FanState.FAN2:
            actions.change_fan_state(device_id, FanState.FAN3)
        elif command == FanState.STOP:
            actions.change_fan_state(device_id, FanState.STOP)

    elif command_type == DeviceType.Dishwashers:
        if test:
            logger.info("Ignoring test command for starting the dishwasher")
            return
            
        if command == "start":
            actions.start_dishwasher(device_id)

def run_action_commands(action_commands, test=False):
    for command in action_commands:
        run_action_command(command, test=test)
