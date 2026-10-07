from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, literal
from fastapi import Depends
from typing import Annotated

from ...models.authors_models import AuthorGetModel, AuthorPostModel
from ...models.search_and_pagination_models import AuthorsSearchModel
from ..shemas import Authors
from ...core.postgresql import get_session



class AuthorsRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_author(self, author_params: AuthorPostModel) -> None:
        new_author = Authors(**author_params.model_dump())
        self.__session.add(new_author)
        await self.__session.commit()


    async def delete_author(self, author_id: int) -> None:
        stmt = select(Authors).where(Authors.id == author_id)
        query_result = await self.__session.scalars(stmt)
        author = query_result.one()

        await self.__session.delete(author)
        await self.__session.commit()


    async def modify_author(self, author_id: int, author_params: AuthorPostModel) -> None:
        stmt = select(Authors).where(Authors.id == author_id)
        query_result = await self.__session.scalars(stmt)
        author = query_result.one()

        for field, value in author_params.model_dump().items():
            setattr(author, field, value)

        await self.__session.commit()


    async def get_all(self, search_params: AuthorsSearchModel) -> dict[int, AuthorGetModel]:
        stmt = select(Authors)

        if search_params.name_part is not None:
            stmt = stmt.where(or_(
                literal(search_params.name_part).icontains(Authors.f),
                literal(search_params.name_part).icontains(Authors.i),
                literal(search_params.name_part).icontains(Authors.o),
            ))

        stmt = stmt.order_by(Authors.f, Authors.i, Authors.o)

        authors = await self.__session.scalars(stmt)
        return {author.id: AuthorGetModel.model_validate(author) for author in authors.all()}


def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> AuthorsRepository:
    return AuthorsRepository(session)