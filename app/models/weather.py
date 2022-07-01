from beanie import Document
from pydantic import BaseModel


class DataFieldSchema(BaseModel):
    humidity: str
    source: str
    temperature: str
    weather: str
    wind: str


class Weather(Document):
    data: DataFieldSchema
    last_update: int

    class Settings:
        name = "test_collection"
