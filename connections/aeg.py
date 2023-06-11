import time
from devices.aeg import AEGOven
import pyelectroluxconnect
from tools.logger import logger

from connections.connection import Connection


class AEGConnection(Connection):

    NAME = "AEG"

    DEVICES = {
        "Oven": AEGOven,
    }
    
    TOKEN_REFRESH_MINUTES = 60

    def __init__(self, *args, **kwargs):
        super(AEGConnection, self).__init__(*args, **kwargs)
        
        if not (self._connection_params.get("username")  and self._connection_params.get("password")):
            raise Exception("AEG username/password missing")
        
        self._ses = pyelectroluxconnect.Session(
            self._connection_params.get("username"), 
            self._connection_params.get("password"), 
            region="apac", 
            tokenFileName = ".electrolux-token", 
            country = "IL", 
            language = None, 
            deviceId = "CustomDeviceId", 
            verifySsl = True, 
            regionServer=None, 
            customApiKey=None, 
            customApiBrand=None
        )
        self._tokenTimestamp = None

    def _validateToken(self):
        if self._tokenTimestamp is None or ((self._tokenTimestamp + self.TOKEN_REFRESH_MINUTES * 60) < time.time()):
            logger.info("Getting AEG token")
            self._ses._createToken()
            self._ses.login()
            self._tokenTimestamp = time.time()

    def check_login(self):
        if self._last_login == None or self._last_login + 6 * 60 * 60 < time.time():
            self._ses.login()
            self._last_login = time.time()

    def get_all_appliances(self):
        self._validateToken()
        appllist = self._ses.getAppliances()
        logger.info(appllist)
        for appliance in appllist:  
            logger.info(self._ses.getApplianceConnectionState(appliance))

    def get_profile_for_appliance(self, appliance):
        self._validateToken()
        logger.info(self._ses.getApplianceProfile(appliance))

    def send_command(self, appliance, hacl, value, destination):
        self._validateToken()
        logger.info (f"Sending command {destination+':'+hacl} with value {value} to {appliance}")
        self._ses.setHacl(appliance, hacl, value, destination)

    def read_state(self, appliance):
        self._validateToken()
        return self._ses.getApplianceState(appliance, paramName = None, rawOutput = False)
