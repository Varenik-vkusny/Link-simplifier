import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field
from functools import lru_cache

class Settings(BaseSettings):
    db_driver: str='postgresql+asyncpg'
    db_user: str | None=None
    db_password: str | None=None
    db_host: str | None=None
    db_port: int | None=None
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
        if self.db_driver.startswith('sqlite'):
            return f'{self.db_driver}:///{self.db_name}'
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
        db_name=':memory:',
        redis_host=redis_host,
        redis_port=6379,
        redis_db=1,

        algorithm="HS256",
        secret_key="test_secret_key_for_jwt_tokens",
        access_token_expire_minutes=30,
        bot_token="fake_bot_token",
        api_base_url="http://test",
        base_url="http://test/"
    )