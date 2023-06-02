class GenericDevice(object):
    def __init__(self, connection, device_id, sub_device_id=None):
        self._connection = connection
        self._device_id = device_id
        self._sub_device_id = sub_device_id
    

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