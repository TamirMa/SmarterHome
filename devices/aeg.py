
from enum import Enum
from tkinter import COMMAND
from devices.generic import GenericDevice


class AEGOven(GenericDevice):

    class PROGRAMS(str, Enum):
        TRUE_FAN_COOKING = 'True Fan Cooking'
        TURBO_GRILLING = 'Turbo Grilling'
        MOIST_FAN_BAKING = 'Moist Fan Baking'
        GRILL = 'Grill'
        CONVENTIONAL_COOKING = 'Conventional Cooking'
        PIZZA_FUNCTION = 'Pizza Function'
        FROZEN_FOODS = 'Frozen Foods'
        BOTTOM_HEAT = 'Bottom Heat'
        NORMAL = 'Normal'
        STEAM_BAKE = 'Steam Bake'
        QUICK = 'Quick'
        INTENSE = 'Intense'

    PROGRAMS_MAPPING = {'True Fan Cooking': '871D',
        'Turbo Grilling': '7150',
        'Moist Fan Baking': '2548',
        'Grill': 'C6EA',
        'Conventional Cooking': '039C',
        'Pizza Function': '70ED',
        'Frozen Foods': '1EA8',
        'Bottom Heat': '1510',
        'Normal': '9CCD',
        'Steam Bake': '31C9',
        'Quick': '71A9',
        'Intense': '98E8'
    }
    
    class CODES:
        PROGRAM = "0x1440"
        TEMPERATURE = "0x0432"
        LIGHT = "0x0490"
        COMMAND = "0x0403"
        STATE = "0x0401"


    # def __init__(self, *args, **kwargs):
    #     super(AEGOven, self).__init__(*args, **kwargs)

    #     self._updated_state = self._connection.read_state(self._device_id)

    def turn_on(self, program, temperature):
        self._updated_state = self._connection.read_state(self._device_id)
        
        self._set_program(program)
        self._set_temperature(temperature)
        self._light_on()
        if self._updated_state["OV1:" + self.CODES.STATE]['stringValue'] != 'Running':
            self._connection.send_command(self._device_id, AEGOven.CODES.COMMAND, "2", "OV1") # start

    def turn_off(self):
        self._connection.send_command(self._device_id, AEGOven.CODES.COMMAND, "3", "OV1") # stop
        
    def _light_on(self):
        if self._updated_state["OV1:" + self.CODES.LIGHT]['stringValue'] != 'On':
            self._connection.send_command(self._device_id, AEGOven.CODES.LIGHT, "1", "OV1") # light
        
    def _light_off(self):
        self._connection.send_command(self._device_id, AEGOven.CODES.LIGHT, "0", "OV1") # light
    
    def _set_program(self, program_name):
        program_code = self.PROGRAMS_MAPPING.get(program_name)
        if not program_code:
            raise Exception(f"Couldn't find a code for program {program_name}")
            
        if self._updated_state["OV1:" + self.CODES.PROGRAM]['stringValue'] != program_code:
            self._connection.send_command(self._device_id, AEGOven.CODES.PROGRAM, "0x" + program_code, "OV1")
    
    def _set_temperature(self, temperature):
        # if self._updated_state["OV1:" + self.CODES.TEMPERATURE]['container']['1']['numberValue'] != temperature:
        self._connection.send_command(self._device_id, AEGOven.CODES.TEMPERATURE, [{"1":str(temperature)},{"3":"0"},{"0":"0"}], "OV1")

    
