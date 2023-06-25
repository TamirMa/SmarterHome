
from enum import Enum
from devices.generic import FanInterface, GenericDevice

class BroadlinkFanDevice(GenericDevice, FanInterface):

    class COMMANDS(str, Enum):
        LIGHT = 'Light'
        FAN2 = 'Fan2'
        FAN3 = 'Fan3'
        STOP_FAN = 'FanOff'

    def toggle(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.LIGHT)

    def start_fan2(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.FAN2)

    def start_fan3(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.FAN3)

    def stop_fan(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.STOP_FAN)


