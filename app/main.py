import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import ENV, SERVICE_QUEUE
from app.app_v1 import app as app_v1
from app.services.broker import Broker, EventService, RPCService
from app.services.redis import RedisService

logging.basicConfig(level=logging.INFO, format="%(levelname)s:\t  %(message)s")
logging.getLogger("uvicorn.access").addFilter(
    lambda record: "GET / " not in record.getMessage()
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    RedisService.connect()
    await Broker.connect()
    logging.info(f"Serving in {ENV} environment")

    tasks = [
        EventService.subscribe(SERVICE_QUEUE, EventService),
        RPCService.respond(EventService),
    ]
    tasks = [asyncio.create_task(task) for task in tasks]

    yield

    [task.cancel() for task in tasks]
    RedisService.disconnect()
    await Broker.close()


app = FastAPI(
    title="Resume Processing API",
    version="1.0.0",
    lifespan=lifespan,
    servers=[{"url": "/v1", "description": "Version 1"}],
    description="Core service for resume processing and enhancement"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/v1", app_v1)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Resume Processing Service",
        "version": "1.0.0",
        "environment": ENV
    }