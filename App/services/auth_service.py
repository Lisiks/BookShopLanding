from typing import Annotated, Optional
from fastapi import Depends, Cookie


from ..database.repositories.users_repository import get_repository, UsersRepository
from ..models.users_models import UserPostModel, UserGetModel, UserLoginModel
from ..models.search_and_pagination_models import UsersSearchModel
from ..exceptions import LoginException, ForbidenException, AuthException, InvalidSessionException

from ..utils import PasswordManager, RedisManager
from ..settings import config



class AuthService:
    def __init__(self, repository: UsersRepository):
        self.__repository = repository


    async def user_login(self, user_data: UserLoginModel) -> str:
        user = await self.__repository.get_by_name(user_data.username)

        if user is None or not PasswordManager.verify_password(user_data.plain_password, user.password_hash):
            raise LoginException("Incorrect login or password!")

        if user.is_blocked:
            raise ForbidenException("This user was blocked!")

        return await RedisManager.create_session(user)


    async def admin_login(self, user_data: UserLoginModel) -> str:
        user = await self.__repository.get_by_name(user_data.username)
        
        if user is None or not PasswordManager.verify_password(user_data.plain_password, user.password_hash):
            raise LoginException("Incorrect login or password!")

        if user.is_blocked:
            raise ForbidenException("This user was blocked!")

        if user.is_admin == False:
            raise ForbidenException("This user isnt an administrator!")

        return await RedisManager.create_session(user)


    async def logout(self, session: str) -> None:
        await RedisManager.delete_session(session)



async def get_data_from_session(
    session: Annotated[Optional[str], Cookie(alias=config.session.cookie_key)] = None
) -> UserGetModel | None:
    
    if session is None:
        return None

    session_data = await RedisManager.read_session(session)

    if session_data is None:
        raise InvalidSessionException("Your session was invalid!")

    return session_data
   



def auth_user(
    user_data: Annotated[Optional[UserGetModel], Depends(get_data_from_session)]
) -> UserGetModel:
    if user_data is None:
        raise AuthException("User is unathorise!")
    return user_data



def auth_admin(
    user_data: Annotated[Optional[UserGetModel], Depends(get_data_from_session)]
) -> UserGetModel:
    if user_data is None:
        raise AuthException("User is unathorise!")

    if not user_data.is_admin:
        raise ForbidenException("This user isnt an administrator!")
    
    return user_data





def get_service(
    repository: Annotated[UsersRepository, Depends(get_repository)],
) -> AuthService:
    return AuthService(repository)