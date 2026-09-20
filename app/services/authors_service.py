from typing import Annotated
from  fastapi import Depends

from ..models.authors_models import AuthorGetModel, AuthorPostModel
from ..models.search_and_pagination_models import AuthorsSearchModel
from ..database.repositories.authors_repository import AuthorsRepository, get_repository

class AuthorsService:
    def __init__(self, repository: AuthorsRepository):
        self.__repository = repository


    async def create_author(self, author_params: AuthorPostModel) -> None:
        await self.__repository.create_author(author_params)


    async def delete_author(self, author_id: int) -> None:
        await self.__repository.delete_author(author_id)


    async def modify_author(self, author_id: int, author_params: AuthorPostModel) -> None:
        await self.__repository.modify_author(author_id, author_params)


    async def get_all(self, search_params: AuthorsSearchModel) -> dict[int, AuthorGetModel]:
        return await self.__repository.get_all(search_params)


def get_service(
    repository: Annotated[AuthorsRepository, Depends(get_repository)]
) -> AuthorsService:
    return AuthorsService(repository)