import time
import json

from connections.connection import Connection
from devices.tuya_remote import TuyaRemoteFingerbotDevice, TuyaRemoteFingerbotOvenDevice
from tuya_connector import TuyaOpenAPI

class TuyaRemoteConnection(Connection):

    NAME = "TuyaRemote"

    DEVICES = {
        "Fingerbot": TuyaRemoteFingerbotDevice,
        "FingerbotOven": TuyaRemoteFingerbotOvenDevice,
    }

    def __init__(self, *args, **kwargs):
        super(TuyaRemoteConnection, self).__init__(*args, **kwargs)
        
        if not (self._connection_params.get("accessId") and self._connection_params.get("accessKey") and self._connection_params.get("endpoint")):
            raise Exception("Tuya Remote accessId/accessKey/endpoint missing")
        
        self._tuya_api = TuyaOpenAPI(
            self._connection_params.get("endpoint"), 
            self._connection_params.get("accessId"), 
            self._connection_params.get("accessKey")
        )
        self._tuya_api.connect()

    def send_command(self, device_id, commands):
        commands = {'commands': commands}
        response = self._tuya_api.post(f'/v1.0/iot-03/devices/{device_id}/commands', commands)
        return response["success"] == True

    def set_properties(self, device_id, properties_dict, retries=10):
        commands = {'properties': json.dumps(properties_dict)}
        for i in range(retries):
            response = self._tuya_api.post(f'/v2.0/cloud/thing/{device_id}/shadow/properties/issue', commands)
            if response["success"] == True:
                # Wait for the property to update
                time.sleep(10)
                return True
            else:
                # Wait 5 seconds for the device to become online
                time.sleep(5)
        return False

    def get_properties(self, device_id):
        response = self._tuya_api.get(f'/v2.0/cloud/thing/{device_id}/shadow/properties')
        return response["result"]["properties"]
