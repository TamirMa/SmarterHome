import time
from devices.aeg import AEGOven
import pyelectroluxconnect

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
        
        self._ses = pyelectroluxconnect.Session(
            self._connection_params.get("username"), 
            self._connection_params.get("password"), 
            region="emea", 
            tokenFileName = ".electrolux-token", 
            country = "FR", 
            language = None, 
            deviceId = "CustomDeviceId", 
            verifySsl = True, 
            regionServer=None, 
            customApiKey=None, 
            customApiBrand=None
        )
        self._last_login = None
        self._ses.login()

    def check_login(self):
        if self._last_login == None or self._last_login + 6 * 60 * 60 < time.time():
            self._ses.login()
            self._last_login = time.time()

    def get_all_appliances(self):
        self.check_login()
        appllist = self._ses.getAppliances()
        print(appllist)
        for appliance in appllist:  
            print(self._ses.getApplianceConnectionState(appliance))

    def get_profile_for_appliance(self, appliance):
        self.check_login()
        print(self._ses.getApplianceProfile(appliance))

    def send_command(self, appliance, hacl, value, destination):
        self.check_login()
        print (f"Sending command {destination+':'+hacl} with value {value} to {appliance}")
        self._ses.setHacl(appliance, hacl, value, destination)

    def read_state(self, appliance):
        self.check_login()
        return self._ses.getApplianceState(appliance, paramName = None, rawOutput = False)