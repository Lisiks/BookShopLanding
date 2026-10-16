from typing import Annotated, Optional
from fastapi import Depends, BackgroundTasks, Cookie


from ..database.repositories.users_repository import get_repository, UsersRepository
from ..models.users_models import UserPostModel, UserGetModel, UserLoginModel
from ..models.search_and_pagination_models import UsersSearchModel
from ..exceptions import ForbidenException, LoginException
from ..utils import RedisManager, PasswordManager




class AdminsService:
    def __init__(self, repository: UsersRepository, bg_tasks: BackgroundTasks):
        self.__repository = repository
        self.__bg_tasks = bg_tasks


    async def create_admin(self, admin_data: UserPostModel) -> None:
        await self.__repository.create_user(admin_data, is_admin=True)


    async def login_admin(self, user_data: UserLoginModel) -> str:
        user = await self.__repository.get_by_name(user_data.username)
        
        if user is None or not PasswordManager.verify_password(user_data.plain_password, user.password_hash):
            raise LoginException("Incorrect login or password!")

        if user.is_blocked:
            raise ForbidenException("This user was blocked!")

        if user.is_admin == False:
            raise ForbidenException("This user isnt an administrator!")

        return await RedisManager.create_session(user)
    
    
    async def logout(self, session: str) -> None:
        await RedisManager.delete_session(session)


    async def get_users(self, search_params: UsersSearchModel) -> dict[int, UserGetModel]:
        return await self.__repository.get_users(search_params)


    async def block(self, user_id: int, request_user_id: int) -> None:
        if user_id == request_user_id:
            raise ForbidenException("User cannot be blocked by yourself!")

        await self.__repository.block_user(user_id)
        self.__bg_tasks.add_task(RedisManager.delete_sessions_by_id, user_id)


    async def unblock(self, user_id: int, request_user_id: int) -> None:
        if user_id == request_user_id:
            raise ForbidenException("User cannot be unblocked by yourself!")

        await self.__repository.unblock_user(user_id)
        self.__bg_tasks.add_task(RedisManager.delete_sessions_by_id, user_id)



def get_service(
    repository: Annotated[UsersRepository, Depends(get_repository)],
    bg_tasks: BackgroundTasks

) -> AdminsService:
    return AdminsService(repository, bg_tasks)


