import json

import pytest
from starlette.testclient import TestClient
from testcontainers.redis import RedisContainer

from config import settings
from offer import app
from offer.dependencies.offer_dependencies import get_cache_storage
from offer.domain.offer import DriveData
from offer.repositories.redis_repo import RedisStorage
from offer.services.offer_service import OfferService


class TestCacheStorage:
    redis_storage = {
        "55.755831, 37.617673": [
            {
                "tariff": {
                    "price": 1000.0,
                    "name": "economy",
                },
                "car_info": {
                    "model": "Hunday Solaris",
                    "color": "black",
                    "number": "A123AA",
                    "driver_name": "Иван Иванов",
                    "driver_phone": "+7-999-123-45-67",
                },
                "time_to_wait": "0:05:00",
            },
            {
                "tariff": {
                    "price": 1500.0,
                    "name": "comfort",
                },
                "car_info": {
                    "model": "KIA Rio",
                    "color": "white",
                    "number": "B456BB",
                    "driver_name": "Петр Петров",
                    "driver_phone": "+7-999-123-45-68",
                },
                "time_to_wait": "0:10:00",
            },
        ]
    }

    async def get_offers(self, user_location: str) -> list[dict] | None:
        return self.redis_storage.get(user_location)

    async def set_offers(self, user_location: str, offers: list[dict]) -> None:
        self.redis_storage[user_location] = json.dumps(offers)

    async def remove_user_location(self, user_location: str) -> None: ...


@pytest.fixture(scope="module")
def cache_storage():
    return TestCacheStorage()


@pytest.fixture(scope="module")
def offer_service(cache_storage):
    return OfferService(cache_storage=cache_storage)


@pytest.fixture
def drive_data():
    return DriveData(
        user_lat=55.75100,
        user_lon=37.61400,
        destination_address="Moscow, Red Square, 1",
        weather="sunny",
    )


@pytest.fixture
def drive_data_with_offers_in_cache():
    return DriveData(
        user_lat=55.755831,
        user_lon=37.617673,
        destination_address="Moscow, Red Square, 1",
        weather="sunny",
    )


@pytest.fixture
def drive_data_not_in_cache():
    return DriveData(
        user_lat=55.123123,
        user_lon=37.123123,
        destination_address="Moscow, Red Square, 1",
        weather="sunny",
    )


@pytest.fixture(scope="session")
def client():
    return TestClient(app=app)


@pytest.fixture(scope="module")
def monkeypatch_cache_storage():
    app.dependency_overrides[get_cache_storage] = TestCacheStorage


@pytest.fixture(scope="module", autouse=True)
def redis_docker_container():
    with RedisContainer().with_exposed_ports(settings.redis_port) as redis_container:
        yield redis_container


@pytest.fixture(scope="module")
def redis_storage(redis_docker_container):
    return RedisStorage(f"redis://localhost:{redis_docker_container.get_exposed_port(settings.redis_port)}/0")
