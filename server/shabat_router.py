import datetime
from enum import Enum
from starlette_context import context
from fastapi import APIRouter
from pydantic import BaseModel
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()
scheduler.start()

shabat_router = APIRouter()

@shabat_router.get("/times")
async def get_shabat_times():
    return {
        "start": None,
        "end": None
    }

class Task(BaseModel):
    id: str
    time: str

def execute_task(id):
    # add your task logic here
    print(f"Executing task for ID: {id}")

@shabat_router.get("/schedule")
async def task_status():
    pass

@shabat_router.post("/schedule")
async def schedule_shabat(tasks:list[Task]):
    for task in tasks:
        schedule_time = datetime.strptime(task.time, '%Y-%m-%d %H:%M:%S')
        scheduler.add_job(execute_task, 'date', run_date=schedule_time, args=[task.id])
    
    return "OK"