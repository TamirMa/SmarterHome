from dotenv import load_dotenv

load_dotenv()

from devices.manager import DeviceManager
from server.dependencies import get_token_header, get_query_token
from fastapi import FastAPI, Depends
from server.control_router import control_router

from starlette.middleware import Middleware
from starlette_context import context
from starlette_context.middleware import RawContextMiddleware


middleware = [Middleware(RawContextMiddleware)]

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

@app.on_event("startup")
async def startup_event() -> None:
    print ("Initializing devices")
    context.devices = DeviceManager()

@app.get("/")
async def root():
    return {"message": "Welcome to the Mayer's family SmartHome server"}