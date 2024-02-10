import pytz
import isodate
import datetime
from typing import Optional

import shabat.times
import shabat.actions

from tools.logger import logger
from devices.generic import CameraInterface
from devices.manager import DeviceType

from starlette_context import context
from fastapi import APIRouter
from pydantic import BaseModel, validator

camera_router = APIRouter()

class CameraEvent(BaseModel):
    device_id: str
    start_time: datetime.datetime
    duration: datetime.timedelta

    end_time: Optional[datetime.datetime] = None

    @validator("end_time", pre=True, always=True)
    def set_end_time(cls, v, values, **kwargs):
        """Set the eggs field based upon a spam value."""
        return values.get('start_time')+ values.get('duration')

@camera_router.get("/retrieve_events")
async def retrieve_events(end_time : datetime.datetime, duration_minutes: int):

    device_ids = context.devices.get_devices_by_type(device_type=DeviceType.Cameras)

    all_events = []
    for device_id in device_ids:
        camera_device : CameraInterface = context.devices.get_device_by_name(device_id)

        events = camera_device.get_events(
            end_time - datetime.timedelta(minutes=duration_minutes),
            end_time,
        )

        for event in events:
            all_events.append(
                CameraEvent(
                    device_id=device_id,
                    start_time=datetime.datetime.fromisoformat(event["programDateTime"]),
                    duration=min(datetime.timedelta(minutes=1), isodate.parse_duration(event["duration"]))
                )
            )
    return all_events

@camera_router.delete("/schedule")
async def delete_all_scheduler():
    # scheduler.remove_all_jobs()
    # return "OK"
    pass

@camera_router.get("/schedule")
async def schedule_shabat():
    # return [
    #     Task(
    #         id=job.id,
    #         handler=job.args[0],
    #         name=job.name,
    #         time=job.next_run_time,
    #     )
    #     for job in scheduler.get_jobs()
    # ]
    pass
    
@camera_router.post("/schedule")
async def schedule_shabat(tasks:list[CameraEvent]):
    # for task in tasks:
    #     if not shabat_actions.get(task.handler):
    #         raise Exception(f"Couldn't find handler for task {task.handler}")

    # for task in tasks:
    #     scheduler.add_job(execute_task, trigger='date', run_date=task.time, args=(task.handler, ), name=task.name, id=task.id, replace_existing=True)
    # return "OK"
    pass
