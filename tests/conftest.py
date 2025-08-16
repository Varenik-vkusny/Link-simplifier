import pytest
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import redis.asyncio as redis
from src.backend.main import app
from src.backend.database import get_db, Base
from src.backend import models
from src.backend.config import get_test_settings, get_settings


app.dependency_overrides[get_settings] = get_test_settings


TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'


test_async_engine = create_async_engine(TEST_DATABASE_URL)


TestAsyncLocalSession = sessionmaker(bind=test_async_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(autouse=True, scope='function')
async def prepare_database():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    test_settings = get_test_settings()
    redis_client = redis.from_url(test_settings.redis_url)
    await redis_client.flushdb()
    await redis_client.aclose()
    
    yield

    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
async def client() -> AsyncGenerator[AsyncClient, None]:

    async def override_db() -> AsyncGenerator[AsyncSession, None]:
        async with TestAsyncLocalSession() as session:
            yield session
    
    app.dependency_overrides[get_db] = override_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac



@pytest.fixture(scope='function')
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncLocalSession() as session:
        yield session


@pytest.fixture(scope='function')
async def test_user(db_session: AsyncSession) -> models.User:

    from src.backend.security import hash_password

    user = models.User(username='test_user', password_hash=hash_password('test_password'))

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return user


@pytest.fixture(scope='function')
async def authenticated_client(client: AsyncClient, test_user: models.User) -> AsyncClient:

    data = {
        'username': test_user.username,
        'password': 'test_password'
    }

    response = await client.post('/token', data=data)

    access_token = response.json()['access_token']

    client.headers['Authorization'] = f'Bearer {access_token}'

    return client



async def user(client: AsyncClient, db_session: AsyncSession, username: str, password: str):

    from src.backend.security import hash_password

    user = models.User(username=username, password_hash=hash_password(password))

    db_session.add(user)
    await db_session.commit()

    data = {
        'username': username,
        'password': password
    }

    response = await client.post('/token', data=data)

    token_data = response.json()

    access_token = token_data['access_token']

    client.headers['Authorization'] = f'Bearer {access_token}'

    return client