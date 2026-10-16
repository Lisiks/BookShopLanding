from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, literal
from fastapi import Depends
from typing import Annotated

from ...dto.shops_dto import ShopGetDTO, ShopPostDTO
from ...dto.search_dto import ShopSearchDTO
from ..models import ShopsORM
from ...core.postgresql import get_session



class ShopsRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_shop(self, shop_params: ShopPostDTO) -> None:
        new_shop = ShopsORM(**shop_params.model_dump())
        self.__session.add(new_shop)
        await self.__session.commit()


    async def delete_shop(self, shop_id: int) -> None:
        stmt = select(ShopsORM).where(ShopsORM.id == shop_id)
        query_result = await self.__session.scalars(stmt)
        shop = query_result.one()

        await self.__session.delete(shop)
        await self.__session.commit()


    async def modify_shop(self, shop_id: int, shop_params: ShopPostDTO) -> None:
        stmt = select(ShopsORM).where(ShopsORM.id == shop_id)
        query_result = await self.__session.scalars(stmt)
        shop = query_result.one()


        for field, value in shop_params.model_dump().items():
            setattr(shop, field, value)

        await self.__session.commit()


    async def get_all(self, search_params: ShopSearchDTO) -> dict[int, ShopGetDTO]:
        stmt = select(ShopsORM)

        if search_params.address is not None:
            stmt = stmt.where(or_(
                literal(search_params.address).icontains(ShopsORM.town),
                literal(search_params.address).icontains(ShopsORM.street),
                literal(search_params.address).icontains(ShopsORM.housing)
            ))

        stmt.order_by(ShopsORM.town, ShopsORM.street, ShopsORM.housing)

        shops = await self.__session.scalars(stmt)
        return {shop.id: ShopGetDTO.model_validate(shop) for shop in shops.all()}


def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> ShopsRepository:
    return ShopsRepository(session)