import datetime
from typing import Optional

import shabat.times
import shabat.actions
from tools.logger import logger

from fastapi import APIRouter
from pydantic import BaseModel, Field, validator
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.start()

shabat_router = APIRouter()


shabat_actions = {
    "shabat_entrance":          ("Entrance",            shabat.actions.shabat_entrance,        None,                   datetime.timedelta(minutes=-5),             None,                   None,    ),
    "prepare_to_dinner":        ("Start Oven (Dinner)", shabat.actions.prepare_to_dinner,      None,                   datetime.timedelta(minutes=30),             None,                   None,    ),
    "shabat_dinner":            ("Dinner",              shabat.actions.shabat_dinner,          None,                   datetime.timedelta(minutes=45),             None,                   None,    ),
    "post_dinner":              ("Stop Oven (Dinner)",  shabat.actions.post_dinner,            None,                   datetime.timedelta(hours=3, minutes=45),    None,                   None,    ),
    "prepare_to_sleep":         ("Prepare to Sleep",    shabat.actions.prepare_to_sleep,       datetime.time(23,30),   None,                                       None,                   None,    ),
    "start_dishwasher":         ("Dishwasher",          shabat.actions.start_dishwasher,       None,                   None,                                       datetime.time(0,15),    None,    ),
    "shutdown_livingroom":      ("Shutdown Living Room",shabat.actions.shutdown_livingroom,    None,                   None,                                       datetime.time(1,30),    None,    ),
    "shabat_morning":           ("Morning",             shabat.actions.shabat_morning,         None,                   None,                                       datetime.time(8,0),     None,    ),
    "prepare_to_lunch_plata":   ("Start Plata (Lunch)", shabat.actions.prepare_to_lunch_plata, None,                   None,                                       datetime.time(11,30),   None,    ),
    "prepare_to_lunch_oven":    ("Start Oven (Lunch)",  shabat.actions.prepare_to_lunch_oven,  None,                   None,                                       datetime.time(13,30),   None,    ),
    "shabat_lunch":             ("Lunch",               shabat.actions.shabat_lunch,           None,                   None,                                       datetime.time(14,0),    None,    ),
    "post_lunch":               ("Stop Oven & Plata",   shabat.actions.post_lunch,             None,                   None,                                       datetime.time(15,30),   None,    ),
    "shabat_before_exit":       ("Twilight Time",       shabat.actions.shabat_before_exit,     None,                   None,                                       None,                   datetime.timedelta(hours=-2), ),
    }

class Task(BaseModel):
    id: str
    handler: str
    name: str
    time: datetime.datetime

    description: Optional[str] = None

    @validator("description", pre=True, always=True)
    def set_description(cls, v, values, **kwargs):
        """Set the eggs field based upon a spam value."""
        return f"{values.get('time').strftime('%H:%M')} - {values.get('name')}"

@shabat_router.get("/generate_tasks")
async def generate_tasks():
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
            name, _, start_abs, start_dyn, end_abs, end_dyn = action_params
            
            if start_abs:
                task_time = datetime.datetime.combine(shabat_start.date(), start_abs)
            elif start_dyn:
                task_time = shabat_start + start_dyn
            elif end_abs:
                task_time = datetime.datetime.combine(shabat_end.date(), end_abs)
            elif end_dyn:
                task_time = shabat_end + end_dyn

            tasks.append(
                Task(
                    id=f"{action_name}_{shabat_start.strftime('%Y_%m_%d')}", 
                    handler=action_name,
                    name=name, 
                    time=task_time
                )
            )

    
    return tasks

@shabat_router.delete("/schedule")
async def delete_all_scheduler():
    scheduler.remove_all_jobs()
    return "OK"

@shabat_router.get("/schedule")
async def schedule_shabat():
    return [
        Task(
            id=job.id,
            handler=job.args[0],
            name=job.name,
            time=job.next_run_time,
        )
        for job in scheduler.get_jobs()
    ]
    
@shabat_router.post("/schedule")
async def schedule_shabat(tasks:list[Task]):
    for task in tasks:
        if not shabat_actions.get(task.handler):
            raise Exception(f"Couldn't find handler for task {task.handler}")

    for task in tasks:
        scheduler.add_job(execute_task, trigger='date', run_date=task.time, args=(task.handler, ), name=task.name, id=task.id, replace_existing=True)
    return "OK"

@shabat_router.post("/test")
async def schedule_shabat():
    shabat.actions.test_scheduler()
    return "OK"
    

def execute_task(task_handler):

    task_handler = shabat_actions.get(task_handler)
    if not task_handler:
        logger.error(f"Couldn't find handler for task {task_handler}")

    method = task_handler[1]

    method()

@shabat_router.get("/times")
async def get_shabat_times():
    return shabat.times.get_shabat_times()
