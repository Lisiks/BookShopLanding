from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from fastapi import Depends
from typing import Annotated

from ..models import UsersORM, CommentsORM
from ...core.postgresql import get_session
from ...dto.comments_dto import CommentGetDTO


class CommentsRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session


    async def create_comment(self, text: str, book_id: int, user_id: int) -> None:
        new_comment = CommentsORM(text=text, book_id=book_id, user_id=user_id)
        self.__session.add(new_comment)
        await self.__session.commit()


    async def delete_comment(self, book_id: int, user_id: int) -> None:
        stmt = select(CommentsORM).where(and_(CommentsORM.book_id == book_id, CommentsORM.user_id == user_id))
        query_result = await self.__session.scalars(stmt)
        comment = query_result.one()

        await self.__session.delete(comment)
        await self.__session.commit()

        
    async def get_by_id(self, book_id: int, user_id: int) -> CommentGetDTO:
        stmt = select(
            CommentsORM.text, CommentsORM.datetime, UsersORM.username, UsersORM.id.label("user_id")
        ).join(
            UsersORM
        ).where(
            and_(CommentsORM.user_id == user_id, CommentsORM.book_id == book_id)
        )

        comment = await self.__session.execute(stmt)
        comment = comment.one()
        
        return CommentGetDTO.model_validate(comment)

    async def get_all(self, book_id: int) -> list[CommentGetDTO]:
        stmt = select(
            CommentsORM.text, CommentsORM.datetime, UsersORM.username, UsersORM.id.label("user_id")
        ).join(
            UsersORM
        ).where(CommentsORM.book_id == book_id).order_by(desc(CommentsORM.datetime))

        comments = await self.__session.execute(stmt)
        return [CommentGetDTO.model_validate(comment) for comment in comments.all()]


def get_repository(session: Annotated[AsyncSession, Depends(get_session)]) -> CommentsRepository:
    return CommentsRepository(session)