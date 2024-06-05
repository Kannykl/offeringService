import uuid
from datetime import timedelta
from enum import Enum

from pydantic import (
    BaseModel,
    Field,
)


class Offer(BaseModel):
    """Модель предложения по заказу такси."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    tariff: "Tariff"
    car_info: "CarInfo"
    time_to_wait: timedelta


class Tariff(BaseModel):
    """Информация о тарифе."""

    price: float
    name: "TarifNames"


class CarInfo(BaseModel):
    """Информация о машине."""

    model: str
    color: str
    number: str
    driver_name: str
    driver_phone: str


class TarifNames(str, Enum):
    """Названия тарифов."""

    economy = "economy"
    business = "business"


class DriveData(BaseModel):
    """Информация о поездке."""

    user_lon: float
    user_lat: float

    weather: str

    destination_address: str


class WeatherState(str, Enum):
    """Состояние погоды."""

    clear = "clear"
    rain = "rain"
    snow = "snow"
    storm = "storm"
    fog = "fog"
    hail = "hail"
    sleet = "sleet"
    wind = "wind"
    cloudy = "cloudy"
    overcast = "overcast"
    partly_cloudy = "partly_cloudy"
    drizzle = "drizzle"
    mist = "mist"
    smoke = "smoke"
    dust = "dust"
    sand = "sand"
    ash = "ash"
    squall = "squall"
    tornado = "tornado"
    hot = "hot"
    cold = "cold"
    unknown = "unknown"
    other = "other"
