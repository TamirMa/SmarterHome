
from devices.generic import GenericDevice


class AEGOven(GenericDevice):

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
        # self._connection.send_command(self._device_id, "0x0401", "871D", "OV1") # status
        self._connection.send_command(self._device_id, "0x0403", "2", "OV1") # start

    def turn_off(self):
        self._connection.send_command(self._device_id, "0x0403", "3", "OV1") # stop
        
    def light_on(self):
        self._connection.send_command(self._device_id, "0x0490", "1", "OV1") # light
        
    def light_off(self):
        self._connection.send_command(self._device_id, "0x0490", "0", "OV1") # light
    
    def set_program(self, program_code):
        self._connection.send_command(self._device_id, "0x1440", "0x" + program_code, "OV1")
    
    def set_temperature(self, temperature):
        self._connection.send_command(self._device_id, "0x0432", [{"1":str(temperature)},{"3":"0"},{"0":"0"}], "OV1")

    
