from typing import Annotated, Optional
from fastapi import Depends, BackgroundTasks, Cookie

from .session_manager import SessionManager, get_session_manager
from ..database.repositories.users_repository import get_repository, UsersRepository
from ..models.users_models import UserPostModel, UserGetModel
from ..models.search_and_pagination_models import UsersSearchAndPaginationModel
from ..exceptions import ForbidenException




class AdminsService:
    def __init__(self, repository: UsersRepository, session_manager: SessionManager, bg_tasks: BackgroundTasks):
        self.__session_manager = session_manager
        self.__repository = repository
        self.__bg_tasks = bg_tasks


    async def create_admin(self, admin_data: UserPostModel) -> None:
        await self.__repository.create_user(admin_data, is_admin=True)


    async def get_admins(self, search_params: UsersSearchAndPaginationModel) -> dict[int, UserGetModel]:
        return await self.__repository.get_users(search_params, is_admin=True)


    async def block(self, user_id: int, request_user_id: int) -> None:
        if user_id == request_user_id:
            raise ForbidenException("User cannot be blocked by himself!")

        await self.__repository.block_user(user_id, is_admin=True)
        self.__bg_tasks.add_task(self.__session_manager.delete_sessions_by_id, user_id)


    async def unblock(self, user_id: int, request_user_id: int) -> None:
        if user_id == request_user_id:
            raise ForbidenException("User cannot be unblocked by himself!")

        await self.__repository.unblock_user(user_id, is_admin=True)
        self.__bg_tasks.add_task(self.__session_manager.delete_sessions_by_id, user_id)


    async def revoke(self, user_id: int, request_user_id: int) -> None:
        if user_id == request_user_id:
            raise ForbidenException("User cannot be revoked by himself!")

        await self.__repository.revoke_user(user_id)
        self.__bg_tasks.add_task(self.__session_manager.delete_sessions_by_id, user_id)


async def get_service(
    repository: Annotated[UsersRepository, Depends(get_repository)],
    session_manager: Annotated[SessionManager, Depends(get_session_manager)],
    bg_tasks: BackgroundTasks

) -> AdminsService:
     return AdminsService(repository, session_manager, bg_tasks)


