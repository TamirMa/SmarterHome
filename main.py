from fastapi import FastAPI

app = FastAPI()


@app.get("/devices/light/{device_id}/status")
async def root(device_id):
    return {"message": f"Getting the status for the device {device_id}"}

@app.get("/")
async def root():
    return {"message": "Welcome to the Mayer's family SmartHome server"}