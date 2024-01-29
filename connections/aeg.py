
from devices.aeg import AEGOven
from pyelectroluxocp.oneAppApi import OneAppApi
from tools.logger import logger

from connections.connection import Connection


class AEGConnection(Connection):

    NAME = "AEG"

    DEVICES = {
        "Oven": AEGOven,
    }
    
    def __init__(self, *args, **kwargs):
        super(AEGConnection, self).__init__(*args, **kwargs)
        
        if not (self._connection_params.get("username")  and self._connection_params.get("password")):
            raise Exception("AEG username/password missing")
        
        self._aeg_api = OneAppApi(
            self._connection_params.get("username"), 
            self._connection_params.get("password"),
        )

    async def get_all_appliances(self):
        logger.info(await self._aeg_api.get_appliances_list(includeMetadata=False))

    async def send_command(self, appliance_id, command_dict):
        logger.info (f"Sending command {command_dict} to {appliance_id}")
        await self._aeg_api.execute_appliance_command(appliance_id, command_dict)

    async def get_device_property(self, appliance_id, property_id):
        device_state = await self._aeg_api.get_appliance_status(appliance_id, includeMetadata=False)
        return device_state["properties"]["reported"].get(property_id)
