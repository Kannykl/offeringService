from typing import Annotated

from fastapi import Depends

from offer.protocols.cache_storage import CacheStorage
from offer.repositories.redis_repo import RedisStorage
from offer.services.offer_service import OfferService


def get_cache_storage() -> CacheStorage:
    return RedisStorage()


def get_offer_service(cache_storage: Annotated[CacheStorage, Depends(get_cache_storage)]) -> OfferService:
    return OfferService(cache_storage=cache_storage)
