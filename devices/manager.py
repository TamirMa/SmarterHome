import os
import json

from connections.aeg import AEGConnection
from connections.tuya import TuyaConnection

CONNECTION_PARAMS_FILE = os.getenv('CONNECTION_PARAMS_FILE')

if CONNECTION_PARAMS_FILE == None:
    raise Exception("ConnectionsParams file is mandetory")

class DeviceManager(object):

    CONNECTIONS = [
        AEGConnection,
        # TuyaConnection,
    ]

    def __init__(self) -> None:
        if not os.path.exists(CONNECTION_PARAMS_FILE):
            raise Exception(f"Couldn't open the ConnectionsParams file at '{CONNECTION_PARAMS_FILE}'")

        connection_params = json.loads(open(CONNECTION_PARAMS_FILE, "r").read())
        self._connections = {
            ConnectionClass.NAME: ConnectionClass(connection_params.get(ConnectionClass.NAME))
            for ConnectionClass in self.CONNECTIONS
        }

        # self._devices = {
        #     "aeg_oven" : AEGOven(self._connections.get("aeg"), "")
        # }
        
    def get_device_by_name(self, device_name):
        print (f"Getting device {device_name}")