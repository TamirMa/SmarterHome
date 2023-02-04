from connections.connection import Connection
from devices.yeelight import YeelightSwitchDevice

class YeelightConnection(Connection):

    NAME = "Yeelight"

    DEVICES = {
        "Light": YeelightSwitchDevice,
    }


    