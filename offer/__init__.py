import uvicorn
from loguru import logger

from config import settings
from offer.app import init_app

logger.add(
    "logs/offer.log",
    format="{time} {level} {message}",
    level=settings.log_level,
    rotation="10 MB",
    compression="zip",
)
app = init_app()


def start_server(port: int = settings.server_port) -> None:
    uvicorn.run("offer:app", port=port, host="0.0.0.0")
