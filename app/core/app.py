from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi.staticfiles import StaticFiles


from .exception_handlers import set_exception_handlers
from ..utils import RedisManager
from ..web import router
from ..database.repositories.users_repository import create_super_user
from ..settings import config



@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None, None]:
    await RedisManager.init_client()
    await create_super_user()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title=config.app.name,
        description=config.app.description,
        version=config.app.version
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    app.include_router(router)
    set_exception_handlers(app)
    return app


