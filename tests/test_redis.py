import pytest
import json
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock
from src.backend import schemas, models
from src.backend.main import app
from src.backend.routers.users import get_current_user
from src.backend.client import get_redis_client
from src.backend.config import get_test_settings
from src.backend.database import get_db


fake_user = models.User(id=35, username='FakeUser')

def override_current_user():
    return fake_user


@pytest.mark.anyio
async def test_redis_hit(client: AsyncClient):

    test_redis = AsyncMock()
    test_db = AsyncMock()

    fake_data = [
        schemas.LinkOut(id=25, original_link='https://some_link', short_code='code', owner=schemas.UserOut(id=35, username='FakeUser'), click_count=1)
    ]

    test_redis.get.return_value = json.dumps(jsonable_encoder(fake_data))

    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_redis_client] = lambda: test_redis

    response = await client.get('/links')

    test_redis.get.assert_awaited_once_with(str(fake_user.id))
    test_db.execute.assert_not_called()

    assert response.status_code == 200
    assert response.json() == jsonable_encoder(fake_data)


@pytest.mark.anyio
async def test_redis_cache_miss(client: AsyncClient):

    test_redis = AsyncMock()
    test_db = AsyncMock()

    fake_data = [
        models.Link(
        id=36, original_link='https://some_url', short_code='t2', click_count=0, owner_id=35, owner=models.User(id=35, username='FakeUser')
        )
    ]

    test_redis.get.return_value = None

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = fake_data

    test_db.execute.return_value = mock_result

    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_redis_client] = lambda: test_redis
    app.dependency_overrides[get_db] = lambda: test_db

    response = await client.get('/links')

    assert response.status_code == 200
    assert isinstance(response.json(), list)

    test_redis.get.assert_awaited_once()
    test_db.execute.assert_awaited_once()