from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated, Optional

from ...models.books_models import BookPostModel, BookGetModel, BookGetModelWithoutORM
from ...models.search_and_pagination_models import BookSearchModel
from ..shemas import Books
from ...core.postgresql import get_session
from ...exceptions import NoRecordException



class BooksRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_book(self, book_params: BookPostModel, image_src: str, demo_src: str) -> None:
        new_book = Books(**book_params.model_dump(by_alias=False), image_file_path=image_src, demo_file_path=demo_src)
        self.__session.add(new_book)
        await self.__session.commit()


    async def delete_book(self, book_id: int) -> BookGetModelWithoutORM:
        book = await self.__session.get(Books, book_id)

        if book is None:
            raise NoRecordException(f"Book with id={book_id} doesnt exists in database!")

        old_book_screen = BookGetModelWithoutORM.model_validate(book, by_alias=False, by_name=True)

        await self.__session.delete(book)
        await self.__session.commit()

        return old_book_screen


    async def modify_book(self, book_id: int, book_params: BookPostModel, image_src: str, demo_src: str) -> BookGetModelWithoutORM:
        book = await self.__session.get(Books, book_id)
        
        if book is None:
            raise NoRecordException(f"Book with id={book_id} doesnt exists in database!")

        old_book_screen = BookGetModelWithoutORM.model_validate(book, by_alias=False, by_name=True)

        for field, value in book_params.model_dump(by_alias=False).items():
            setattr(book, field, value)

        book.image_file_path = image_src
        book.demo_file_path = demo_src

        await self.__session.commit()

        return old_book_screen


    async def get_by_id(self, book_id: int) -> BookGetModel:
        stmt = select(Books).options(joinedload(Books.author), joinedload(Books.jahnre))
        book = await self.__session.scalar(stmt)
          
        if book is None:
            raise NoRecordException(f"Book with id={book_id} doesnt exists in database!")

        return BookGetModel.model_validate(book, by_alias=False, by_name=True)


    async def get_all(self, search_params: BookSearchModel) -> dict[int, BookGetModel]:
        stmt = select(Books).options(joinedload(Books.author), joinedload(Books.jahnre))

        if search_params.title is not None:
            stmt = stmt.where(Books.title.ilike(f"%{search_params.title }%"))

        if search_params.max_price is not None:
            stmt = stmt.where(Books.price <= search_params.max_price)

        if search_params.min_price is not None:
            stmt = stmt.where(Books.price >= search_params.min_price)

        if search_params.author_id is not None:
            stmt = stmt.where(Books.author_id == search_params.author_id)

        if search_params.jahnre_id is not None:
            stmt = stmt.where(Books.author_id == search_params.jahnre_id)

        stmt = stmt.order_by(Books.id).limit(search_params.limit).offset(search_params.offset)

        books = await self.__session.scalars(stmt)
        return {book.id: BookGetModel.model_validate(book, by_alias=False, by_name=True) for book in books.all()}


def get_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> BooksRepository:
    return BooksRepository(session)