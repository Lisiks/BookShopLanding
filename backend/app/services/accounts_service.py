from typing import Annotated, Optional
from fastapi import Depends, BackgroundTasks, Cookie


from ..database.repositories.users_repository import get_repository, UsersRepository
from ..models.users_models import UserPostModel, UserLoginModel
from ..utils import RedisManager, PasswordManager

from ..exceptions import LoginException, ForbidenException




class AccountsService:
    def __init__(self, repository: UsersRepository, bg_tasks: BackgroundTasks):
        self.__repository = repository
        self.__bg_tasks = bg_tasks


    async def create_account(self, user_params: UserPostModel) -> None:
        await self.__repository.create_user(user_params, is_admin=False)


    async def login_account(self, user_data: UserLoginModel) -> str:
        user = await self.__repository.get_by_name(user_data.username)

        if user is None or not PasswordManager.verify_password(user_data.plain_password, user.password_hash):
            raise LoginException("Incorrect login or password!")

        if user.is_blocked:
            raise ForbidenException("This user was blocked!")

        return await RedisManager.create_session(user)


    async def logout(self, session: str) -> None:
        await RedisManager.delete_session(session)
    


def get_service(
    repository: Annotated[UsersRepository, Depends(get_repository)],
    bg_tasks: BackgroundTasks
) -> AccountsService:
     return AccountsService(repository, bg_tasks)
     