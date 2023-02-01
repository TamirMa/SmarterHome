
from devices.generic import SwitchInterface, GenericDevice


class TuyaBaseDevice(GenericDevice):
    def __init__(self, *args, **kwargs):
        super(TuyaBaseDevice, self).__init__(*args, **kwargs)
        self._d = self._connection.initialize_device(self._device_id)

class TuyaSwitchDevice(TuyaBaseDevice, SwitchInterface):
    def turn_on(self):
        self._d.set_status(True, self._sub_device_id)

    def turn_off(self):
        self._d.set_status(False, self._sub_device_id)

    def is_on(self):
        return self._d.status()['dps'][str(self._sub_device_id)] == True

