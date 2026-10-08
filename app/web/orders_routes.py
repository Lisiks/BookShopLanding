from fastapi import Depends, Body, APIRouter, status, Cookie, Path, Query, Form
from typing import Annotated, Optional

from ..services.orders_service import OrdersService, get_service
from ..utils.auth import auth_user, auth_admin
from ..models.users_models import UserGetModel
from ..models.orders_models import OrderGetModel, OrderPostModel
from ..models.search_and_pagination_models import OrderSearchModel
from ..enums import OrderStatuses

router = APIRouter(prefix="/orders", tags=["📦 Orders"])



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create_order(
    user_data: Annotated[UserGetModel, Depends(auth_user)],
    service: Annotated[OrdersService, Depends(get_service)],
    order_params: Annotated[OrderPostModel, Body()]
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


@router.get("/", status_code=status.HTTP_200_OK, response_model=dict[int, OrderGetModel], dependencies=[Depends(auth_admin)])
async def get_all(
    service: Annotated[OrdersService, Depends(get_service)],
    search_params: Annotated[OrderSearchModel, Query()]
) -> dict[int, OrderGetModel]:
    return await service.get_all(search_params)
   
