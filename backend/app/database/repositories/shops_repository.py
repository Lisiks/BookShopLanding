from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, literal
from fastapi import Depends
from typing import Annotated

from ...models.shops_models import ShopGetModel, ShopPostModel
from ...models.search_and_pagination_models import ShopSearchModel
from ..shemas import Shops
from ...core.postgresql import get_session
from ...exceptions import NoRecordException



class ShopsRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_shop(self, shop_params: ShopPostModel) -> None:
        new_shop = Shops(**shop_params.model_dump())
        self.__session.add(new_shop)
        await self.__session.commit()


    async def delete_shop(self, shop_id: int) -> None:
        stmt = select(Shops).where(Shops.id == shop_id)
        query_result = await self.__session.execute(stmt)
        shop = query_result.one()

        await self.__session.delete(shop)
        await self.__session.commit()


    async def modify_shop(self, shop_id: int, shop_params: ShopPostModel) -> None:
        stmt = select(Shops).where(Shops.id == shop_id)
        query_result = await self.__session.execute(stmt)
        shop = query_result.one()

        for field, value in shop_params.model_dump().items():
            setattr(shop, field, value)

        await self.__session.commit()


    async def get_all(self, search_params: ShopSearchModel) -> dict[int, ShopGetModel]:
        stmt = select(Shops)

        if search_params.address is not None:
            stmt = stmt.where(or_(
                literal(search_params.address).icontains(Shops.town),
                literal(search_params.address).icontains(Shops.street),
                literal(search_params.address).icontains(Shops.housing)
            ))

        stmt.order_by(Shops.town, Shops.street, Shops.housing)

        shops = await self.__session.scalars(stmt)
        return {shop.id: ShopGetModel.model_validate(shop) for shop in shops.all()}


def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> ShopsRepository:
    return ShopsRepository(session)