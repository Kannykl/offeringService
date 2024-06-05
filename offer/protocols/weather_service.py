from typing import Protocol

from offer.domain.offer import DriveData


class WeatherService(Protocol):

    def get_current_weather(self, drive_data: DriveData) -> str:
        """Получить информацию о погоде."""
        pass
