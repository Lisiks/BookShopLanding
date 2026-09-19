import redis
from ..settings import config

class RedisManager:
    __client: redis.asyncio.Redis

    @classmethod
    def init_client(cls) -> None:
        cls.__client = redis.asyncio.Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db
        )

    @classmethod
    def get_client(cls) -> redis.asyncio.Redis:
        return cls.__client