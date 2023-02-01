from server.dependencies import get_token_header
from fastapi import FastAPI, APIRouter, Depends

control_router = APIRouter()

@control_router.get("/light/{device_id}/status")
async def root(device_id):
    return {"message": f"Getting the status for the device {device_id}"}

