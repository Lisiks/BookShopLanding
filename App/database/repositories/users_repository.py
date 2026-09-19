from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from ...models.users_models import UserPostModel, UserGetModel, UserGetPasswordModel
from ...models.search_and_pagination_models import UsersSearchAndPaginationModel
from ..shemas import Users
from ...core.postgresql import get_session


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session


    async def create_user(self, user_params: UserPostModel, is_admin: bool) -> UserGetModel:
        new_user = Users(**user_params.model_dump(by_alias=False), is_admin=is_admin)
        self.__session.add(new_user)
        await self.__session.commit()
        return UserGetModel.model_validate(new_user, by_alias=False, by_name=True)


    async def get_users(self, search_params: UsersSearchAndPaginationModel, is_admin: bool) -> dict[int, UserGetModel]:
        stmt = select(Users).where(Users.is_admin == is_admin)

      
        if UsersSearchAndPaginationModel.username is not None:
            stmt = stmt.where(Users.username.ilike(f"%{search_params.username}"))

        stmt = stmt.order_by(Users.id).limit(search_params.limit).offset(search_params.offset)

        users = await self.__session.execute(stmt)

        return {user.id: UserGetModel.model_validate(user, by_alias=False, by_name=True) for user in users.all()}


    async def change_user_admin_mode(self, user_id: int, admin_mode: bool) -> UserGetModel | None:
        user = await self.__session.get(Users, user_id)

        if user is None:
            return None

        user.is_admin = admin_mode
        await self.__session.commit()
        return UserGetModel.model_validate(user, by_alias=False, by_name=True)


    async def change_user_block_mode(self, user_id: int, block_mode: bool) -> UserGetModel | None:
        user = await self.__session.get(Users, user_id)

        if user is None:
            return None

        user.is_blocked = block_mode
        await self.__session.commit()
        return UserGetModel.model_validate(user, by_alias=False, by_name=True)


    async def get_by_name(self, username: str) -> UserGetPasswordModel | None:
        stmt = select(Users).where(Users.username == username)
        user = await self.__session.scalar(stmt)
        return UserGetPasswordModel.model_validate(user, by_alias=False, by_name=True) if user is not None else None


    async def get_by_id(self, user_id: int) -> UserGetModel | None:
        user = await self.__session.get(Users, user_id)
        return UserGetModel.model_validate(user, by_alias=False, by_name=True) if user is not None else None


async def get_repository(session: Annotated[AsyncSession, Depends[get_session]]) -> UsersRepository:
    return UsersRepository(session)