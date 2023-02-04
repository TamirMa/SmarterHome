import os
import json

from connections.aeg import AEGConnection
from connections.broadlink import BroadlinkConnection
from connections.homeconnect import HomeConnectConnection
from connections.shelly import ShellyConnection
from connections.smartthings import SmartThingsConnection
from connections.tuya import TuyaConnection
from connections.yeelight import YeelightConnection

CONNECTION_PARAMS_FILE = os.getenv('CONNECTION_PARAMS_FILE')
DEVICES_FILE = os.getenv('DEVICES_FILE')

if CONNECTION_PARAMS_FILE == None:
    raise Exception("ConnectionsParams file is mandetory")

if DEVICES_FILE == None:
    raise Exception("Devices file is mandetory")

class DeviceManager(object):

    CONNECTIONS = [
        AEGConnection,
        TuyaConnection,
        ShellyConnection,
        BroadlinkConnection,
        HomeConnectConnection,
        SmartThingsConnection,
        YeelightConnection,
    ]

    def __init__(self) -> None:
        if not os.path.exists(CONNECTION_PARAMS_FILE):
            raise Exception(f"Couldn't open the ConnectionsParams file at '{CONNECTION_PARAMS_FILE}'")

        connection_params = json.loads(open(CONNECTION_PARAMS_FILE, "r").read())
        self._connections = {
            ConnectionClass.NAME: ConnectionClass(connection_params.get(ConnectionClass.NAME))
            for ConnectionClass in self.CONNECTIONS
        }

        if not os.path.exists(DEVICES_FILE):
            raise Exception(f"Couldn't open the Devices file at '{DEVICES_FILE}'")

        all_devices = json.loads(open(DEVICES_FILE, "r").read())
        self._devices = {
            device_definition["name"] : self._connections.get(device_definition["connection"]).create_device(device_definition) if self._connections.get(device_definition["connection"]) else None
            for device_definition in all_devices
        }
        
    def get_device_by_name(self, device_name):
        print (f"Getting device {device_name}")
        device = self._devices.get(device_name)
        if not device:
            raise Exception(f"Couldn't get the device {device_name}")

        return device