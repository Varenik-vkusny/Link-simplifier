import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    algorithm: str
    secret_key: str
    access_token_expire_minutes: int
    bot_token: str
    api_base_url: str
    base_url: str
    redis_url: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


@lru_cache
def get_settings():
    return Settings()


def get_test_settings():
    return Settings(
        database_url="sqlite+aiosqlite:///:memory:",
        redis_url="redis://localhost:6379/1",
        algorithm="HS256",
        secret_key="test_secret_key_for_jwt_tokens",
        access_token_expire_minutes=30,
        bot_token="fake_bot_token",
        api_base_url="http://test",
        base_url="http://test/"
    )