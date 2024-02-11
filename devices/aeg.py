
from enum import Enum
from devices.generic import OvenInterface, GenericDevice
from tools.logger import logger


class AEGOven(GenericDevice, OvenInterface):

    class PROGRAMS(str, Enum):
        TRUE_FAN_COOKING = 'True Fan Cooking'
        TURBO_GRILLING = 'Turbo Grilling'
        MOIST_FAN_BAKING = 'Moist Fan Baking'
        GRILL = 'Grill'
        CONVENTIONAL_COOKING = 'Conventional Cooking'
        PIZZA_FUNCTION = 'Pizza Function'
        FROZEN_FOODS = 'Frozen Foods'
        BOTTOM_HEAT = 'Bottom Heat'
        STEAM_BAKE = 'Steam Bake'

    PROGRAMS_MAPPING = {'True Fan Cooking': 'TRUE_FAN',
        'Turbo Grilling': 'GRILL_FAN',
        'Moist Fan Baking': 'MOIST_FAN_BAKING',
        'Grill': 'GRILL',
        'Conventional Cooking': 'CONVENTIONAL_COOKING',
        'Pizza Function': 'PIZZA',
        'Frozen Foods': 'FROZEN_FOOD',
        'Bottom Heat': 'BOTTOM',
        'Steam Bake': 'DIRECT_STEAM',
    }

    async def turn_on(self, program, temperature):
        appliance_state = await self._connection.get_device_property(self._device_id, "applianceState")
        
        if appliance_state not in ('READY_TO_START', 'RUNNING'):
            logger.error(f"Can't start oven, Oven '{self._device_id}' is in state: '{appliance_state}'")

        await self.set_program(program)
        await self.set_temperature(temperature)

        appliance_state = await self._connection.get_device_property(self._device_id, "applianceState")
        logger.info(f"Oven '{self._device_id}' is '{appliance_state}'")
        if appliance_state == 'READY_TO_START':
            logger.info(f"starting oven.")
            await self._connection.send_command(self._device_id, {"executeCommand" : "START"}) # start
        elif appliance_state == 'RUNNING':
            logger.info(f"ignoring start.")
        else: 
            raise Exception(f"How did we get here?? Oven state was changed while setting the program and temperature")

    async def turn_off(self):
        await self._connection.send_command(self._device_id, {"executeCommand" : "STOPRESET"}) # stop
        
    async def set_program(self, program_name):
        program_code = self.PROGRAMS_MAPPING.get(program_name)
        if not program_code:
            raise Exception(f"Couldn't find the program '{program_name}'")
        
        # if await self._connection.get_device_property(self._device_id, "program") != program_code:
        await self._connection.send_command(self._device_id, {"program" : program_code})
    
    async def set_temperature(self, temperature):
        # if await self._connection.get_device_property(self._device_id, "targetTemperatureC") != temperature:
        await self._connection.send_command(self._device_id, {"targetTemperatureC" : temperature})

    
    async def light_on(self):
        # if not await self._connection.get_device_property(self._device_id, "cavityLight"):
        await self._connection.send_command(self._device_id, {"cavityLight": "ON"})
        
    async def light_off(self):
        # if await self._connection.get_device_property(self._device_id, "cavityLight"):
        await self._connection.send_command(self._device_id, {"cavityLight": "OFF"})
    
