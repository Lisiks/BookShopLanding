from typing import Annotated, Optional
from fastapi import Depends, BackgroundTasks, Cookie


from ..database.repositories.users_repository import get_repository, UsersRepository
from ..models.users_models import UserPostModel, UserGetModel
from ..models.search_and_pagination_models import UsersSearchModel
from ..utils import RedisManager




class UsersService:
    def __init__(self, repository: UsersRepository, bg_tasks: BackgroundTasks):
        self.__repository = repository
        self.__bg_tasks = bg_tasks


    async def create_user(self, user_params: UserPostModel) -> None:
        await self.__repository.create_user(user_params, False)


    async def get_users(self, search_params: UsersSearchModel) -> dict[int, UserGetModel]:
        return await self.__repository.get_users(search_params, False)



    async def block(self, user_id: int) -> None:
        await self.__repository.block_user(user_id, is_admin=False)
        self.__bg_tasks.add_task(RedisManager.delete_sessions_by_id, user_id)
    
    
    async def unblock(self, user_id: int) -> None:
        await self.__repository.unblock_user(user_id, is_admin=False)
        self.__bg_tasks.add_task(RedisManager.delete_sessions_by_id, user_id)


    async def grant(self, user_id: int) -> None:
        await self.__repository.grant_user(user_id)
        self.__bg_tasks.add_task(RedisManager.delete_sessions_by_id, user_id)


def get_service(
    repository: Annotated[UsersRepository, Depends(get_repository)],
    bg_tasks: BackgroundTasks
) -> UsersService:
     return UsersService(repository, bg_tasks)
     