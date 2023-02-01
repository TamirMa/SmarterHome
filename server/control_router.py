import time
from starlette_context import context
from fastapi import APIRouter

control_router = APIRouter()

@control_router.get("/light/{device_id}/status")
async def root(device_id):
    light = context.devices.get_device_by_name(device_id)
    return {"message": f"Getting the status for the device {device_id}"}

@control_router.get("/oven/{device_id}/status")
async def root(device_id):
    oven = context.devices.get_device_by_name(device_id)
    return {"message": f"Getting the status for the device {oven}"}
