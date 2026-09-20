from typing import Annotated
from fastapi import Depends

from ..database.repositories.health_check_manager import HealthCheckManager, get_healthcheck_manager
from ..utils import RedisManager



class HealthCheckService:
    def __init__(self, database_healthcheck_manager: HealthCheckManager):
        self.__database_healthcheck_manager = database_healthcheck_manager


    async def check_redis_health(self) -> str:
        health = await RedisManager.health_check()
        return "Health" if health else "Died"

    async def check_db_health(self) -> str:
        health = await self.__database_healthcheck_manager.simple_check()
        return "Health" if health else "Died"

    def check_app_health(self) -> str:
        return "Health"


def get_healthcheck_service(
    session: Annotated[HealthCheckManager, Depends(get_healthcheck_manager)]
) -> HealthCheckService:
    return HealthCheckService(session)