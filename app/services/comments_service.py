from fastapi import Depends, BackgroundTasks
from typing import Annotated
from fastapi_cache import FastAPICache

from ..database.repositories.comments_repository import CommentsRepository, get_repository
from ..models.comments_models import CommentGetModel
from ..settings import config


class CommentsService:
    def __init__(self, repository: CommentsRepository, bg_tasks: BackgroundTasks):
        self.__repository = repository
        self.__bg_tasks = bg_tasks


    async def create_comment(self, text: str, book_id: int, user_id: int) -> None:
        await self.__repository.create_comment(text, book_id, user_id)
        self.__bg_tasks.add_task(FastAPICache.clear, f"{config.cache.namespaces.comments}-{book_id}")

    async def delete_comment(self, book_id: int, user_id: int) -> None:
        await self.__repository.delete_comment(book_id, user_id)
        self.__bg_tasks.add_task(FastAPICache.clear, f"{config.cache.namespaces.comments}-{book_id}")
        self.__bg_tasks.add_task(FastAPICache.clear, f"{config.cache.namespaces.comments}-{book_id}-{user_id}")

    async def get_by_id(self, book_id: int, user_id: int) -> CommentGetModel:
        return await self.__repository.get_by_id(book_id, user_id)

    async def get_all(self, book_id) -> dict[int, CommentGetModel]:
        return await self.__repository.get_all(book_id)


def get_service(
    repository: Annotated[CommentsRepository, Depends(get_repository)],
    bg_tasks: BackgroundTasks
) -> CommentsService:
    return CommentsService(repository, bg_tasks)
        


