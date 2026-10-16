from fastapi import APIRouter, Depends, Path, Query, status, Form
from typing import Annotated
from fastapi_cache.decorator import cache

from ..services.genre_service import GenreService, get_service
from ..utils.auth import auth_admin
from ..dto.genres_dto import GenreGetDTO, GenrePostDTO
from ..dto.search_dto import GenreSearchDTO
from ..settings import config

from ..utils.cache_key_builders import default_search_key_builder

router = APIRouter(prefix="/genres", tags=["✒️ genres"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def create_genre(
    genre_params: Annotated[GenrePostDTO, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[GenreService, Depends(get_service)]
) -> dict[str, str]:
    await service.create_genre(genre_params)
    return {"msg": "created"}


@router.delete("/{genre_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def delete_genre(
    genre_id: Annotated[int, Path(gt=0)],
    service: Annotated[GenreService, Depends(get_service)]
) -> dict[str, str]:
    await service.delete_genre(genre_id)
    return {"msg": "deleted"}


@router.patch("/{genre_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def modify_janhre(
    genre_params: Annotated[GenrePostDTO, Form(media_type="application/x-www-form-urlencoded")],
    genre_id: Annotated[int, Path(gt=0)],
    service: Annotated[GenreService, Depends(get_service)]
) -> dict[str, str]:
    await service.modify_genre(genre_id, genre_params)
    return {"msg": "modified"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict[int, GenreGetDTO])
@cache(expire=config.cache.ttl, namespace=config.cache.namespaces.genres, key_builder=default_search_key_builder)
async def get_all(
    search_params: Annotated[GenreSearchDTO, Query()],
    service: Annotated[GenreService, Depends(get_service)]
) -> dict[int, GenreGetDTO]:
    return await service.get_all(search_params)