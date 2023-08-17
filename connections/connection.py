from tools.logger import logger

class Connection(object):

    DEVICES = {}

    def __init__(self, params):
        self._connection_params = params

    def create_device(self, device_definition, all_connections : dict):
        linked_device = None
        linked_device_definition = device_definition.get("linked_device")
        if linked_device_definition:
            connection = all_connections.get(linked_device_definition["connection"])
            if not connection:
                logger.error(f"Couldn't find a connection for device {linked_device_definition['name']}")
            try:
                linked_device = connection.create_device(linked_device_definition, all_connections=all_connections)
            except Exception as e:
                logger.exception(f"Exception when creating a device: {linked_device_definition['name']}, {linked_device_definition}")


        device_type = device_definition.get("type")
        if device_type not in self.DEVICES:
            raise Exception(f"Couldn't find device of type '{device_type}' in {self.DEVICES.keys()}")

        device_id = device_definition.get("connection_id")
        if not device_id:
            raise Exception("Couldn't get the device id")
        Device = self.DEVICES.get(device_type)
        return Device(
                self, 
                device_id, 
                sub_device_id=
                device_definition.get("sub_device_id"), 
                linked_device=linked_device,
                hidden=device_definition.get("hidden")
            )
        
        