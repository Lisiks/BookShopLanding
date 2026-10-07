from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from fastapi import Depends
from typing import Annotated

from ..shemas import Comments, Users
from ...core.postgresql import get_session
from ...models.comments_models import CommentGetModel
from ...exceptions import NoRecordException

class CommentsRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session


    async def create_comment(self, text: str, book_id: int, user_id: int) -> None:
        new_comment = Comments(text=text, book_id=book_id, user_id=user_id)
        self.__session.add(new_comment)
        await self.__session.commit()


    async def delete_comment(self, book_id: int, user_id: int) -> None:
        comment = await self.__session.get(Comments, (book_id, user_id))

        if comment is None:
            raise NoRecordException(f"This user hasn't comment on book with id={book_id}!")

        await self.__session.delete(comment)
        await self.__session.commit()

        
    async def get_by_user_id(self, book_id: int, user_id: int) -> CommentGetModel | None:
        stmt = select(
            Comments.text, Comments.datetime, Users.username
        ).join(
            Users
        ).where(
            and_(Comments.user_id == user_id, Comments.book_id == book_id)
        )

        comment = await self.__session.execute(stmt)
        comment = comment.one()
        
        return CommentGetModel.model_validate(comment) if comment is not None else None

    async def get_all(self, book_id: int, expired_user_id: int | None = None) -> list[CommentGetModel]:
        stmt = select(
            Comments.text, Comments.datetime, Users.username
        ).join(
            Users
        ).where(Comments.book_id == book_id)

        if expired_user_id is not None:
            stmt = stmt.where(Comments.user_id != expired_user_id)

        stmt = stmt.order_by(Comments.datetime)

        comments = await self.__session.execute(stmt)
        return [CommentGetModel.model_validate(comment) for comment in comments.all()]


def get_repository(session: Annotated[AsyncSession, Depends(get_session)]) -> CommentsRepository:
    return CommentsRepository(session)