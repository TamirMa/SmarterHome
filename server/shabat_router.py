import time
import datetime
import json
import os
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

SHABBAT_CONFIG_FILE = os.getenv("SHABBAT_CONFIG_FILE")


class Task(BaseModel):
    id: str
    commands: list
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

    with open(SHABBAT_CONFIG_FILE, "r") as shabbat_config_file:
        shabbat_config = json.load(shabbat_config_file)

    tasks = []
    shabat_times = shabat.times.get_shabat_times()

    for shabat_day in shabat_times:
        shabat_start = shabat_day["start"]
        shabat_end   = shabat_day["end"]

        for action in shabbat_config.get("actions", []):
            action_id = action["id"]
            name = action["description"]
            commands = action.get("commands", [])
            
            if action.get("absolute_time"):
                absolute_start_time = datetime.datetime.strptime(action.get("absolute_time"), '%H:%M').time()
                # If the absolute time is before shabbat entrance, this time is on the second day
                if absolute_start_time < shabat_start.time():
                    task_time = datetime.datetime.combine(shabat_end.date(), absolute_start_time)
                else: # absolute_start_time >= shabat_start.time()
                    task_time = datetime.datetime.combine(shabat_start.date(), absolute_start_time)
            elif action.get("relative_time"):
                relative_start_time = action.get("relative_time")
                task_time = shabat_start + datetime.timedelta(minutes=relative_start_time)
            else:
                raise Exception(f"Shabbat Action {action_id} doesn't define a start time (relative or absolute)")

            tasks.append(
                Task(
                    id=f"{action_id}_{task_time.strftime('%Y_%m_%d_%H_%M_%S')}", 
                    commands=commands,
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
            commands=job.args[0],
            name=job.name,
            time=job.next_run_time,
        )
        for job in scheduler.get_jobs()
    ]
    
@shabat_router.post("/schedule")
async def schedule_shabat(tasks:list[Task]):
    for task in tasks:
        scheduler.add_job(execute_task, trigger='date', run_date=task.time, args=(task.commands, ), name=task.name, id=task.id, replace_existing=True)
    return "OK"

def execute_task(commands):

    shabat.actions.run_action_commands(commands)

@shabat_router.get("/times")
async def get_shabat_times():
    return shabat.times.get_shabat_times()

@shabat_router.post("/test")
def test_scheduler():

    with open(SHABBAT_CONFIG_FILE, "r") as shabbat_config_file:
        shabbat_config = json.load(shabbat_config_file)

    for action in shabbat_config.get("actions", []):
        action_id = action["id"]
        name = action["description"]
        commands = action.get("commands", [])

        logger.info(f"Testing shabbat_command {action_id} ({name})")
        shabat.actions.run_action_commands(commands, test=True)
        time.sleep(10)
    return "Success"