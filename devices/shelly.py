
from devices.generic import SwitchInterface, GenericDevice
import ShellyPy


class ShellyBaseDevice(GenericDevice):
    def __init__(self, *args, **kwargs):
        super(ShellyBaseDevice, self).__init__(*args, **kwargs)
        self._d = ShellyPy.Shelly(self._device_id)
        
class ShellySwitchDevice(ShellyBaseDevice, SwitchInterface):
    def turn_on(self):
        self._d.relay(0, turn=True)

    def turn_off(self):
        self._d.relay(0, turn=False)

    def is_on(self):
        super(ShellySwitchDevice, self).is_on()

