from connections.connection import Connection
from devices.shelly import ShellySocketDevice, ShellyLightDevice

class ShellyConnection(Connection):

    NAME = "Shelly"

    DEVICES = {
        "Light": ShellyLightDevice,
        "Socket": ShellySocketDevice,
    }


    