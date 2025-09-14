import logging
import redis.asyncio as redis
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from .config import get_settings
from .routers import users, links, redirect
from . import client
from .scheduler_jobs import sync_redis_clicks_to_db

settings = get_settings()


logging.basicConfig(level=logging.INFO)

scheduler = AsyncIOScheduler(timezone="Asia/Almaty")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Приложение запускается")

    client.redis_client = redis.from_url(
        settings.redis_url, encoding="utf-8", decode_responses=True
    )
    logging.info("Redis client запущен")

    scheduler.add_job(sync_redis_clicks_to_db, trigger="interval", hours=1)
    scheduler.start()
    logging.info("Планировщик запущен")

    yield

    if client.redis_client:

        logging.info("Останавливаю Redis client")
        await client.redis_client.aclose()

    logging.info("Приложение остановлено")


app = FastAPI(lifespan=lifespan)
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app)

app.include_router(users.router)
app.include_router(links.router)
app.include_router(redirect.router)


@app.post("/")
def Hello():
    return {"message": "Welcome to my app!"}
