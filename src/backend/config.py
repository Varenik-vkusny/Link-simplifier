import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from functools import lru_cache

class Settings(BaseSettings):
    db_driver: str='postgresql+asyncpg'
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    redis_host: str
    redis_port: int
    redis_db: int=0

    algorithm: str
    secret_key: str
    access_token_expire_minutes: int
    bot_token: str
    api_base_url: str
    base_url: str

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f'{self.db_driver}://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'
        )
    
    @computed_field
    @property
    def redis_url(self) -> str:
        return (
            f'redis://{self.redis_host}:{self.redis_port}/{self.redis_db}'
        )

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_settings():
    return Settings()


def get_test_settings():

    redis_host = os.getenv('TEST_REDIS_HOST', 'localhost')
    return Settings(
        database_url="sqlite+aiosqlite:///:memory:",
        redis_url=f"redis://{redis_host}:6379/1",
        algorithm="HS256",
        secret_key="test_secret_key_for_jwt_tokens",
        access_token_expire_minutes=30,
        bot_token="fake_bot_token",
        api_base_url="http://test",
        base_url="http://test/"
    )