import os
import json

from connections.aeg import AEGConnection
from connections.broadlink import BroadlinkConnection
from connections.homeconnect import HomeConnectConnection
from connections.shelly import ShellyConnection
from connections.smartthings import SmartThingsConnection
from connections.tuya import TuyaConnection
from connections.yeelight import YeelightConnection
from devices.generic import CurtainInterface, DishwasherInterface, LightInterface, OvenInterface, SocketInterface

from tools.logger import logger

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

        self._connections = {}
        self._devices = {}

        # self.reload_connections()
        # self.reload_devices()

    def reload_connections(self):
        connection_params = json.loads(open(CONNECTION_PARAMS_FILE, "r").read())
        connections = { }
        for ConnectionClass in self.CONNECTIONS:
            try:
                connection = ConnectionClass(connection_params.get(ConnectionClass.NAME))
                connections[ConnectionClass.NAME] = connection
            except:
                logger.exception(f"Couldn't initialize connection {ConnectionClass}, skipping")

        self._connections = connections

    def reload_devices(self):

        if not os.path.exists(DEVICES_FILE):
            raise Exception(f"Couldn't open the Devices file at '{DEVICES_FILE}'")

        all_devices = json.loads(open(DEVICES_FILE, "r").read())
        devices = { }

        for device_definition in all_devices:
            connection = self._connections.get(device_definition["connection"])
            if not connection:
                logger.error(f"Couldn't find a connection for device {device_definition['name']}")
                continue
            try:
                devices[device_definition["name"]] = connection.create_device(device_definition)
            except Exception as e:
                logger.exception(f"Exception when creating a device: {device_definition['name']}, {device_definition}")

        self._devices = devices

        
    def get_device_by_name(self, device_name):
        logger.debug (f"Getting device {device_name}")
        device = self._devices.get(device_name)
        if not device:
            logger.exception(f"Couldn't get the device {device_name}")
            return

        return device

    def get_devices_by_type(self, device_type=None):
        logger.debug (f"Getting devices list ({device_type})")
        device_class = None
        if device_type == "light":
            device_class = LightInterface
        elif device_type == "oven":
            device_class = OvenInterface
        elif device_type == "dishwasher":
            device_class = DishwasherInterface
        elif device_type == "curtain":
            device_class = CurtainInterface
        elif device_type == "socket":
            device_class = SocketInterface
        elif device_type == "all":
            pass
        else:
            raise Exception(f"Unknow device type {device_type}")

        return [
            device_id
            for device_id, device in self._devices.items()
            if device_type == None or isinstance(device, device_class)
        ]
        