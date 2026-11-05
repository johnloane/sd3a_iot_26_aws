import asyncio
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi_mqtt import FastMQTT, MQTTConfig

#Global
alive = 0
data = {
    "alarm":False,
    "motion":0,
    "keep_alive":"0"
}

MQTT_HOST = "mosquitto"

mqtt_config = MQTTConfig(host=MQTT_HOST, port=1883)
mqtt = FastMQTT(config=mqtt_config)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mqtt.mqtt_startup()
    yield
    await mqq.mqtt_shutdown()


app = FastAPI(lifespan=lifespan)


@mqtt.subscribe("sensors/+/status")
async def sensor_status_handler(client, topic, payload, qos, properties):
    data = payload.decode()
    print(f"Received from {topic}: {data}")
    #Update the database to reflect what came in

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request:Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/keep_alive")
async def keep_alive():
    global alive
    alive += 1
    data["keep_alive"] = str(alive)
    return data

@app.post("/status={name}-{action}")
async def status(name:str, action: str):
    if name == "buzzer":
        if action == "on":
            data["alarm"] = True
        elif action == "off":
            data["alarm"] = False
    return "ok"

if __name__ == '__init__':
    uvicorn.run("main:app", host="127.0.0.1", port = 8000)
