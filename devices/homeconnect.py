
from enum import Enum
from devices.generic import GenericDevice
from homeconnect.api import HomeConnectAppliance


class BoschDishwasher(GenericDevice):

    class PROGRAMS(str, Enum):
        AUTH = "Dishcare.Dishwasher.Program.Auto2"
        ECO_50 = "Dishcare.Dishwasher.Program.Eco50"
        PRE_RINSE = "Dishcare.Dishwasher.Program.PreRinse"
        QUICK_65 = "Dishcare.Dishwasher.Program.Quick65"
        # MACHINE_CARE = "Dishcare.Dishwasher.Program.MachineCare"
        INTENSIVE_70 = 'Dishcare.Dishwasher.Program.Intensiv70',

    class COMMON_ENUMS:
        ON = "BSH.Common.EnumType.PowerState.On"
        OFF = "BSH.Common.EnumType.PowerState.Off"
        POWER_STATE = "BSH.Common.Setting.PowerState"
        
    def __init__(self, *args, **kwargs):
        super(BoschDishwasher, self).__init__(*args, **kwargs)
        self._d : HomeConnectAppliance = self._connection.initialize_device(self._device_id)

    def start(self, program):
        self._dishwasher_on()
        self._d.start_program(program)
        
    def _dishwasher_on(self):
        self._d.set_setting(self.COMMON_ENUMS.POWER_STATE, self.COMMON_ENUMS.ON)
        
    def _dishwasher_off(self):
        self._d.set_setting(self.COMMON_ENUMS.POWER_STATE, self.COMMON_ENUMS.OFF)
    
