import dateutil.parser
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
from fastapi.responses import Response
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
    
    @property
    def event_id(self):
        """Set the eggs field based upon a spam value."""
        return f"{self.start_time.isoformat()}->{self.end_time.isoformat()}|{self.device_id}"

@camera_router.get("/retrieve_events")
async def retrieve_events(end_time : datetime.datetime, duration_minutes: int, device_id : str = None):
    if device_id != None:
        device = context.devices.get_device_by_name(device_id)
        if device == None or not isinstance(device, CameraInterface):
            raise Exception(f"This is not a Camera device ({device_id})")
        camera_device : CameraInterface = device
        device_ids = [ camera_device ]
    else:
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
                    start_time=dateutil.parser.parse(event["programDateTime"]),
                    duration=min(datetime.timedelta(minutes=1), isodate.parse_duration(event["duration"]))
                )
            )
    return all_events
    
@camera_router.post("/download")
async def download_event(camera_event:CameraEvent):
    device = context.devices.get_device_by_name(camera_event.device_id)
    if device == None or not isinstance(device, CameraInterface):
        raise Exception(f"This is not a Camera device ({camera_event.device_id})")
    camera_device : CameraInterface = device
    
    video_bytes = camera_device.download_event_by_time(
        camera_event.start_time,
        camera_event.end_time
    )
    return Response(
        video_bytes,
        media_type="video/mp4"
    )

