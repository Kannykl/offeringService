import json

import aioredis
from offer import logger
from config import settings


class RedisStorage:

    # Время жизни кеша (5 минут)
    CACHE_OFFERS_TTL: int = 60 * 5

    def __init__(self, url: str = settings.redis_dns):

        self.redis_client = aioredis.from_url(url, decode_responses=True)

    async def get_offers(self, user_location: str) -> list[dict] | None:
        """
        Получает предложения для пользователя по его местоположению
        Args:
            user_location (str): Местоположение пользователя ('37.620393, 55.753960')
        Returns:
            list[dict]: Список предложений
        """
        offers = await self.redis_client.get(user_location)
        if not offers:
            return

        return json.loads(offers)

    async def set_offers(self, user_location: str, offers: list[dict]) -> None:
        """
        Сохраняет предложения для пользователя по его местоположению на 5 минут.
        Args:
            user_location (str): Местоположение пользователя ('37.620393, 55.753960')
            offers (list[dict]): Список предложений

        Returns:
            None
        """
        await self.redis_client.set(user_location, json.dumps(offers))
        await self.redis_client.expire(user_location, self.CACHE_OFFERS_TTL)

    async def remove_user_location(self, user_location: str) -> None:
        await self.redis_client.delete(user_location)
