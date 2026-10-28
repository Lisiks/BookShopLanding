from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select, literal, union_all, desc
from sqlalchemy.exc import NoResultFound
from fastapi import Depends
from typing import Annotated, Optional

from ...dto.orders_dto import OrderPostDTO, OrderGetDTO
from ...dto.search_dto import OrderSearchDTO
from ..models import OrdersORM, BooksORM, OrdersItemsORM
from ...core.postgresql import get_session
from ...enums import OrderStatuses




class OrdersRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session


    async def create_order(self, order_params: OrderPostDTO, user_id: int) -> None:
        stmt = union_all(
            *[select(BooksORM.id.label("book_id"), literal(item.count).label("count"), BooksORM.price.label("price")).where(BooksORM.id == item.book_id)
            for item in order_params.items]
        )

        item_data = await self.__session.execute(stmt)
        item_data = item_data.mappings().all()

        if len(item_data) != len(order_params.items):
            raise NoResultFound()

    
        order = OrdersORM(
            user_id=user_id,
            status=OrderStatuses.InAssembly,
            shop_id=order_params.shop_id,
            items=[OrdersItemsORM(**item) for item in item_data]
        )

        self.__session.add(order)
        await self.__session.commit()


    async def change_order_status(self, order_id: int, new_status: OrderStatuses) -> int:
        stmt = select(OrdersORM).where(OrdersORM.id == order_id)
        query_result = await self.__session.scalars(stmt)
        order = query_result.one()

        order.status = new_status
        await self.__session.commit()

        return order.user_id


    async def get_all(self, search_params: OrderSearchDTO, user_id: Optional[int] = None) -> dict[int, OrderGetDTO]:
        stmt = select(OrdersORM).options(
            joinedload(OrdersORM.shop),
            joinedload(OrdersORM.user),
            selectinload(OrdersORM.items).joinedload(OrdersItemsORM.book)
        )

        if search_params.status is not None:
            stmt = stmt.where(OrdersORM.status == search_params.status)

        if search_params.shop_id is not None:
            stmt = stmt.where(OrdersORM.shop_id == search_params.shop_id)

        if user_id is not None:
            stmt = stmt.where(OrdersORM.user_id == user_id)

        stmt = stmt.order_by(desc(OrdersORM.datetime), OrdersORM.id).limit(search_params.limit).offset(search_params.offset)

        orders = await self.__session.scalars(stmt)
        return {order.id: OrderGetDTO.model_validate(order, by_alias=False, by_name=True) for order in orders.all()}

def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> OrdersRepository:
    return OrdersRepository(session)