import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend import models



@pytest.mark.anyio
async def test_register(client: AsyncClient, db_session: AsyncSession):

    json = {
        'username': 'new_user',
        'password': 'new_password'
    }

    response = await client.post('/users/register', json=json)

    assert response.status_code == 201

    data = response.json()
    assert 'id' in data
    assert data['username'] == 'new_user'

    db_user = await db_session.get(models.User, data['id'])

    assert db_user
    assert db_user.username == data['username']



@pytest.mark.anyio
async def test_register_duplicate(client: AsyncClient, test_user: models.User):

    json = {
        'username': test_user.username,
        'password': 'new_password'
    }

    response = await client.post('/users/register', json=json)

    assert response.status_code == 409
    assert response.json()['detail'] == 'Пользователь с таким именем уже есть!'



@pytest.mark.anyio
async def test_authorization(client: AsyncClient, test_user: models.User):

    data = {
        'username': test_user.username,
        'password': 'test_password'
    }

    response = await client.post('/token', data=data)

    assert response.status_code == 200

    data = response.json()
    assert 'access_token' in data 



@pytest.mark.anyio
async def test_not_authorization(client: AsyncClient):

    data = {
        'username': 'some_user',
        'password': 'some_pass'
    }

    response = await client.post('/token', data=data)

    assert response.status_code == 401
    assert response.json()['detail'] == 'Неправильное имя или пароль!'