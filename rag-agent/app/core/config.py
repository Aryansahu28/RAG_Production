from functools import lru_cache
from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Centralized application configuration.

    Values are loaded from environment variables
    and the .env file.
    """
    DATABASE_URL: str = Field(...,description="Asynchronous MySQL database connection URL")
    DB_POOL_SIZE: int = Field(default=10, ge=1)
    DB_MAX_OVERFLOW: int = Field(default=20, ge=0)
    DB_POOL_TIMEOUT: int = Field(default=30, ge=1)
    DB_POOL_RECYCLE: int = Field(default=1800, ge=1)
    DB_ECHO: bool = False


     # Application settings
    app_name: str = "RAG Agent"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = False

    # API settings
    api_v1_prefix: str = "/api/v1"

    # Logging settings
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings()-> Settings:
    """
    Return a cached application settings instance.
    """
    return Settings()

settings = get_settings()
