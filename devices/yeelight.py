
from devices.generic import LightInterface, GenericDevice
from yeelight import Bulb

    
class YeelightSwitchDevice(GenericDevice, LightInterface):
    def __init__(self, *args, **kwargs):
        super(YeelightSwitchDevice, self).__init__(*args, **kwargs)
        self._d = Bulb(self._device_id)
        
    def turn_on(self):
        self._d.turn_on()

    def turn_off(self):
        self._d.turn_off()

    def is_on(self):
        return self._d.last_properties["power"] == "on"

