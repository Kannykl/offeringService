from pydantic import computed_field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    service_name: str = "Сервис предложений UTaxi"
    server_port: int
    weather_service_api_key: str

    redis_port: int
    redis_host: str

    log_level: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @computed_field
    @property
    def redis_dns(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"


settings = Settings()
