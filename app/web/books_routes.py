from fastapi import APIRouter, Depends, Path, Query, status, Form
from typing import Annotated

from ..services.books_service import BooksService, get_service
from ..services.auth_service import auth_admin
from ..models.books_models import BookGetModel, BookPostModel
from ..models.search_and_pagination_models import BookSearchModel

router = APIRouter(prefix="/books", tags=["📚 books"])

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def create_book(
    book_params: Annotated[BookPostModel, Form(media_type="multipart/form-data")],
    service: Annotated[BooksService, Depends(get_service)]
) -> dict[str, str]:
    await service.create_book(book_params)
    return {"msg": "created"}


@router.delete("/delete/{book_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def delete_book(
    book_id: Annotated[int, Path(gt=0)],
    service: Annotated[BooksService, Depends(get_service)]
) -> dict[str, str]:
    await service.delete_book(book_id)
    return {"msg": "deleted"}


@router.patch("/modify/{book_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def modify_book(
    book_params: Annotated[BookPostModel, Form(media_type="multipart/form-data")],
    book_id: Annotated[int, Path(gt=0)],
    service: Annotated[BooksService, Depends(get_service)]
) -> dict[str, str]:
    await service.modify_book(book_id, book_params)
    return {"msg": "modified"}


@router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=BookGetModel)
async def get_by_id(
    book_id: Annotated[int, Path(gt=0)],
    service: Annotated[BooksService, Depends(get_service)]
) -> BookGetModel:
    return await service.get_by_id(book_id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict[int, BookGetModel])
async def get_all(
    search_params: Annotated[BookSearchModel, Query()],
    service: Annotated[BooksService, Depends(get_service)]
) -> dict[int, BookGetModel]:
    return await service.get_all(search_params)