

class Connection(object):

    DEVICES = {}

    def __init__(self, params):
        self._connection_params = params

    def create_device(self, device_definition):
        device_type = device_definition.get("type")
        if device_type not in self.DEVICES:
            raise Exception(f"Couldn't find device of type '{device_type}' in {self.DEVICES.keys()}")

        device_id = device_definition.get("connection_id")
        if not device_id:
            raise Exception("Couldn't get the device id")
        Device = self.DEVICES.get(device_type)
        try:
            return Device(self, device_id, sub_device_id=device_definition.get("sub_device_id"))
        except Exception as e:
            print (f"Exception when creating a device: {Device.__name__}, {device_definition}")
            
        