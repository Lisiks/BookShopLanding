from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from ...models.jahnres_models import JahnreGetModel, JahnrePostModel
from ...models.search_and_pagination_models import JahnresSearchModel
from ..shemas import Jahnres
from ...core.postgresql import get_session
from ...exceptions import NoRecordException



class JahnresRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_jahnre(self, jahnre_params: JahnrePostModel) -> None:
        new_jahnre = Jahnres(**jahnre_params.model_dump())
        self.__session.add(new_jahnre)
        await self.__session.commit()


    async def delete_jahnre(self, jahnre_id: int) -> None:
        jahnre = await self.__session.get(Jahnres, jahnre_id)

        if jahnre is None:
            raise NoRecordException(f"Jahnre with id={jahnre_id} doesnt exists in database!")

        await self.__session.delete(jahnre)
        await self.__session.commit()


    async def modify_jahnre(self, jahnre_id: int, jahnre_params: JahnrePostModel) -> None:
        jahnre = await self.__session.get(Jahnres, jahnre_id)
        
        if jahnre is None:
            raise NoRecordException(f"Jahnre with id={jahnre_id} doesnt exists in database!")

        for field, value in jahnre_params.model_dump().items():
            setattr(jahnre, field, value)

        await self.__session.commit()


    async def get_all(self, search_params: JahnresSearchModel) -> dict[int, JahnreGetModel]:
        stmt = select(Jahnres)

        if search_params.name is not None:
            stmt = stmt.where(Jahnres.name.ilike(f"{search_params.name}%"))

        jahnres = await self.__session.scalars(stmt)
        return {jahnre.id: JahnreGetModel.model_validate(jahnre) for jahnre in jahnres.all()}


def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> JahnresRepository:
    return JahnresRepository(session)