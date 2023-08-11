import json
from connections.connection import Connection
from devices.tuya import TuyaACDevice, TuyaLightDevice, TuyaSocketDevice, TuyaSwitchDevice, TuyaCurtainDevice
import tinytuya

class TuyaConnection(Connection):

    NAME = "Tuya"

    DEVICES = {
        "Light": TuyaLightDevice,
        "Socket": TuyaSocketDevice,
        "Curtain": TuyaCurtainDevice,
        "AC": TuyaACDevice,
    }

    def __init__(self, *args, **kwargs):
        super(TuyaConnection, self).__init__(*args, **kwargs)
        
        devices_json_path = self._connection_params.get("devices_json_path")
        self._devices_json = json.loads(open(devices_json_path, "r").read())

    def get_dict_of_device(self, device_id):
        for device_info in self._devices_json:
            if device_info["id"] == device_id:
                return device_info
        raise Exception(f"Couldn't find the device_id '{device_id}' in the definitions file")

    def initialize_device(self, device_id):
        device_dict = self.get_dict_of_device(device_id)
        return tinytuya.OutletDevice(
           dev_id=device_dict["id"],
        #    address=device_dict["ip"],
           local_key=device_dict["key"],
           version="3.4",
        )
