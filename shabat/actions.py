import time

from server.control_router import FanState, LightState, SocketState
from tools import actions


def shabat_entrance():
    """
    Turn On - Balcony, Entrance Light, Kitchen Lights, Living Room Light, Toilet, Hand Wash Sink, Kitchen Socket, MasterBedroomBathroomLight, MasterBedroomLight
    Turn Off - TV, receiver
    """
    actions.change_light_state("BalconyLight", LightState.ON)
    actions.change_light_state("EntranceLight", LightState.ON)
    actions.change_light_state("KitchenMainLight", LightState.ON)
    actions.change_light_state("KitchenSecondaryLight", LightState.ON)
    actions.change_light_state("KitchenLED", LightState.ON)
    actions.change_light_state("LivingRoomLight", LightState.ON)
    actions.change_light_state("GuestRestroomsToiletLight", LightState.ON)
    actions.change_light_state("GuestRestroomsSinkLight", LightState.ON)
    actions.change_light_state("MasterBedroomLight", LightState.ON)
    # tools.change_light_state("MasterBedroomBathroomLight", LightState.ON)
    
    actions.change_socket_state("KitchenSocket", SocketState.ON)

def prepare_to_dinner():
    """
    Tunr On - Oven
    """
    actions.turn_on_oven()    

def shabat_dinner():
    """
    Turn On - DiningTable
    """
    actions.change_light_state("DiningTableLight", LightState.ON)

def post_dinner():
    """
    Tunr Off - Oven
    """
    actions.turn_off_oven()

def prepare_to_sleep():
    """
    Turn Off - MasterBedroomLight
    """
    actions.change_light_state("MasterBedroomLight", LightState.OFF)
    actions.change_socket_state("KitchenSocket", SocketState.OFF)
    actions.change_fan_state("MasterBedroomFan", FanState.FAN3)
    

def shutdown_livingroom():
    """
    Turn Off - Balcony, Entrance Light, Kitchen Lights, Living Room Light, Toilet, Hand Wash Sink, Kitchen Socket, DiningTable
    Close living room curtain
    """
    actions.change_light_state("DiningTableLight", LightState.OFF)
    actions.change_light_state("BalconyLight", LightState.OFF)
    actions.change_light_state("EntranceLight", LightState.OFF)
    actions.change_light_state("KitchenMainLight", LightState.OFF)
    actions.change_light_state("KitchenSecondaryLight", LightState.OFF)
    actions.change_light_state("KitchenLED", LightState.OFF)
    actions.change_light_state("LivingRoomLight", LightState.OFF)
    actions.change_light_state("GuestRestroomsToiletLight", LightState.OFF)
    actions.change_light_state("GuestRestroomsSinkLight", LightState.OFF)
    actions.change_light_state("MasterBedroomLight", LightState.OFF)
    # tools.change_light_state("MasterBedroomBathroomLight", LightState.OFF)

def start_dishwasher():
    actions.start_dishwasher()

def shabat_morning():
    """
    Turn On - Toilet
    Open living room curtain
    """
    actions.change_light_state("GuestRestroomsToiletLight", LightState.ON)
    
def prepare_to_lunch_plata():
    actions.change_socket_state("KitchenSocket", SocketState.ON)

def prepare_to_lunch_oven():
    actions.turn_on_oven()

def shabat_lunch():
    """
    Turn On - Kitchen Lights, DiningTable
    """
    actions.change_light_state("DiningTableLight", LightState.ON)
    actions.change_light_state("KitchenMainLight", LightState.ON)
    actions.change_light_state("KitchenSecondaryLight", LightState.ON)
    actions.change_light_state("KitchenLED", LightState.ON)
    actions.change_fan_state("MasterBedroomFan", FanState.STOP)

def post_lunch():
    actions.turn_off_oven()

def shabat_before_exit():
    """
    Turn On - Balcony, Living Room Light, Hand Wash Sink
    Turn Off - DiningTable
    """
    actions.change_socket_state("KitchenSocket", SocketState.OFF)
    actions.change_light_state("BalconyLight", LightState.ON)
    actions.change_light_state("LivingRoomLight", LightState.ON)
    actions.change_light_state("GuestRestroomsSinkLight", LightState.ON)
    actions.change_light_state("DiningTableLight", LightState.OFF)

def test_scheduler():
    shabat_entrance()
    time.sleep(3)
    shabat_entrance()
    time.sleep(3)
    prepare_to_sleep()
    time.sleep(3)
    shutdown_livingroom()
    time.sleep(3)
    shabat_morning()
    time.sleep(3)
    prepare_to_lunch_plata()
    time.sleep(3)
    shabat_lunch()
    time.sleep(3)
    shabat_before_exit()


