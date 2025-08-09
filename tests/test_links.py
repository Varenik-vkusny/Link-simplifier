import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend import models
from .conftest import user


@pytest.mark.anyio
async def test_create_short_link(authenticated_client: AsyncClient, db_session: AsyncSession, test_user: models.User):

    json = {
        'original_link': 'https://github.com/Varenik-vkusny/Link-simplifier'
    }

    response = await authenticated_client.post('/links', json=json)

    assert response.status_code == 201

    data = response.json()
    assert 'short_link' in data
    assert data['short_link'].startswith('http://localhost:8000/')

    db_link = await db_session.get(models.Link, data['id'])
    assert db_link
    assert db_link.original_link == 'https://github.com/Varenik-vkusny/Link-simplifier'
    assert db_link.short_code in data['short_link']
    assert db_link.owner_id == test_user.id



@pytest.mark.anyio
async def test_not_authenticated_create_short_link(client: AsyncClient):

    json = {
        'original_link': 'https://learningenglish.voanews.com/p/5609.html'
    }

    response = await client.post('/links', json=json)

    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'



@pytest.mark.anyio
async def test_create_short_link_duplicate(authenticated_client: AsyncClient):

    json = {
        'original_link': 'https://github.com/Varenik-vkusny/Link-simplifier'
    }

    response = await authenticated_client.post('/links', json=json)

    json = {
        'original_link': 'https://github.com/Varenik-vkusny/Link-simplifier'
    }

    response = await authenticated_client.post('/links', json=json)

    assert response.status_code == 409
    assert response.json()['detail'] == 'У вас уже есть такая ссылка!'



@pytest.mark.anyio
async def test_get_links(authenticated_client: AsyncClient):

    json = {
        'original_link': 'https://github.com/Varenik-vkusny/Link-simplifier'
    }

    response = await authenticated_client.post('/links', json=json)

    response = await authenticated_client.get('/links')

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    


@pytest.mark.anyio
async def test_not_authenticated_get_links(client: AsyncClient):

    response = await client.get('/links')

    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'



@pytest.mark.anyio
async def test_get_zero_links(authenticated_client: AsyncClient):

    response = await authenticated_client.get('/links')

    assert response.status_code == 404
    assert response.json()['detail'] == 'У вас пока нет ни одной ссылки, создайте новую!'



@pytest.mark.anyio
async def test_put_link(authenticated_client: AsyncClient):

    json = {
        'original_link': 'https://github.com/Varenik-vkusny/Link-simplifier'
    }

    response = await authenticated_client.post('/links', json=json)

    link_id = response.json()['id']

    json = {
        'original_link': 'https://learningenglish.voanews.com/p/5609.html'
    }

    response = await authenticated_client.put(f'/links/{link_id}', json=json)

    assert response.status_code == 200
    
    data = response.json()
    assert data['original_link'] == 'https://learningenglish.voanews.com/p/5609.html'



@pytest.mark.anyio
async def test_not_current_user_put_link(authenticated_client: AsyncClient, client: AsyncClient, db_session: AsyncSession, test_user: models.User):

    json = {
        'original_link': 'https://github.com/Varenik-vkusny/Link-simplifier'
    }

    response = await authenticated_client.post('/links', json=json)

    link_id = response.json()['id']

    some_user = await user(client, db_session, 'user', 'pass')

    json = {
        'original_link': 'https://learningenglish.voanews.com/p/5609.html'
    }

    response = await some_user.put(f'/links/{link_id}', json=json)

    assert response.status_code == 403
    assert response.json()['detail'] == 'Ссылка с таким id не ваша! Вы не можете ее редактировать!'



@pytest.mark.anyio
async def test_put_no_link(authenticated_client: AsyncClient):

    json = {
        'original_link': 'https://learningenglish.voanews.com/p/5609.html'
    }

    response = await authenticated_client.put('/links/1', json=json)

    assert response.status_code == 404
    assert response.json()['detail'] == 'Нет ссылки с таким id!'



@pytest.mark.anyio
async def test_delete_link(authenticated_client: AsyncClient, db_session: AsyncSession):

    json = {
        'original_link': 'https://github.com/Varenik-vkusny/Link-simplifier'
    }

    response = await authenticated_client.post('/links', json=json)

    link_id = response.json()['id']

    response = await authenticated_client.delete(f'/links/{link_id}')

    assert response.status_code == 204
    
    db_link = await db_session.get(models.Link, link_id)
    assert not db_link



@pytest.mark.anyio
async def test_not_authenticated_delete_link(client: AsyncClient):

    response = await client.delete('/links/1')

    assert response.status_code == 401
    assert response.json()['detail'] == 'Not authenticated'



@pytest.mark.anyio
async def test_no_link_delete(authenticated_client: AsyncClient):

    response = await authenticated_client.delete('/links/2')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Нет ссылки с таким id!'



@pytest.mark.anyio
async def test_not_current_user_delete(authenticated_client: AsyncClient, client: AsyncClient, db_session: AsyncSession, test_user: models.User):

    json = {
        'original_link': 'https://github.com/Varenik-vkusny/Link-simplifier'
    }

    response = await authenticated_client.post('/links', json=json)

    link_id = response.json()['id']

    some_user = await user(client, db_session, 'user', 'pass')

    response = await some_user.delete(f'/links/{link_id}')

    assert response.status_code == 403
    assert response.json()['detail'] == 'Это не ваша ссылка, вы не можете ее удалить!'