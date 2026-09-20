import redis
from uuid import uuid4

from ..settings import config
from ..models.users_models import UserGetPasswordModel, UserGetModel

class RedisManager:
    __client: redis.asyncio.Redis

    @classmethod
    async def init_client(cls) -> None:
        cls.__client = await redis.asyncio.Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db
        )

    @classmethod
    def get_client(cls) -> redis.asyncio.Redis:
        return cls.__client




    @classmethod
    async def health_check(cls) -> bool:
        return await cls.__client.ping()





    @classmethod
    async def create_session(cls, user_params: UserGetPasswordModel) -> str:
        session = str(uuid4())
        
        await cls.__client.hset(
            config.session.hash_key, 
            mapping={session: user_params.model_dump_json()} 
        )
        
        await cls.__client.hexpire(config.session.hash_key, config.session.ttl, session)
        
        return session


    @classmethod
    async def read_session(cls, session: str) -> str | None:
        user_json_string = await cls.__client.hget(config.session.hash_key, session)
        return UserGetModel.model_validate_json(user_json_string.decode()) if user_json_string is not None else None


    @classmethod
    async def delete_session(self, session: str) -> None:
        await self.__client.hdel(config.session.hash_key, session)

        

    @classmethod
    async def delete_sessions_by_id(self, user_id: int) -> None:
        sessions_dict = await self.__client.hgetall(config.session.hash_key)

        user_sessions = [session for session, data in sessions_dict.items() if UserGetModel.model_validate_json(data.decode()).id == user_id]

        await self.__client.hdel(config.session.hash_key, *user_sessions)