from fastapi import Depends, Form, APIRouter, status, Cookie, Path, Query
from fastapi.responses import JSONResponse
from typing import Annotated, Optional
from fastapi_cache.decorator import cache

from ..services.accounts_service import AccountsService, get_service as get_account_service
from ..services.orders_service import OrdersService, get_service as get_order_service

from ..utils.auth import auth_user

from ..models.orders_models import OrderGetModel
from ..models.users_models import UserPostModel, UserGetModel, UserLoginModel
from ..models.search_and_pagination_models import OrderSearchModel
from ..settings import config
from ..exceptions import LoginException
from ..utils.cache_key_builders import user_orders_key_builder

router = APIRouter(prefix="/accounts", tags=["👥 accounts"])


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def create_account(
    user_params: Annotated[UserPostModel, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[AccountsService, Depends(get_account_service)]
) -> dict[str, str]:
    await service.create_account(user_params)
    return {"msg": "created"}


@router.post(path="/login", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def login(
    user_params: Annotated[UserLoginModel, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[AccountsService, Depends(get_account_service)],
    session: Annotated[Optional[str], Cookie(alias=config.session.cookie_key)] = None
) -> dict[str, str]:
    if session is not None:
        raise LoginException("You are already login!")
    
    sesion = await service.login_account(user_params)

    responce = JSONResponse(content={"msg": "success"})
    responce.set_cookie(
        key=config.session.cookie_key,
        value=sesion,
        samesite="lax",
        httponly=True,
    )
    return responce


@router.get(path="/logout", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def logout(
    service: Annotated[AccountsService, Depends(get_account_service)],
    session: Annotated[str, Cookie(alias=config.session.cookie_key)]
) -> dict[str, str]:
    await service.logout(session)
    responce = JSONResponse(content={"msg": "success"})
    responce.delete_cookie(key=config.session.cookie_key)
    return responce


@router.get(path="/me", status_code=status.HTTP_200_OK, response_model=UserGetModel)
async def me(
    session_data: Annotated[UserGetModel, Depends(auth_user)]
) -> UserGetModel:
    return session_data


@router.get(path="/me/orders", status_code=status.HTTP_200_OK, response_model=dict[int, OrderGetModel])
@cache(expire=config.cache.ttl, namespace=config.cache.namespaces.orders, key_builder=user_orders_key_builder)
async def get_orders(
    user_data: Annotated[UserGetModel, Depends(auth_user)],
    service: Annotated[OrdersService, Depends(get_order_service)],
    search_params: Annotated[OrderSearchModel, Query()]
) -> dict[int, OrderGetModel]:
    return await service.get_by_user_id(search_params, user_data.id)
