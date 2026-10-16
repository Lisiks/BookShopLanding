from typing import Annotated
from fastapi import Depends, BackgroundTasks
from fastapi_cache import FastAPICache

from ..models.shops_models import ShopGetModel, ShopPostModel
from ..models.search_and_pagination_models import ShopSearchModel
from ..database.repositories.shops_repository import ShopsRepository, get_repository
from ..settings import config


class ShopService:
    def __init__(self, repository: ShopsRepository, bg_tasks: BackgroundTasks):
        self.__repository = repository
        self.__bg_tasks = bg_tasks


    async def create_shop(self, shop_params: ShopPostModel) -> None:
        await self.__repository.create_shop(shop_params)
        self.__bg_tasks.add_task(FastAPICache.clear, config.cache.namespaces.shops)


    async def delete_shop(self, shop_id: int) -> None:
        await self.__repository.delete_shop(shop_id)
        self.__bg_tasks.add_task(FastAPICache.clear, config.cache.namespaces.shops)


    async def modify_shop(self, shop_id: int, shop_params: ShopPostModel) -> None:
        await self.__repository.modify_shop(shop_id, shop_params)
        self.__bg_tasks.add_task(FastAPICache.clear, config.cache.namespaces.shops)


    async def get_all(self, search_params: ShopPostModel) -> dict[int, ShopGetModel]:
        return await self.__repository.get_all(search_params)


def get_service(
    repository: Annotated[ShopsRepository, Depends(get_repository)],
    bg_tasks: BackgroundTasks
) -> ShopService:
    return ShopService(repository, bg_tasks)