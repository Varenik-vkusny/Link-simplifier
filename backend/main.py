import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import async_engine, Base

logging.basicConfig(level=logging.INFO)

async def db_init():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan():
    logging.info('Приложение запускается')
    await db_init()
    yield
    logging.info('Приложение остановлено')


app = FastAPI(lifespan=lifespan)


@app.post('/')
def Hello():
    return {'message': 'Welcome to my app!'}