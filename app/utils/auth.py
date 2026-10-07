from typing import Annotated, Optional
from fastapi import Depends, Cookie

from ..settings import config
from .redis_manager import RedisManager
from ..models.users_models import UserGetModel
from ..exceptions import ForbidenException, InvalidSessionException


async def auth_user(
    session: Annotated[str, Cookie(alias=config.session.cookie_key)]
) -> UserGetModel:
    session_data = await RedisManager.read_session(session)

    if session_data is None:
        raise InvalidSessionException("User is unathorise!")
    
    return session_data



async def auth_admin(
    session: Annotated[str, Cookie(alias=config.session.cookie_key)]
) -> UserGetModel:
    session_data = await RedisManager.read_session(session)

    if session_data is None:
        raise InvalidSessionException("User is unathorise!")

    if not session_data.is_admin:
        raise ForbidenException("This user isnt an administrator!")
    
    return session_data