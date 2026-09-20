from fastapi import APIRouter, Depends, Path, Query, status, Form
from typing import Annotated

from ..services.authors_service import AuthorsService, get_service
from ..services.auth_service import auth_admin
from ..models.authors_models import AuthorGetModel, AuthorPostModel
from ..models.search_and_pagination_models import AuthorsSearchModel

router = APIRouter(prefix="/authors", tags=["✍️ authors"])

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def create_author(
    author_params: Annotated[AuthorPostModel, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[AuthorsService, Depends(get_service)]
) -> dict[str, str]:
    await service.create_author(author_params)
    return {"msg": "created"}


@router.delete("/delete/{author_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def delete_author(
    author_id: Annotated[int, Path(gt=0)],
    service: Annotated[AuthorsService, Depends(get_service)]
) -> dict[str, str]:
    await service.delete_author(author_id)
    return {"msg": "deleted"}


@router.patch("/modify/{author_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def modify_author(
    author_params: Annotated[AuthorPostModel, Form(media_type="application/x-www-form-urlencoded")],
    author_id: Annotated[int, Path(gt=0)],
    service: Annotated[AuthorsService, Depends(get_service)]
) -> dict[str, str]:
    await service.modify_author(author_id, author_params)
    return {"msg": "modified"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict[int, AuthorGetModel])
async def get_all(
    search_params: Annotated[AuthorsSearchModel, Query()],
    service: Annotated[AuthorsService, Depends(get_service)]
) -> dict[int, AuthorGetModel]:
    return await service.get_all(search_params)