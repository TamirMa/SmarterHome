from devices.generic import GenericDevice

class SamsungTVDevice(GenericDevice):
    def switch_on(self):
        self._connection.send_command(self._device_id, "main", "switch", "on")

    def switch_off(self):
        self._connection.send_command(self._device_id, "main", "switch", "off")
