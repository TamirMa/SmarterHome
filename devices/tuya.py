
from devices.generic import AirConditionInterface, CurtainInterface, LightInterface, SocketInterface, GenericDevice


class TuyaBaseDevice(GenericDevice):
    def __init__(self, *args, **kwargs):
        super(TuyaBaseDevice, self).__init__(*args, **kwargs)
        self._d = self._connection.initialize_device(self._device_id)

class TuyaSwitchDevice(TuyaBaseDevice):
    def turn_on(self):
        self._d.set_status(True, self._sub_device_id)

    def turn_off(self):
        self._d.set_status(False, self._sub_device_id)

    def is_on(self):
        return self._d.status()['dps'][str(self._sub_device_id)] == True

class TuyaLightDevice(TuyaSwitchDevice, LightInterface):
    pass

class TuyaSocketDevice(TuyaSwitchDevice, SocketInterface):
    pass

class TuyaCurtainDevice(TuyaBaseDevice, CurtainInterface):
    # We don't really need to use the sub_device_id because on all of our devices
    # we only have 1 curtain per device, if in the future we want to have a seconday
    # curtain, the dps value to update should be 4
    def open(self):
        self._d.set_value('1', 'open')

    def close(self):
        self._d.set_value('1', 'close')

    def stop(self):
        self._d.set_value('1', 'stop')

class TuyaACDevice(TuyaBaseDevice, AirConditionInterface):

    def turn_on(self):
        self._d.set_value('1', True)

    def turn_off(self):
        self._d.set_value('1', False)

    def set_temperature(self, temp):
        if not isinstance(temp, int) or (temp < 18) or (temp > 30):
            raise Exception("Temperature should be a number between 18°C-30°C")
        self._d.set_value('2', temp)
    
    def set_fan_speed(self, fan_speed: AirConditionInterface.FAN_SPEED):
        self._d.set_value('5', fan_speed)
    
    def set_mode(self, ac_mode: AirConditionInterface.AC_MODE):
        self._d.set_value('4', ac_mode)
