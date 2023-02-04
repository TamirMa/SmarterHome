
from devices.generic import SwitchInterface, GenericDevice


class SmartThingsBaseDevice(GenericDevice):
    def __init__(self, *args, **kwargs):
        super(SmartThingsBaseDevice, self).__init__(*args, **kwargs)
        self._d = self._connection.initialize_device(self._device_id)

class SamsungTVDevice(SmartThingsBaseDevice):
    def switch_on(self):
        self._d.switch_on()

    def switch_off(self):
        self._d.switch_off()
