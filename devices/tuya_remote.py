import time

from devices.generic import OvenInterface, FingerbotInterface, GenericDevice
from tools.logger import logger


class TuyaRemoteFingerbotDevice(GenericDevice, FingerbotInterface):
    def single_click(self):
        logger.info(f"{self._device_id} - Sending a single click to device")
        self._connection.send_command(self._device_id, [{'code': 'switch_1', 'value': True}])

    def set_mode(self, new_mode):
        self._connection.set_properties(self._device_id, {"mode" : new_mode})

    def set_click_duration(self, duration):
        self._connection.set_properties(self._device_id, {"sustain_time" : duration})

    def set_arm_movement_percentages(self, arm_movement_percentages):
        self._connection.set_properties(self._device_id, {"down_percent" : arm_movement_percentages})


    def click(self, duration=0.2, arm_movement_percentages=100):
        properties = self._connection.get_properties(self._device_id)
        properties = {property["code"] : property for property in properties}
        
        if properties["mode"].get("value") != 'click':
            logger.info(f"{self._device_id} - Setting to mode 'click' (now:{properties['mode'].get('value')})")
            self.set_mode('click')

        if properties["sustain_time"].get("value") != duration:
            logger.info(f"{self._device_id} - Setting to sustain_time '{duration}' (now:{properties['sustain_time'].get('value')})")
            self.set_click_duration(duration)
    
        if properties["down_percent"].get("value") != arm_movement_percentages:
            logger.info(f"{self._device_id} - Setting to sustain_time '{arm_movement_percentages}' (now:{properties['sustain_time'].get('value')})")
            self.set_arm_movement_percentages(arm_movement_percentages)

        self.single_click()

class TuyaRemoteFingerbotOvenDevice(TuyaRemoteFingerbotDevice, OvenInterface):
    async def turn_on(self, program, temperature):
        self.click(1, 51)
        time.sleep(3)
        self.click(1, 51)

    async def turn_off(self):
        self.click(4, 51)
