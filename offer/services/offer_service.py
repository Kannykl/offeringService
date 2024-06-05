from dataclasses import dataclass
from datetime import timedelta
from typing import NewType
from urllib.parse import urlencode

import requests
from geopy.distance import great_circle
from requests import HTTPError

from offer import logger
from offer.domain.offer import (
    CarInfo,
    DriveData,
    Offer,
    Tariff,
    TarifNames,
)
from offer.protocols.cache_storage import CacheStorage
from offer.services.exceptions import WrongLocationException

# Расчеты по поездке производятся в рублях
Ruble = NewType("RUBLE", float)
Meter = NewType("Meter", float)


@dataclass(frozen=True, slots=True)
class Coordinates:
    latitude: float
    longtitude: float


class OfferService:

    # Стоимость поездки за метр
    RUBLE_PER_METRE: Ruble = 0.2

    def __init__(self, cache_storage: CacheStorage):
        self.cache_storage = cache_storage

    async def get_offers(self, drive_data: DriveData) -> list[dict]:
        """
        Создает предложения по заказу такси.
        Args:
            drive_data (DriveData): Данные о поездке.

        Returns:
            list[dict]: Список предложений.
        """

        offers_from_cache = await self.cache_storage.get_offers(f"{drive_data.user_lat}, {drive_data.user_lon}")

        if offers_from_cache:
            return offers_from_cache

        offers = [
            Offer(
                tariff=Tariff(
                    price=self.calculate_base_drive_cost(drive_data),
                    name=TarifNames.economy,
                ),
                car_info=CarInfo(
                    model="Hunday Solaris",
                    color="black",
                    number="A123AA",
                    driver_name="Иван Иванов",
                    driver_phone="+7-999-123-45-67",
                ),
                time_to_wait=timedelta(minutes=5),
            ).model_dump(mode="json"),
            Offer(
                tariff=Tariff(
                    price=self.calculate_base_drive_cost(drive_data) * 1.5,
                    name=TarifNames.business,
                ),
                car_info=CarInfo(
                    model="Toyota Camry",
                    color="white",
                    number="A321AA",
                    driver_name="Петр Петров",
                    driver_phone="+7-999-765-43-21",
                ),
                time_to_wait=timedelta(minutes=10),
            ).model_dump(mode="json"),
        ]

        await self.cache_storage.set_offers(f"{drive_data.user_lat}, {drive_data.user_lon}", offers)

        return offers

    def calculate_base_drive_cost(self, drive_data: DriveData) -> Ruble:
        """
        Рассчитывает стоимость поездки.
        Args:
            drive_data (DriveData): Данные о поездке.

        Returns:
            Ruble: Стоимость поездки.
        """
        coefficients = {
            "sunny": 0.95,
            "dry": 0.87,
            "day": 0.93,
            "night": 1.2,
            "rainy": 1.4,
            "foggy": 1.25,
            "snowy": 1.78,
            "icy": 1.5,
        }
        try:
            location = self.convert_address_to_coordinates(drive_data.destination_address)

        except HTTPError:
            raise WrongLocationException()

        desitanation_lat, destination_lon = location.latitude, location.longtitude

        distance = self.calculate_distance(drive_data.user_lat, drive_data.user_lon, desitanation_lat, destination_lon)

        for coeff in coefficients:
            if coeff in drive_data.weather:
                return Ruble(round(distance * self.RUBLE_PER_METRE * coefficients[coeff], 2))

        else:
            return Ruble(round(distance * self.RUBLE_PER_METRE, 2))

    def calculate_distance(self, start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> Meter:
        """
        Рассчитывает расстояние между двумя точками.
        Args:
            start_lat (float): Координата местонахождения пользователя (широта).
            start_lon (float): Координата местонахождения пользователя (долгота).
            end_lat (float): Координата пункта назначения (широта).
            end_lon (float): Координата пункта назначения (долгота).

        Returns:
            float: Расстояние между двумя точками в метрах.
        """

        coords_1 = (start_lat, start_lon)

        coords_2 = (end_lat, end_lon)

        distance = great_circle(coords_1, coords_2).meters

        return Meter(distance)

    def convert_address_to_coordinates(self, address: str) -> Coordinates:
        """
        Конвертирует адрес в координаты.
        Args:
            address (str): Адрес.

        Returns:
            Coordinates: Координаты.
        """

        params = urlencode({"q": address, "format": "jsonv2", "addressdetails": 0, "limit": 1})

        response = requests.get("https://nominatim.openstreetmap.org/search", params=params)

        logger.info(f"Fetching coordinates for address=%s; GOT status=%s", address, response.status_code)

        response.raise_for_status()

        data = response.json()

        return Coordinates(latitude=data[0]["lat"], longtitude=data[0]["lon"])
