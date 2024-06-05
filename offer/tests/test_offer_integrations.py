import pytest


@pytest.mark.asyncio
async def test_get_offers(client, drive_data, redis_storage):
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
