from typing import Annotated
from  fastapi import Depends, BackgroundTasks
import asyncio

from ..utils import FileManager
from ..models.books_models import BookGetModelWithoutORM, BookGetModel, BookPostModel
from ..models.search_and_pagination_models import BookSearchModel
from ..database.repositories.book_repository import BooksRepository, get_repository


class BooksService:
    def __init__(self, repository: BooksRepository):
        self.__repository = repository


    async def create_book(self, book_params: BookPostModel) -> None:
        try:
            image_web_path, demo_web_path = await asyncio.gather(
                FileManager.save_image_file(book_params.image_file),
                FileManager.save_demo_file(book_params.demo_file)
            )

            await self.__repository.create_book(book_params, image_web_path, demo_web_path)

        except Exception:
            await asyncio.gather(
                FileManager.delete_image_file(image_web_path),
                FileManager.delete_demo_file(demo_web_path)
            )
            raise


    async def delete_book(self, book_id: int) -> None:
        deleted_book_screen = await self.__repository.delete_book(book_id)
        await asyncio.gather(
            FileManager.delete_image_file(deleted_book_screen.image_file_path),
            FileManager.delete_demo_file(deleted_book_screen.demo_file_path)
        )


    async def modify_book(self, book_id: int, book_params: BookPostModel) -> None:
        try:
            image_web_path, demo_web_path = await asyncio.gather(
                FileManager.save_image_file(book_params.image_file),
                FileManager.save_demo_file(book_params.demo_file)
            )

            updated_book_screen = await self.__repository.modify_book(book_id, book_params, image_web_path, demo_web_path)

            await asyncio.gather(
                FileManager.delete_image_file(updated_book_screen.image_file_path),
                FileManager.delete_demo_file(updated_book_screen.demo_file_path)
            )
            
        except Exception:
            await asyncio.gather(
                FileManager.delete_image_file(image_web_path),
                FileManager.delete_demo_file(demo_web_path)
            )
            raise


    async def get_by_id(self, book_id: int) -> BookGetModel:
        return await self.__repository.get_by_id(book_id)

    async def get_all(self, search_params: BookSearchModel) -> dict[int, BookGetModel]:
        return await self.__repository.get_all(search_params)


def get_service(
    repository: Annotated[BooksRepository, Depends(get_repository)],
) -> BooksService:
    return BooksService(repository)
        