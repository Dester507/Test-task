from fastapi import APIRouter

from ..database.database import retrieve_weather


router = APIRouter()


@router.get(
    "/weather",
    name="weather:get",
    description="Get last temperatures from MongoDB"
)
async def get_weather():
    ans = {}
    sources = [f"source_{x}" for x in range(1, 6)]
    # Get data from MongoDB
    for source in sources:
        source_data = await retrieve_weather(source)
        ans[f"temperature_{source}"] = source_data[0].data.temperature
    # Perform data
    temperatures_int = []
    valid_list = [str(n) for n in range(10)] + ["+", "-"]
    for temperature in list(ans.values()):
        text = ""
        for letter in temperature:
            if letter not in valid_list:
                temperatures_int.append(int(text))
                break
            else:
                text += letter
    ans["max_temperature"] = f"{max(temperatures_int)}°C"
    ans["min_temperature"] = f"{min(temperatures_int)}°C"
    average_temperature = sum(temperatures_int) / 5
    if average_temperature > 0:
        average_temperature = f"+{average_temperature}°C"
    else:
        average_temperature = f"{average_temperature}°C"
    ans["average_temperature"] = average_temperature
    return ans
