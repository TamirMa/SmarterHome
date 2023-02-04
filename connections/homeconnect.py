import json
import os
from devices.homeconnect import BoschDishwasher
from homeconnect import HomeConnectAPI

from connections.connection import Connection

class HomeConnectConnection(Connection):

    NAME = "HomeConnect"

    DEVICES = {
        "BoschDishwasher": BoschDishwasher,
    }

    TOKEN_CACHE = ".home_connect.token"

    def __init__(self, *args, **kwargs):
        super(HomeConnectConnection, self).__init__(*args, **kwargs)
        
        if not (self._connection_params.get("clientId") and self._connection_params.get("clientSecret") and self._connection_params.get("redirectURI")):
            raise Exception("HomeConnect parameters are missing")
        
        token = None
        if os.path.exists(HomeConnectConnection.TOKEN_CACHE):
            token = json.loads(open(HomeConnectConnection.TOKEN_CACHE, "r").read())

        client_id = self._connection_params.get("clientId")
        client_secret = self._connection_params.get("clientSecret")
        redirect_uri = self._connection_params.get("redirectURI")

        self._hc = HomeConnectAPI(token, client_id, client_secret, redirect_uri, token_updater=self.update_token_cache)
        
    def update_token_cache(self, token):
        with open(HomeConnectConnection.TOKEN_CACHE, "w") as f:
            json.dump(token, f)

    def initialize_device(self, device_id):
        all_appliances = self._hc.get_appliances()
        for appliance in all_appliances:
            if appliance.haId == device_id:
                return appliance
        raise Exception(f"Couldn't find the device_id '{device_id}' in this HomeConnect account")
        