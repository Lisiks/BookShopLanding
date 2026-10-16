from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from .exception_handlers import set_exception_handlers
from ..utils import RedisManager
from ..web import router
from ..database.repositories.users_repository import create_super_user
from ..settings import config



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None, None]:
    await RedisManager.init_client()
    await create_super_user()
    FastAPICache.init(RedisBackend(RedisManager.get_client()), prefix=config.cache.namespaces.app)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title=config.app.name,
        description=config.app.description,
        version=config.app.version
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.app.allowed_origins_list,
        allow_credentials=True,
        allow_headers=["*"],
        allow_methods=["*"]
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    app.include_router(router)
    set_exception_handlers(app)
    return app


