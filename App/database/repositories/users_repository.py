from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...models.users_models import UserPostModel, UserGetModel
from ...models.search_and_pagination_models import UsersSearchAndPaginationModel
from ..shemas import Users


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.__session = session


    async def create_user(self, user_params: UserPostModel, is_admin: bool) -> UserGetModel:
        new_user = Users(**user_params.model_dump(), is_admin=is_admin)
        self.__session.add(new_user)
        await self.__session.commit()
        return UserGetModel.model_validate(new_user)


    async def get_users(self, search_params: UsersSearchAndPaginationModel, is_admin: bool) -> dict[int, UserGetModel]:
        stmt = select(Users).where(Users.is_admin == is_admin)

      
        if UsersSearchAndPaginationModel.username is not None:
            stmt = stmt.where(Users.username.ilike(f"%{search_params.username}"))

        stmt = stmt.order_by(Users.id).limit(search_params.limit).offset(search_params.offset)

        users = await self.__session.execute(stmt)

        return {user.id: UserGetModel.model_validate(user) for user in users.all()}


    async def change_user_admin_mode(self, user_id: int, admin_mode: bool) -> UserGetModel | None:
        user = await self.__session.get(Users, user_id)

        if user is None:
            return None

        user.is_admin = admin_mode
        await self.__session.commit()
        return UserGetModel.model_validate(user)


    async def change_user_block_mode(self, user_id: int, block_mode: bool) -> UserGetModel | None:
        user = await self.__session.get(Users, user_id)

        if user is None:
            return None

        user.is_blocked = block_mode
        await self.__session.commit()
        return UserGetModel.model_validate(user)


    async def get_by_name(self, username: str) -> UserGetModel | None:
        stmt = select(Users).where(Users.username == username)

        users = await self.__session.execute(stmt)
        user = users.one()

        return UserGetModel.model_validate(user) if user is not None else None


  