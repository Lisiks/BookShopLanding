from typing import Annotated
from fastapi import Depends, BackgroundTasks
from fastapi_cache import FastAPICache

from ..dto.genres_dto import GenreGetDTO, GenrePostDTO
from ..dto.search_dto import GenreSearchDTO
from ..database.repositories.genres_repository import GenresRepository, get_repository
from ..settings import config



class GenreService:
    def __init__(self, repository: GenresRepository, bg_tasks: BackgroundTasks):
        self.__repository = repository
        self.__bg_tasks = bg_tasks


    async def create_genre(self, genre_params: GenrePostDTO) -> None:
        await self.__repository.create_genre(genre_params)
        self.__bg_tasks.add_task(FastAPICache.clear, config.cache.namespaces.genres)


    async def delete_genre(self, genre_id: int) -> None:
        await self.__repository.delete_genre(genre_id)
        self.__bg_tasks.add_task(FastAPICache.clear, config.cache.namespaces.genres)


    async def modify_genre(self, genre_id: int, genre_params: GenrePostDTO) -> None:
        await self.__repository.modify_genre(genre_id, genre_params)
        self.__bg_tasks.add_task(FastAPICache.clear, config.cache.namespaces.genres)


    async def get_all(self, search_params: GenreSearchDTO) -> dict[int, GenreGetDTO]:
        return await self.__repository.get_all(search_params)


def get_service(
    repository: Annotated[GenresRepository, Depends(get_repository)],
    bg_tasks: BackgroundTasks
) -> GenreService:
    return GenreService(repository, bg_tasks)