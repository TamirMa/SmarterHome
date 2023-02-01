class GenericDevice(object):
    def __init__(self, device_id):
        self._device_id = device_id
    
class SwitchDevice(GenericDevice):

    def turn_on(self):
        raise NotImplemented()

    def turn_off(self):
        raise NotImplemented()

