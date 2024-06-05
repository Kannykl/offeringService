from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from offer.dependencies.offer_dependencies import get_offer_service
from offer.domain.offer import DriveData
from offer.services.exceptions import WrongLocationException
from offer.services.offer_service import OfferService

router = APIRouter(prefix="/offers", tags=["offers"])


@router.post(
    "/",
    summary="Получение предложений по заказу такси.",
    description="В зависимости от погоды и местоположения пользователя создает предложения по заказу такси.",
    response_model=list[dict],
    responses={
        200: {
            "description": "Успешный запрос. Возвращает список предложений.",
            "content": {
                "application/json": {
                    "example": [
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
            },
        },
        400: {"description": "Wrong location."},
        500: {"description": "Internal Server Error"},
    },
)
async def get_offers_handler(
    drive_data: DriveData, offer_service: Annotated[OfferService, Depends(get_offer_service)]
):
    try:
        return await offer_service.get_offers(drive_data=drive_data)

    except WrongLocationException as exc:
        raise HTTPException(status_code=400, detail=str(exc))
