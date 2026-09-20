from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sqlalchemy.exc
import redis.exceptions
import socket

from ..utils import RedisManager
from ..web import router
from ..database.repositories.users_repository import create_super_user
from ..settings import config
from ..exceptions import InvalidSessionException, LoginException, ForbidenException, AuthException, NoRecordException, QueryException


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

    app.include_router(router)
    set_exception_handlers(app)
    return app


def set_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(InvalidSessionException)
    def invalid_session_exception_handler(request: Request, exc: InvalidSessionException) -> JSONResponse:
        responce = JSONResponse(content={"msg":"invalid session, cookie was cleared"}, status_code=status.HTTP_403_FORBIDDEN)
        responce.delete_cookie(key=config.session.cookie_key)
        return responce


    @app.exception_handler(NoRecordException)
    def no_record_exception_handler(request: Request, exc: NoRecordException) -> JSONResponse:
        return JSONResponse(content={"msg": exc.args[0]}, status_code=status.HTTP_404_NOT_FOUND)


    @app.exception_handler(AuthException)
    def auth_exception_handler(request: Request, exc: AuthException) -> JSONResponse:
        return JSONResponse(content={"msg": exc.args[0]}, status_code=status.HTTP_401_UNAUTHORIZED)


    @app.exception_handler(LoginException)
    def login_exception_handler(request: Request, exc: LoginException) -> JSONResponse:
        if exc.args[0] == "You are already login!":
            return JSONResponse(content={"msg": exc.args[0]}, status_code=status.HTTP_400_BAD_REQUEST)

        return JSONResponse(content={"msg": exc.args[0]}, status_code=status.HTTP_401_UNAUTHORIZED)


    @app.exception_handler(ForbidenException)
    def forbiden_exception_handler(request: Request, exc: ForbidenException) -> JSONResponse:
        return JSONResponse(content={"msg": exc.args[0]}, status_code=status.HTTP_403_FORBIDDEN)


    @app.exception_handler(QueryException)
    def query_excception_handler(request: Request, exc: QueryException) -> JSONResponse:
        return JSONResponse(content={"msg": exc.args[0]}, status_code=status.HTTP_400_BAD_REQUEST)


    @app.exception_handler(sqlalchemy.exc.IntegrityError)
    def query_excception_handler(request: Request, exc: sqlalchemy.exc.IntegrityError) -> JSONResponse:
        exception_description = exc.args[0]

        if "duplicate key value violates unique constraint \"users_username_key\"" in exception_description:
            return JSONResponse(content={"msg": "User with this username already exists in database"}, status_code=status.HTTP_409_CONFLICT)

        if "duplicate key value violates unique constraint \"jahnres_name_key\"" in exception_description:
            return JSONResponse(content={"msg": "Jahnre with this username already exists in database"}, status_code=status.HTTP_409_CONFLICT)


        return JSONResponse(content={"msg": "ya"}, status_code=418)

    @app.exception_handler(redis.exceptions.ConnectionError)
    def redis_connection_exception_handler(request: Request, exc: redis.exceptions.ConnectionError) -> JSONResponse:
        return JSONResponse(content={"msg": "redis was died!"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE) 

    @app.exception_handler(socket.gaierror)
    def database_connection_exception_handler(request: Request, exc: socket.gaierror) -> JSONResponse:
        return JSONResponse(content={"msg": "database was died!"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE) 
        
        
