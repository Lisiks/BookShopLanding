from typing import Annotated
from  fastapi import Depends

from ..models.jahnres_models import JahnreGetModel, JahnrePostModel
from ..models.search_and_pagination_models import JahnresSearchModel
from ..database.repositories.jahnres_repository import JahnresRepository, get_repository

class JahnreService:
    def __init__(self, repository: JahnresRepository):
        self.__repository = repository


    async def create_jahnre(self, jahnre_params: JahnrePostModel) -> None:
        await self.__repository.create_jahnre(jahnre_params)


    async def delete_jahnre(self, jahnre_id: int) -> None:
        await self.__repository.delete_jahnre(jahnre_id)


    async def modify_jahnre(self, jahnre_id: int, jahnre_params: JahnrePostModel) -> None:
        await self.__repository.modify_jahnre(jahnre_id, jahnre_params)


    async def get_all(self, search_params: JahnresSearchModel) -> dict[int, JahnreGetModel]:
        return await self.__repository.get_all(search_params)


def get_service(
    repository: Annotated[JahnresRepository, Depends(get_repository)]
) -> JahnreService:
    return JahnreService(repository)