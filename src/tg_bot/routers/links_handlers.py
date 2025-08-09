import httpx
from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from src.backend.config import settings
from .auth_handlers import users_with_token


def get_inline_kb(link_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Изменить ссылку', callback_data=f'update_{link_id}'),
                InlineKeyboardButton(text='Удалить ссылку', callback_data=f'delete_{link_id}')
            ]
        ]
    )

    return keyboard


API_BASE_URL = settings.api_base_url


class LinkStates(StatesGroup):
    waiting_for_original_link = State()
    waiting_for_update_link = State()

router = Router()


@router.message(F.text == 'Получить короткую ссылку')
async def start_create_short_link(message: types.Message, state: FSMContext):

    await message.answer('Давайте создадим короткую ссылку! Вставьте ссылку (она должна начинаться с http:// или https://): ')

    await state.set_state(LinkStates.waiting_for_original_link)



@router.message(LinkStates.waiting_for_original_link)
async def original_link_handler(message: types.Message, state: FSMContext):

    if not message.text.startswith(("http://", "https://")):
        await message.answer('Вы ввели ссылку неправильно!')
        await state.clear()
        return

    json = {
        'original_link': message.text
    }

    headers = {
        'Authorization': f'Bearer {users_with_token.get(message.from_user.id, '')}'
    }

    async with httpx.AsyncClient() as client: 
        try:
            response = await client.post(f'{API_BASE_URL}/links', json=json, headers=headers)

            response.raise_for_status()

            data = response.json()

            await message.answer(f'Упрощенная ссылка: {data['short_link']}')
            await state.clear()

        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу!')
            await state.clear()
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await message.answer(error_detail)
            await state.clear()
    


@router.message(F.text == 'Мои ссылки')
async def get_links(message: types.Message):

    headers = {
        'Authorization': f'Bearer {users_with_token.get(message.from_user.id, '')}'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{API_BASE_URL}/links', headers=headers)

            response.raise_for_status()

            links = response.json()
            
            for link in links:
                await message.answer(f'{link['id']}) Оригинальная ссылка: {link['original_link']}\n'
                                     f'Упрощенная ссылка: {link['short_link']}\n\n'
                                     f'{link['owner']['username']} | {link['created_at']}\n'
                                     f'Кликнули: {link['click_count']} раз', reply_markup=get_inline_kb(link['id']))
        
        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу!')
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await message.answer(error_detail)



@router.callback_query(F.data.startswith('update_'))
async def start_update_link(callback: types.CallbackQuery, state: FSMContext):

    await state.update_data(id=callback.data.split('_')[1])

    await callback.message.answer('Отлично! Теперь введите новую ссылку (она должна начинаться с http:// или https://): ')

    await state.set_state(LinkStates.waiting_for_update_link)



@router.message(LinkStates.waiting_for_update_link)
async def update_link_handler(message: types.Message, state: FSMContext):

    if not message.text.startswith(("http://", "https://")):
        await message.answer('Вы ввели ссылку неправильно!')
        await state.clear()
        return

    data = await state.get_data()

    id = data['id']
    update_link = message.text

    json = {
        'original_link': update_link
    }

    headers = {
        'Authorization': f'Bearer {users_with_token.get(message.from_user.id, '')}'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f'{API_BASE_URL}/links/{id}', json=json, headers=headers)

            response.raise_for_status()

            data = response.json()

            await message.answer('Ссылка успешно изменена! \n\n'
                                f'{data['id']}) Оригинальная ссылка: {data['original_link']}\n'
                                f'Упрощенная ссылка: {data['short_link']}\n\n'
                                f'{data['owner']['username']} | {data['created_at']}')
            await state.clear()

        except httpx.RequestError:
            await message.answer('Ошибка при подключении к серверу!')
            await state.clear()
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await message.answer(error_detail)
            await state.clear()



@router.callback_query(F.data.startswith('delete_'))
async def delete_link(callback: types.CallbackQuery):

    link_id = callback.data.split('_')[1]

    headers = {
        'Authorization': f'Bearer {users_with_token.get(callback.from_user.id, '')}'
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f'{API_BASE_URL}/links/{link_id}', headers=headers)

            response.raise_for_status()

            await callback.message.answer('Ссылка успешно удалена!')

        except httpx.RequestError:
            await callback.message.answer('Ошибка при подключении к серверу!')
        except httpx.HTTPError:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            await callback.message.answer(error_detail)