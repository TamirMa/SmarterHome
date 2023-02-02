import requests
import schedule
import time

from server.control_router import LightState

def change_light_state(device_id, light_state : LightState):
    requests.post(
        f"http://10.0.0.202:8080/devices/light/{device_id}",
        params={"light_state": light_state}
    )

def test_office_light():
    change_light_state("OfficeLight", LightState.ON)
    time.sleep(3)
    change_light_state("OfficeLight", LightState.OFF)

def job():
    print("I'm working...")

def scheduler_main():
    # test_office_light()

    # schedule.every(10).minutes.do(job)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    # schedule.every(5).to(10).minutes.do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    # schedule.every().minute.at(":17").do(job)

    # schedule.every(10).seconds.do(job)
    schedule.every().thursday.at('10:30').do(test_office_light)

    while True:
        schedule.run_pending()
        time.sleep(1)
