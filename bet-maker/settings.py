from enum import Enum
from functools import lru_cache

from pydantic import computed_field, Field
from pydantic_settings import BaseSettings


class AppMode(Enum):
    DEV = "Development"
    PROD = "Production"


class ApiSettings(BaseSettings):

    API_PORT: int = Field(default=8000, validation_alias="BET_API_PORT")
    APP_MODE: AppMode

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @computed_field
    @property
    def postgres_url(self) -> str:
        return f"postgresql+asyncpg://" \
               f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/" \
               f"postgres?async_fallback=True"

@lru_cache()
def get_api_settings():
    return ApiSettings()
