from typing import List
from functools import lru_cache

from pydantic import BaseSettings, Field
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from ..models.weather import Weather


class Settings(BaseSettings):
    APP_NAME: str = "API for test task"
    APP_VERSION: str = "0.0.1"
    ALLOWED_HOSTS: List[str] = ["*"]

    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # DATABASE_URL: str = "mongodb+srv://dester:admin@clusterfortestwork.jqfpq.mongodb.net/?retryWrites=true&w=majority"


@lru_cache()
def cached_settings():
    return Settings()


settings = cached_settings()


async def initiate_database():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(database=client.test_database, document_models=[Weather])
