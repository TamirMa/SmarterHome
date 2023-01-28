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

class AEGOven(object):
    def __init__(self, aeg_connection, appliance):
        self._aeg_connection = aeg_connection
        self._appliance = appliance

    class PROGRAMS:
        TRUE_FAN_COOKING = '871D'
        GRILL = 'C6EA'
        PIZZA = '70ED'
        CONVENTIONAL = '039C'
        # {'7150': 'Turbo Grilling'}
        # {'2548': 'Moist Fan Baking'},
        # {'C6EA': 'Grill'},
        # {'039C': 'Conventional Cooking'},
        # {'70ED': 'Pizza Function'},
        # {'1EA8': 'Frozen Foods'},
        # {'1510': 'Bottom Heat'},
        # {'9CCD': 'Normal'},
        # {'31C9': 'Steam Bake'},
        # {'71A9': 'Quick'},
        # {'98E8': 'Intense'},

    def turn_on(self):
        self.set_program(self.PROGRAMS.TRUE_FAN_COOKING)
        self.set_temperature(180)
        self.light_on()
        # self._aeg_connection.send_command(self._appliance, "0x0401", "871D", "OV1") # status
        self._aeg_connection.send_command(self._appliance, "0x0403", "2", "OV1") # start

    def turn_off(self):
        self._aeg_connection.send_command(self._appliance, "0x0403", "3", "OV1") # stop
        
    def light_on(self):
        self._aeg_connection.send_command(self._appliance, "0x0490", "1", "OV1") # light
        
    def light_off(self):
        self._aeg_connection.send_command(self._appliance, "0x0490", "0", "OV1") # light
    
    def set_program(self, program_code):
        self._aeg_connection.send_command(self._appliance, "0x1440", "0x" + program_code, "OV1")
    
    def set_temperature(self, temperature):
        self._aeg_connection.send_command(self._appliance, "0x0432", [{"1":str(temperature)},{"3":"0"},{"0":"0"}], "OV1")

    
