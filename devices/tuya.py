
import time
from devices.generic import AirConditionInterface, CurtainInterface, LightInterface, OvenInterface, SocketInterface, GenericDevice, HeaterInterface, FingerbotInterface

class TuyaBaseDevice(GenericDevice):
    def __init__(self, *args, linked_device=None, **kwargs):
        super(TuyaBaseDevice, self).__init__(*args, **kwargs)
        self._d = self._connection.initialize_device(self._device_id, linked_device=linked_device)


class TuyaBLEGatewayDevice(TuyaBaseDevice):
    pass

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

class TuyaFingerbotDevice(TuyaBaseDevice, FingerbotInterface):
    def click(self, duration=0.2, arm_movement_percentages=100):
        status = self._d.status()
        if status == None:
            time.sleep(1)
            status = self._d.status()
            if status == None:
                raise Exception("Tuya device is not connected")
        if status["dps"]["101"] != 'click':
            self._d.set_value('101', 'click')
        if status["dps"]["103"] != duration:
            self._d.set_value('103', duration)
        if status["dps"]["102"] != arm_movement_percentages:
            self._d.set_value('102', arm_movement_percentages)
        self._d.set_value('1', True)

class TuyaFingerbotOvenDevice(TuyaFingerbotDevice, OvenInterface):
    async def turn_on(self, program, temperature):
        self.click(1, 51)
        time.sleep(3)
        self.click(1, 51)

    async def turn_off(self):
        self.click(4, 51)

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


class TuyaHeaterDevice(TuyaBaseDevice, HeaterInterface):
    # We don't really need to use the sub_device_id because on all of our devices
    # we only have 1 curtain per device, if in the future we want to have a seconday
    # curtain, the dps value to update should be 4
    def turn_on(self, timer=None):
        self._d.set_value('1', True)
        if isinstance(timer, int):
            self._d.set_value('7', timer)

    def turn_off(self):
        self._d.set_value('1', False)

    def is_on(self):
        return self._d.status()['dps']['1'] == True
