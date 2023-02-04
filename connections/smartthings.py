from devices.smartthings import SamsungTVDevice
import SmartThings

from connections.connection import Connection

class SmartThingsConnection(Connection):

    NAME = "SmartThings"

    DEVICES = {
        "SamsungTV": SamsungTVDevice,
    }

    def __init__(self, *args, **kwargs):
        super(SmartThingsConnection, self).__init__(*args, **kwargs)
        
        if not self._connection_params.get("token"):
            raise Exception("SmartThings token is missing")
        
        pat = self._connection_params.get("token")

        self._st = SmartThings.Account(pat)
        
    def initialize_device(self, device_id):    
        all_devices = self._st.devices()
        for device in all_devices:
            if device.device_id == device_id:
                return device
        raise Exception(f"Couldn't find the device_id '{device_id}' in this SmartThings account")