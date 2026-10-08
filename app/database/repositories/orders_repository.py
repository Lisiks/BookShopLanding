from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, literal, union_all
from sqlalchemy.exc import NoResultFound
from fastapi import Depends
from typing import Annotated, Optional

from ...models.orders_models import OrderPostModel, OrderGetModel
from ...models.search_and_pagination_models import OrderSearchModel
from ..shemas import Orders, OrdersItems, Books
from ...core.postgresql import get_session
from ...enums import OrderStatuses




class OrdersRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session


    async def create_order(self, order_params: OrderPostModel, user_id: int) -> None:
        stmt = union_all(
            *[select(Books.id.label("book_id"), literal(item.count).label("count"), Books.price.label("price")).where(Books.id == item.book_id)
            for item in order_params.items]
        )

        item_data = await self.__session.execute(stmt)
        item_data = item_data.mappings().all()

        if len(item_data) != len(order_params.items):
            raise NoResultFound()

    
        order = Orders(
            user_id=user_id,
            status=OrderStatuses.InAssembly,
            shop_id=order_params.shop_id,
            items=[OrdersItems(**item) for item in item_data]
        )

        self.__session.add(order)
        await self.__session.commit()


    async def change_order_status(self, order_id: int, new_status: OrderStatuses) -> None:
        stmt = select(Orders).where(Orders.id == order_id)
        query_result = await self.__session.scalars(stmt)
        order = query_result.one()

        order.status = new_status
        await self.__session.commit()


    async def get_all(self, search_params: OrderSearchModel, user_id: Optional[int] = None) -> dict[int, OrderGetModel]:
        stmt = select(Orders).options(
            joinedload(Orders.shop),
            joinedload(Orders.user),
            selectinload(Orders.items).joinedload(OrdersItems.book)
        )

        if search_params.status is not None:
            stmt = stmt.where(Orders.status == search_params.status)

        if search_params.shop_id is not None:
            stmt = stmt.where(Orders.shop_id == search_params.shop_id)

        if user_id is not None:
            stmt = stmt.where(Orders.user_id == user_id)

        stmt = stmt.limit(search_params.limit).offset(search_params.offset)

        orders = await self.__session.scalars(stmt)
        return {order.id: OrderGetModel.model_validate(order, by_alias=False, by_name=True) for order in orders.all()}

def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> OrdersRepository:
    return OrdersRepository(session)