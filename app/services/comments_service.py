import asyncio
from fastapi import Depends
from typing import Annotated

from ..database.repositories.comments_repository import CommentsRepository, get_repository
from ..models.comments_models import CommentGetModel


class CommentsService:
    def __init__(self, repository: CommentsRepository):
        self.__repository = repository


    async def create_comment(self, text: str, book_id: int, user_id: int) -> None:
        await self.__repository.create_comment(text, book_id, user_id)

    async def delete_comment(self, book_id: int, user_id: int) -> None:
        await self.__repository.delete_comment(book_id, user_id)

    async def get_all(self, book_id: int, user_id: int | None) -> dict[str, CommentGetModel]:
        if user_id is None:
            user_comment = None
            comments = await self.__repository.get_all(book_id)
        else:
            user_comment = await self.__repository.get_by_user_id(book_id, user_id)
            comments = await self.__repository.get_all(book_id, user_id)

        return {
            "userComment": user_comment,
            "comments": comments
        }


def get_service(repository: Annotated[CommentsRepository, Depends(get_repository)]) -> CommentsService:
    return CommentsService(repository)
        


