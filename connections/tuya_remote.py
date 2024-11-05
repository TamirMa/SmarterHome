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
        assert response["success"] == True

    def set_properties(self, device_id, properties_dict):
        commands = {'properties': json.dumps(properties_dict)}
        response = self._tuya_api.post(f'/v2.0/cloud/thing/{device_id}/shadow/properties/issue', commands)
        assert response["success"] == True
        time.sleep(10)

    def get_properties(self, device_id):
        response = self._tuya_api.get(f'/v2.0/cloud/thing/{device_id}/shadow/properties')
        return response["result"]["properties"]
