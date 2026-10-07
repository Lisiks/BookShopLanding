from fastapi import Depends, Form, APIRouter, status, Cookie, Path, Query
from fastapi.responses import JSONResponse
from typing import Annotated, Optional

from ..services.accounts_service import AccountsService, get_service as get_account_service

from ..utils.auth import auth_user
from ..models.users_models import UserPostModel, UserGetModel, UserLoginModel
from ..models.search_and_pagination_models import UsersSearchModel
from ..settings import config
from ..exceptions import LoginException


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
