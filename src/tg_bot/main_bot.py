import logging
import asyncio
from aiogram import Bot, Dispatcher
from src.backend.config import get_settings
from .routers import auth_handlers, links_handlers, common_handlers

settings = get_settings()

logging.basicConfig(level=logging.INFO)


async def main():

    logging.info('Запускаю бота')

    bot = Bot(settings.bot_token)
    dp = Dispatcher()

    dp.include_router(common_handlers.router)
    dp.include_router(auth_handlers.router)
    dp.include_router(links_handlers.router)

    await dp.start_polling(bot)

    logging.info('Бот запущен')


if __name__ == '__main__':
    asyncio.run(main())