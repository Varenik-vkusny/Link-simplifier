import logging
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from .config import settings
from .routers import users, links, redirect
from src.tg_bot.routers import common_handlers, auth_handlers, links_handlers

from aiogram import Bot, Dispatcher

logging.basicConfig(level=logging.INFO)


bot = Bot(settings.bot_token)
dp = Dispatcher()
dp.include_router(common_handlers.router)
dp.include_router(auth_handlers.router)
dp.include_router(links_handlers.router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('Приложение запускается')

    logging.info('Запускаю бота...')
    asyncio.create_task(dp.start_polling(bot))
    logging.info('Бот запущен')

    yield
    logging.info('Приложение остановлено')


app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(links.router)
app.include_router(redirect.router)


@app.post('/')
def Hello():
    return {'message': 'Welcome to my app!'}