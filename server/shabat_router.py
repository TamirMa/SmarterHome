import datetime

import shabat.times
import shabat.actions
from tools.logger import logger

from fastapi import APIRouter
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.start()

shabat_router = APIRouter()


shabat_actions = {
    "shabat_entrance":          (shabat.actions.shabat_entrance,        None,                   datetime.timedelta(minutes=-5),             None,                   None,    ),
    "prepare_to_dinner":        (shabat.actions.prepare_to_dinner,      None,                   datetime.timedelta(minutes=30),             None,                   None,    ),
    "shabat_dinner":            (shabat.actions.shabat_dinner,          None,                   datetime.timedelta(minutes=45),             None,                   None,    ),
    "post_dinner":              (shabat.actions.post_dinner,            None,                   datetime.timedelta(hours=3, minutes=45),    None,                   None,    ),
    "prepare_to_sleep":         (shabat.actions.prepare_to_sleep,       datetime.time(23,30),   None,                                       None,                   None,    ),
    "shutdown_livingroom":      (shabat.actions.shutdown_livingroom,    None,                   None,                                       datetime.time(1,30),    None,    ),
    "shabat_morning":           (shabat.actions.shabat_morning,         None,                   None,                                       datetime.time(8,0),     None,    ),
    "prepare_to_lunch_plata":   (shabat.actions.prepare_to_lunch_plata, None,                   None,                                       datetime.time(11,30),   None,    ),
    "prepare_to_lunch_oven":    (shabat.actions.prepare_to_lunch_oven,  None,                   None,                                       datetime.time(13,30),   None,    ),
    "shabat_lunch":             (shabat.actions.shabat_lunch,           None,                   None,                                       datetime.time(14,0),    None,    ),
    "post_lunch":               (shabat.actions.post_lunch,             None,                   None,                                       datetime.time(15,30),   None,    ),
    "shabat_before_exit":       (shabat.actions.shabat_before_exit,     None,                   None,                                       None,                   datetime.timedelta(hours=-2), ),
    }

class Task(BaseModel):
    id: str
    time: datetime.datetime

@shabat_router.get("/schedule")
async def task_status():
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

    tasks = []
    shabat_times = shabat.times.get_shabat_times()

    for shabat_day in shabat_times:
        shabat_start = shabat_day["start"]
        shabat_end   = shabat_day["end"]
        for action_name, action_params in shabat_actions.items():
            _, start_abs, start_dyn, end_abs, end_dyn = action_params
            
            if start_abs:
                task_time = datetime.datetime.combine(shabat_start.date(), start_abs)
            elif start_dyn:
                task_time = shabat_start + start_dyn
            elif end_abs:
                task_time = datetime.datetime.combine(shabat_end.date(), end_abs)
            elif end_dyn:
                task_time = shabat_end + end_dyn

            tasks.append(
                Task(id=f"{action_name}_{shabat_start.strftime('%Y_%m_%d')}", time=task_time)
            )

    
    return tasks

@shabat_router.post("/schedule")
async def schedule_shabat(tasks:list[Task]):
    for task in tasks:
        if not shabat_actions.get(task.id):
            raise Exception(f"Couldn't find handler for task {task.id}")

    for task in tasks:
        scheduler.add_job(execute_task, trigger='date', run_date=task.time, args=(task.id, ), name=task.id, id=task.id)
    return "OK"
    

def execute_task(task_id):

    task_handler = shabat_actions.get(task_id)
    if not task_handler:
        logger.error(f"Couldn't find handler for task {task_id}")

    method = task_handler[0]

    method()

@shabat_router.get("/times")
async def get_shabat_times():
    return shabat.times.get_shabat_times()
