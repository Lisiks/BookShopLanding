from typing import Annotated
from fastapi import Depends, BackgroundTasks
from fastapi_cache import FastAPICache

from ..models.authors_models import AuthorGetModel, AuthorPostModel
from ..models.search_and_pagination_models import AuthorsSearchModel
from ..database.repositories.authors_repository import AuthorsRepository, get_repository
from ..settings import config


class AuthorsService:
    def __init__(self, repository: AuthorsRepository, bg_tasks: BackgroundTasks):
        self.__repository = repository
        self.__bg_tasks = bg_tasks


    async def create_author(self, author_params: AuthorPostModel) -> None:
        await self.__repository.create_author(author_params)
        self.__bg_tasks.add_task(FastAPICache.clear, config.cache.namespaces.authors)


    async def delete_author(self, author_id: int) -> None:
        await self.__repository.delete_author(author_id)
        self.__bg_tasks.add_task(FastAPICache.clear, config.cache.namespaces.authors)


    async def modify_author(self, author_id: int, author_params: AuthorPostModel) -> None:
        await self.__repository.modify_author(author_id, author_params)
        self.__bg_tasks.add_task(FastAPICache.clear, config.cache.namespaces.authors)


    async def get_all(self, search_params: AuthorsSearchModel) -> dict[int, AuthorGetModel]:
        return await self.__repository.get_all(search_params)


def get_service(
    repository: Annotated[AuthorsRepository, Depends(get_repository)],
    bg_tasks: BackgroundTasks
) -> AuthorsService:
    return AuthorsService(repository, bg_tasks)