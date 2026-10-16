from fastapi import Depends, Form, APIRouter, status, Cookie, Path, Query
from fastapi.responses import JSONResponse
from typing import Annotated, Optional

from ..services.admins_service import AdminsService, get_service as get_admin_service
from ..utils.auth import auth_admin
from ..models.users_models import UserPostModel, UserGetModel, UserLoginModel
from ..models.search_and_pagination_models import UsersSearchModel
from ..settings import config
from ..exceptions import LoginException


router = APIRouter(prefix="/admins", tags=["🧑‍💻 admins"])


@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=dict[str, str], dependencies=[Depends(auth_admin)])
async def create_admin(
    user_params: Annotated[UserPostModel, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[AdminsService, Depends(get_admin_service)]
) -> dict[str, str]:
    await service.create_admin(user_params)
    return {"msg": "created"}


@router.post(path="/login", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def login_admin(
    user_params: Annotated[UserLoginModel, Form(media_type="application/x-www-form-urlencoded")],
    service: Annotated[AdminsService, Depends(get_admin_service)],
    session: Annotated[Optional[str], Cookie(alias=config.session.cookie_key)] = None
) -> dict[str, str]:
    if session is not None:
        raise LoginException("You are already login!")
    
    sesion = await service.login_admin(user_params)

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
    service: Annotated[AdminsService, Depends(get_admin_service)],
    session: Annotated[str, Cookie(alias=config.session.cookie_key)]
) -> dict[str, str]:
    await service.logout(session)
    responce = JSONResponse(content={"msg": "success"})
    responce.delete_cookie(key=config.session.cookie_key)
    return responce


@router.get(path="/users", status_code=status.HTTP_200_OK, response_model=dict[int, UserGetModel], dependencies=[Depends(auth_admin)])
async def get_all(
    search_params: Annotated[UsersSearchModel, Query()],
    service: Annotated[AdminsService, Depends(get_admin_service)]
) -> dict[int, UserGetModel]:
    return await service.get_users(search_params)


@router.patch(path="/users/block/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def block_admin(
    user_id: Annotated[int, Path(gt=0)],
    request_user_data: Annotated[UserGetModel, Depends(auth_admin)],
    service: Annotated[AdminsService, Depends(get_admin_service)]
) -> UserGetModel:
    await service.block(user_id, request_user_data.id)
    return {"msg": "blocked"}


@router.patch(path="/users/unblock/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=dict[str, str])
async def unblock_admin(
    user_id: Annotated[int, Path(gt=0)],
    request_user_data: Annotated[UserGetModel, Depends(auth_admin)],
    service: Annotated[AdminsService, Depends(get_admin_service)]
) -> UserGetModel:
    await service.unblock(user_id, request_user_data.id)
    return {"msg": "unblocked"}


