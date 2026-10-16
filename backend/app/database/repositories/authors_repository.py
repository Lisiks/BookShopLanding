from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, literal
from fastapi import Depends
from typing import Annotated

from ...dto.authors_dto import AuthorGetDTO, AuthorPostDTO
from ...dto.search_dto import AuthorSearchDTO
from ..models import AuthorsORM
from ...core.postgresql import get_session



class AuthorsRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_author(self, author_params: AuthorPostDTO) -> None:
        new_author = AuthorsORM(**author_params.model_dump())
        self.__session.add(new_author)
        await self.__session.commit()


    async def delete_author(self, author_id: int) -> None:
        stmt = select(AuthorsORM).where(AuthorsORM.id == author_id)
        query_result = await self.__session.scalars(stmt)
        author = query_result.one()

        await self.__session.delete(author)
        await self.__session.commit()


    async def modify_author(self, author_id: int, author_params: AuthorPostDTO) -> None:
        stmt = select(AuthorsORM).where(AuthorsORM.id == author_id)
        query_result = await self.__session.scalars(stmt)
        author = query_result.one()

        for field, value in author_params.model_dump().items():
            setattr(author, field, value)

        await self.__session.commit()


    async def get_all(self, search_params: AuthorSearchDTO) -> dict[int, AuthorGetDTO]:
        stmt = select(AuthorsORM)

        if search_params.name_part is not None:
            stmt = stmt.where(or_(
                literal(search_params.name_part).icontains(AuthorsORM.f),
                literal(search_params.name_part).icontains(AuthorsORM.i),
                literal(search_params.name_part).icontains(AuthorsORM.o),
            ))

        stmt = stmt.order_by(AuthorsORM.f, AuthorsORM.i, AuthorsORM.o)

        authors = await self.__session.scalars(stmt)
        return {author.id: AuthorGetDTO.model_validate(author) for author in authors.all()}


def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> AuthorsRepository:
    return AuthorsRepository(session)