from aiogram import Router
from aiogram.filters import CommandStart
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Зарегестрироваться'),
            KeyboardButton(text='Авторизоваться')
        ],
        [
            KeyboardButton(text='Получить короткую ссылку'),
            KeyboardButton(text='Мои ссылки')
        ]
    ]
)


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):

    await message.answer('Привет! Добро пожаловать в бота, который сокращает ваши ссылки.', reply_markup=main_kb)

