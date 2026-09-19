from typing import Annotated, Optional
from fastapi import Depends, BackgroundTasks, Cookie
from uuid import uuid4
import redis

from ..database.repositories.users_repository import get_repository, UsersRepository
from ..models.users_models import UserPostModel, UserGetModel, UserLoginModel
from ..models.search_and_pagination_models import UsersSearchAndPaginationModel
from ..exceptions import NoRecordException, LoginException, BlockedUserException, ForbidenException, AuthinticateException

from ..utils import PasswordManager, RedisManager
from ..settings import config


class UsersService:
    def __init__(self, repository: UsersRepository, redis_client: redis.asyncio.Redis, bg_tasks: BackgroundTasks):
        self.__redis_client = redis_client
        self.__repository = repository
        self.__bg_tasks = bg_tasks

    async def create_user(self, user_params: UserPostModel, is_admin: bool) -> UserGetModel:
        return await self.__repository.create_user(user_params, is_admin)

    async def get_users(self, search_params: UsersSearchAndPaginationModel, is_admin: bool) -> dict[int, UserGetModel]:
        return await self.__repository.get_users(search_params)

    async def change_user_admin_mode(self, user_id: int, admin_mode: bool) -> UserGetModel:
        changed_user = await self.__repository.change_user_admin_mode(user_id, admin_mode)

        if changed_user is None:
            raise NoRecordException(f"User with id={user_id} doesnt exists in database!")


        self.__bg_tasks.add_task(self.__logout_all, changed_user.id)

        return changed_user


    async def change_user_block_mode(self, user_id: int, block_mode: bool) -> UserGetModel:
        changed_user = await self.__repository.change_user_block_mode(user_id, block_mode)

        if changed_user is None:
            raise NoRecordException(f"User with id={user_id} doesnt exists in database!")

        self.__bg_tasks.add_task(self.__logout_all, changed_user.id)

        return changed_user


    async def get_by_id(self, user_id: int) -> UserGetModel:
        user = await self.__repository.get_by_id(user_id)

        if user is None:
            raise NoRecordException(f"User with id={user_id} doesnt exists in database!")

        return user


    async def user_login(self, user_login_params: UserLoginModel, is_admin: bool) -> str:
        user = await self.__repository.get_by_name(user_login_params.username)

        if user is None or not PasswordManager.verify_password(user_login_params.plain_password, user.password_hash):
            raise LoginException("Incorrect login or password!")

        if user.is_blocked:
            raise BlockedUserException("This user was blocked!")

        if user.is_admin == False and is_admin == True:
            raise ForbidenException("This user isnt an administrator!")

        session_uuid = uuid4()

        await self.__redis_client.hset(
            key=config.session.hash_key, mapping={session_uuid: user.model_dump_json()}
        )
        await self.__redis_client.hexpire(config.session.hash_key, config.session.ttl, session_uuid)

        return session_uuid


    async def logout(self, session_uuid: str) -> None:
        await self.__redis_client.hdel(config.session.hash_key, session_uuid)


    async def __logout_all(self, user_id: int) -> None:
        sessions_dict = await self.__redis_client.hgetall(config.session.hash_key)

        user_sessions = [session for session, data in sessions_dict.items() if UserGetModel.model_validate_json(data.decode()).id == user_id]

        await self.__redis_client.hdel(config.session.hash_key, *user_sessions)



        
    
async def get_session_data(
    redis_client: Annotated[redis.asyncio.Redis, Depends(RedisManager.get_client)],
    session: Annotated[Optional[str], Cookie(config.session.cookie_key)] = ""
) -> UserGetModel | None:
    data = await redis_client.hget(config.session.hash_key, session)

    return UserGetModel.model_validate_json(data.encode()) if data is None else None



def get_user_auth_data(
    user_data: Annotated[Optional[UserGetModel], Depends(get_session_data)]
) -> UserGetModel:
    if user_data is None:
        raise AuthinticateException("User is unathorise!")

    if user_data.is_blocked == True:
        raise BlockedUserException("This user was blocked!")

    return user_data



def get_admin_auth_data(
    user_data: Annotated[Optional[UserGetModel], Depends(get_session_data)]
) -> UserGetModel:
    if user_data is None:
        raise AuthinticateException("User is unathorise!")

    if user_data.is_blocked == True:
        raise BlockedUserException("This user was blocked!")

    if not user_data.is_admin:
        raise ForbidenException("This user isnt an administrator!")
    
    return user_data


async def get_service(
    repository: Annotated[UsersRepository, Depends(get_repository)],
    redis_client: Annotated[redis.asyncio.Redis, Depends(RedisManager.get_client)],
    bg_tasks: BackgroundTasks

) -> UsersService:
     return UsersService(repository, redis_client, bg_tasks)
     