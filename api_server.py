from dotenv import load_dotenv

load_dotenv()

import os
import datetime

from tools.logger import logger
from devices.manager import DeviceManager
from server.dependencies import get_token_header, get_query_token
from fastapi import FastAPI, Depends
from server.control_router import control_router
from server.camera_router import camera_router
from server.shabat_router import shabat_router

from starlette.middleware import Middleware
from starlette_context import context
from starlette_context.middleware import RawContextMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler


SERVER_PORT = int(os.getenv("SERVER_PORT", 9000))

middleware = [Middleware(RawContextMiddleware)]

scheduler = AsyncIOScheduler()
scheduler.start()

app = FastAPI(
    # dependencies=[Depends(get_query_token)]
)

app.include_router(
    control_router,
    prefix="/devices",
    # dependencies=[Depends(get_token_header)],
    # responses={418: {"description": "I'm a teapot"}},
    responses={404: {"description": "Not found"}},
)

app.include_router(
    shabat_router,
    prefix="/shabat",
    # dependencies=[Depends(get_token_header)],
    # responses={418: {"description": "I'm a teapot"}},
    responses={404: {"description": "Not found"}},
)

app.include_router(
    camera_router,
    prefix="/camera",
    # dependencies=[Depends(get_token_header)],
    # responses={418: {"description": "I'm a teapot"}},
    responses={404: {"description": "Not found"}},
)

@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Initializing the device manager")
    device_manager = DeviceManager()
    context.devices = device_manager

@app.get("/")
async def root():
    return {"message": "Welcome to the Mayer's family SmartHome server"}


def reload_devices():
    logger.info("Reloading devices")
    context.devices.reload_connections()
    context.devices.reload_devices()

# Schedule the job to run every 5 minutes
scheduler.add_job(reload_devices, 'interval', minutes=5, next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=10))

