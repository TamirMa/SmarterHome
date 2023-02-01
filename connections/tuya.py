import json
import tinytuya

class TuyaConnection(object):
    def __init__(self, *args, **kwargs):
        super(TuyaConnection, self).__init__(*args, **kwargs)
        
        devices_json_path = self._connection_params.get("devices_json_path"), 
        self._devices_json = json.loads(open(devices_json_path, "r").read())

    def get_dict_of_device(self, device_id):
        return

    def initialize_device(self, device_id):
        device_dict = self.get_dict_of_device(device_id)
        self._d = tinytuya.OutletDevice(
           dev_id=device_dict["device_id"],
           address='',
           local_key=device_dict["local_key"],
           version=device_dict["protocol_version"],
        )
