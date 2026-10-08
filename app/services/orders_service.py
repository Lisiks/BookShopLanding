from typing import Annotated
from  fastapi import Depends, BackgroundTasks


from ..enums import OrderStatuses
from ..models.orders_models import OrderGetModel, OrderPostModel
from ..models.search_and_pagination_models import OrderSearchModel
from ..database.repositories.orders_repository import OrdersRepository, get_repository


class OrdersService:
    def __init__(self, repository: OrdersRepository):
        self.__repository = repository

    async def create_order(self, order_params: OrderPostModel, user_id: int) -> None:
        await self.__repository.create_order(order_params, user_id)

    async def change_order_status(self, order_id: int, new_status: OrderStatuses) -> None:
        await self.__repository.change_order_status(order_id, new_status)

    async def get_all(self, search_params: OrderSearchModel) -> dict[int, OrderGetModel]:
        return await self.__repository.get_all(search_params)

    async def get_by_user_id(self, search_params: OrderSearchModel, user_id: int) -> dict[int, OrderGetModel]:
        return await self.__repository.get_all(search_params, user_id)



def get_service(
    repository: Annotated[OrdersRepository, Depends(get_repository)]
) -> OrdersService:
    return OrdersService(repository)