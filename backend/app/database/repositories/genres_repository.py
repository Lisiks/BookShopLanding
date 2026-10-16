from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from ...dto.genres_dto import GenreGetDTO, GenrePostDTO
from ...dto.search_dto import GenreSearchDTO
from ..models import GenresORM
from ...core.postgresql import get_session


class GenresRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_genre(self, genre_params: GenrePostDTO) -> None:
        new_genre = GenresORM(**genre_params.model_dump())
        self.__session.add(new_genre)
        await self.__session.commit()


    async def delete_genre(self, genre_id: int) -> None:
        stmt = select(GenresORM).where(GenresORM.id == genre_id)
        query_result = await self.__session.scalars(stmt)
        genre = query_result.one()

        await self.__session.delete(genre)
        await self.__session.commit()


    async def modify_genre(self, genre_id: int, genre_params: GenrePostDTO) -> None:
        stmt = select(GenresORM).where(GenresORM.id == genre_id)
        
        query_result = await self.__session.scalars(stmt)
        genre = query_result.one()

        for field, value in genre_params.model_dump().items():
            setattr(genre, field, value)

        await self.__session.commit()


    async def get_all(self, search_params: GenreSearchDTO) -> dict[int, GenreGetDTO]:
        stmt = select(GenresORM)

        if search_params.name is not None:
            stmt = stmt.where(GenresORM.name.ilike(f"%{search_params.name}%"))
            
        stmt = stmt.order_by(GenresORM.name)

        genres = await self.__session.scalars(stmt)
        return {genre.id: GenreGetDTO.model_validate(genre) for genre in genres.all()}


def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> GenresRepository:
    return GenresRepository(session)