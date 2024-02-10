import os
import json
import isodate
import pytz
import datetime
import requests

from glocaltokens.client import GLocalAuthenticationTokens

from tools.logger import logger
import xml.etree.ElementTree as ET
from connections.connection import Connection

from devices.google import NestDoorbellDevice

class GoogleConnection(Connection):

    NAME = "Google"

    DEVICES = {
        "Doorbell": NestDoorbellDevice,
    }
    
    NEST_SCOPE = "oauth2:https://www.googleapis.com/auth/nest-account"

    def __init__(self, *args, **kwargs):
        super(GoogleConnection, self).__init__(*args, **kwargs)
        
        if not (self._connection_params.get("master_token") and self._connection_params.get("username") and self._connection_params.get("password")):
            raise Exception("Google master_token/username/password missing")
        
        self._google_auth = GLocalAuthenticationTokens(
            master_token=self._connection_params.get("master_token"), 
            username=self._connection_params.get("username"), 
            password=self._connection_params.get("password"),
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
