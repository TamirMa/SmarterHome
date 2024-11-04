import json
from connections.connection import Connection
from devices.tuya import TuyaBasicDevice, TuyaACDevice, TuyaHeaterDevice, TuyaLightDevice, TuyaSocketDevice, TuyaFingerbotDevice, TuyaCurtainDevice
import tinytuya

class TuyaConnection(Connection):

    NAME = "Tuya"

    DEVICES = {
        "Hub": TuyaBasicDevice,
        "Light": TuyaLightDevice,
        "Socket": TuyaSocketDevice,
        "Curtain": TuyaCurtainDevice,
        "AC": TuyaACDevice,
        "Heater": TuyaHeaterDevice,
        "Fingerbot": TuyaFingerbotDevice,
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

    def initialize_basic_device(self, device_id, linked_device=None):
        device_dict = self.get_dict_of_device(device_id)
        return tinytuya.Device(
           dev_id=device_dict["id"],
        #    address=device_dict["ip"],
           local_key=device_dict["key"],
           parent=linked_device._d if linked_device is not None else None,
           version="3.4",
        )
    
    def initialize_outlet_device(self, device_id, linked_device=None):
        device_dict = self.get_dict_of_device(device_id)
        return tinytuya.OutletDevice(
           dev_id=device_dict["id"],
        #    address=device_dict["ip"],
           local_key=device_dict["key"],
           parent=linked_device,
           version="3.4",
        )
