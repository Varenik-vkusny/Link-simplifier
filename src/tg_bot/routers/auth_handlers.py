import httpx
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import types
from src.backend.config import settings

users_with_token = {}

API_BASE_URL = settings.api_base_url


class AuthorizationStates(StatesGroup):
    waiting_for_register_username = State()
    waiting_for_register_password = State()
    waiting_for_auth_username = State()
    waiting_for_auth_password = State()


router = Router()


@router.message(F.text == 'Зарегестрироваться')
async def start_register(message: types.Message, state: FSMContext):

    await message.answer('Давайте начнем регистрацию! Введите свое имя: ')

    await state.set_state(AuthorizationStates.waiting_for_register_username)



@router.message(AuthorizationStates.waiting_for_register_username)
async def register_username_handler(message: types.Message, state: FSMContext):

    await state.update_data(username=message.text)

    await message.answer('Теперь введите новый пароль (минимум три символа): ')

    await state.set_state(AuthorizationStates.waiting_for_register_password)



@router.message(AuthorizationStates.waiting_for_register_password)
async def register_password_handler(message: types.Message, state: FSMContext):

    if len(message.text) < 3:
        await message.answer('Вы ввели слишком маленький пароль!')
        await state.clear()

    data = await state.get_data()
    username = data['username']
    password = message.text

    json = {
        'username': username,
        'password': password
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f'{API_BASE_URL}/users/register', json=json)

            response.raise_for_status()

            data = response.json()

            await message.answer(f'{data['username']}, вы успешно зарегестрированы!')
            await state.clear()
        
        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу!')
            await state.clear()
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await message.answer(error_detail)
            await state.clear()



@router.message(F.text == 'Авторизоваться')
async def start_auth(message: types.Message, state: FSMContext):

    await message.answer('Давайте начнем авторизацию! Введите свое имя: ')

    await state.set_state(AuthorizationStates.waiting_for_auth_username)



@router.message(AuthorizationStates.waiting_for_auth_username)
async def auth_username_handler(message: types.Message, state: FSMContext):

    await state.update_data(username=message.text)

    await message.answer('Теперь введите свой пароль: ')

    await state.set_state(AuthorizationStates.waiting_for_auth_password)



@router.message(AuthorizationStates.waiting_for_auth_password)
async def auth_password_handler(message: types.Message, state: FSMContext):

    data = await state.get_data()
    username = data['username']
    password = message.text


    data = {
        'username': username,
        'password': password
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f'{API_BASE_URL}/token', data=data)

            response.raise_for_status()

            data = response.json()

            users_with_token[message.from_user.id] = data['access_token']

            await message.answer('Вы успешно авторизованы!')
            await state.clear()

        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу!')
            await state.clear()
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await message.answer(error_detail)
            await state.clear()
