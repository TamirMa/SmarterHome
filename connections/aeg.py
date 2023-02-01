import pyelectroluxconnect

from connections.connection import Connection

class AEGConnection(Connection):

    NAME = "AEG"

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
        self._ses.login()

    def get_all_appliances(self):
        appllist = self._ses.getAppliances()
        print(appllist)
        for appliance in appllist:  
	        print(self._ses.getApplianceConnectionState(appliance))

    def get_profile_for_appliance(self, appliance):
        print(self._ses.getApplianceProfile(appliance))

    def send_command(self, appliance, hacl, value, destination):
        self._ses.setHacl(appliance, hacl, value, destination)
