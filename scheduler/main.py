import schedule
import time

from server.control_router import FanState, LightState, SocketState
from scheduler import tools


def shabat_entrance():
    """
    Turn On - Balcony, Entrance Light, Kitchen Lights, Living Room Light, Toilet, Hand Wash Sink, Kitchen Socket, MasterBedroomBathroomLight, MasterBedroomLight
    Turn Off - TV, receiver
    """
    tools.change_light_state("BalconyLight", LightState.ON)
    tools.change_light_state("EntranceLight", LightState.ON)
    tools.change_light_state("KitchenMainLight", LightState.ON)
    tools.change_light_state("KitchenSecondaryLight", LightState.ON)
    # tools.change_light_state("KitchenLED", LightState.ON)
    tools.change_light_state("LivingRoomLight", LightState.ON)
    tools.change_light_state("GuestRestroomsToiletLight", LightState.ON)
    tools.change_light_state("GuestRestroomsSinkLight", LightState.ON)
    tools.change_light_state("MasterBedroomLight", LightState.ON)
    # tools.change_light_state("MasterBedroomBathroomLight", LightState.ON)
    
    tools.change_socket_state("KitchenSocket", SocketState.ON)
    

def shabat_dinner():
    """
    Turn On - DiningTable
    """
    tools.change_light_state("DiningTableLight", LightState.ON)

def prepare_to_sleep():
    """
    Turn Off - MasterBedroomLight
    """
    tools.change_light_state("MasterBedroomLight", LightState.OFF)
    tools.change_socket_state("KitchenSocket", SocketState.OFF)
    tools.change_fan_state("MasterBedroomFan", FanState.FAN3)
    

def shutdown_livingroom():
    """
    Turn Off - Balcony, Entrance Light, Kitchen Lights, Living Room Light, Toilet, Hand Wash Sink, Kitchen Socket, DiningTable
    Close living room curtain
    """
    tools.change_light_state("DiningTableLight", LightState.OFF)
    tools.change_light_state("BalconyLight", LightState.OFF)
    tools.change_light_state("EntranceLight", LightState.OFF)
    tools.change_light_state("KitchenMainLight", LightState.OFF)
    tools.change_light_state("KitchenSecondaryLight", LightState.OFF)
    tools.change_light_state("KitchenLED", LightState.OFF)
    tools.change_light_state("LivingRoomLight", LightState.OFF)
    tools.change_light_state("GuestRestroomsToiletLight", LightState.OFF)
    tools.change_light_state("GuestRestroomsSinkLight", LightState.OFF)
    tools.change_light_state("MasterBedroomLight", LightState.OFF)
    # tools.change_light_state("MasterBedroomBathroomLight", LightState.OFF)

def shabat_morning():
    """
    Turn On - Toilet
    Open living room curtain
    """
    tools.change_fan_state("MasterBedroomFan", FanState.STOP)
    tools.change_light_state("GuestRestroomsToiletLight", LightState.ON)
    
def prepare_to_lunch():
    tools.change_socket_state("KitchenSocket", SocketState.ON)

def shabat_lunch():
    """
    Turn On - Kitchen Lights, DiningTable
    """
    tools.change_light_state("DiningTableLight", LightState.ON)
    tools.change_light_state("KitchenMainLight", LightState.ON)
    tools.change_light_state("KitchenSecondaryLight", LightState.ON)
    tools.change_light_state("KitchenLED", LightState.ON)

def shabat_before_exit():
    """
    Turn On - Balcony, Living Room Light, Hand Wash Sink
    Turn Off - DiningTable
    """
    tools.change_socket_state("KitchenSocket", SocketState.OFF)
    tools.change_light_state("BalconyLight", LightState.ON)
    tools.change_light_state("LivingRoomLight", LightState.ON)
    tools.change_light_state("GuestRestroomsSinkLight", LightState.ON)
    tools.change_light_state("DiningTableLight", LightState.OFF)


def scheduler_main():   
    # schedule.every(30).seconds.do(job)
    # schedule.every(30).minutes.do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("13:30").do(job)
    # schedule.every(5).to(30).minutes.do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:35").do(job)
    # schedule.every().minute.at(":37").do(job)

    print ("Starting scheduler")
    
    schedule.every().friday.at('18:34').do(tools.turn_on_oven)
    
    schedule.every().friday.at('19:00').do(shabat_entrance)
    schedule.every().friday.at('19:30').do(shabat_dinner)
    schedule.every().friday.at('20:15').do(tools.turn_on_oven)
    schedule.every().friday.at('22:15').do(tools.turn_off_oven)
    schedule.every().friday.at('23:30').do(prepare_to_sleep)
    schedule.every().saturday.at('00:01').do(tools.start_dishwasher)
    schedule.every().saturday.at('01:30').do(shutdown_livingroom)
    schedule.every().saturday.at('08:30').do(shabat_morning)
    schedule.every().saturday.at('13:00').do(prepare_to_lunch)
    schedule.every().saturday.at('13:30').do(tools.turn_on_oven)
    schedule.every().saturday.at('14:00').do(shabat_lunch)
    schedule.every().saturday.at('15:30').do(tools.turn_off_oven)
    schedule.every().saturday.at('17:30').do(shabat_before_exit)

    print(schedule.get_jobs())
    while True:
        schedule.run_pending()
        time.sleep(3)

def test_scheduler():

    print ("Testing scheduler")
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
    prepare_to_lunch()
    time.sleep(3)
    shabat_lunch()
    time.sleep(3)
    shabat_before_exit()


