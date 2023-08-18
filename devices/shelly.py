
from devices.generic import LightInterface, GenericDevice
import ShellyPy


class ShellyBaseDevice(GenericDevice):
    def __init__(self, *args, **kwargs):
        super(ShellyBaseDevice, self).__init__(*args, **kwargs)
        self._d = ShellyPy.Shelly(self._device_id)
        
class ShellySwitchDevice(ShellyBaseDevice, LightInterface):
    def turn_on(self):
        self._d.relay(self._sub_device_id if self._sub_device_id != None else 0, turn=True)

    def turn_off(self):
        self._d.relay(self._sub_device_id if self._sub_device_id != None else 0, turn=False)

    def is_on(self):
        relay_status = self._d.relay(self._sub_device_id if self._sub_device_id != None else 0)
        if isinstance(self._d, ShellyPy.ShellyGen1):
            return relay_status.get("ison", False)
        if isinstance(self._d, ShellyPy.ShellyGen2):
            return relay_status.get("output", False)

    def get_consumption(self):
        if isinstance(self._d, ShellyPy.ShellyGen1):
            try:
                consumption_dict = self._d.meter(self._sub_device_id if self._sub_device_id != None else 0)
                return consumption_dict.get("power")
            except ShellyPy.error.NotFound:
                return None
        if isinstance(self._d, ShellyPy.ShellyGen2):
            try:
                consumption_dict = self._d.relay(self._sub_device_id if self._sub_device_id != None else 0)
                return consumption_dict.get("apower")
            except ShellyPy.error.NotFound:
                return None
