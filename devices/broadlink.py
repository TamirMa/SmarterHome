
from enum import Enum
from devices.generic import FanInterface, GenericDevice, LightInterface

class BroadlinkFanDevice(GenericDevice, FanInterface, LightInterface):

    class COMMANDS(str, Enum):
        LIGHT = 'Light'
        FAN2 = 'Fan2'
        FAN3 = 'Fan3'
        STOP_FAN = 'FanOff'
    
    class STATES(str, Enum):
        LIGHT_OFF = 'LightOff'
        LIGHT_ON = 'LightOn'
        FAN_OFF = 'FanOff'
        FAN1 = 'Fan2'
        FAN2 = 'Fan2'
        FAN3 = 'Fan3'
        FAN4 = 'Fan3'
        FAN5 = 'Fan3'
        FAN6 = 'Fan3'

    CONSUMPTION_MAP = [
        (0, 18,  (STATES.LIGHT_OFF, STATES.FAN_OFF)),
        (19,23, (STATES.LIGHT_ON, STATES.FAN_OFF)),
    ]

    def _update_state(self):
        if self._linked_device is not None:

            consumption = self._linked_device.get_consumption()
            # Consumption can be None when the device doesn't support measuring consumption
            if consumption != None:
                for start_level, stop_level, (light_state, fan_state) in self.CONSUMPTION_MAP:
                    if consumption >= start_level and consumption <= stop_level:
                        self._light_state = light_state
                        self._fan_state = fan_state
                        return
        
        self._light_state = self.STATES.LIGHT_OFF
        self._fan_state = self.STATES.FAN_OFF

    def is_on(self):
        self._update_state()
        return self._light_state == self.STATES.LIGHT_ON

    def toggle(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.LIGHT)
    
    def turn_on(self):
        if not self.is_on():
            self.toggle()
        
    def turn_off(self):
        if self.is_on():
            self.toggle()
        
    def start_fan2(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.FAN2)

    def start_fan3(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.FAN3)

    def stop_fan(self):
        self._connection.send_command_to_device(self._device_id, BroadlinkFanDevice.COMMANDS.STOP_FAN)


