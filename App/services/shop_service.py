from typing import Annotated
from  fastapi import Depends

from ..models.shops_models import ShopGetModel, ShopPostModel
from ..models.search_and_pagination_models import ShopSearchModel
from ..database.repositories.shops_repository import ShopsRepository, get_repository

class ShopService:
    def __init__(self, repository: ShopsRepository):
        self.__repository = repository


    async def create_shop(self, shop_params: ShopPostModel) -> None:
        await self.__repository.create_shop(shop_params)


    async def delete_shop(self, shop_id: int) -> None:
        await self.__repository.delete_shop(shop_id)


    async def modify_shop(self, shop_id: int, shop_params: ShopPostModel) -> None:
        await self.__repository.modify_shop(shop_id, shop_params)


    async def get_all(self, search_params: ShopPostModel) -> dict[int, ShopGetModel]:
        return await self.__repository.get_all(search_params)


def get_service(
    repository: Annotated[ShopsRepository, Depends(get_repository)]
) -> ShopService:
    return ShopService(repository)