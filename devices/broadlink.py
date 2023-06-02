
from enum import Enum
from devices.generic import LightInterface, GenericDevice
import broadlink


class BroadlinkFanDevice(GenericDevice, LightInterface):

    class COMMANDS(str, Enum):
        LIGHT = 'Light'
        FAN1 = 'Fan1'
        FAN_OFF = 'FanOff'

    def turn_on(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.LIGHT)

    def turn_off(self):
        self.turn_on()

    def is_on(self):
        return None

