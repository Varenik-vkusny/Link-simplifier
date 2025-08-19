import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .config import get_settings
from .routers import users, links, redirect

settings = get_settings()


logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('Приложение запускается')

    yield
    logging.info('Приложение остановлено')


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(links.router)
app.include_router(redirect.router)


@app.post('/')
def Hello():
    return {'message': 'Welcome to my app!'}