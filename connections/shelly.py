from connections.connection import Connection
from devices.shelly import ShellySwitchDevice

class ShellyConnection(Connection):

    NAME = "Shelly"

    DEVICES = {
        "Light": ShellySwitchDevice,
        "Socket": ShellySwitchDevice,
    }


    