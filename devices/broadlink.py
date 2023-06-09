
from enum import Enum
from devices.generic import FanInterface, LightInterface, GenericDevice
import broadlink


class BroadlinkFanDevice(GenericDevice, LightInterface, FanInterface):

    class COMMANDS(str, Enum):
        LIGHT = 'Light'
        FAN2 = 'Fan2'
        FAN3 = 'Fan3'
        STOP_FAN = 'FanOff'

    def turn_on(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.LIGHT)

    def turn_off(self):
        self.turn_on()

    def is_on(self):
        return None

    def start_fan2(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.FAN2)

    def start_fan3(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.FAN3)

    def stop_fan(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.STOP_FAN)


