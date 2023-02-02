import base64
from enum import Enum
from tkinter import COMMAND
from connections.connection import Connection
from devices.broadlink import BroadlinkFanDevice

import json
import broadlink

class BroadlinkConnection(Connection):

    NAME = "Broadlink"

    DEVICES = {
        "Fan": BroadlinkFanDevice,
    }

    def __init__(self, *args, **kwargs):
        super(BroadlinkConnection, self).__init__(*args, **kwargs)
        
        commands_json_path = self._connection_params.get("commands_json_path")
        self._devices_json = json.loads(open(commands_json_path, "r").read())

        self._device = broadlink.hello(self._connection_params.get("broadlink_ip_addr"))

    def send_command_to_device(self, device_id, command: BroadlinkFanDevice.COMMANDS):
        commands = self._devices_json.get(device_id, {})
        packet = commands.get(command)
        self._device.auth()
        self._device.send_data(base64.b64decode(packet.encode()))


    

