from fastapi import Depends, Body, APIRouter, status, Cookie, Path, Query, Form
from typing import Annotated, Optional
from fastapi_cache.decorator import cache

from ..services.orders_service import OrdersService, get_service
from ..utils.auth import auth_user, auth_admin
from ..dto.users_dto import UserGetDTO
from ..dto.orders_dto import OrderGetDTO, OrderPostDTO
from ..dto.search_dto import OrderSearchDTO
from ..enums import OrderStatuses
from ..utils.cache_key_builders import default_search_key_builder
from ..settings import config


router = APIRouter(prefix="/orders", tags=["📦 orders"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create_order(
    user_data: Annotated[UserGetDTO, Depends(auth_user)],
    service: Annotated[OrdersService, Depends(get_service)],
    order_params: Annotated[OrderPostDTO, Body()]
) -> dict[str, str]:
    await service.create_order(order_params, user_data.id)
    return {"msg": "created"}


@router.patch("/{order_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def change_order_status(
    order_id: Annotated[int, Path(gt=0)],
    service: Annotated[OrdersService, Depends(get_service)],
    order_status: Annotated[OrderStatuses, Form(media_type="application/x-www-form-urlencoded")]
) -> dict[str, str]:
    await service.change_order_status(order_id, order_status)
    return {"msg": "changed"}


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict[int, OrderGetDTO], dependencies=[Depends(auth_admin)])
@cache(expire=config.cache.ttl, namespace=config.cache.namespaces.orders, key_builder=default_search_key_builder)
async def get_all(
    service: Annotated[OrdersService, Depends(get_service)],
    search_params: Annotated[OrderSearchDTO, Query()]
) -> dict[int, OrderGetDTO]:
    return await service.get_all(search_params)
   
