
from devices.generic import SwitchDevice


class TuyaBaseDevice(object):
    def __init__(self, tuya_connection, device_id, sub_device_id=1):
        self._d = tuya_connection.initialize_device(device_id)
        self._sub_device_id = sub_device_id

class TuyaSwitchDevice(TuyaBaseDevice, SwitchDevice):
    def turn_off(self):
        self._d.set_status(True, self._sub_device_id)

    def turn_off(self):
        self._d.set_status(False, self._sub_device_id)

