import httpx

from config import settings
from offer import logger
from offer.domain.offer import DriveData


class OpenWeatherAPIService:
    """Сервис для получения информации о погоде."""

    def __init__(self, api_key: str = settings.weather_service_api_key):
        self.base_url = (
            f"https://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&exclude=hourly,daily&" f"appid={api_key}"
        )
        logger.info("OpenWeatherAPIService initialized.")

    async def get_current_weather(self, drive_data: DriveData) -> str:
        """Получить информацию о погоде."""
        async with httpx.AsyncClient() as session:
            response = await session.get(self.base_url % (drive_data.user_lat, drive_data.user_lon))
            response.raise_for_status()
            data = response.json()
            weather = data["weather"][0]["description"]

            return weather
