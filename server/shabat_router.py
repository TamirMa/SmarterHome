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


shabat_actions = {
    "shabat_entrance":          shabat.actions.shabat_entrance,        
    "prepare_to_dinner":        shabat.actions.prepare_to_dinner,      
    "shabat_dinner":            shabat.actions.shabat_dinner,          
    "post_dinner":              shabat.actions.post_dinner,            
    "prepare_to_sleep":         shabat.actions.prepare_to_sleep,       
    "start_dishwasher":         shabat.actions.start_dishwasher,       
    "shutdown_livingroom":      shabat.actions.shutdown_livingroom,    
    "shabat_morning":           shabat.actions.shabat_morning,         
    "prepare_to_lunch_plata":   shabat.actions.prepare_to_lunch_plata, 
    "prepare_to_lunch_oven":    shabat.actions.prepare_to_lunch_oven,  
    "shabat_lunch":             shabat.actions.shabat_lunch,           
    "post_lunch":               shabat.actions.post_lunch,             
    "shabat_before_exit":       shabat.actions.shabat_before_exit,
}

class Task(BaseModel):
    id: str
    handler_id: str
    commands: str
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
        # shabat_end   = shabat_day["end"]

        for action in shabbat_config.get("actions", []):
            action_id = action["id"]
            name = action["description"]
            commands = action.get("commands", [])
            
            if action.get("absolute_time"):
                absolute_start_time = action.get("absolute_time")
                # If the absolute time is before shabbat entrance, this time is on the second day
                if absolute_start_time < shabat_start.time():
                    task_time = datetime.datetime.combine(shabat_start.date(), absolute_start_time)
                else: # absolute_start_time >= shabat_start.time()
                    task_time = datetime.datetime.combine(shabat_start.date(), absolute_start_time)
            elif action.get("relative_time"):
                relative_start_time = action.get("relative_time")
                task_time = shabat_start + relative_start_time
            else:
                raise Exception(f"Shabbat Action {action_id} doesn't define a start time (relative or absolute)")

            tasks.append(
                Task(
                    id=f"{action_id}_{shabat_start.strftime('%Y_%m_%d_%H_%M_%S')}", 
                    handler_id=action_id,
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
            handler=job.args[0],
            name=job.name,
            time=job.next_run_time,
        )
        for job in scheduler.get_jobs()
    ]
    
@shabat_router.post("/schedule")
async def schedule_shabat(tasks:list[Task]):
    for task in tasks:
        if not shabat_actions.get(task.handler_id):
            raise Exception(f"Couldn't find handler for task {task.handler_id}")

    for task in tasks:
        scheduler.add_job(execute_task, trigger='date', run_date=task.time, args=(task.handler_id, ), name=task.name, id=task.id, replace_existing=True)
    return "OK"

def execute_task(task_handler):

    task_handler = shabat_actions.get(task_handler)
    if not task_handler:
        logger.error(f"Couldn't find handler for task {task_handler}")

    method = task_handler

    method()

@shabat_router.get("/times")
async def get_shabat_times():
    return shabat.times.get_shabat_times()
