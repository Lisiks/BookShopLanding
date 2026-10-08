from fastapi import APIRouter, Depends, Path, Query, status, Form, Body
from typing import Annotated, Optional

from ..services.books_service import BooksService, get_service as get_book_service
from ..utils.auth import auth_admin, auth_user
from ..models.books_models import BookGetModel, BookPostModel
from ..models.search_and_pagination_models import BookSearchModel
from ..models.shoppig_cart_models import ShppingCartModel
from ..services.comments_service import CommentsService, get_service as get_comment_service
from ..models.comments_models import CommentGetModel
from ..models.users_models import UserGetModel

router = APIRouter(prefix="/books", tags=["📚 books"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def create_book(
    book_params: Annotated[BookPostModel, Form(media_type="multipart/form-data")],
    service: Annotated[BooksService, Depends(get_book_service)]
) -> dict[str, str]:
    await service.create_book(book_params)
    return {"msg": "created"}


@router.delete("/{book_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def delete_book(
    book_id: Annotated[int, Path(gt=0)],
    service: Annotated[BooksService, Depends(get_book_service)]
) -> dict[str, str]:
    await service.delete_book(book_id)
    return {"msg": "deleted"}


@router.patch("/{book_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def modify_book(
    book_params: Annotated[BookPostModel, Form(media_type="multipart/form-data")],
    book_id: Annotated[int, Path(gt=0)],
    service: Annotated[BooksService, Depends(get_book_service)]
) -> dict[str, str]:
    await service.modify_book(book_id, book_params)
    return {"msg": "modified"}


@router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model=BookGetModel)
async def get_by_id(
    book_id: Annotated[int, Path(gt=0)],
    service: Annotated[BooksService, Depends(get_book_service)]
) -> BookGetModel:
    return await service.get_by_id(book_id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict[int, BookGetModel])
async def get_all(
    search_params: Annotated[BookSearchModel, Query()],
    service: Annotated[BooksService, Depends(get_book_service)]
) -> dict[int, BookGetModel]:
    return await service.get_all(search_params)


@router.post("/list", status_code=status.HTTP_200_OK, response_model=dict[int, BookGetModel], dependencies=[Depends(auth_user)])
async def get_by_list(
    shoping_cart: Annotated[ShppingCartModel, Body()],
    service: Annotated[BooksService, Depends(get_book_service)]
) -> dict[int, BookGetModel]:
    return await service.get_by_list(shoping_cart.items)


@router.post("/{book_id}/comments", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create_comment(
    book_id: Annotated[int, Path(gt=0)],
    user_data: Annotated[UserGetModel, Depends(auth_user)],
    text: Annotated[str, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[CommentsService, Depends(get_comment_service)]
) -> dict[str, str]:
    await service.create_comment(text, book_id, user_data.id)
    return {"msg": "created"}


@router.delete("/{book_id}/comments", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def delete_comment(
    book_id: Annotated[int, Path(gt=0)],
    user_data: Annotated[UserGetModel, Depends(auth_user)],
    service: Annotated[CommentsService, Depends(get_comment_service)]
) -> dict[str, str]:
    await service.delete_comment(book_id, user_data.id)
    return {"msg": "deleted"}


@router.get("/{book_id}/comments/me", status_code=status.HTTP_200_OK, response_model=CommentGetModel)
async def get_comment_me(
    book_id: Annotated[int, Path(gt=0)],
    service: Annotated[CommentsService, Depends(get_comment_service)],
    user_data: Annotated[UserGetModel, Depends(auth_user)]
) -> CommentGetModel:
    return await service.get_by_id(book_id, user_data.id)


@router.get("/{book_id}/comments", status_code=status.HTTP_200_OK, response_model=dict[int, CommentGetModel])
async def get_all_comments(
    book_id: Annotated[int, Path(gt=0)],
    service: Annotated[CommentsService, Depends(get_comment_service)]
) -> dict[str, CommentGetModel | list[CommentGetModel]]:
    return await service.get_all(book_id)