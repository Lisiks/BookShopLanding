from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
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
        stmt = select(Comments).where(and_(Comments.book_id == book_id, Comments.user_id == user_id))
        query_result = await self.__session.scalars(stmt)
        comment = query_result.one()

        await self.__session.delete(comment)
        await self.__session.commit()

        
    async def get_by_id(self, book_id: int, user_id: int) -> CommentGetModel:
        stmt = select(
            Comments.text, Comments.datetime, Users.username, Users.id.label("user_id")
        ).join(
            Users
        ).where(
            and_(Comments.user_id == user_id, Comments.book_id == book_id)
        )

        comment = await self.__session.execute(stmt)
        comment = comment.one()
        
        return CommentGetModel.model_validate(comment)

    async def get_all(self, book_id: int) -> list[CommentGetModel]:
        stmt = select(
            Comments.text, Comments.datetime, Users.username, Users.id.label("user_id")
        ).join(
            Users
        ).where(Comments.book_id == book_id)

        stmt = stmt.order_by(desc(Comments.datetime))

        comments = await self.__session.execute(stmt)
        return {comment.user_id : CommentGetModel.model_validate(comment) for comment in comments.all()}


def get_repository(session: Annotated[AsyncSession, Depends(get_session)]) -> CommentsRepository:
    return CommentsRepository(session)