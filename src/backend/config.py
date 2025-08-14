from pydantic_settings import BaseSettings, SettingsConfigDict


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


settings = Settings()