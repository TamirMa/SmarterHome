import datetime

import shabat.actions
from tools.logger import logger

from fastapi import APIRouter
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.start()

shabat_router = APIRouter()


shabat_actions = {
    "shabat_entrance":          (shabat.actions.shabat_entrance,        None,                   -5,             None,                   None,    ),
    "prepare_to_dinner":        (shabat.actions.prepare_to_dinner,      None,                   +30,            None,                   None,    ),
    "shabat_dinner":            (shabat.actions.shabat_dinner,          None,                   +45,            None,                   None,    ),
    "post_dinner":              (shabat.actions.post_dinner,            None,                   (3 * 60) + 45,  None,                   None,    ),
    "prepare_to_sleep":         (shabat.actions.prepare_to_sleep,       datetime.time(23,30),   None,           None,                   None,    ),
    "shutdown_livingroom":      (shabat.actions.shutdown_livingroom,    None,                   None,           datetime.time(1,30),    None,    ),
    "shabat_morning":           (shabat.actions.shabat_morning,         None,                   None,           datetime.time(8,0),     None,    ),
    "prepare_to_lunch_plata":   (shabat.actions.prepare_to_lunch_plata, None,                   None,           datetime.time(11,30),   None,    ),
    "prepare_to_lunch_oven":    (shabat.actions.prepare_to_lunch_oven,  None,                   None,           datetime.time(13,30),   None,    ),
    "shabat_lunch":             (shabat.actions.shabat_lunch,           None,                   None,           datetime.time(14,0),    None,    ),
    "post_lunch":               (shabat.actions.post_lunch,             None,                   None,           datetime.time(15,30),   None,    ),
    "shabat_before_exit":       (shabat.actions.shabat_before_exit,     None,                   None,           None,                   -2 * 60, ),
    }

class Task(BaseModel):
    id: str
    time: str

@shabat_router.get("/schedule")
async def task_status():
    return [
        job.name
        for job in scheduler.get_jobs()
    ]

@shabat_router.post("/schedule")
async def schedule_shabat(tasks:list[Task]):
    for task in tasks:
        if not shabat_actions.get(task.id):
            raise Exception(f"Couldn't find handler for task {task.id}")

    for task in tasks:
        schedule_time = datetime.datetime.strptime(task.time, '%Y-%m-%d %H:%M:%S')
        scheduler.add_job(execute_task, trigger='date', run_date=schedule_time, args=(task.id, ), name=task.id, id=task.id)
    return "OK"
    

def execute_task(task_id):

    task_handler = shabat_actions.get(task_id)
    if not task_handler:
        logger.error(f"Couldn't find handler for task {task_id}")

    method = task_handler[0]

    method()

@shabat_router.get("/times")
async def get_shabat_times():
    """
    
    schedule.every().friday.at('19:00').do(shabat_entrance)
    schedule.every().friday.at('19:30').do(shabat_dinner)
    schedule.every().friday.at('18:40').do(actions.turn_on_oven)
    schedule.every().friday.at('22:30').do(actions.turn_off_oven)
    schedule.every().friday.at('23:30').do(prepare_to_sleep)
    schedule.every().saturday.at('01:30').do(shutdown_livingroom)
    schedule.every().saturday.at('08:30').do(shabat_morning)
    schedule.every().saturday.at('13:00').do(prepare_to_lunch)
    schedule.every().saturday.at('13:00').do(actions.turn_on_oven)
    schedule.every().saturday.at('14:00').do(shabat_lunch)
    schedule.every().saturday.at('15:30').do(actions.turn_off_oven)
    schedule.every().saturday.at('17:30').do(shabat_before_exit)

    """
    return {
        "start": None,
        "end": None
    }
