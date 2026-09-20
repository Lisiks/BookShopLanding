from fastapi import Depends, Form, APIRouter, status, Cookie, Path, Query
from fastapi.responses import JSONResponse
from typing import Annotated, Optional

from ..services.users_service import UsersService, get_service as get_user_service
from ..services.auth_service import AuthService, get_service as get_auth_service, auth_user, auth_admin
from ..models.users_models import UserPostModel, UserGetModel, UserLoginModel
from ..models.search_and_pagination_models import UsersSearchModel
from ..settings import config
from ..exceptions import LoginException


router = APIRouter(prefix="/users", tags=["👥 users"])


@router.post(path="/register", status_code=status.HTTP_201_CREATED, response_model=dict[str, str])
async def register(
    user_params: Annotated[UserPostModel, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[UsersService, Depends(get_user_service)]
) -> dict[str, str]:
    await service.create_user(user_params)
    return {"msg": "created"}


@router.post(path="/login", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def login(
    user_params: Annotated[UserLoginModel, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[AuthService, Depends(get_auth_service)],
    session: Annotated[Optional[str], Cookie(alias=config.session.cookie_key)] = None
) -> dict[str, str]:
    if session is not None:
        raise LoginException("You are already login!")
    
    sesion = await service.user_login(user_params)

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
    service: Annotated[AuthService, Depends(get_auth_service)],
    session: Annotated[Optional[str], Cookie(alias=config.session.cookie_key)] = ""
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


@router.patch(path="/block/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str | int], dependencies=[Depends(auth_admin)])
async def block_user(
    user_id: Annotated[int, Path(gt=0)],
    service: Annotated[UsersService, Depends(get_user_service)]
) -> UserGetModel:
    await service.block(user_id)
    return {"msg": "blocked"}


@router.patch(path="/unblock/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str | int], dependencies=[Depends(auth_admin)])
async def unblock_user(
    user_id: Annotated[int, Path(gt=0)],
    service: Annotated[UsersService, Depends(get_user_service)]
) -> UserGetModel:
    await service.unblock(user_id)
    return {"msg": "unblocked"}


@router.patch(path="/grant/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str | int], dependencies=[Depends(auth_admin)])
async def grant(
    user_id: Annotated[int, Path(gt=0)],
    service: Annotated[UsersService, Depends(get_user_service)]
) -> UserGetModel:
    await service.grant(user_id)
    return {"msg": "granted"}


@router.get(path="/", status_code=status.HTTP_200_OK, response_model=dict[int, UserGetModel], dependencies=[Depends(auth_admin)])
async def get_all(
    search_params: Annotated[UsersSearchModel, Query()],
    service: Annotated[UsersService, Depends(get_user_service)]
) -> dict[int, UserGetModel]:
    return await service.get_users(search_params)
