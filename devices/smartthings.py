from devices.generic import TVInterface

class SamsungTVDevice(TVInterface):
    def switch_on(self):
        self._connection.send_command(self._device_id, "main", "switch", "on")

    def switch_off(self):
        self._connection.send_command(self._device_id, "main", "switch", "off")
