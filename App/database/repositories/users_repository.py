from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends
from typing import Annotated

from ...models.users_models import UserPostModel, UserGetModel, UserGetPasswordModel
from ...models.search_and_pagination_models import UsersSearchModel
from ..shemas import Users
from ...core.postgresql import get_session, session_fabric
from ...exceptions import NoRecordException, QueryException

from ...settings import config


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session


    async def create_user(self, user_params: UserPostModel, is_admin: bool) -> None:
        new_user = Users(**user_params.model_dump(by_alias=False), is_admin=is_admin)
        self.__session.add(new_user)
        await self.__session.commit()


    async def get_users(self, search_params: UsersSearchModel, is_admin: bool) -> dict[int, UserGetModel]:
        stmt = select(Users).where(Users.is_admin == is_admin)

        if search_params.username is not None:
            stmt = stmt.where(Users.username.ilike(f"{search_params.username}%"))

        stmt = stmt.order_by(Users.id).limit(search_params.limit).offset(search_params.offset)

        users = await self.__session.scalars(stmt)

        return {user.id: UserGetModel.model_validate(user, by_alias=False, by_name=True) for user in users.all()}

    async def grant_user(self, user_id: int) -> None:
        user = await self.__session.get(Users, user_id)

        if user is None:
            raise NoRecordException(f"User with id={user_id} doesnt exists in database!")

        if user.is_admin == True:
            raise QueryException("This user is already an administrator!")


        user.is_admin = True
        await self.__session.commit()

    async def revoke_user(self, user_id: int) -> None:
        user = await self.__session.get(Users, user_id)
        
        if user is None:
            raise NoRecordException(f"User with id={user_id} doesnt exists in database!")

        if user.is_admin is not True:
            raise QueryException("This user isn't administrator!")

        user.is_admin = False
        await self.__session.commit()


    async def block_user(self, user_id: int, is_admin: bool) -> None:
        user = await self.__session.get(Users, user_id)

        if user is None:
            raise NoRecordException(f"User with id={user_id} doesnt exists in database!")

        if user.is_admin is not is_admin:
            raise QueryException("This user isn't administrator!" if is_admin else "This user is administrator!")

        user.is_blocked = True
        await self.__session.commit()


    async def unblock_user(self, user_id: int, is_admin: bool) -> None:
        user = await self.__session.get(Users, user_id)

        if user is None:
            raise NoRecordException(f"User with id={user_id} doesnt exists in database!")

        if user.is_admin is not is_admin:
            raise QueryException("This user isn't administrator!" if is_admin else "This user is administrator!")

        user.is_blocked = False
        await self.__session.commit()
    
    
    async def get_by_name(self, username: str) -> UserGetPasswordModel | None:
        stmt = select(Users).where(Users.username == username)
        user = await self.__session.scalar(stmt)
        return UserGetPasswordModel.model_validate(user, by_alias=False, by_name=True) if user is not None else None


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