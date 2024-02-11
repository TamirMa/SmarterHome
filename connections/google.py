import os
import json
import isodate
import pytz
import datetime
import requests

from tools.logger import logger
import xml.etree.ElementTree as ET
from connections.connection import Connection

from devices.google import NestDoorbellDevice

import glocaltokens.client

class GLocalAuthenticationTokensMultiService(glocaltokens.client.GLocalAuthenticationTokens):
    def __init__(self, *args, **kwargs) -> None:
        super(GLocalAuthenticationTokensMultiService, self).__init__(*args, **kwargs)

        self._last_access_token_service = None
    
    def get_access_token(self, service=glocaltokens.client.ACCESS_TOKEN_SERVICE) -> str | None:
        temp = glocaltokens.client.ACCESS_TOKEN_SERVICE

        glocaltokens.client.ACCESS_TOKEN_SERVICE = service
        if self._last_access_token_service != service:
            self.access_token_date = None
        res = super(GLocalAuthenticationTokensMultiService, self).get_access_token()
        self._last_access_token_service = service

        glocaltokens.client.ACCESS_TOKEN_SERVICE = temp

        return res

class GoogleConnection(Connection):

    NAME = "Google"

    DEVICES = {
        "Doorbell": NestDoorbellDevice,
    }
    
    NEST_SCOPE = "oauth2:https://www.googleapis.com/auth/nest-account"

    def __init__(self, *args, **kwargs):
        super(GoogleConnection, self).__init__(*args, **kwargs)
        
        if not (self._connection_params.get("master_token") and self._connection_params.get("username")):
            raise Exception("Google master_token/username missing")
        
        self._google_auth = GLocalAuthenticationTokensMultiService(
            master_token=self._connection_params.get("master_token"), 
            username=self._connection_params.get("username"), 
            password="FAKE_PASSWORD",
        )

    def make_nest_get_request(self, device_id : str, url : str, params={}):
        url = url.format(device_id=device_id)
        logger.debug(f"Sending request to: '{url}' with params: '{params}'")

        access_token = self._google_auth.get_access_token(service=GoogleConnection.NEST_SCOPE)
        if not access_token:
            raise Exception("Couldn't get a Nest access token")
        
        res = requests.get(
            url=url, 
            params=params, 
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        res.raise_for_status()
        return res.content

    def get_nest_camera_device_ids(self):

        homegraph_response = self._google_auth.get_homegraph()

        # This one will list all your home devices
        # One of them would be your Nest Camera, let's find it
        return [
            device.device_info.agent_info.unique_id
            for device in homegraph_response.home.devices
            if "action.devices.traits.CameraStream" in device.traits and "Nest" in device.hardware.model
        ]
