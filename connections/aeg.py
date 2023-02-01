import pyelectroluxconnect

class AEGConnection(object):
    def __init__(self, username, password):
        self._ses = pyelectroluxconnect.Session(
            username, 
            password, 
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
