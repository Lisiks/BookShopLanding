from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, label, text
from fastapi import Depends
from typing import Annotated

from ...core.postgresql import get_session


class HealthCheckManager:
    def __init__(self, session: AsyncSession):
        self.__session = session


    async def simple_check(self) -> bool:
        stmt = select(text("TRUE"))
        return await self.__session.scalar(stmt)


def get_healthcheck_manager(session: Annotated[AsyncSession, Depends(get_session)]) -> HealthCheckManager:
    return HealthCheckManager(session)


