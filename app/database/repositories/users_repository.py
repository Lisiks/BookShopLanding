from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from ...models.users_models import UserPostModel, UserGetModel
from ...models.search_and_pagination_models import UsersSearchModel
from ..shemas import Users
from ...core.postgresql import get_session, session_fabric


from ...settings import config


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session


    async def create_user(self, user_params: UserPostModel, is_admin: bool) -> None:
        new_user = Users(**user_params.model_dump(by_alias=False), is_admin=is_admin)
        self.__session.add(new_user)
        await self.__session.commit()


    async def get_users(self, search_params: UsersSearchModel) -> dict[int, UserGetModel]:
        stmt = select(Users).where(Users.is_admin == search_params.is_admin)

        if search_params.username is not None:
            stmt = stmt.where(Users.username.ilike(f"%{search_params.username}%"))

        stmt = stmt.order_by(Users.id).limit(search_params.limit).offset(search_params.offset)

        users = await self.__session.scalars(stmt)

        return {user.id: UserGetModel.model_validate(user, by_alias=False, by_name=True) for user in users.all()}


    async def block_user(self, user_id: int) -> None:
        stmt = select(Users).where(Users.id == user_id)
        query_result = await self.__session.scalars(stmt)
        user = query_result.one()

        user.is_blocked = True
        await self.__session.commit()


    async def unblock_user(self, user_id: int) -> None:
        stmt = select(Users).where(Users.id == user_id)
        query_result = await self.__session.scalars(stmt)
        user = query_result.one()

        user.is_blocked = False
        await self.__session.commit()
    
    
    async def get_by_name(self, username: str) -> UserGetModel | None:
        stmt = select(Users).where(Users.username == username)
        user = await self.__session.scalar(stmt)
        return UserGetModel.model_validate(user, by_alias=False, by_name=True) if user is not None else None


def get_repository(session: Annotated[AsyncSession, Depends(get_session)]) -> UsersRepository:
    return UsersRepository(session)


async def create_super_user() -> None:
    super_user_model = UserPostModel.model_validate({
        "username": config.app.su_login,
        "plainPassword": config.app.su_password
    })

    async with session_fabric() as session:
        stmt = select(Users).where(Users.username == config.app.su_login)
        super_user = await session.scalar(stmt)

        if super_user is None:
            new_user = Users(**super_user_model.model_dump(by_alias=False), is_blocked=False, is_admin=True)
            session.add(new_user)

        else:
            super_user.password_hash = super_user_model.password_hash

        await session.commit()