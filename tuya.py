import tinytuya
import json

from devices import SwitchDevice

class TuyaConnection(object):
    def __init__(self, devices_json_path):
        self._devices_json = json.loads(open(devices_json_path, "r").read())

class TuyaBaseDevice(object):
    def __init__(self, tuya_connection, device_id, sub_device_id=1):
        device_dict = tuya_connection.get_dict_of_device(device_id)
        self._d = tinytuya.OutletDevice(
           dev_id=device_dict["device_id"],
           address='',
           local_key=device_dict["local_key"],
           version=device_dict["protocol_version"],
        )

        self._sub_device_id = sub_device_id

class TuyaSwitchDevice(TuyaBaseDevice, SwitchDevice):
    def turn_off(self):
        self._d.set_status(True, self._sub_device_id)

    def turn_off(self):
        self._d.set_status(False, self._sub_device_id)

