from typing import List

from ..models.weather import Weather


weather_collection = Weather


async def retrieve_weather(source: str):
    weather = await weather_collection.find(
        Weather.data.source == source
    ).sort(
        "-last_update"
    ).limit(
        1
    ).to_list()
    return weather
