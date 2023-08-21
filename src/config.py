from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """FastAPI settings."""
    model_config = SettingsConfigDict(env_file="config/.env")

    # App
    APP_NAME: str = "Exchange Rates API"
    APP_DESCRIPTION: str = "Exchange Rates API using FastAPI"
    APP_VERSION: str = "0.0.1"
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000
    APP_RELOAD: bool = False
    APP_DEBUG: bool = True
    LOG_LEVEL: str = "info"

    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "test"
    DB_PASSWORD: str = "test"
    DB_NAME: str = "exchange_fastapi"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_CACHE_EXPIRE: int = 60 * 60

    # API
    API_V1_URL: str = "/api/v1"
    API_DOCS_URL: str = "/api/v1/docs"

    # Auth
    SECRET_KEY: str = "SECRET_KEY"


settings = Settings()
