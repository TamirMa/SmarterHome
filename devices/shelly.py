
from devices.generic import LightInterface, GenericDevice, SocketInterface
import ShellyPy


class ShellyBaseDevice(GenericDevice):
    def __init__(self, *args, **kwargs):
        super(ShellyBaseDevice, self).__init__(*args, **kwargs)
        try:
            self._d = ShellyPy.Shelly(self._device_id)
        except ValueError as e:
            if "Generation 3 not supported" in str(e):
                self._d = ShellyPy.ShellyGen2(self._device_id)
            else:
                raise
        
class ShellySwitchDevice(ShellyBaseDevice):
    def turn_on(self):
        self._d.relay(self._sub_device_id if self._sub_device_id != None else 0, turn=True)

    def turn_off(self):
        self._d.relay(self._sub_device_id if self._sub_device_id != None else 0, turn=False)

    def is_on(self):
        relay_status = self._d.relay(self._sub_device_id if self._sub_device_id != None else 0)
        ison = relay_status.get("ison")
        if ison != None:
            return ison
        return relay_status.get("output", False)

    def get_consumption(self):
        try:
            consumption_dict = self._d.meter(self._sub_device_id if self._sub_device_id != None else 0)
            return consumption_dict.get("power")
        except NotImplementedError:
            try:
                consumption_dict = self._d.relay(self._sub_device_id if self._sub_device_id != None else 0)
                return consumption_dict.get("apower")
            except NotImplementedError:
                return None

class ShellyLightDevice(ShellySwitchDevice, LightInterface):
    pass

class ShellySocketDevice(ShellySwitchDevice, SocketInterface):
    pass