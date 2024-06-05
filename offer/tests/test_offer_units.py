from datetime import timedelta

import pytest

from offer.domain.offer import TarifNames


def test_calculate_distance(offer_service):
    distance = offer_service.calculate_distance("55.755831", "37.617673", "55.755831", "37.617673")
    assert distance == 0.0


def test_calculate_not_zero_meters_distance(offer_service):
    distance = offer_service.calculate_distance("55.755831", "37.617673", "55.755831", "37.617773")
    assert distance == 6.257178675721266


def test_convert_address_to_coordinates(offer_service):
    location = offer_service.convert_address_to_coordinates("Moscow, st. Tverskaya, 1")
    assert location.latitude, location.longtitude == ("55.75578165", "37.61490396465909")


def test_calculate_base_drive_cost(offer_service, drive_data):
    cost = offer_service.calculate_base_drive_cost(drive_data)
    assert cost == 102.33


@pytest.mark.asyncio
async def test_get_offers_from_cache(offer_service, drive_data_with_offers_in_cache):
    offers = await offer_service.get_offers(drive_data=drive_data_with_offers_in_cache)
    assert offers == [
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


@pytest.mark.asyncio
async def test_get_offers_without_cache(offer_service, drive_data_not_in_cache):
    offers = await offer_service.get_offers(drive_data=drive_data_not_in_cache)

    for offer in offers:
        offer.pop("id")

    assert offers == [
        {
            "tariff": {
                "price": 14613.52,
                "name": "economy",
            },
            "car_info": {
                "model": "Hunday Solaris",
                "color": "black",
                "number": "A123AA",
                "driver_name": "Иван Иванов",
                "driver_phone": "+7-999-123-45-67",
            },
            "time_to_wait": timedelta(minutes=5),
        },
        {
            "tariff": {
                "price": 21920.28,
                "name": TarifNames.business,
            },
            "car_info": {
                "model": "Toyota Camry",
                "color": "white",
                "number": "A321AA",
                "driver_name": "Петр Петров",
                "driver_phone": "+7-999-765-43-21",
            },
            "time_to_wait": timedelta(minutes=10),
        },
    ]


def test_get_offers_handler(client, drive_data, offer_service, monkeypatch_cache_storage):
    response = client.post("/offers", json=drive_data.model_dump(mode="json"))

    assert response.status_code == 200
    assert response.json() == [
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
