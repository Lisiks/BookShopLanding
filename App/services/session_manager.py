from uuid import uuid4
import redis
from typing import Annotated
from fastapi import Depends

from ..utils import RedisManager
from ..models.users_models import UserGetPasswordModel, UserGetModel
from ..settings import config


class SessionManager:
    def __init__(self, redis_client: redis.asyncio.Redis):
        self.__redis_client = redis_client


    async def create_session(self, user_data: UserGetPasswordModel) -> str:
        session = str(uuid4())

        await self.__redis_client.hset(
            config.session.hash_key, 
            mapping={session: user_data.model_dump_json()} 
        )

        await self.__redis_client.hexpire(config.session.hash_key, config.session.ttl, session)

        return session


    async def read_session(self, session: str) -> UserGetModel | None:
        user_data = await self.__redis_client.hget(config.session.hash_key, session)
        return UserGetModel.model_validate_json(user_data.decode()) if user_data is not None else None


    async def delete_session(self, session: str) -> None:
        await self.__redis_client.hdel(config.session.hash_key, session)


    async def delete_sessions_by_id(self, user_id: int) -> None:
        sessions_dict = await self.__redis_client.hgetall(config.session.hash_key)

        user_sessions = [session for session, data in sessions_dict.items() if UserGetModel.model_validate_json(data.decode()).id == user_id]
        
        await self.__redis_client.hdel(config.session.hash_key, *user_sessions)


def get_session_manager(redis_client: Annotated[redis.asyncio.Redis, Depends(RedisManager.get_client)]) -> SessionManager:
    return SessionManager(redis_client)