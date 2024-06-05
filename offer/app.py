from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import settings
from offer.api.v1.offers import router


def init_app() -> FastAPI:
    app = FastAPI(title=settings.service_name, lifespan=lifespan)
    app.include_router(router)

    return app


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
