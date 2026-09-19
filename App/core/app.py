from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from ..utils import RedisManager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None, None]:
    await RedisManager.init_client()
    yield



def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    return app