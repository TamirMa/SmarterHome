import requests
import schedule
import time

from server.control_router import LightState

def change_light_state(device_id, light_state : LightState):
    requests.post(
        f"http://10.0.0.202:8080/devices/light/{device_id}",
        params={"light_state": light_state}
    )

def shabat_entrance():
    """
    Turn On - Balcony, Entrance Light, Kitchen Lights, Living Room Light, Toilet, Hand Wash Sink, Kitchen Socket, MasterBedroomBathroomLight, MasterBedroomLight
    Turn Off - TV, receiver
    """
    change_light_state("BalconyLight", LightState.ON)
    change_light_state("EntranceLight", LightState.ON)
    change_light_state("KitchenMainLight", LightState.ON)
    change_light_state("KitchenSecondaryLight", LightState.ON)
    # change_light_state("KitchenLED", LightState.ON)
    change_light_state("LivingRoomLight", LightState.ON)
    change_light_state("GuestRestroomsToiletLight", LightState.ON)
    change_light_state("GuestRestroomsSinkLight", LightState.ON)
    change_light_state("MasterBedroomLight", LightState.ON)
    # change_light_state("MasterBedroomBathroomLight", LightState.ON)
    
    change_light_state("KitchenSocket", LightState.ON)
    

def shabat_dinner():
    """
    Turn On - DiningTable
    """
    change_light_state("DiningTableLight", LightState.ON)

def prepare_to_sleep():
    """
    Turn Off - MasterBedroomLight
    """
    change_light_state("MasterBedroomLight", LightState.OFF)
    change_light_state("KitchenSocket", LightState.OFF)
    

def turn_on_oven():
    """
    Turn On - Oven
    """

def turn_off_oven():
    """
    Turn Off - Oven
    """
    

def shutdown_livingroom():
    """
    Turn Off - Balcony, Entrance Light, Kitchen Lights, Living Room Light, Toilet, Hand Wash Sink, Kitchen Socket, DiningTable
    Close living room curtain
    """
    change_light_state("BalconyLight", LightState.OFF)
    change_light_state("EntranceLight", LightState.OFF)
    change_light_state("KitchenMainLight", LightState.OFF)
    change_light_state("KitchenSecondaryLight", LightState.OFF)
    # change_light_state("KitchenLED", LightState.OFF)
    change_light_state("LivingRoomLight", LightState.OFF)
    change_light_state("GuestRestroomsToiletLight", LightState.OFF)
    change_light_state("GuestRestroomsSinkLight", LightState.OFF)
    change_light_state("MasterBedroomLight", LightState.OFF)
    # change_light_state("MasterBedroomBathroomLight", LightState.OFF)

def shabat_morning():
    """
    Turn On - Toilet
    Open living room curtain
    """
    change_light_state("GuestRestroomsToiletLight", LightState.ON)
    

def shabat_lunch():
    """
    Turn On - Kitchen Lights, DiningTable
    """
    change_light_state("DiningTableLight", LightState.ON)
    change_light_state("KitchenMainLight", LightState.ON)
    change_light_state("KitchenSecondaryLight", LightState.ON)
    # change_light_state("KitchenLED", LightState.ON)

def shabat_before_exit():
    """
    Turn On - Balcony, Living Room Light, Hand Wash Sink
    Turn Off - DiningTable
    """
    change_light_state("BalconyLight", LightState.ON)
    change_light_state("LivingRoomLight", LightState.ON)
    change_light_state("GuestRestroomsSinkLight", LightState.ON)
    change_light_state("DiningTableLight", LightState.OFF)


def scheduler_main():
    # test_office_light()

    # schedule.every(10).minutes.do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    # schedule.every(5).to(10).minutes.do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    # schedule.every().minute.at(":17").do(job)

    shabat_entrance()
    time.sleep(1)
    shabat_dinner()
    time.sleep(1)
    prepare_to_sleep()
    time.sleep(1)
    shutdown_livingroom()
    time.sleep(1)
    shabat_morning()
    time.sleep(1)
    shabat_lunch()
    time.sleep(1)
    shabat_before_exit()
    time.sleep(1)
    return
    # schedule.every(10).seconds.do(job)
    schedule.every().friday.at('16:30').do(shabat_entrance)
    schedule.every().friday.at('18:30').do(shabat_dinner)
    schedule.every().friday.at('23:30').do(prepare_to_sleep)
    schedule.every().saturday.at('01:30').do(shutdown_livingroom)
    schedule.every().saturday.at('08:30').do(shabat_morning)
    schedule.every().saturday.at('14:00').do(shabat_lunch)
    schedule.every().saturday.at('16:30').do(shabat_before_exit)

    
    while True:
        schedule.run_pending()
        time.sleep(1)
"""
      /* Lights */
      AddScheduleForRule.apply(shabat_morning_rule_id, havdalaTime.withHour(8).withMinute(0))  
      AddScheduleForRule.apply(shabat_entrance_rule_id, candlesTime)  
      AddScheduleForRule.apply(dinner_start_rule_id, candlesTime)  
      AddScheduleForRule.apply(sleep_rule_id, candlesTime.withHour(23).withMinute(30))  
      AddScheduleForRule.apply(turn_off_living_room_rule_id, havdalaTime.withHour(1).withMinute(0))  
      AddScheduleForRule.apply(lunch_rule_id, havdalaTime.withHour(14).withMinute(0))  
      AddScheduleForRule.apply(turn_on_living_room_rule_id, havdalaTime.minusHours(2))  
      AddScheduleForRule.apply(shabat_exit_rule_id, havdalaTime)
"""
