from enum import Enum

class GenericDevice(object):
    def __init__(self, connection, device_id, sub_device_id=None, linked_device=None, hidden=False, tags=[]):
        self._connection = connection
        self._device_id = device_id
        self._sub_device_id = sub_device_id
        self._linked_device = linked_device
        self._hidden = hidden
        self._tags = tags

    def is_hidden(self):
        return self._hidden

    def get_tags(self):
        return self._tags[:]
    

class SwitchInterface(object):
    def turn_on(self):
        raise NotImplementedError()

    def turn_off(self):
        raise NotImplementedError()

    def is_on(self):
        raise NotImplementedError()

class LightInterface(SwitchInterface):
    pass

class SocketInterface(SwitchInterface):
    pass

class CameraInterface(object):
    def get_events(self, start_time, end_time):
        raise NotImplemented()

    def download_event_by_time(self, start_time, end_time):
        raise NotImplemented()


class DoorbellInterface(CameraInterface):
    pass

class HeaterInterface(object):
    def turn_on(self, timer=None):
        raise NotImplementedError()

    def turn_off(self):
        raise NotImplementedError()

    def is_on(self):
        raise NotImplementedError()


class FanInterface(object):
    def start_fan2(self):
        raise NotImplementedError()

    def start_fan3(self):
        raise NotImplementedError()

    def stop_fan(self):
        raise NotImplementedError()


class AirConditionInterface(object):

    class FAN_SPEED(str, Enum):
        LOW = "low"
        MID = "middle"
        HIGH = "high"
        AUTO = "auto"

    class AC_MODE(str, Enum):
        COOLING = "cooling"
        HEATING = "heating"
        AUTO = "auto"
        FAN_ONLY = "fan"
        DEHUM = "dehum"
    
    def turn_on(self):
        raise NotImplementedError()

    def turn_off(self):
        raise NotImplementedError()

    def set_temperature(self, temp):
        raise NotImplementedError()
    
    def set_fan_speed(self, fan_speed : FAN_SPEED):
        raise NotImplementedError()
    
    def set_mode(self, ac_mode : AC_MODE):
        raise NotImplementedError()


class CurtainInterface(object):
    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

class OvenInterface(object):
    pass

class DishwasherInterface(object):
    pass

class TVInterface(GenericDevice):
    def switch_on(self):
        raise NotImplementedError()

    def switch_off(self):
        raise NotImplementedError()
