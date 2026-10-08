from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


import sqlalchemy.exc
import redis.exceptions
import socket


from ..settings import config
from ..exceptions import InvalidSessionException, LoginException, ForbidenException, AuthException, QueryException



def set_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(InvalidSessionException)
    def invalid_session_exception_handler(request: Request, exc: InvalidSessionException) -> JSONResponse:
        responce = JSONResponse(content={"msg":"invalid session, cookie was cleared"}, status_code=status.HTTP_401_UNAUTHORIZED)
        responce.delete_cookie(key=config.session.cookie_key)
        return responce


    @app.exception_handler(sqlalchemy.exc.NoResultFound)
    def no_record_exception_handler(request: Request, exc: sqlalchemy.exc.NoResultFound) -> JSONResponse:
        return JSONResponse(content={"msg": "This resourses was not found!"}, status_code=status.HTTP_404_NOT_FOUND)


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
            return JSONResponse(content={"msg": "Jahnre with this name already exists in database"}, status_code=status.HTTP_409_CONFLICT)

        if "duplicate key value violates unique constraint \"shops_phone_key\"" in exception_description:
            return JSONResponse(content={"msg": "Shop with this phone already exists in database"}, status_code=status.HTTP_409_CONFLICT)

        if "duplicate key value violates unique constraint \"address_uq\"" in exception_description:
            return JSONResponse(content={"msg": "Shop with this address already exists in database"}, status_code=status.HTTP_409_CONFLICT)

        if "insert or update on table \"books\" violates foreign key constraint \"authors_id_fk\"" in exception_description:
            return JSONResponse(content={"msg": "Author with this id doesnt exists in database"}, status_code=status.HTTP_409_CONFLICT)

        if "insert or update on table \"books\" violates foreign key constraint \"jahnres_id_fk\"" in exception_description:
            return JSONResponse(content={"msg": "Jahnre with this id doesnt exists in database"}, status_code=status.HTTP_409_CONFLICT)

        if "duplicate key value violates unique constraint \"books_isbn_key\"" in exception_description:
            return JSONResponse(content={"msg": "Book with thid ISBN already exists in database"}, status_code=status.HTTP_409_CONFLICT)

        if "duplicate key value violates unique constraint \"comments_pk\"" in exception_description:
            return JSONResponse(content={"msg": "User already commented this book"}, status_code=status.HTTP_409_CONFLICT)

        if "insert or update on table \"comments\" violates foreign key constraint \"books_id_fk\"" in exception_description:
            return JSONResponse(content={"msg": "Book with this id doesnt exists in database"}, status_code=status.HTTP_409_CONFLICT)

        if "update or delete on table \"authors\" violates foreign key constraint \"authors_id_fk\" on table \"books\"" in exception_description:
            return JSONResponse(content={"msg": "Book with this author exists in database"}, status_code=status.HTTP_409_CONFLICT)

        if "update or delete on table \"jahnres\" violates foreign key constraint \"jahnres_id_fk\" on table \"books\"" in exception_description:
            return JSONResponse(content={"msg": "Book with this jahnre exists in database"}, status_code=status.HTTP_409_CONFLICT)

        if "insert or update on table \"orders\" violates foreign key constraint \"shops_id_fk\"" in exception_description:
            return JSONResponse(content={"msg": "Shop with this id doesnt exists in database"}, status_code=status.HTTP_409_CONFLICT)
        
        return JSONResponse(content={"msg": "database incached error"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @app.exception_handler(redis.exceptions.ConnectionError)
    def redis_connection_exception_handler(request: Request, exc: redis.exceptions.ConnectionError) -> JSONResponse:
        return JSONResponse(content={"msg": "redis was died!"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE) 

    @app.exception_handler(socket.gaierror)
    def database_connection_exception_handler(request: Request, exc: socket.gaierror) -> JSONResponse:
        return JSONResponse(content={"msg": "database was died!"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE) 
        
        