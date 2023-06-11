import requests
from devices.smartthings import SamsungTVDevice
from tools.logger import logger
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
        
        self._pat = self._connection_params.get("token")

    def send_command(self, device_id, component, capability, command):
        res = requests.post(
            f"https://api.smartthings.com/v1/devices/{device_id}/commands", json={
                 "commands": [
                     {
                         "component": component,
                         "capability": capability,
                         "command": command,
                     }
                 ]
             }, headers={"Authorization": "Bearer " + self._pat})
        logger.info(res.content)